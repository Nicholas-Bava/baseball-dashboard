# app/db/duckdb_client.py
import duckdb

def get_connection():
    # In-memory connection - no file locking issues
    # We read directly from Parquet files via get_parquet_union()
    # so we don't need a persistent DB file
    return duckdb.connect()