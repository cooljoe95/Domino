# West End Seat Availability Scraper

Monitors seat availability across West End theatre shows to track how many seats sell in the final 3 days before performances. Built for **The Shakeup** to identify which shows consistently have unsold premium inventory close to showtime.

## What it does

1. **Scrapes** London Theatre Direct (API or website) daily for every West End show's upcoming performances and seat availability by section.
2. **Stores** timestamped snapshots in a portable SQLite database.
3. **Analyses** the data to reveal late-sale patterns: which shows, sections, and days of the week have the most unsold seats at T-3 and T-0.

---

## Quick Start

### Prerequisites

- Python 3.10+ (tested on 3.11)
- `pip` for installing dependencies

### Local Setup

```bash
cd scraper/
pip install -r requirements.txt
```

### Get an LTD API Key (recommended)

1. Visit [developer.londontheatredirect.com](https://developer.londontheatredirect.com/)
2. Register for a developer account and create an API key.
3. Export the key:
   ```bash
   export LTD_API_KEY='your-api-key-here'
   ```

If no API key is set, the scraper automatically falls back to web scraping mode (less granular data but works immediately).

### Run the Scraper

```bash
# Normal run (auto-detects API vs web mode)
python scraper.py

# Force web scraping mode
python scraper.py --mode web

# Dry run — fetches data but doesn't write to the database
python scraper.py --dry-run

# Run analysis on collected data
python scraper.py --analyze
# or equivalently:
python analyze.py
python analyze.py --csv   # also save results as CSV files
```

---

## Data Schema

### `shows`
| Column | Description |
|--------|-------------|
| `show_id` | Unique identifier (from API or SHA-256 hash) |
| `show_name` | Display name |
| `venue_name` | Theatre venue |
| `venue_capacity` | Total venue capacity (if known) |
| `url` | Link to the show page |

### `performances`
| Column | Description |
|--------|-------------|
| `performance_id` | Unique identifier |
| `show_id` | FK → shows |
| `performance_date` | ISO date (YYYY-MM-DD) |
| `performance_time` | Time (HH:MM, 24h) |
| `day_of_week` | e.g. "Saturday" |

### `snapshots`
| Column | Description |
|--------|-------------|
| `performance_id` | FK → performances |
| `scraped_at` | UTC timestamp of this snapshot |
| `days_until_performance` | Signed float — negative means past |
| `section_name` | e.g. "Stalls", "Royal Circle" |
| `seats_available` | Count at time of scrape |
| `min_price_pence` | Lowest price in pence |
| `max_price_pence` | Highest price in pence |

---

## Analysis

After 4–5 days of data collection, run the analysis:

```bash
python analyze.py --csv
```

This produces:

| Analysis | What it shows |
|----------|---------------|
| **Late Sale Analysis** | Seats at T-7, T-3, T-0 and how many sold in the final 3 days |
| **Show Ranking** | Shows ranked by average unsold premium seats at T-3 (best Shakeup candidates) |
| **Day-of-Week Patterns** | Tue vs Wed vs Thu vs Sat matinee vs Sat evening |
| **Section Analysis** | Which sections (Stalls, Circle, Balcony) have most late availability |

CSV files are saved to `data/reports/`.

---

## GitHub Actions (Automated Daily Scrape)

The scraper is designed to run unattended via GitHub Actions — no need to keep your laptop open.

### Setup

1. Push this repo to GitHub.
2. Go to **Settings → Secrets and variables → Actions**.
3. Add a secret called `LTD_API_KEY` with your API key.
4. The workflow at `.github/workflows/scrape.yml` runs daily at **02:00 UTC** (3am BST).

### How it works

- GitHub spins up a fresh Ubuntu runner every day.
- It checks out the repo, installs dependencies, runs the scraper.
- The updated `data/availability.db` is committed and pushed back to the repo.
- Each day's data accumulates, building a time-series of seat availability.

### Manual trigger

Go to **Actions → Daily West End Seat Availability Scrape → Run workflow**.

---

## Configuration

All settings live in `config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LTD_API_KEY` | _(empty)_ | API key for London Theatre Direct |
| `SCRAPE_MODE` | auto-detected | `api` or `web` |
| `DAYS_AHEAD` | `10` | How many days ahead to look for performances |
| `RATE_LIMIT_SECONDS` | `2` | Delay between HTTP requests |
| `MAX_RETRIES` | `3` | Retry count on transient failures |
| `DB_PATH` | `data/availability.db` | SQLite database location |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

### Excluding shows

Edit the `EXCLUDE_SHOWS` list in `config.py`:

```python
EXCLUDE_SHOWS = ["Frozen", "The Lion King"]
```

---

## Project Structure

```
scraper/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration
├── db.py                        # SQLite schema and helpers
├── scraper.py                   # Main scraper (API + web modes)
├── analyze.py                   # Analysis and reporting
├── data/
│   ├── availability.db          # SQLite database (auto-created)
│   └── reports/                 # CSV exports (gitignored)
├── .github/
│   └── workflows/
│       └── scrape.yml           # GitHub Actions daily cron
└── .gitignore
```

---

## Troubleshooting

**"No show links found" in web mode:**
The LTD website structure may have changed. Open the site in a browser, inspect the show listing elements, and update the CSS selectors in `scraper.py → scrape_via_web()`.

**API returns 401/403:**
Your API key may be invalid or expired. Check at [developer.londontheatredirect.com](https://developer.londontheatredirect.com/).

**GitHub Actions push fails:**
Ensure the workflow has `contents: write` permission and that branch protection rules allow pushes from `github-actions[bot]`.

---

## License

Internal project for The Shakeup. Not for public distribution.
