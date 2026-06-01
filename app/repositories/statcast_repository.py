# app/repositories/statcast_repository.py
import pandas as pd
import duckdb
import os
from app.constants.qualifiers import STATCAST_BATTED_BALL_TYPE, GAME_TYPE_REGULAR

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

class StatcastRepository:

    def __init__(self):
        self.con = duckdb.connect()

    def get_player_zones(self, player_id: int, season: int) -> pd.DataFrame:
        """
        Returns zone-level Statcast data for a specific player and season.
        One row per zone.
        """
        zone_path = os.path.join(PARQUET_DIR, f"statcast_zones_{season}.parquet")
        zone_path = zone_path.replace("\\", "/")

        if not os.path.exists(zone_path):
            return pd.DataFrame()

        return self.con.execute(f"""
            SELECT zone, batted_balls_in_zone, xbacon, xwobacon,
                   avg_exit_velo, avg_launch_angle, hard_hit_pct,
                   barrel_pct, sweet_spot_pct, whiff_pct, swing_pct
            FROM read_parquet('{zone_path}')
            WHERE playerId = ?
            AND zone IS NOT NULL
            ORDER BY zone
        """, [player_id]).df()

    def get_league_zone_averages(self, season: int) -> pd.DataFrame:
        """
        Returns league average stats per zone for a given season.
        Queried directly from raw pitch-by-pitch Statcast data.
        """
        statcast_path = os.path.join(PARQUET_DIR, f"statcast_{season}.parquet")
        statcast_path = statcast_path.replace("\\", "/")

        if not os.path.exists(statcast_path):
            return pd.DataFrame()

        # Contact quality - batted balls only
        contact_df = self.con.execute(f"""
            SELECT
                zone,
                COUNT(*) as total_batted_balls,
                ROUND(AVG(estimated_ba_using_speedangle), 3) as league_xbacon,
                ROUND(AVG(estimated_woba_using_speedangle), 3) as league_xwobacon,
                ROUND(AVG(launch_speed), 1) as league_avg_exit_velo,
                ROUND(100.0 * SUM(CASE WHEN launch_speed >= 95 THEN 1 ELSE 0 END) / COUNT(*), 1) as league_hard_hit_pct,
                ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) / NULLIF(COUNT(launch_speed_angle), 0), 1) as league_barrel_pct,
                ROUND(100.0 * SUM(CASE WHEN launch_angle BETWEEN 8 AND 32 THEN 1 ELSE 0 END) / NULLIF(COUNT(launch_speed), 0), 1) as league_sweet_spot_pct
            FROM read_parquet('{statcast_path}')
            WHERE type = '{STATCAST_BATTED_BALL_TYPE}'
            AND game_type = '{GAME_TYPE_REGULAR}'
            AND zone IS NOT NULL
            GROUP BY zone
            ORDER BY zone
        """).df()

        # Swing/discipline - all pitches
        discipline_df = self.con.execute(f"""
            SELECT
                zone,
                ROUND(100.0 * COUNT(CASE WHEN description IN (
                    'swinging_strike', 'swinging_strike_blocked', 'swinging_pitchout',
                    'foul', 'foul_tip', 'foul_pitchout', 'foul_bunt',
                    'hit_into_play', 'hit_into_play_no_out', 'hit_into_play_score',
                    'pitchout_hit_into_play', 'pitchout_hit_into_play_no_out',
                    'pitchout_hit_into_play_score'
                ) THEN 1 END) / COUNT(*), 1) as league_swing_pct,
                ROUND(100.0 * COUNT(CASE WHEN description IN (
                    'swinging_strike', 'swinging_strike_blocked',
                    'swinging_pitchout', 'foul_tip'
                ) THEN 1 END) / NULLIF(COUNT(CASE WHEN description IN (
                    'swinging_strike', 'swinging_strike_blocked', 'swinging_pitchout',
                    'foul', 'foul_tip', 'foul_pitchout', 'foul_bunt',
                    'hit_into_play', 'hit_into_play_no_out', 'hit_into_play_score',
                    'pitchout_hit_into_play', 'pitchout_hit_into_play_no_out',
                    'pitchout_hit_into_play_score'
                ) THEN 1 END), 0), 1) as league_whiff_pct
            FROM read_parquet('{statcast_path}')
            WHERE game_type = '{GAME_TYPE_REGULAR}'
            AND zone IS NOT NULL
            GROUP BY zone
            ORDER BY zone
        """).df()

        return contact_df.merge(discipline_df, on='zone', how='left')

    def get_player_season_statcast(self, player_id: int, season: int) -> pd.DataFrame:
        """
        Returns season-level Statcast aggregates for a player.
        """
        agg_path = os.path.join(PARQUET_DIR, f"statcast_batting_agg_{season}.parquet")
        agg_path = agg_path.replace("\\", "/")

        if not os.path.exists(agg_path):
            return pd.DataFrame()

        return self.con.execute(f"""
            SELECT *
            FROM read_parquet('{agg_path}')
            WHERE playerId = ?
        """, [player_id]).df()