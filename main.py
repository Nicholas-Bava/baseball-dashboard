# main.py
from app.services.batting_service import BattingService
from app.services.pitching_service import PitchingService
from app.services.player_service import PlayerService

batting_svc = BattingService()
pitching_svc = PitchingService()
player_svc = PlayerService()

from app.repositories.batting_repository import BattingRepository
batting_repo = BattingRepository()

# Check how many seasons we have
import duckdb
con = duckdb.connect()

from app.db.parquet_utils import get_parquet_union
union = get_parquet_union("batting")

from app.services.league_context_service import LeagueContextService
import json

import duckdb
from app.constants.qualifiers import get_statcast_qualifier

con = duckdb.connect()

import duckdb
from app.constants.qualifiers import get_statcast_qualifier

con = duckdb.connect()

df = con.execute(f"""
    SELECT playerName, season, avg_exit_velo, hard_hit_pct, 
           barrel_pct, xba, xwoba, whiff_pct, chase_pct
    FROM read_parquet('data/parquet/statcast_batting_agg_2024.parquet')
    WHERE total_pa >= {get_statcast_qualifier(2024)}
    ORDER BY barrel_pct DESC
    LIMIT 10
""").df()

print(df.to_string())

df = con.execute("""
    SELECT 
        COUNT(CASE WHEN events IS NOT NULL THEN 1 END) as total_pa,
        COUNT(CASE WHEN events = 'walk' THEN 1 END) as walks,
        COUNT(CASE WHEN events = 'intent_walk' THEN 1 END) as ibb,
        COUNT(CASE WHEN events = 'hit_by_pitch' THEN 1 END) as hbp,
        COUNT(CASE WHEN events = 'sac_fly' THEN 1 END) as sac_flies,
        COUNT(CASE WHEN events = 'sac_bunt' THEN 1 END) as sac_bunts
    FROM read_parquet('data/parquet/statcast_2024.parquet')
    WHERE batter = 592450
    AND game_type = 'R'
""").df()

print(df.to_string())

df = con.execute("""
    SELECT *
    FROM read_parquet('data/parquet/statcast_2024.parquet')
    LIMIT 1
""").df()

print(df.columns.tolist())

df = con.execute("""
    SELECT 
        hyper_speed,
        launch_speed,
        estimated_ba_using_speedangle
    FROM read_parquet('data/parquet/statcast_2024.parquet')
    WHERE batter = 592450
    AND type = 'X'
    AND game_type = 'R'
    AND hyper_speed IS NOT NULL
    LIMIT 5
""").df()

print(df.to_string())

df = con.execute("""
    SELECT 
        COUNT(*) as all_batted_balls,
        COUNT(CASE WHEN launch_speed IS NOT NULL THEN 1 END) as with_exit_velo,
        SUM(estimated_woba_using_speedangle) as sum_xwoba,
        AVG(estimated_woba_using_speedangle) as avg_xwoba
    FROM read_parquet('data/parquet/statcast_2024.parquet')
    WHERE batter = 592450
    AND type = 'X'
    AND game_type = 'R'
""").df()

print(df.to_string())

df = con.execute("""
    SELECT 
        events,
        woba_value,
        woba_denom,
        COUNT(*) as count
    FROM read_parquet('data/parquet/statcast_2022.parquet')
    WHERE batter = 592450
    AND game_type = 'R'
    AND events IS NOT NULL
    GROUP BY events, woba_value, woba_denom
    ORDER BY events
""").df()

print(df.to_string())

import duckdb
from app.constants.woba_weights import get_woba_weights
from app.constants.qualifiers import get_statcast_qualifier

con = duckdb.connect()

# Judge across multiple years
for year in [2017, 2019, 2022, 2024]:
    df = con.execute(f"""
        SELECT 
            playerName, season, avg_exit_velo, hard_hit_pct, 
            barrel_pct, xba, xwoba, xbacon, xwobacon
        FROM read_parquet('data/parquet/statcast_batting_agg_{year}.parquet')
        WHERE playerName = 'Aaron Judge'
    """).df()
    print(df.to_string())
    print()

# Also check Juan Soto 2024 as a comparison
df2 = con.execute("""
    SELECT 
        playerName, season, avg_exit_velo, hard_hit_pct,
        barrel_pct, xba, xwoba, xbacon, xwobacon
    FROM read_parquet('data/parquet/statcast_batting_agg_2024.parquet')
    WHERE playerName = 'Juan Soto'
""").df()
print(df2.to_string())

df = con.execute("""
    SELECT 
        SUM(estimated_woba_using_speedangle) as sum_unfiltered,
        SUM(CASE WHEN woba_denom = 1 
            THEN estimated_woba_using_speedangle 
            ELSE 0 END) as sum_filtered,
        COUNT(CASE WHEN type = 'X' AND woba_denom != 1 
            AND estimated_woba_using_speedangle IS NOT NULL
            THEN 1 END) as excluded_batted_balls
    FROM read_parquet('data/parquet/statcast_2024.parquet')
    WHERE batter = 592450
    AND type = 'X'
    AND game_type = 'R'
""").df()

print(df.to_string())

con = duckdb.connect()

df = con.execute("""
    SELECT 
        COUNT(CASE WHEN events IS NOT NULL THEN 1 END) as total_pa,
        COUNT(CASE WHEN events = 'walk' THEN 1 END) as walks,
        COUNT(CASE WHEN events = 'intent_walk' THEN 1 END) as ibb,
        COUNT(CASE WHEN events = 'hit_by_pitch' THEN 1 END) as hbp,
        SUM(woba_denom) as woba_denom_sum,
        SUM(CASE WHEN type = 'X' THEN estimated_woba_using_speedangle ELSE 0 END) as sum_xwobacon
    FROM read_parquet('data/parquet/statcast_2022.parquet')
    WHERE batter = 592450
    AND game_type = 'R'
""").df()

print(df.to_string())

df = con.execute("""
    SELECT 
        SUM(CASE 
            WHEN type = 'X' AND woba_denom = 1 
                THEN estimated_woba_using_speedangle
            WHEN type != 'X' AND woba_denom = 1 
                THEN woba_value
            ELSE 0 
        END) as xwoba_numerator,
        SUM(woba_denom) as denom
    FROM read_parquet('data/parquet/statcast_2022.parquet')
    WHERE batter = 592450
    AND game_type = 'R'
""").df()

print(df.to_string())

xwoba = df.iloc[0]['xwoba_numerator'] / df.iloc[0]['denom']
print(f"xwOBA: {xwoba:.4f}")
print(f"Baseball Savant: .468")

for year in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]:
    try:
        df = con.execute(f"""
            SELECT 
                SUM(CASE 
                    WHEN type = 'X' AND woba_denom = 1 
                        THEN estimated_woba_using_speedangle
                    WHEN type != 'X' AND woba_denom = 1 
                        THEN woba_value
                    ELSE 0 
                END) as xwoba_numerator,
                SUM(woba_denom) as denom
            FROM read_parquet('data/parquet/statcast_{year}.parquet')
            WHERE batter = 592450
            AND game_type = 'R'
        """).df()

        xwoba = df.iloc[0]['xwoba_numerator'] / df.iloc[0]['denom']
        print(f"{year}: {xwoba:.4f}")
    except Exception as e:
        print(f"{year}: ERROR - {e}")

from app.constants.woba_weights import get_woba_weights
weights = get_woba_weights(2022)

for year in [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]:
    df = con.execute(f"""
        SELECT 
            SUM(CASE WHEN type = 'X' 
                THEN estimated_woba_using_speedangle ELSE 0 END) as sum_xwobacon,
            SUM(woba_denom) as denom_with_ci,
            SUM(CASE WHEN events != 'catcher_interf' 
                THEN woba_denom ELSE 0 END) as denom_without_ci,
            COUNT(CASE WHEN events = 'walk' THEN 1 END) as walks,
            COUNT(CASE WHEN events = 'hit_by_pitch' THEN 1 END) as hbp
        FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 592450
        AND game_type = 'R'
    """).df()

    weights = get_woba_weights(year)
    row = df.iloc[0]

    numerator = row['sum_xwobacon'] + row['walks'] * weights['wBB'] + row['hbp'] * weights['wHBP']

    xwoba_with_ci = numerator / row['denom_with_ci']
    xwoba_without_ci = numerator / row['denom_without_ci']

    print(f"{year}: with_CI={xwoba_with_ci:.4f} without_CI={xwoba_without_ci:.4f}")

for year in [2017, 2019, 2022, 2024]:
    df = con.execute(f"""
        SELECT 
            COUNT(*) as total_batted_balls,
            COUNT(launch_speed) as with_exit_velo,
            COUNT(launch_speed_angle) as with_lsa,
            SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) as barrels,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) / COUNT(launch_speed_angle), 1) as barrel_pct_lsa
        FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 592450
        AND type = 'X'
        AND game_type = 'R'
    """).df()
    print(f"{year}: {df.to_string()}")
    print()

for year in [2017, 2019, 2022, 2024]:
    df = con.execute(f"""
        SELECT 
            COUNT(launch_speed) as tracked,
            COUNT(CASE WHEN launch_speed >= 98 THEN 1 END) as eligible_98,
            SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) as barrels,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) / COUNT(launch_speed), 1) as barrel_all_tracked,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) / COUNT(CASE WHEN launch_speed >= 98 THEN 1 END), 1) as barrel_98plus
        FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 592450
        AND type = 'X'
        AND game_type = 'R'
    """).df()
    print(f"{year}: {df.to_string()}")
    print()

import duckdb
from app.constants.woba_weights import get_woba_weights

con = duckdb.connect()

for year in [2017, 2019, 2022, 2024]:
    df = con.execute(f"""
        SELECT playerName, season, avg_exit_velo, hard_hit_pct, 
               barrel_pct, xba, xwoba, xbacon, xwobacon
        FROM read_parquet('data/parquet/statcast_batting_agg_{year}.parquet')
        WHERE playerName = 'Aaron Judge'
    """).df()
    print(df.to_string())
    print()