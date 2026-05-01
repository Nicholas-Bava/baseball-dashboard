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

import json

print("=== Judge Batting ===")
print(json.dumps(player_svc.get_player_profile("Aaron Judge", "batting"), indent=2))

print("=== Scherzer Pitching ===")
print(json.dumps(player_svc.get_player_profile("Max Scherzer", "pitching"), indent=2))