# app/schemas/pitching_schema.py
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class PitchingSeasonDTO:
    season: int
    playerName: str
    playerId: int
    team: Optional[str] = None
    gamesPlayed: Optional[int] = None
    gamesStarted: Optional[int] = None
    gamesPitched: Optional[int] = None
    gamesFinished: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    winPercentage: Optional[str] = None
    era: Optional[str] = None
    inningsPitched: Optional[str] = None
    hits: Optional[int] = None
    runs: Optional[int] = None
    earnedRuns: Optional[int] = None
    homeRuns: Optional[int] = None
    baseOnBalls: Optional[int] = None
    intentionalWalks: Optional[int] = None
    strikeOuts: Optional[int] = None
    hitByPitch: Optional[int] = None
    hitBatsmen: Optional[int] = None
    whip: Optional[str] = None
    battersFaced: Optional[int] = None
    outs: Optional[int] = None
    strikes: Optional[int] = None
    strikePercentage: Optional[str] = None
    strikeoutsPer9Inn: Optional[str] = None
    walksPer9Inn: Optional[str] = None
    hitsPer9Inn: Optional[str] = None
    homeRunsPer9: Optional[str] = None
    runsScoredPer9: Optional[str] = None
    strikeoutWalkRatio: Optional[str] = None
    pitchesPerInning: Optional[str] = None
    saves: Optional[int] = None
    saveOpportunities: Optional[int] = None
    blownSaves: Optional[int] = None
    holds: Optional[int] = None
    completeGames: Optional[int] = None
    shutouts: Optional[int] = None
    balks: Optional[int] = None
    wildPitches: Optional[int] = None
    pickoffs: Optional[int] = None
    inheritedRunners: Optional[int] = None
    inheritedRunnersScored: Optional[int] = None
    groundOuts: Optional[int] = None
    airOuts: Optional[int] = None
    groundOutsToAirouts: Optional[str] = None
    sacBunts: Optional[int] = None
    sacFlies: Optional[int] = None

    def to_dict(self):
        return asdict(self)