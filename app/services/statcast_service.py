# app/services/statcast_service.py
from app.repositories.statcast_repository import StatcastRepository

class StatcastService:

    def __init__(self):
        self.repo = StatcastRepository()

    def get_player_zone_data(self, player_id: int, season: int) -> dict:
        """
        Returns player zone data and league averages combined.
        Frontend uses this to color the heat map.
        """
        player_zones = self.repo.get_player_zones(player_id, season)
        league_zones = self.repo.get_league_zone_averages(season)

        if player_zones.empty:
            return {}

        # Merge player and league data on zone
        merged = player_zones.merge(
            league_zones,
            on='zone',
            how='left'
        )

        return {
            'playerId': player_id,
            'season': season,
            'zones': merged.to_dict(orient='records')
        }

    def get_player_season_statcast(self, player_id: int, season: int) -> dict:
        df = self.repo.get_player_season_statcast(player_id, season)
        print(f"DEBUG: player_id={player_id} type={type(player_id)} season={season} empty={df.empty}")
        if df.empty:
            return {}
        return df.iloc[0].to_dict()

    def get_player_statcast_rankings(self, player_id: int, season: int) -> dict:
        return self.repo.get_player_statcast_rankings(player_id, season)