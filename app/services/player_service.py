# app/services/player_service.py
import pandas as pd
from app.repositories.batting_repository import BattingRepository
from app.repositories.pitching_repository import PitchingRepository
from app.schemas.batting_schema import BattingSeasonDTO
from app.schemas.pitching_schema import PitchingSeasonDTO
from app.schemas.player_schema import PlayerProfileDTO

class PlayerService:

    def __init__(self):
        self.batting_repo = BattingRepository()
        self.pitching_repo = PitchingRepository()

    def get_player_profile(self, player_name: str, stat_type: str = "batting") -> dict:

        batting_df = pd.DataFrame()
        pitching_df = pd.DataFrame()

        if stat_type == "batting":
            batting_df = self.batting_repo.get_by_player(player_name)
        elif stat_type == "pitching":
            pitching_df = self.pitching_repo.get_by_player(player_name)
        else:
            return {"error": f"Invalid type: {stat_type}. Must be 'batting' or 'pitching'"}

        if batting_df.empty and pitching_df.empty:
            return {}

        source_df = batting_df if not batting_df.empty else pitching_df
        player_id = int(source_df.iloc[0]["playerId"])

        batting_seasons = [
            self._build_batting_dto(row)
            for _, row in batting_df.iterrows()
        ]

        pitching_seasons = [
            self._build_pitching_dto(row)
            for _, row in pitching_df.iterrows()
        ]

        profile = PlayerProfileDTO(
            playerName=player_name,
            playerId=player_id,
            isTwoWay=False,
            batting=batting_seasons,
            pitching=pitching_seasons
        )

        return profile.to_dict()

    def _build_batting_dto(self, row: pd.Series) -> BattingSeasonDTO:
        def safe_int(val):
            try:
                return int(val) if val is not None and str(val) not in ["", "nan"] else None
            except:
                return None

        def safe_str(val):
            try:
                return str(val) if val is not None and str(val) not in ["", "nan", "-.--"] else None
            except:
                return None

        return BattingSeasonDTO(
            season=safe_int(row.get("season")),
            playerName=str(row.get("playerName", "")),
            playerId=safe_int(row.get("playerId")),
            team=safe_str(row.get("team")),
            age=safe_int(row.get("age")),
            gamesPlayed=safe_int(row.get("gamesPlayed")),
            atBats=safe_int(row.get("atBats")),
            plateAppearances=safe_int(row.get("plateAppearances")),
            runs=safe_int(row.get("runs")),
            hits=safe_int(row.get("hits")),
            doubles=safe_int(row.get("doubles")),
            triples=safe_int(row.get("triples")),
            homeRuns=safe_int(row.get("homeRuns")),
            rbi=safe_int(row.get("rbi")),
            stolenBases=safe_int(row.get("stolenBases")),
            caughtStealing=safe_int(row.get("caughtStealing")),
            stolenBasePercentage=safe_str(row.get("stolenBasePercentage")),
            caughtStealingPercentage=safe_str(row.get("caughtStealingPercentage")),
            baseOnBalls=safe_int(row.get("baseOnBalls")),
            intentionalWalks=safe_int(row.get("intentionalWalks")),
            strikeOuts=safe_int(row.get("strikeOuts")),
            hitByPitch=safe_int(row.get("hitByPitch")),
            avg=safe_str(row.get("avg")),
            obp=safe_str(row.get("obp")),
            slg=safe_str(row.get("slg")),
            ops=safe_str(row.get("ops")),
            babip=safe_str(row.get("babip")),
            totalBases=safe_int(row.get("totalBases")),
            leftOnBase=safe_int(row.get("leftOnBase")),
            groundOuts=safe_int(row.get("groundOuts")),
            airOuts=safe_int(row.get("airOuts")),
            groundIntoDoublePlay=safe_int(row.get("groundIntoDoublePlay")),
            groundOutsToAirouts=safe_str(row.get("groundOutsToAirouts")),
            numberOfPitches=safe_int(row.get("numberOfPitches")),
            sacBunts=safe_int(row.get("sacBunts")),
            sacFlies=safe_int(row.get("sacFlies")),
            catchersInterference=safe_int(row.get("catchersInterference")),
            atBatsPerHomeRun=safe_str(row.get("atBatsPerHomeRun"))
        )

    def _build_pitching_dto(self, row: pd.Series) -> PitchingSeasonDTO:
        def safe_int(val):
            try:
                return int(val) if val is not None and str(val) not in ["", "nan"] else None
            except:
                return None

        def safe_str(val):
            try:
                return str(val) if val is not None and str(val) not in ["", "nan", "-.--"] else None
            except:
                return None

        return PitchingSeasonDTO(
            season=safe_int(row.get("season")),
            playerName=str(row.get("playerName", "")),
            playerId=safe_int(row.get("playerId")),
            team=safe_str(row.get("team")),
            gamesPlayed=safe_int(row.get("gamesPlayed")),
            gamesStarted=safe_int(row.get("gamesStarted")),
            gamesPitched=safe_int(row.get("gamesPitched")),
            gamesFinished=safe_int(row.get("gamesFinished")),
            wins=safe_int(row.get("wins")),
            losses=safe_int(row.get("losses")),
            winPercentage=safe_str(row.get("winPercentage")),
            era=safe_str(row.get("era")),
            inningsPitched=safe_str(row.get("inningsPitched")),
            hits=safe_int(row.get("hits")),
            runs=safe_int(row.get("runs")),
            earnedRuns=safe_int(row.get("earnedRuns")),
            homeRuns=safe_int(row.get("homeRuns")),
            baseOnBalls=safe_int(row.get("baseOnBalls")),
            intentionalWalks=safe_int(row.get("intentionalWalks")),
            strikeOuts=safe_int(row.get("strikeOuts")),
            hitByPitch=safe_int(row.get("hitByPitch")),
            hitBatsmen=safe_int(row.get("hitBatsmen")),
            whip=safe_str(row.get("whip")),
            battersFaced=safe_int(row.get("battersFaced")),
            outs=safe_int(row.get("outs")),
            strikes=safe_int(row.get("strikes")),
            strikePercentage=safe_str(row.get("strikePercentage")),
            strikeoutsPer9Inn=safe_str(row.get("strikeoutsPer9Inn")),
            walksPer9Inn=safe_str(row.get("walksPer9Inn")),
            hitsPer9Inn=safe_str(row.get("hitsPer9Inn")),
            homeRunsPer9=safe_str(row.get("homeRunsPer9")),
            runsScoredPer9=safe_str(row.get("runsScoredPer9")),
            strikeoutWalkRatio=safe_str(row.get("strikeoutWalkRatio")),
            pitchesPerInning=safe_str(row.get("pitchesPerInning")),
            saves=safe_int(row.get("saves")),
            saveOpportunities=safe_int(row.get("saveOpportunities")),
            blownSaves=safe_int(row.get("blownSaves")),
            holds=safe_int(row.get("holds")),
            completeGames=safe_int(row.get("completeGames")),
            shutouts=safe_int(row.get("shutouts")),
            balks=safe_int(row.get("balks")),
            wildPitches=safe_int(row.get("wildPitches")),
            pickoffs=safe_int(row.get("pickoffs")),
            inheritedRunners=safe_int(row.get("inheritedRunners")),
            inheritedRunnersScored=safe_int(row.get("inheritedRunnersScored")),
            groundOuts=safe_int(row.get("groundOuts")),
            airOuts=safe_int(row.get("airOuts")),
            groundOutsToAirouts=safe_str(row.get("groundOutsToAirouts")),
            sacBunts=safe_int(row.get("sacBunts")),
            sacFlies=safe_int(row.get("sacFlies"))
        )

    def search(self, query: str) -> list:
        batters = self.batting_repo.search_players(query)
        pitchers = self.pitching_repo.search_players(query)
        combined = pd.concat([batters, pitchers]).drop_duplicates(subset="playerId")
        return combined.to_dict(orient="records")