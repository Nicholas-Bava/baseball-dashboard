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