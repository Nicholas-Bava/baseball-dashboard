# app/services/batting_service.py
import pandas as pd
from app.repositories.batting_repository import BattingRepository

class BattingService:

    def __init__(self):
        self.repo = BattingRepository()

    def get_leaderboard(self, stat: str, season: int = None, limit: int = 25) -> pd.DataFrame:
        return self.repo.get_leaderboard(stat, season, limit)

    def get_player_career(self, player_name: str) -> dict:
        df = self.repo.get_by_player(player_name)
        if df.empty:
            return {}

        # Use to_json then back to dict to handle numpy type serialization
        import json
        seasons = json.loads(df.to_json(orient="records"))

        return {
            "player": player_name,
            "seasons": seasons,
            "career_hr": int(df["homeRuns"].astype(float).sum()),
            "career_rbi": int(df["rbi"].astype(float).sum()),
            "best_avg": float(df["avg"].max())
        }

    def get_season_summary(self, season: int) -> dict:
        df = self.repo.get_by_season(season)
        if df.empty:
            return {}
        return {
            "season": season,
            "total_players": len(df),
            "total_hr": df["homeRuns"].astype(int).sum(),
            "avg_avg": df["avg"].astype(float).mean().round(3)
        }

    def search_players(self, query: str) -> pd.DataFrame:
        return self.repo.search_players(query)