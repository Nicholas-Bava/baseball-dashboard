# app/db/parquet_utils.py
import os

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

def get_parquet_union(stat_type: str) -> str:
    """
    Dynamically builds a UNION ALL query from all parquet files
    matching the given stat type (e.g. 'batting' or 'pitching').
    Automatically picks up new years as files are added.
    """
    files = sorted([
        f for f in os.listdir(PARQUET_DIR)
        if f.startswith(stat_type) and f.endswith(".parquet")
    ])

    if not files:
        raise FileNotFoundError(f"No parquet files found for type: {stat_type}")

    selects = [
        f"SELECT * FROM read_parquet('{os.path.join(PARQUET_DIR, f).replace(chr(92), '/')}')"
        for f in files
    ]

    return f"({' UNION ALL '.join(selects)})"