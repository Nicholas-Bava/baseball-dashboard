# app/repositories/league_context_repository.py
import pandas as pd
import duckdb
from app.db.duckdb_client import get_connection
from app.db.parquet_utils import get_parquet_union
from app.constants.qualifiers import (
    get_batting_qualifier,
    COUNTING_STAT_MIN_PA
)

class LeagueContextRepository:

    def get_batting_league_context(self, stat: str, seasons: list) -> pd.DataFrame:
        """
        Returns league average and league leader for a given batting stat
        across multiple seasons. Uses appropriate PA qualifier based on
        whether the stat is a rate stat or counting stat.
        """
        con = duckdb.connect()
        union = get_parquet_union("batting")
        results = []

        for season in seasons:
            rate_stats = ['avg', 'obp', 'slg', 'ops', 'babip']
            # Always use official batting qualifier regardless of stat type
            min_pa = get_batting_qualifier(season)

            df =con.execute(f"""
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
            leader_df = con.execute(f"""
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

    def get_player_rankings(self, player_id: int, season: int) -> dict:
        """
        Returns the player's rank for each key stat in a given season.
        Only ranks against qualified players (502 PA minimum).
        """
        con = duckdb.connect()
        union = get_parquet_union("batting")
        min_pa = get_batting_qualifier(season)

        stats = {
            'singles': 'DESC',
            'doubles': 'DESC',
            'triples': 'DESC',
            'hits': 'DESC',
            'homeRuns': 'DESC',
            'rbi': 'DESC',
            'stolenBases': 'DESC',
            'avg': 'DESC',
            'ops': 'DESC',
            'xbh': 'DESC',
        }

        rankings = {}

        for stat, direction in stats.items():
            if stat == 'singles':
                stat_expr = """
                        (TRY_CAST(hits AS INTEGER)
                        - TRY_CAST(doubles AS INTEGER)
                        - TRY_CAST(triples AS INTEGER)
                        - TRY_CAST(homeRuns AS INTEGER)) as singles
                    """
                order_expr = "singles"
                null_check = "singles IS NOT NULL"
            elif stat == 'xbh':
                stat_expr = """
                        (TRY_CAST(doubles AS INTEGER)
                        + TRY_CAST(triples AS INTEGER)
                        + TRY_CAST(homeRuns AS INTEGER)) as xbh
                    """
                order_expr = "xbh"
                null_check = "xbh IS NOT NULL"
            else:
                stat_expr = stat
                order_expr = f"TRY_CAST({stat} AS FLOAT)"
                null_check = f"TRY_CAST({stat} AS FLOAT) IS NOT NULL"

            # season and min_pa are parameterized with ?
            # stat column names stay in f-string but come from
            # our hardcoded dictionary — never from user input
            df = con.execute(f"""
                    SELECT playerName, playerId, {stat_expr},
                        RANK() OVER (ORDER BY {order_expr} {direction}) as rank,
                        COUNT(*) OVER () as total_players
                    FROM {union}
                    WHERE season = ?
                    AND TRY_CAST(plateAppearances AS INTEGER) >= ?
                    AND {null_check}
                """, [season, min_pa]).df()

            player_row = df[df['playerId'] == player_id]

            if not player_row.empty:
                rankings[stat] = {
                    'rank': int(player_row.iloc[0]['rank']),
                    'value': str(player_row.iloc[0][stat]),
                    'totalPlayers': int(player_row.iloc[0]['total_players'])
                }
            else:
                rankings[stat] = None

        return rankings