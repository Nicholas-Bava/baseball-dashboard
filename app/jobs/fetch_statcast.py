# app/jobs/fetch_statcast.py
import os
import time
import pybaseball
from datetime import datetime

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

# Enable pybaseball cache to avoid re-downloading
pybaseball.cache.enable()

def get_season_dates(year: int):
    """
    Uses full year range to capture all possible games.
    game_type = 'R' filter in queries handles excluding
    spring training, playoffs etc.
    """
    return (f"{year}-01-01", f"{year}-12-31")

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