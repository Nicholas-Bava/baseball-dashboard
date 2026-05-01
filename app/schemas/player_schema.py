# app/schemas/player_schema.py
from dataclasses import asdict
from dataclasses import dataclass
from typing import List
from app.schemas.batting_schema import BattingSeasonDTO
from app.schemas.pitching_schema import PitchingSeasonDTO

@dataclass
class PlayerProfileDTO:
    playerName: str
    playerId: int
    isTwoWay: bool
    batting: List[BattingSeasonDTO]
    pitching: List[PitchingSeasonDTO]

    def to_dict(self):
        return {
            "playerName": self.playerName,
            "playerId": self.playerId,
            "isTwoWay": self.isTwoWay,
            "batting": [asdict(b) for b in self.batting],
            "pitching": [asdict(p) for p in self.pitching]
        }