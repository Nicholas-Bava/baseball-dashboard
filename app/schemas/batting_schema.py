# app/schemas/batting_schema.py
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class BattingSeasonDTO:
    season: int
    playerName: str
    playerId: int
    team: Optional[str] = None
    age: Optional[int] = None
    gamesPlayed: Optional[int] = None
    atBats: Optional[int] = None
    plateAppearances: Optional[int] = None
    runs: Optional[int] = None
    hits: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    homeRuns: Optional[int] = None
    rbi: Optional[int] = None
    stolenBases: Optional[int] = None
    caughtStealing: Optional[int] = None
    stolenBasePercentage: Optional[str] = None
    caughtStealingPercentage: Optional[str] = None
    baseOnBalls: Optional[int] = None
    intentionalWalks: Optional[int] = None
    strikeOuts: Optional[int] = None
    hitByPitch: Optional[int] = None
    avg: Optional[str] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    babip: Optional[str] = None
    totalBases: Optional[int] = None
    leftOnBase: Optional[int] = None
    groundOuts: Optional[int] = None
    airOuts: Optional[int] = None
    groundIntoDoublePlay: Optional[int] = None
    groundOutsToAirouts: Optional[str] = None
    numberOfPitches: Optional[int] = None
    sacBunts: Optional[int] = None
    sacFlies: Optional[int] = None
    catchersInterference: Optional[int] = None
    atBatsPerHomeRun: Optional[str] = None

    def to_dict(self):
        return asdict(self)