# app/services/league_context_service.py
from app.repositories.league_context_repository import LeagueContextRepository
from app.schemas.league_context_schema import LeagueContextDTO

class LeagueContextService:

    def __init__(self):
        self.repo = LeagueContextRepository()

    def get_batting_context(self, stat: str, seasons: list) -> list:
        """
        Returns league average and league leader for a batting stat
        across the given seasons. Used to add context lines to the
        career stat chart on the player profile page.
        """
        df = self.repo.get_batting_league_context(stat, seasons)

        if df.empty:
            return []

        return [
            LeagueContextDTO(
                season=int(row['season']),
                stat=stat,
                leagueAverage=row['leagueAverage'],
                leagueLeaderValue=row['leagueLeaderValue'],
                leagueLeaderName=row['leagueLeaderName']
            ).to_dict()
            for _, row in df.iterrows()
        ]

    def get_player_rankings(self, player_id: int, season: int) -> dict:
        return self.repo.get_player_rankings(player_id, season)

    def get_stat_distribution(self, stat: str, seasons: list) -> dict:
        return self.repo.get_stat_distribution(stat, seasons)