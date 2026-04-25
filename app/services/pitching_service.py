# app/services/pitching_service.py
import pandas as pd
from app.repositories.pitching_repository import PitchingRepository

class PitchingService:

    def __init__(self):
        self.repo = PitchingRepository()

    def get_leaderboard(self, stat: str, season: int = None, limit: int = 25) -> pd.DataFrame:
        return self.repo.get_leaderboard(stat, season, limit)

    def get_player_career(self, player_name: str) -> dict:
        df = self.repo.get_by_player(player_name)
        if df.empty:
            return {}
        return {
            "player": player_name,
            "seasons": df.to_dict(orient="records"),
            "career_wins": df["wins"].astype(int).sum(),
            "career_strikeouts": df["strikeOuts"].astype(int).sum(),
            "best_era": df[df["era"] != "-.--"]["era"].astype(float).min()
        }

    def get_season_summary(self, season: int) -> dict:
        df = self.repo.get_by_season(season)
        if df.empty:
            return {}
        qualified = df[df["era"] != "-.--"]
        return {
            "season": season,
            "total_pitchers": len(df),
            "avg_era": qualified["era"].astype(float).mean().round(2),
            "total_strikeouts": df["strikeOuts"].astype(int).sum()
        }

    def search_players(self, query: str) -> pd.DataFrame:
        return self.repo.search_players(query)