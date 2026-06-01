# app/jobs/aggregate_statcast_zones.py
import os
import duckdb
import pandas as pd
from app.constants.qualifiers import STATCAST_BATTED_BALL_TYPE, STATCAST_HARD_HIT_MPH, STATCAST_BARREL_CODE, GAME_TYPE_REGULAR

PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

def get_statcast_path(year: int) -> str:
    return os.path.join(PARQUET_DIR, f"statcast_{year}.parquet")

def get_zone_path(year: int) -> str:
    return os.path.join(PARQUET_DIR, f"statcast_zones_{year}.parquet")

def aggregate_zones(year: int):
    statcast_path = get_statcast_path(year)
    zone_path = get_zone_path(year)

    if os.path.exists(zone_path):
        print(f"  statcast_zones_{year}.parquet already exists — skipping")
        return

    if not os.path.exists(statcast_path):
        print(f"  statcast_{year}.parquet not found — skipping")
        return

    print(f"  Aggregating zones {year}...")

    con = duckdb.connect()

    # ============================================
    # QUERY 1 — Contact quality by zone
    # Batted balls only, grouped by batter + zone
    # ============================================
    contact_df = con.execute(f"""
        SELECT
            batter as playerId,
            zone,
            COUNT(*) as batted_balls_in_zone,
            ROUND(AVG(launch_speed), 1) as avg_exit_velo,
            ROUND(AVG(launch_angle), 1) as avg_launch_angle,
            ROUND(100.0 * SUM(CASE WHEN launch_speed >= {STATCAST_HARD_HIT_MPH} THEN 1 ELSE 0 END) / COUNT(*), 1) as hard_hit_pct,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = {STATCAST_BARREL_CODE} THEN 1 ELSE 0 END) / NULLIF(COUNT(launch_speed_angle), 0), 1) as barrel_pct,
            ROUND(100.0 * SUM(CASE WHEN launch_angle BETWEEN 8 AND 32 THEN 1 ELSE 0 END) / NULLIF(COUNT(launch_speed), 0), 1) as sweet_spot_pct,
            ROUND(AVG(estimated_ba_using_speedangle), 3) as xbacon,
            ROUND(AVG(estimated_woba_using_speedangle), 3) as xwobacon
        FROM read_parquet('{statcast_path.replace(chr(92), '/')}')
        WHERE type = '{STATCAST_BATTED_BALL_TYPE}'
        AND game_type = '{GAME_TYPE_REGULAR}'
        AND zone IS NOT NULL
        GROUP BY batter, zone
    """).df()

    # ============================================
    # QUERY 2 — Swing/discipline by zone
    # All pitches, grouped by batter + zone
    # ============================================
    discipline_df = con.execute(f"""
        SELECT
            batter as playerId,
            zone,
            COUNT(*) as pitches_in_zone,
            COUNT(CASE WHEN description IN (
                'swinging_strike', 'swinging_strike_blocked', 'swinging_pitchout',
                'foul', 'foul_tip', 'foul_pitchout', 'foul_bunt',
                'hit_into_play', 'hit_into_play_no_out', 'hit_into_play_score',
                'pitchout_hit_into_play', 'pitchout_hit_into_play_no_out',
                'pitchout_hit_into_play_score'
            ) THEN 1 END) as swings,
            COUNT(CASE WHEN description IN (
                'swinging_strike', 'swinging_strike_blocked',
                'swinging_pitchout', 'foul_tip'
            ) THEN 1 END) as whiffs
        FROM read_parquet('{statcast_path.replace(chr(92), '/')}')
        WHERE game_type = '{GAME_TYPE_REGULAR}'
        AND zone IS NOT NULL
        GROUP BY batter, zone
    """).df()

    # Calculate rates
    discipline_df['swing_pct'] = (
        discipline_df['swings'] / discipline_df['pitches_in_zone'] * 100
    ).round(1)
    discipline_df['whiff_pct'] = (
        discipline_df['whiffs'] / discipline_df['swings'] * 100
    ).round(1)

    # ============================================
    # MERGE
    # ============================================
    merged = contact_df.merge(
        discipline_df[['playerId', 'zone', 'pitches_in_zone', 'swings',
                       'swing_pct', 'whiff_pct']],
        on=['playerId', 'zone'],
        how='outer'
    )

    # Get player names from batting stats
    batting_path = os.path.join(PARQUET_DIR, f"batting_{year}.parquet")
    if os.path.exists(batting_path):
        names_df = con.execute(f"""
            SELECT DISTINCT playerId, playerName
            FROM read_parquet('{batting_path.replace(chr(92), '/')}')
        """).df()
        merged = merged.merge(names_df, on='playerId', how='left')
    else:
        merged['playerName'] = None

    merged['season'] = year

    merged.to_parquet(zone_path, index=False)
    print(f"  Saved {len(merged):,} player-zone rows → statcast_zones_{year}.parquet")

if __name__ == "__main__":
    years = range(2015, 2026)
    total = len(years)

    print(f"Aggregating zone data for {total} seasons...\n")

    for i, year in enumerate(years):
        print(f"[{i+1}/{total}] Season {year}")
        try:
            aggregate_zones(year)
        except Exception as e:
            print(f"  ERROR aggregating zones {year}: {e}")

    print("\nAll done!")