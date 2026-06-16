"""
config.py — Central configuration for the West End seat availability scraper.

All settings can be overridden via environment variables. The scraper
auto-detects whether to use the LTD REST API or fall back to web scraping
based on whether an API key is present.
"""

import os
import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.path.join(os.path.dirname(__file__), "scraper.log")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

# ---------------------------------------------------------------------------
# LTD API configuration
# ---------------------------------------------------------------------------
# Obtain an API key from https://developer.londontheatredirect.com/
# Store it in the environment variable LTD_API_KEY or as a GitHub Secret.
LTD_API_KEY: str = os.environ.get("LTD_API_KEY", "")

# Base URL for the LTD REST API (v2).
# If you find the real endpoints differ, update these paths accordingly.
LTD_API_BASE: str = os.environ.get(
    "LTD_API_BASE", "https://api.londontheatredirect.com/rest/v2"
)

# Individual endpoint paths — easy to tweak without touching scraper logic.
LTD_EVENTS_ENDPOINT: str = "/Events"
LTD_PERFORMANCES_ENDPOINT: str = "/Events/{event_id}/Performances"
LTD_AREAS_ENDPOINT: str = "/Performances/{performance_id}/Areas"

# ---------------------------------------------------------------------------
# Scrape mode
# ---------------------------------------------------------------------------
# 'api'  — uses the LTD REST API (requires LTD_API_KEY)
# 'web'  — falls back to scraping the public LTD website
# Auto-detected: if an API key is set we prefer the API.
SCRAPE_MODE: str = os.environ.get(
    "SCRAPE_MODE", "api" if LTD_API_KEY else "web"
)

# ---------------------------------------------------------------------------
# Scraping parameters
# ---------------------------------------------------------------------------
# How many days ahead to look for performances.
DAYS_AHEAD: int = int(os.environ.get("DAYS_AHEAD", "10"))

# Minimum delay in seconds between HTTP requests (rate limiting).
RATE_LIMIT_SECONDS: float = float(os.environ.get("RATE_LIMIT_SECONDS", "2"))

# Maximum number of retries on transient failures.
MAX_RETRIES: int = int(os.environ.get("MAX_RETRIES", "3"))

# Base delay (seconds) for exponential back-off (delay = base * 2^attempt).
BACKOFF_BASE: float = float(os.environ.get("BACKOFF_BASE", "2"))

# User-Agent strings to rotate through when making HTTP requests.
USER_AGENTS: list[str] = [
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DB_PATH: str = os.environ.get(
    "DB_PATH",
    os.path.join(os.path.dirname(__file__), "data", "availability.db"),
)

# ---------------------------------------------------------------------------
# Show filters (applied during scraping)
# ---------------------------------------------------------------------------
# Shows whose names (case-insensitive) contain any of these strings will be
# skipped during scraping.  Filtering can also happen later in analyze.py.
EXCLUDE_SHOWS: list[str] = [
    # e.g. "Frozen", "The Lion King"
]

# ---------------------------------------------------------------------------
# LTD public website URLs (used by the web-scrape fallback mode)
# ---------------------------------------------------------------------------
LTD_WEB_BASE: str = "https://www.londontheatredirect.com"
LTD_WEB_SHOWS_URL: str = f"{LTD_WEB_BASE}/all-events"
