# app/jobs/aggregate_statcast.py
import os
import duckdb
import pandas as pd
from app.constants.woba_weights import get_woba_weights
from app.constants.qualifiers import STATCAST_BATTED_BALL_TYPE, STATCAST_HARD_HIT_MPH, STATCAST_BARREL_CODE, GAME_TYPE_REGULAR
PARQUET_DIR = os.path.join(os.path.dirname(__file__), "../../data/parquet")

def get_statcast_path(year: int) -> str:
    return os.path.join(PARQUET_DIR, f"statcast_{year}.parquet")

def get_agg_path(year: int) -> str:
    return os.path.join(PARQUET_DIR, f"statcast_batting_agg_{year}.parquet")

def aggregate_season(year: int):
    statcast_path = get_statcast_path(year)
    agg_path = get_agg_path(year)

    # Skip if already aggregated
    if os.path.exists(agg_path):
        print(f"  statcast_batting_agg_{year}.parquet already exists — skipping")
        return

    if not os.path.exists(statcast_path):
        print(f"  statcast_{year}.parquet not found — skipping")
        return

    print(f"  Aggregating {year}...")

    con = duckdb.connect()

    # ============================================
    # QUERY 1 — Contact quality metrics
    # Filter: batted balls only with valid exit velo
    # ============================================
    contact_df = con.execute(f"""
        SELECT
            batter as playerId,
            COUNT(*) as total_batted_balls,
            ROUND(AVG(launch_speed), 1) as avg_exit_velo,
            ROUND(AVG(launch_angle), 1) as avg_launch_angle,
            ROUND(100.0 * SUM(CASE WHEN launch_speed >= {STATCAST_HARD_HIT_MPH} THEN 1 ELSE 0 END) / COUNT(*), 1) as hard_hit_pct,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = {STATCAST_BARREL_CODE} THEN 1 ELSE 0 END) / COUNT(launch_speed), 1) as barrel_pct,
            ROUND(100.0 * SUM(CASE WHEN launch_angle BETWEEN 8 AND 32 THEN 1 ELSE 0 END) / COUNT(launch_speed), 1) as sweet_spot_pct
        FROM read_parquet('{statcast_path.replace(chr(92), '/')}')
        WHERE type = '{STATCAST_BATTED_BALL_TYPE}'
        AND game_type = '{GAME_TYPE_REGULAR}'
        GROUP BY batter
    """).df()

    # ============================================
    # QUERY 2 — Expected stats
    # Filter: batted balls only, nulls handled by AVG
    # ============================================
    expected_df = con.execute(f"""
        SELECT
            batter as playerId,
            ROUND(AVG(estimated_ba_using_speedangle), 3) as xbacon,
            ROUND(AVG(estimated_slg_using_speedangle), 3) as xslgcon,
            ROUND(AVG(estimated_woba_using_speedangle), 3) as xwobacon,
            SUM(estimated_ba_using_speedangle) as sum_xbacon,
            SUM(estimated_slg_using_speedangle) as sum_xslgcon,
            SUM(CASE WHEN events != 'intent_walk' 
                THEN estimated_woba_using_speedangle 
                ELSE 0 END) as sum_xwobacon
        FROM read_parquet('{statcast_path.replace(chr(92), '/')}')
        WHERE type = '{STATCAST_BATTED_BALL_TYPE}'
        AND game_type = '{GAME_TYPE_REGULAR}'
        GROUP BY batter
    """).df()

    # ============================================
    # QUERY 3 — Plate discipline
    # Uses all pitches not just batted balls
    # description field tells us what happened
    # ============================================
    discipline_df = con.execute(f"""
        SELECT
            batter as playerId,
            -- Total plate appearances
            COUNT(CASE WHEN events IS NOT NULL THEN 1 END) as total_pa,
            -- Walks
            COUNT(CASE WHEN events = 'walk' THEN 1 END) as walks,
            -- Intentional Walks
            COUNT(CASE WHEN events = 'intent_walk' THEN 1 END) as ibb,
            -- Hit by pitch
            COUNT(CASE WHEN events = 'hit_by_pitch' THEN 1 END) as hbp,
            -- Sac Flies
            COUNT(CASE WHEN events = 'sac_fly' THEN 1 END) as sac_flies,
            -- Sac Bunts
            COUNT(CASE WHEN events = 'sac_bunt' THEN 1 END) as sac_bunts,
            -- Total swings
            COUNT(CASE WHEN description IN (
                'swinging_strike', 'swinging_strike_blocked',
                'foul', 'foul_tip', 'hit_into_play',
                'hit_into_play_no_out', 'hit_into_play_score',
                'foul_bunt', 'missed_bunt'
            ) THEN 1 END) as total_swings,
            -- Whiffs
            COUNT(CASE WHEN description IN (
                'swinging_strike', 'swinging_strike_blocked'
            ) THEN 1 END) as total_whiffs,
            -- Chase swings
            COUNT(CASE WHEN zone > 10 AND description IN (
                'swinging_strike', 'swinging_strike_blocked',
                'foul', 'foul_tip', 'hit_into_play',
                'hit_into_play_no_out', 'hit_into_play_score'
            ) THEN 1 END) as chase_swings,
            -- Pitches outside zone
            COUNT(CASE WHEN zone > 10 THEN 1 END) as total_outside_zone,
            SUM(woba_denom) as woba_denom_sum,
            SUM(CASE WHEN type != 'X' AND woba_denom = 1 
                THEN woba_value ELSE 0 END) as non_contact_woba,
            COUNT(CASE WHEN events = 'catcher_interf' THEN 1 END) as ci
        FROM read_parquet('{statcast_path.replace(chr(92), '/')}')
        WHERE game_type = '{GAME_TYPE_REGULAR}'
        GROUP BY batter
    """).df()

    # Calculate plate discipline rates
    discipline_df['whiff_pct'] = (
        discipline_df['total_whiffs'] / discipline_df['total_swings'] * 100
    ).round(1)
    discipline_df['chase_pct'] = (
        discipline_df['chase_swings'] / discipline_df['total_outside_zone'] * 100
    ).round(1)
    discipline_df['contact_pct'] = (
        100 - discipline_df['whiff_pct']
    ).round(1)

    # ============================================
    # MERGE all three query results
    # Join on playerId
    # ============================================
    merged = contact_df.merge(expected_df, on='playerId', how='left')
    merged = merged.merge(
        discipline_df[['playerId', 'total_pa', 'walks', 'hbp', 'ibb', 'sac_flies', 'ci', 'sac_bunts',
                       'total_swings', 'whiff_pct', 'woba_denom_sum', 'chase_pct', 'contact_pct']],
        on='playerId',
        how='left'
    )

    # Calculate xwOBA using season-specific weights
    weights = get_woba_weights(year)

    merged['xwoba'] = (
                              merged['sum_xwobacon'] +
                              merged['walks'] * weights['wBB'] +
                              merged['hbp'] * weights['wHBP']
                      ) / (merged['woba_denom_sum'] - merged['ci'])

    merged['ab'] = (
            merged['total_pa'] - merged['walks'] - merged['ibb'] -
            merged['hbp'] - merged['sac_flies'] - merged['sac_bunts'] - merged['ci']
    )

    merged['xba'] = (
            merged['sum_xbacon'] / merged['ab']
    ).round(3)

    merged['xslg'] = (
            merged['sum_xslgcon'] / merged['ab']
    ).round(3)

    # Get player names from batting stats Parquet - useful for debug
    batting_path = os.path.join(PARQUET_DIR, f"batting_{year}.parquet")
    if os.path.exists(batting_path):
        names_df = con.execute(f"""
            SELECT DISTINCT playerId, playerName
            FROM read_parquet('{batting_path.replace(chr(92), '/')}')
        """).df()
        merged = merged.merge(names_df, on='playerId', how='left')
    else:
        merged['playerName'] = None

    # Add season column
    merged['season'] = year

    # Save to Parquet
    merged.to_parquet(agg_path, index=False)
    print(f"  Saved {len(merged):,} players → statcast_batting_agg_{year}.parquet")

if __name__ == "__main__":
    years = range(2015, 2026)
    total = len(years)

    print(f"Aggregating Statcast data for {total} seasons...\n")

    for i, year in enumerate(years):
        print(f"[{i+1}/{total}] Season {year}")
        try:
            aggregate_season(year)
        except Exception as e:
            print(f"  ERROR aggregating {year}: {e}")

    print("\nAll done!")