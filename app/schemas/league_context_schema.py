# app/schemas/league_context_schema.py
from dataclasses import dataclass, asdict

@dataclass
class LeagueContextDTO:
    season: int
    stat: str
    leagueAverage: float
    leagueLeaderValue: float
    leagueLeaderName: str

    def to_dict(self):
        return asdict(self)