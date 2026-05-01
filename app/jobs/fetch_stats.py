# app/jobs/fetch_stats.py
import os
import time
from app.adapters.pybaseball_adapter import PybaseballAdapter

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

adapter = PybaseballAdapter()

def fetch_and_store_batting(year: int):
    df = adapter.fetch_batting_stats(year)
    path = os.path.join(PARQUET_DIR, f"batting_{year}.parquet")
    df.to_parquet(path, index=False)
    print(f"Saved {len(df)} batting rows → batting_{year}.parquet")

def fetch_and_store_pitching(year: int):
    df = adapter.fetch_pitching_stats(year)
    path = os.path.join(PARQUET_DIR, f"pitching_{year}.parquet")
    df.to_parquet(path, index=False)
    print(f"Saved {len(df)} pitching rows → pitching_{year}.parquet")

if __name__ == "__main__":
    years = range(1995, 2025)  # 1995 through 2024
    total = len(years)

    for i, year in enumerate(years):
        print(f"\n[{i+1}/{total}] Fetching {year}...")
        fetch_and_store_batting(year)
        fetch_and_store_pitching(year)
        time.sleep(1)  # be polite to the API

    print("\nAll done!")