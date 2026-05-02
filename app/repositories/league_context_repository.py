# app/repositories/league_context_repository.py
import pandas as pd
from app.db.duckdb_client import get_connection
from app.db.parquet_utils import get_parquet_union
from app.constants.qualifiers import (
    get_batting_qualifier,
    COUNTING_STAT_MIN_PA
)

class LeagueContextRepository:

    def __init__(self):
        self.con = get_connection()

    def get_batting_league_context(self, stat: str, seasons: list) -> pd.DataFrame:
        """
        Returns league average and league leader for a given batting stat
        across multiple seasons. Uses appropriate PA qualifier based on
        whether the stat is a rate stat or counting stat.
        """
        union = get_parquet_union("batting")
        results = []

        for season in seasons:
            rate_stats = ['avg', 'obp', 'slg', 'ops', 'babip']
            # Always use official batting qualifier regardless of stat type
            min_pa = get_batting_qualifier(season)

            df = self.con.execute(f"""
                SELECT
                    {season} as season,
                    AVG(TRY_CAST({stat} AS FLOAT)) as leagueAverage,
                    MAX(TRY_CAST({stat} AS FLOAT)) as leagueLeaderValue
                FROM {union}
                WHERE season = {season}
                AND TRY_CAST(plateAppearances AS INTEGER) >= {min_pa}
                AND TRY_CAST({stat} AS FLOAT) IS NOT NULL
            """).df()

            # Get the league leader name separately
            leader_df = self.con.execute(f"""
                SELECT playerName, TRY_CAST({stat} AS FLOAT) as statValue
                FROM {union}
                WHERE season = {season}
                AND TRY_CAST(plateAppearances AS INTEGER) >= {min_pa}
                AND TRY_CAST({stat} AS FLOAT) IS NOT NULL
                ORDER BY TRY_CAST({stat} AS FLOAT) DESC
                LIMIT 1
            """).df()

            if not df.empty and not leader_df.empty:
                results.append({
                    'season': season,
                    'leagueAverage': round(float(df.iloc[0]['leagueAverage']), 3),
                    'leagueLeaderValue': round(float(df.iloc[0]['leagueLeaderValue']), 3),
                    'leagueLeaderName': leader_df.iloc[0]['playerName']
                })

        return pd.DataFrame(results)