"""
db.py — SQLite database schema and helper functions.

Stores shows, performances, and point-in-time seat-availability snapshots.
Uses WAL journal mode so the analysis scripts can safely read while the
scraper writes.
"""

from __future__ import annotations

import logging
import os
import sqlite3
from typing import Optional

from config import DB_PATH

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS shows (
    show_id         TEXT PRIMARY KEY,
    show_name       TEXT NOT NULL,
    venue_name      TEXT,
    venue_capacity  INTEGER,
    url             TEXT,
    first_seen_at   TEXT DEFAULT (datetime('now')),
    UNIQUE(show_name, venue_name)
);

CREATE TABLE IF NOT EXISTS performances (
    performance_id    TEXT PRIMARY KEY,
    show_id           TEXT NOT NULL REFERENCES shows(show_id),
    performance_date  TEXT NOT NULL,          -- ISO-8601 date  (YYYY-MM-DD)
    performance_time  TEXT,                   -- HH:MM (24-h)
    day_of_week       TEXT,                   -- e.g. 'Monday'
    UNIQUE(show_id, performance_date, performance_time)
);

CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    performance_id         TEXT    NOT NULL REFERENCES performances(performance_id),
    scraped_at             TEXT    NOT NULL DEFAULT (datetime('now')),
    days_until_performance REAL    NOT NULL,
    section_name           TEXT    NOT NULL,
    seats_available        INTEGER NOT NULL,
    min_price_pence        INTEGER,
    max_price_pence        INTEGER,
    currency               TEXT    DEFAULT 'GBP'
);

CREATE INDEX IF NOT EXISTS idx_snapshots_perf ON snapshots(performance_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_days ON snapshots(days_until_performance);
CREATE INDEX IF NOT EXISTS idx_snapshots_scraped ON snapshots(scraped_at);
"""


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Return a new connection with WAL mode and foreign keys enabled."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def init_db(db_path: str = DB_PATH) -> None:
    """Create the database file (and parent directories) and apply the schema."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = _get_connection(db_path)
    try:
        conn.executescript(_SCHEMA_SQL)
        conn.commit()
        logger.info("Database initialised at %s", db_path)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Upsert helpers
# ---------------------------------------------------------------------------

def upsert_show(
    show_id: str,
    show_name: str,
    venue_name: Optional[str] = None,
    venue_capacity: Optional[int] = None,
    url: Optional[str] = None,
    *,
    db_path: str = DB_PATH,
) -> None:
    """Insert or update a show record.

    On conflict (same show_name + venue_name) we update the mutable fields
    but preserve ``first_seen_at``.
    """
    conn = _get_connection(db_path)
    try:
        conn.execute(
            """
            INSERT INTO shows (show_id, show_name, venue_name, venue_capacity, url)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(show_id) DO UPDATE SET
                show_name      = excluded.show_name,
                venue_name     = excluded.venue_name,
                venue_capacity = COALESCE(excluded.venue_capacity, shows.venue_capacity),
                url            = COALESCE(excluded.url, shows.url)
            """,
            (show_id, show_name, venue_name, venue_capacity, url),
        )
        conn.commit()
    finally:
        conn.close()


def upsert_performance(
    performance_id: str,
    show_id: str,
    performance_date: str,
    performance_time: Optional[str] = None,
    day_of_week: Optional[str] = None,
    *,
    db_path: str = DB_PATH,
) -> None:
    """Insert or update a performance record."""
    conn = _get_connection(db_path)
    try:
        conn.execute(
            """
            INSERT INTO performances
                (performance_id, show_id, performance_date, performance_time, day_of_week)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(performance_id) DO UPDATE SET
                performance_date = excluded.performance_date,
                performance_time = excluded.performance_time,
                day_of_week      = excluded.day_of_week
            """,
            (performance_id, show_id, performance_date, performance_time, day_of_week),
        )
        conn.commit()
    finally:
        conn.close()


def insert_snapshot(
    performance_id: str,
    days_until_performance: float,
    section_name: str,
    seats_available: int,
    min_price_pence: Optional[int] = None,
    max_price_pence: Optional[int] = None,
    currency: str = "GBP",
    *,
    db_path: str = DB_PATH,
) -> None:
    """Record a point-in-time availability snapshot for one section."""
    conn = _get_connection(db_path)
    try:
        conn.execute(
            """
            INSERT INTO snapshots
                (performance_id, days_until_performance, section_name,
                 seats_available, min_price_pence, max_price_pence, currency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                performance_id,
                days_until_performance,
                section_name,
                seats_available,
                min_price_pence,
                max_price_pence,
                currency,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def insert_snapshots_batch(
    rows: list[tuple],
    *,
    db_path: str = DB_PATH,
) -> int:
    """Bulk-insert snapshot rows.  Each tuple must match the column order:

    (performance_id, days_until_performance, section_name,
     seats_available, min_price_pence, max_price_pence, currency)

    Returns the number of rows inserted.
    """
    if not rows:
        return 0
    conn = _get_connection(db_path)
    try:
        conn.executemany(
            """
            INSERT INTO snapshots
                (performance_id, days_until_performance, section_name,
                 seats_available, min_price_pence, max_price_pence, currency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        return len(rows)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def get_snapshot_count(db_path: str = DB_PATH) -> int:
    """Return the total number of snapshot rows in the database."""
    conn = _get_connection(db_path)
    try:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM snapshots").fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


def get_show_count(db_path: str = DB_PATH) -> int:
    """Return the total number of tracked shows."""
    conn = _get_connection(db_path)
    try:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM shows").fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


def get_performance_count(db_path: str = DB_PATH) -> int:
    """Return the total number of tracked performances."""
    conn = _get_connection(db_path)
    try:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM performances").fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Public accessor — used by analyze.py for ad-hoc queries."""
    return _get_connection(db_path)
