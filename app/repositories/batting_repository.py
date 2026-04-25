# app/repositories/batting_repository.py
import pandas as pd
from app.db.duckdb_client import get_connection
from app.db.parquet_utils import get_parquet_union

class BattingRepository:

    def get_all(self) -> pd.DataFrame:
        con = get_connection()
        union = get_parquet_union("batting")
        return con.execute(f"SELECT * FROM {union}").df()

    def get_by_season(self, year: int) -> pd.DataFrame:
        con = get_connection()
        union = get_parquet_union("batting")
        return con.execute(f"""
            SELECT * FROM {union}
            WHERE season = {year}
        """).df()

    def get_by_player(self, player_name: str) -> pd.DataFrame:
        con = get_connection()
        union = get_parquet_union("batting")
        return con.execute(f"""
            SELECT * FROM {union}
            WHERE LOWER(playerName) = LOWER('{player_name}')
            ORDER BY season
        """).df()

    # batting_repository.py - get_leaderboard
    def get_leaderboard(self, stat: str, season: int = None, limit: int = 25) -> pd.DataFrame:
        con = get_connection()
        union = get_parquet_union("batting")
        season_filter = f"WHERE season = {season}" if season else ""
        return con.execute(f"""
            SELECT playerName, season, homeRuns, rbi, avg
            FROM {union}
            {season_filter}
            ORDER BY {stat} DESC
            LIMIT {limit}
        """).df()

    def search_players(self, query: str) -> pd.DataFrame:
        con = get_connection()
        union = get_parquet_union("batting")
        return con.execute(f"""
            SELECT DISTINCT playerName, playerId
            FROM {union}
            WHERE LOWER(playerName) LIKE LOWER('%{query}%')
            ORDER BY playerName
        """).df()