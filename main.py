# main.py
from app.services.batting_service import BattingService
from app.services.pitching_service import PitchingService
from app.services.player_service import PlayerService

batting_svc = BattingService()
pitching_svc = PitchingService()
player_svc = PlayerService()

print("=== HR Leaderboard (2024) ===")
print(batting_svc.get_leaderboard("homeRuns", season=2024, limit=5))

print("\n=== Judge Career ===")
print(batting_svc.get_player_career("Aaron Judge"))

print("\n=== 2024 Batting Season Summary ===")
print(batting_svc.get_season_summary(2024))

print("\n=== ERA Leaderboard (2024) ===")
print(pitching_svc.get_leaderboard("era", season=2024, limit=5))

print("\n=== 2024 Pitching Season Summary ===")
print(pitching_svc.get_season_summary(2024))

print("\n=== Ohtani Player Profile ===")
print(player_svc.get_player_profile("Shohei Ohtani"))

print("\n=== Player Search: soto ===")
print(player_svc.search("soto"))