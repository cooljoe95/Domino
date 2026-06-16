#!/usr/bin/env python3
"""
analyze.py — Analysis scripts for the West End seat-availability data.

Run after at least 4–5 days of data collection:

    python analyze.py              # full summary report
    python analyze.py --csv        # also write CSVs to data/reports/
    python scraper.py --analyze    # equivalent shortcut

All analysis queries run against the SQLite database defined in config.DB_PATH.
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional

from config import DB_PATH
from db import get_connection, init_db

logger = logging.getLogger(__name__)

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "data", "reports")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _table(headers: list[str], rows: list[tuple], col_widths: Optional[list[int]] = None) -> str:
    """Render a simple ASCII table.

    If *col_widths* is not provided, widths are auto-detected from data.
    """
    if not rows:
        return "(no data)\n"

    # Auto-detect widths.
    if col_widths is None:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))

    fmt = "  ".join(f"{{:<{w}}}" for w in col_widths)
    lines = [
        fmt.format(*headers),
        fmt.format(*(["─" * w for w in col_widths])),
    ]
    for row in rows:
        lines.append(fmt.format(*(str(v) for v in row)))
    return "\n".join(lines) + "\n"


def _save_csv(filename: str, headers: list[str], rows: list[tuple]) -> str:
    """Write *rows* to a CSV file inside REPORTS_DIR. Returns the path."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return path


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def late_sale_analysis(conn: sqlite3.Connection, *, save_csv_flag: bool = False) -> str:
    """For each performance, compute seat availability at T-7, T-3, and the
    last snapshot (≈T-0).  Calculate **seats sold in the final 3 days**:

        seats_sold_final_3d = seats_at_T3 − seats_at_T0

    Results are grouped by show, venue, section, and day of week.
    """
    # Find the closest snapshot to each milestone for every
    # (performance, section) pair.
    query = """
    WITH ranked AS (
        SELECT
            s.performance_id,
            p.show_id,
            sh.show_name,
            sh.venue_name,
            p.performance_date,
            p.day_of_week,
            s.section_name,
            s.seats_available,
            s.days_until_performance,
            -- bucket: which milestone is this closest to?
            CASE
                WHEN s.days_until_performance >= 5   THEN 'T-7'
                WHEN s.days_until_performance >= 1.5 THEN 'T-3'
                ELSE 'T-0'
            END AS bucket,
            ROW_NUMBER() OVER (
                PARTITION BY s.performance_id, s.section_name,
                    CASE
                        WHEN s.days_until_performance >= 5   THEN 'T-7'
                        WHEN s.days_until_performance >= 1.5 THEN 'T-3'
                        ELSE 'T-0'
                    END
                ORDER BY
                    -- closest to the ideal milestone point
                    ABS(s.days_until_performance - CASE
                        WHEN s.days_until_performance >= 5   THEN 7
                        WHEN s.days_until_performance >= 1.5 THEN 3
                        ELSE 0
                    END)
            ) AS rn
        FROM snapshots s
        JOIN performances p ON p.performance_id = s.performance_id
        JOIN shows sh ON sh.show_id = p.show_id
    )
    SELECT
        show_name,
        venue_name,
        performance_date,
        day_of_week,
        section_name,
        MAX(CASE WHEN bucket = 'T-7' THEN seats_available END) AS seats_t7,
        MAX(CASE WHEN bucket = 'T-3' THEN seats_available END) AS seats_t3,
        MAX(CASE WHEN bucket = 'T-0' THEN seats_available END) AS seats_t0
    FROM ranked
    WHERE rn = 1
    GROUP BY performance_id, section_name
    HAVING seats_t3 IS NOT NULL AND seats_t0 IS NOT NULL
    ORDER BY show_name, performance_date, section_name
    """
    rows_raw = conn.execute(query).fetchall()

    headers = [
        "Show", "Venue", "Date", "Day", "Section",
        "Seats@T-7", "Seats@T-3", "Seats@T-0", "Sold Final 3d",
    ]
    rows = []
    for r in rows_raw:
        t7 = r["seats_t7"] if r["seats_t7"] is not None else "—"
        t3 = r["seats_t3"]
        t0 = r["seats_t0"]
        sold = t3 - t0 if t3 is not None and t0 is not None else "—"
        rows.append((
            r["show_name"], r["venue_name"] or "", r["performance_date"],
            r["day_of_week"] or "", r["section_name"],
            t7, t3, t0, sold,
        ))

    output = "\n━━━ Late Sale Analysis ━━━\n\n"
    output += _table(headers, rows)

    if save_csv_flag and rows:
        path = _save_csv("late_sale_analysis.csv", headers, rows)
        output += f"\n  → Saved to {path}\n"

    return output


def show_ranking(conn: sqlite3.Connection, *, save_csv_flag: bool = False) -> str:
    """Rank shows by average **premium-section** seats unsold at T-3.

    "Premium" is defined as sections whose names contain common premium
    keywords (Stalls, Royal Circle, Dress Circle, Premium, etc.).
    Shows with more unsold premium seats are better Shakeup candidates.
    """
    query = """
    WITH closest_t3 AS (
        SELECT
            s.performance_id,
            p.show_id,
            sh.show_name,
            s.section_name,
            s.seats_available,
            ROW_NUMBER() OVER (
                PARTITION BY s.performance_id, s.section_name
                ORDER BY ABS(s.days_until_performance - 3)
            ) AS rn
        FROM snapshots s
        JOIN performances p ON p.performance_id = s.performance_id
        JOIN shows sh ON sh.show_id = p.show_id
        WHERE s.days_until_performance BETWEEN 1 AND 5
    )
    SELECT
        show_name,
        section_name,
        COUNT(*) AS num_performances,
        ROUND(AVG(seats_available), 1) AS avg_unsold_t3,
        MAX(seats_available) AS max_unsold_t3,
        MIN(seats_available) AS min_unsold_t3
    FROM closest_t3
    WHERE rn = 1
      AND (
          section_name LIKE '%Stall%'
          OR section_name LIKE '%Royal%'
          OR section_name LIKE '%Dress%'
          OR section_name LIKE '%Premium%'
          OR section_name LIKE '%Circle%'
      )
    GROUP BY show_name, section_name
    ORDER BY avg_unsold_t3 DESC
    """
    rows_raw = conn.execute(query).fetchall()

    headers = ["Show", "Section", "# Perfs", "Avg Unsold@T-3", "Max", "Min"]
    rows = [
        (r["show_name"], r["section_name"], r["num_performances"],
         r["avg_unsold_t3"], r["max_unsold_t3"], r["min_unsold_t3"])
        for r in rows_raw
    ]

    output = "\n━━━ Show Ranking (by unsold premium seats at T-3) ━━━\n\n"
    output += _table(headers, rows)

    if save_csv_flag and rows:
        path = _save_csv("show_ranking.csv", headers, rows)
        output += f"\n  → Saved to {path}\n"

    return output


def day_of_week_pattern(conn: sqlite3.Connection, *, save_csv_flag: bool = False) -> str:
    """Analyse cyclicality: how does late availability differ by day of
    week and matinee vs. evening?

    Matinee = performance_time before 17:00.
    """
    query = """
    WITH closest_t3 AS (
        SELECT
            s.performance_id,
            p.day_of_week,
            CASE
                WHEN p.performance_time < '17:00' THEN 'Matinee'
                ELSE 'Evening'
            END AS time_slot,
            s.seats_available,
            ROW_NUMBER() OVER (
                PARTITION BY s.performance_id, s.section_name
                ORDER BY ABS(s.days_until_performance - 3)
            ) AS rn
        FROM snapshots s
        JOIN performances p ON p.performance_id = s.performance_id
        WHERE s.days_until_performance BETWEEN 1 AND 5
    )
    SELECT
        day_of_week,
        time_slot,
        COUNT(*) AS num_snapshots,
        ROUND(AVG(seats_available), 1) AS avg_unsold,
        SUM(seats_available) AS total_unsold
    FROM closest_t3
    WHERE rn = 1 AND day_of_week IS NOT NULL
    GROUP BY day_of_week, time_slot
    ORDER BY
        CASE day_of_week
            WHEN 'Monday'    THEN 1
            WHEN 'Tuesday'   THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday'  THEN 4
            WHEN 'Friday'    THEN 5
            WHEN 'Saturday'  THEN 6
            WHEN 'Sunday'    THEN 7
        END,
        time_slot
    """
    rows_raw = conn.execute(query).fetchall()

    headers = ["Day", "Slot", "# Snapshots", "Avg Unsold", "Total Unsold"]
    rows = [
        (r["day_of_week"], r["time_slot"], r["num_snapshots"],
         r["avg_unsold"], r["total_unsold"])
        for r in rows_raw
    ]

    output = "\n━━━ Day-of-Week Patterns ━━━\n\n"
    output += _table(headers, rows)

    if save_csv_flag and rows:
        path = _save_csv("day_of_week_pattern.csv", headers, rows)
        output += f"\n  → Saved to {path}\n"

    return output


def section_analysis(conn: sqlite3.Connection, *, save_csv_flag: bool = False) -> str:
    """Which sections have the most late availability?

    Stalls vs. Dress Circle vs. Upper Circle vs. Balcony, etc.
    """
    query = """
    WITH closest_t3 AS (
        SELECT
            s.section_name,
            s.seats_available,
            s.min_price_pence,
            s.max_price_pence,
            ROW_NUMBER() OVER (
                PARTITION BY s.performance_id, s.section_name
                ORDER BY ABS(s.days_until_performance - 3)
            ) AS rn
        FROM snapshots s
        WHERE s.days_until_performance BETWEEN 1 AND 5
    )
    SELECT
        section_name,
        COUNT(*) AS num_snapshots,
        ROUND(AVG(seats_available), 1) AS avg_unsold,
        SUM(seats_available) AS total_unsold,
        ROUND(AVG(min_price_pence) / 100.0, 2) AS avg_min_price_gbp,
        ROUND(AVG(max_price_pence) / 100.0, 2) AS avg_max_price_gbp
    FROM closest_t3
    WHERE rn = 1
    GROUP BY section_name
    ORDER BY avg_unsold DESC
    """
    rows_raw = conn.execute(query).fetchall()

    headers = [
        "Section", "# Snapshots", "Avg Unsold", "Total Unsold",
        "Avg Min £", "Avg Max £",
    ]
    rows = [
        (
            r["section_name"], r["num_snapshots"], r["avg_unsold"],
            r["total_unsold"],
            f"£{r['avg_min_price_gbp']:.2f}" if r["avg_min_price_gbp"] else "—",
            f"£{r['avg_max_price_gbp']:.2f}" if r["avg_max_price_gbp"] else "—",
        )
        for r in rows_raw
    ]

    output = "\n━━━ Section Analysis ━━━\n\n"
    output += _table(headers, rows)

    if save_csv_flag and rows:
        path = _save_csv("section_analysis.csv", headers, rows)
        output += f"\n  → Saved to {path}\n"

    return output


def data_overview(conn: sqlite3.Connection) -> str:
    """Quick overview of what's in the database — useful sanity check."""
    stats = {}
    for table in ("shows", "performances", "snapshots"):
        row = conn.execute(f"SELECT COUNT(*) AS cnt FROM {table}").fetchone()
        stats[table] = row["cnt"]

    date_range = conn.execute(
        "SELECT MIN(scraped_at) AS earliest, MAX(scraped_at) AS latest FROM snapshots"
    ).fetchone()

    output = "\n━━━ Data Overview ━━━\n\n"
    output += f"  Shows tracked:        {stats['shows']}\n"
    output += f"  Performances tracked: {stats['performances']}\n"
    output += f"  Availability snapshots: {stats['snapshots']}\n"
    if date_range and date_range["earliest"]:
        output += f"  Earliest snapshot:    {date_range['earliest']}\n"
        output += f"  Latest snapshot:      {date_range['latest']}\n"
    else:
        output += "  (no snapshots yet)\n"
    output += "\n"

    # Top 10 shows by snapshot count.
    top_shows = conn.execute("""
        SELECT sh.show_name, COUNT(*) AS cnt
        FROM snapshots s
        JOIN performances p ON p.performance_id = s.performance_id
        JOIN shows sh ON sh.show_id = p.show_id
        GROUP BY sh.show_name
        ORDER BY cnt DESC
        LIMIT 10
    """).fetchall()

    if top_shows:
        output += "  Top shows by snapshot count:\n"
        for r in top_shows:
            output += f"    • {r['show_name']}: {r['cnt']} snapshots\n"
        output += "\n"

    return output


# ---------------------------------------------------------------------------
# Summary report
# ---------------------------------------------------------------------------

def summary_report(*, save_csv_flag: bool = False) -> None:
    """Print a comprehensive text report covering all analyses.

    This is the data that feeds into the IFV (Initial Funding Vehicle)
    application for The Shakeup.
    """
    init_db()
    conn = get_connection()
    try:
        report = []
        report.append("=" * 70)
        report.append("  WEST END SEAT AVAILABILITY — ANALYSIS REPORT")
        report.append(f"  Generated: {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        report.append("=" * 70)

        report.append(data_overview(conn))
        report.append(late_sale_analysis(conn, save_csv_flag=save_csv_flag))
        report.append(show_ranking(conn, save_csv_flag=save_csv_flag))
        report.append(day_of_week_pattern(conn, save_csv_flag=save_csv_flag))
        report.append(section_analysis(conn, save_csv_flag=save_csv_flag))

        report.append("=" * 70)
        report.append("  END OF REPORT")
        report.append("=" * 70)

        full_report = "\n".join(report)
        print(full_report)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse West End seat-availability data.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Save analysis results as CSV files in data/reports/.",
    )
    args = parser.parse_args()
    summary_report(save_csv_flag=args.csv)


if __name__ == "__main__":
    main()
