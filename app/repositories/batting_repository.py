# app/repositories/batting_repository.py
import numpy as np
import pandas as pd

from app.constants.woba_weights import get_woba_weights
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

        df = con.execute(f"""
                SELECT * FROM {union}
                WHERE LOWER(playerName) = LOWER('{player_name}')
                ORDER BY season
            """).df()

        if df.empty:
            return df

        # Calculate wOBA for each season using FanGraphs weights
        def calc_woba(row):
            try:
                weights = get_woba_weights(int(row['season']))
                ubb = float(row['baseOnBalls'] or 0) - float(row['intentionalWalks'] or 0)
                hbp = float(row['hitByPitch'] or 0)
                h = float(row['hits'] or 0)
                doubles = float(row['doubles'] or 0)
                triples = float(row['triples'] or 0)
                hr = float(row['homeRuns'] or 0)
                singles = h - doubles - triples - hr
                ab = float(row['atBats'] or 0)
                sf = float(row['sacFlies'] or 0)

                numerator = (
                        ubb * weights['wBB'] +
                        hbp * weights['wHBP'] +
                        singles * weights['w1B'] +
                        doubles * weights['w2B'] +
                        triples * weights['w3B'] +
                        hr * weights['wHR']
                )
                denominator = ab + ubb + hbp + sf
                return round(float(numerator / denominator), 3) if denominator > 0 else None
            except:
                return None

        df['woba'] = df.apply(calc_woba, axis=1)

        #df = df.replace({np.nan: None})

        df = df.astype(object).where(pd.notna(df), None)

        # Debug - find int64 columns
        for col in df.columns:
            if df[col].dtype == 'int64':
                print(f"int64 column: {col}")

        return df

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