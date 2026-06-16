#!/usr/bin/env python3
"""
scraper.py — West End seat-availability scraper.

Two operating modes:
  1. API mode  — hits the London Theatre Direct REST API (requires LTD_API_KEY)
  2. Web mode  — scrapes the public LTD website as a fallback

Run:
    python scraper.py              # normal scrape
    python scraper.py --dry-run    # fetch data but skip database writes
    python scraper.py --analyze    # run analysis instead of scraping
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import logging
import random
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup

import config
from db import (
    get_snapshot_count,
    init_db,
    insert_snapshot,
    insert_snapshots_batch,
    upsert_performance,
    upsert_show,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

# Cycle through user-agents to reduce chance of fingerprinting blocks.
_UA_CYCLE = itertools.cycle(config.USER_AGENTS)


def _make_session(*, api_mode: bool = False) -> requests.Session:
    """Build a ``requests.Session`` with sensible defaults.

    In API mode the ``Api-Key`` header is added automatically.
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": next(_UA_CYCLE),
            "Accept": "application/json" if api_mode else "text/html",
            "Accept-Language": "en-GB,en;q=0.9",
        }
    )
    if api_mode and config.LTD_API_KEY:
        session.headers["Api-Key"] = config.LTD_API_KEY
    return session


def _request_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: Optional[dict[str, Any]] = None,
    max_retries: int = config.MAX_RETRIES,
    backoff_base: float = config.BACKOFF_BASE,
) -> Optional[requests.Response]:
    """GET *url* with exponential back-off on transient failures.

    Returns the ``Response`` on success or ``None`` after exhausting retries.
    """
    for attempt in range(max_retries + 1):
        try:
            # Rotate user-agent per request.
            session.headers["User-Agent"] = next(_UA_CYCLE)

            resp = session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp

        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else 0
            if status in (429, 500, 502, 503, 504):
                delay = backoff_base * (2**attempt) + random.uniform(0, 1)
                logger.warning(
                    "HTTP %s for %s — retrying in %.1fs (attempt %d/%d)",
                    status, url, delay, attempt + 1, max_retries,
                )
                time.sleep(delay)
                continue
            logger.error("HTTP %s for %s — not retryable", status, url)
            return None

        except requests.exceptions.RequestException as exc:
            delay = backoff_base * (2**attempt) + random.uniform(0, 1)
            logger.warning(
                "%s for %s — retrying in %.1fs (attempt %d/%d)",
                type(exc).__name__, url, delay, attempt + 1, max_retries,
            )
            time.sleep(delay)

    logger.error("All %d retries exhausted for %s", max_retries, url)
    return None


def _rate_limit() -> None:
    """Sleep for the configured rate-limit interval."""
    time.sleep(config.RATE_LIMIT_SECONDS)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _days_until(perf_dt: datetime) -> float:
    """Signed days from now (UTC) until *perf_dt*.  Negative = in the past."""
    now = datetime.now(tz=timezone.utc)
    # Ensure perf_dt is tz-aware.
    if perf_dt.tzinfo is None:
        perf_dt = perf_dt.replace(tzinfo=timezone.utc)
    return (perf_dt - now).total_seconds() / 86400


def _make_id(*parts: str) -> str:
    """Deterministic short ID from arbitrary strings (for show/performance IDs
    when the API doesn't supply one)."""
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _is_excluded(show_name: str) -> bool:
    """Check if a show should be skipped based on EXCLUDE_SHOWS."""
    lower = show_name.lower()
    return any(exc.lower() in lower for exc in config.EXCLUDE_SHOWS)


def _cutoff_date() -> datetime:
    """The latest performance date we care about (now + DAYS_AHEAD)."""
    return datetime.now(tz=timezone.utc) + timedelta(days=config.DAYS_AHEAD)


# ═══════════════════════════════════════════════════════════════════════════
# API MODE
# ═══════════════════════════════════════════════════════════════════════════

def scrape_via_api(*, dry_run: bool = False) -> None:
    """Use the LTD REST API to fetch availability data.

    Flow:
      1. GET /Events — list all available shows.
      2. For each show, GET /Events/{id}/Performances — upcoming performances.
      3. For each performance within DAYS_AHEAD window,
         GET /Performances/{id}/Areas — per-section seat counts.
      4. Store a snapshot row for every section.
    """
    session = _make_session(api_mode=True)
    base = config.LTD_API_BASE.rstrip("/")
    snapshot_rows: list[tuple] = []

    # --- Step 1: fetch all events (shows) -----------------------------------
    events_url = f"{base}{config.LTD_EVENTS_ENDPOINT}"
    logger.info("Fetching events list from %s", events_url)
    resp = _request_with_retry(session, events_url)
    if resp is None:
        logger.error("Failed to fetch events — aborting API scrape.")
        return

    try:
        data = resp.json()
    except (json.JSONDecodeError, ValueError):
        logger.error("Non-JSON response from events endpoint.")
        return

    # The API may wrap results under a key like "Events" or return a list.
    events: list[dict] = data if isinstance(data, list) else data.get("Events", data.get("events", []))

    logger.info("Found %d events.", len(events))

    cutoff = _cutoff_date()

    for event in events:
        # --- Normalise event fields ----------------------------------------
        # Field names may differ; try several common casings.
        show_name = (
            event.get("Name")
            or event.get("name")
            or event.get("EventName")
            or "Unknown"
        )
        if _is_excluded(show_name):
            logger.debug("Skipping excluded show: %s", show_name)
            continue

        event_id = str(
            event.get("Id")
            or event.get("id")
            or event.get("EventId")
            or _make_id(show_name)
        )
        venue = event.get("VenueName") or event.get("venue_name") or event.get("Venue", {}).get("Name")
        venue_capacity = event.get("VenueCapacity") or event.get("venue_capacity")
        show_url = event.get("Url") or event.get("url")

        if not dry_run:
            upsert_show(event_id, show_name, venue, venue_capacity, show_url)

        # --- Step 2: fetch performances for this event ----------------------
        perfs_path = config.LTD_PERFORMANCES_ENDPOINT.format(event_id=event_id)
        perfs_url = f"{base}{perfs_path}"
        _rate_limit()
        logger.info("  [%s] Fetching performances …", show_name)
        resp = _request_with_retry(session, perfs_url)
        if resp is None:
            logger.warning("  Skipping %s — could not fetch performances.", show_name)
            continue

        try:
            perfs_data = resp.json()
        except (json.JSONDecodeError, ValueError):
            logger.warning("  Non-JSON performances response for %s", show_name)
            continue

        perfs: list[dict] = (
            perfs_data
            if isinstance(perfs_data, list)
            else perfs_data.get("Performances", perfs_data.get("performances", []))
        )

        for perf in perfs:
            # Parse performance datetime.
            perf_date_raw = (
                perf.get("Date")
                or perf.get("date")
                or perf.get("PerformanceDate")
                or ""
            )
            try:
                perf_dt = datetime.fromisoformat(perf_date_raw.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                logger.debug("    Skipping perf with unparseable date: %s", perf_date_raw)
                continue

            # Skip performances outside our window.
            if perf_dt > cutoff:
                continue

            perf_id = str(
                perf.get("Id")
                or perf.get("id")
                or perf.get("PerformanceId")
                or _make_id(event_id, perf_date_raw)
            )
            perf_date_str = perf_dt.strftime("%Y-%m-%d")
            perf_time_str = perf_dt.strftime("%H:%M")
            day_of_week = perf_dt.strftime("%A")
            days_until = _days_until(perf_dt)

            if not dry_run:
                upsert_performance(perf_id, event_id, perf_date_str, perf_time_str, day_of_week)

            # --- Step 3: fetch areas (sections) for performance -------------
            areas_path = config.LTD_AREAS_ENDPOINT.format(performance_id=perf_id)
            areas_url = f"{base}{areas_path}"
            _rate_limit()
            resp = _request_with_retry(session, areas_url)
            if resp is None:
                logger.warning("    Could not fetch areas for perf %s", perf_id)
                continue

            try:
                areas_data = resp.json()
            except (json.JSONDecodeError, ValueError):
                logger.warning("    Non-JSON areas response for perf %s", perf_id)
                continue

            areas: list[dict] = (
                areas_data
                if isinstance(areas_data, list)
                else areas_data.get("Areas", areas_data.get("areas", []))
            )

            for area in areas:
                section = (
                    area.get("Name")
                    or area.get("name")
                    or area.get("AreaName")
                    or "Unknown"
                )
                seats = int(area.get("AvailableCount", area.get("available_count", 0)))
                min_p = area.get("MinPrice") or area.get("min_price")
                max_p = area.get("MaxPrice") or area.get("max_price")
                # Convert pounds to pence if the value looks like pounds (< 1000).
                if min_p is not None:
                    min_p = int(float(min_p) * 100) if float(min_p) < 1000 else int(min_p)
                if max_p is not None:
                    max_p = int(float(max_p) * 100) if float(max_p) < 1000 else int(max_p)

                snapshot_rows.append(
                    (perf_id, days_until, section, seats, min_p, max_p, "GBP")
                )

        logger.info(
            "  [%s] Collected %d section snapshots so far.",
            show_name, len(snapshot_rows),
        )

    # --- Bulk insert --------------------------------------------------------
    if dry_run:
        logger.info("DRY RUN — would insert %d snapshot rows.", len(snapshot_rows))
    else:
        inserted = insert_snapshots_batch(snapshot_rows)
        logger.info("Inserted %d snapshot rows.", inserted)


# ═══════════════════════════════════════════════════════════════════════════
# WEB FALLBACK MODE
# ═══════════════════════════════════════════════════════════════════════════

def scrape_via_web(*, dry_run: bool = False) -> None:
    """Fallback: scrape the public LTD website for availability counts.

    This is less granular than the API but works without an API key.  The
    selectors below were written against the LTD site structure as of
    mid-2025; they may need updating if the site redesigns.

    Flow:
      1. Fetch the main shows listing page and extract show links.
      2. Visit each show page to find upcoming performance dates.
      3. For each performance page, extract available-seat counts per
         price band / section.
    """
    session = _make_session(api_mode=False)
    snapshot_rows: list[tuple] = []
    cutoff = _cutoff_date()

    # --- Step 1: get the show listings page ---------------------------------
    logger.info("Fetching show listings from %s", config.LTD_WEB_SHOWS_URL)
    resp = _request_with_retry(session, config.LTD_WEB_SHOWS_URL)
    if resp is None:
        logger.error("Failed to fetch shows listing page — aborting web scrape.")
        return

    soup = BeautifulSoup(resp.text, "lxml")

    # Look for show cards / links.  These selectors are best-effort and may
    # need adjusting if LTD redesigns the page.
    # Common patterns: <a class="show-card" href="/show/wicked-tickets/...">
    show_links: list[dict[str, str]] = []

    # Strategy A: <a> tags whose href starts with /show/ or /musical/
    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"]
        if re.match(r"^/(show|musical|play|event)/", href):
            name = a_tag.get_text(strip=True) or href.split("/")[-1].replace("-", " ").title()
            full_url = f"{config.LTD_WEB_BASE}{href}" if href.startswith("/") else href
            show_links.append({"name": name, "url": full_url})

    # Strategy B: look for data-attributes or JSON-LD
    for script_tag in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script_tag.string or "")
            items = ld if isinstance(ld, list) else [ld]
            for item in items:
                if item.get("@type") in ("Event", "TheaterEvent"):
                    name = item.get("name", "Unknown")
                    url = item.get("url", "")
                    show_links.append({"name": name, "url": url})
        except (json.JSONDecodeError, TypeError):
            pass

    # Deduplicate by URL.
    seen_urls: set[str] = set()
    unique_shows: list[dict[str, str]] = []
    for sl in show_links:
        if sl["url"] not in seen_urls:
            seen_urls.add(sl["url"])
            unique_shows.append(sl)

    logger.info("Found %d unique show links.", len(unique_shows))

    if not unique_shows:
        logger.warning(
            "No show links found — the site structure may have changed. "
            "Check the CSS selectors in scraper.py → scrape_via_web()."
        )

    # --- Step 2 & 3: visit each show page and extract performances ----------
    for show_info in unique_shows:
        show_name = show_info["name"]
        show_url = show_info["url"]

        if _is_excluded(show_name):
            logger.debug("Skipping excluded show: %s", show_name)
            continue

        show_id = _make_id(show_name, show_url)
        venue_name: Optional[str] = None

        _rate_limit()
        logger.info("  [%s] Fetching show page …", show_name)
        resp = _request_with_retry(session, show_url)
        if resp is None:
            logger.warning("  Skipping %s — could not fetch show page.", show_name)
            continue

        show_soup = BeautifulSoup(resp.text, "lxml")

        # Try to extract venue name from the page.
        venue_el = (
            show_soup.find(class_=re.compile(r"venue", re.I))
            or show_soup.find("span", class_="venue-name")
            or show_soup.find(attrs={"itemprop": "location"})
        )
        if venue_el:
            venue_name = venue_el.get_text(strip=True)

        if not dry_run:
            upsert_show(show_id, show_name, venue_name, url=show_url)

        # --- Extract performance dates / availability -----------------------
        # LTD typically shows a calendar or a list of dates with an
        # availability indicator.  We look for date-bearing elements.

        # Pattern A: calendar cells with data-date attributes.
        perf_elements = show_soup.find_all(attrs={"data-date": True})

        # Pattern B: links whose href contains a date-like segment.
        if not perf_elements:
            perf_elements = [
                a
                for a in show_soup.find_all("a", href=True)
                if re.search(r"\d{4}-\d{2}-\d{2}", a["href"])
            ]

        # Pattern C: structured data.
        for script_tag in show_soup.find_all("script", type="application/ld+json"):
            try:
                ld = json.loads(script_tag.string or "")
                items = ld if isinstance(ld, list) else [ld]
                for item in items:
                    if item.get("@type") in ("Event", "TheaterEvent"):
                        start = item.get("startDate", "")
                        if start:
                            # Create a synthetic element dict for uniform processing.
                            perf_elements.append({"_ld_date": start, "_ld": item})
            except (json.JSONDecodeError, TypeError):
                pass

        logger.info("    Found %d performance elements.", len(perf_elements))

        for perf_el in perf_elements:
            # --- Parse the performance datetime ---
            if isinstance(perf_el, dict) and "_ld_date" in perf_el:
                raw_date = perf_el["_ld_date"]
            elif hasattr(perf_el, "get") and callable(perf_el.get):
                raw_date = perf_el.get("data-date", "")
            elif hasattr(perf_el, "attrs"):
                raw_date = perf_el.attrs.get("data-date", "")
            else:
                # Try extracting from href.
                href = perf_el.get("href", "") if hasattr(perf_el, "get") else ""
                match = re.search(r"\d{4}-\d{2}-\d{2}", href)
                raw_date = match.group(0) if match else ""

            if not raw_date:
                continue

            try:
                perf_dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            except ValueError:
                try:
                    perf_dt = datetime.strptime(raw_date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
                except ValueError:
                    continue

            if perf_dt > cutoff:
                continue

            perf_date_str = perf_dt.strftime("%Y-%m-%d")
            perf_time_str = perf_dt.strftime("%H:%M") if perf_dt.hour else None
            day_of_week = perf_dt.strftime("%A")
            perf_id = _make_id(show_id, perf_date_str, perf_time_str or "")
            days_until = _days_until(perf_dt)

            if not dry_run:
                upsert_performance(perf_id, show_id, perf_date_str, perf_time_str, day_of_week)

            # --- Extract availability counts --------------------------------
            # Web pages rarely give per-section counts on a listing.
            # We might get an overall "X tickets available" or price-band info
            # from the performance page.  Grab what we can.

            seats_text = ""
            section_name = "General"  # Default when no section detail available.
            seats_available = 0

            # If perf_el is a tag with text content like "42 available" or similar:
            if hasattr(perf_el, "get_text"):
                seats_text = perf_el.get_text(strip=True)
            elif isinstance(perf_el, dict):
                offers = perf_el.get("_ld", {}).get("offers", {})
                if isinstance(offers, dict):
                    seats_available = int(offers.get("inventoryLevel", 0))
                    section_name = offers.get("name", "General")

            # Try to pull a number from the text.
            if seats_text:
                nums = re.findall(r"(\d+)\s*(?:ticket|seat|available)", seats_text, re.I)
                if nums:
                    seats_available = int(nums[0])

            # Only store if we actually found seat data.
            if seats_available > 0:
                snapshot_rows.append(
                    (perf_id, days_until, section_name, seats_available, None, None, "GBP")
                )

    # --- Bulk insert --------------------------------------------------------
    if dry_run:
        logger.info("DRY RUN — would insert %d snapshot rows.", len(snapshot_rows))
    else:
        inserted = insert_snapshots_batch(snapshot_rows)
        logger.info("Inserted %d snapshot rows.", inserted)


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="West End seat-availability scraper.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch data but do NOT write to the database.",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run analysis on collected data instead of scraping.",
    )
    parser.add_argument(
        "--mode",
        choices=["api", "web"],
        default=None,
        help="Force a specific scrape mode (overrides auto-detection).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point."""
    args = parse_args(argv)

    # Handle --analyze: delegate to analyze.py.
    if args.analyze:
        from analyze import summary_report
        init_db()
        summary_report()
        return

    # Determine scrape mode.
    mode = args.mode or config.SCRAPE_MODE
    logger.info("=" * 60)
    logger.info("West End Seat Availability Scraper")
    logger.info("Mode: %s | Dry run: %s | Days ahead: %d",
                mode.upper(), args.dry_run, config.DAYS_AHEAD)
    logger.info("Database: %s", config.DB_PATH)
    logger.info("=" * 60)

    init_db()

    if mode == "api":
        if not config.LTD_API_KEY:
            logger.warning(
                "API mode selected but LTD_API_KEY is not set. "
                "Falling back to web scrape mode."
            )
            mode = "web"

    if mode == "api":
        scrape_via_api(dry_run=args.dry_run)
    else:
        scrape_via_web(dry_run=args.dry_run)

    count = get_snapshot_count()
    logger.info("Scrape complete. Total snapshots in database: %d", count)


if __name__ == "__main__":
    main()
