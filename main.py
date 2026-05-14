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
    FROM read_parquet('data/parquet/statcast_2024.parquet')
    WHERE batter = 592450
    AND game_type = 'R'
    AND events IS NOT NULL
    GROUP BY events, woba_value, woba_denom
    ORDER BY events
""").df()

print(df.to_string())