# app/jobs/fetch_stats.py
import os
from app.adapters.pybaseball_adapter import PybaseballAdapter

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

adapter = PybaseballAdapter()

def fetch_and_store_batting(year: int):
    df = adapter.fetch_batting_stats(year)
    path = os.path.join(PARQUET_DIR, f"batting_{year}.parquet")
    df.to_parquet(path, index=False)
    print(f"Saved {len(df)} batting rows to {path}")

def fetch_and_store_pitching(year: int):
    df = adapter.fetch_pitching_stats(year)
    path = os.path.join(PARQUET_DIR, f"pitching_{year}.parquet")
    df.to_parquet(path, index=False)
    print(f"Saved {len(df)} pitching rows to {path}")

if __name__ == "__main__":
    for year in [2022, 2023, 2024]:
        fetch_and_store_batting(year)
        fetch_and_store_pitching(year)