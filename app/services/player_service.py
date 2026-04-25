# app/services/player_service.py
import pandas as pd
from app.repositories.batting_repository import BattingRepository
from app.repositories.pitching_repository import PitchingRepository

class PlayerService:

    def __init__(self):
        self.batting_repo = BattingRepository()
        self.pitching_repo = PitchingRepository()

    def get_player_profile(self, player_name: str) -> dict:
        batting = self.batting_repo.get_by_player(player_name)
        pitching = self.pitching_repo.get_by_player(player_name)

        profile = {
            "player": player_name,
            "is_two_way": not pitching.empty and not batting.empty,
            "batting": batting.to_dict(orient="records") if not batting.empty else [],
            "pitching": pitching.to_dict(orient="records") if not pitching.empty else []
        }

        return profile

    def search(self, query: str) -> list:
        batters = self.batting_repo.search_players(query)
        pitchers = self.pitching_repo.search_players(query)

        # Combine and deduplicate by playerId
        combined = pd.concat([batters, pitchers]).drop_duplicates(subset="playerId")
        return combined.to_dict(orient="records")