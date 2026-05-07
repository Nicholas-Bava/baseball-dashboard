# app/jobs/fetch_statcast.py
import os
import time
import pybaseball
from datetime import datetime

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

# Enable pybaseball cache to avoid re-downloading
pybaseball.cache.enable()

def get_season_dates(year: int):
    """Returns start and end dates for a given MLB season."""
    season_dates = {
        2015: ("2015-04-05", "2015-10-04"),
        2016: ("2016-04-03", "2016-10-02"),
        2017: ("2017-04-02", "2017-10-01"),
        2018: ("2018-03-29", "2018-09-30"),
        2019: ("2019-03-20", "2019-09-29"),
        2020: ("2020-07-23", "2020-09-27"),  # COVID shortened
        2021: ("2021-04-01", "2021-10-03"),
        2022: ("2022-04-07", "2022-10-05"),
        2023: ("2023-03-30", "2023-10-01"),
        2024: ("2024-03-20", "2024-09-29"),
        2025: ("2025-03-27", "2025-09-28"),
    }
    return season_dates.get(year)

def fetch_and_store_statcast(year: int):
    path = os.path.join(PARQUET_DIR, f"statcast_{year}.parquet")

    # Skip if already exists - crash resilience
    if os.path.exists(path):
        print(f"  statcast_{year}.parquet already exists — skipping")
        return

    dates = get_season_dates(year)
    if not dates:
        print(f"  No dates configured for {year} — skipping")
        return

    start_dt, end_dt = dates
    print(f"  Fetching {year} ({start_dt} to {end_dt})...")

    df = pybaseball.statcast(start_dt=start_dt, end_dt=end_dt)

    if df is None or df.empty:
        print(f"  No data returned for {year}")
        return

    df.to_parquet(path, index=False)
    print(f"  Saved {len(df):,} rows → statcast_{year}.parquet")

if __name__ == "__main__":
    years = range(2015, 2026)
    total = len(years)

    print(f"Starting Statcast fetch for {total} seasons...")
    print("Already completed seasons will be skipped automatically.\n")

    for i, year in enumerate(years):
        print(f"[{i+1}/{total}] Season {year}")
        try:
            fetch_and_store_statcast(year)
        except Exception as e:
            print(f"  ERROR fetching {year}: {e}")
            print(f"  Skipping {year} and continuing...")
        time.sleep(2)  # be polite between seasons

    print("\nAll done!")