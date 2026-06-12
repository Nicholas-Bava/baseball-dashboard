# app/adapters/pybaseball_adapter.py
import statsapi
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PybaseballAdapter:



    def fetch_batting_stats(self, year: int) -> pd.DataFrame:

        CANONICAL_BATTING_COLUMNS = [
            'age', 'gamesPlayed', 'groundOuts', 'airOuts', 'runs', 'doubles', 'triples',
            'homeRuns', 'strikeOuts', 'baseOnBalls', 'intentionalWalks', 'hits',
            'hitByPitch', 'avg', 'atBats', 'obp', 'slg', 'ops', 'caughtStealing',
            'stolenBases', 'stolenBasePercentage', 'caughtStealingPercentage',
            'groundIntoDoublePlay', 'numberOfPitches', 'plateAppearances', 'totalBases',
            'rbi', 'leftOnBase', 'sacBunts', 'sacFlies', 'babip', 'groundOutsToAirouts',
            'catchersInterference', 'atBatsPerHomeRun', 'playerId', 'playerName', 'season'
        ]

        logger.info(f"Fetching batting stats for {year}")
        data = statsapi.get('stats', {
            'stats': 'season',
            'group': 'hitting',
            'season': year,
            'playerPool': 'All',
            'limit': 2000
        })
        rows = [s['stat'] | {'playerId': s['player']['id'], 'playerName': s['player']['fullName'], 'season': year}
                for s in data['stats'][0]['splits']]
        df = pd.DataFrame(rows)
        df = df.reindex(columns=CANONICAL_BATTING_COLUMNS)
        return df

    def fetch_pitching_stats(self, year: int) -> pd.DataFrame:
        logger.info(f"Fetching pitching stats for {year}")
        data = statsapi.get('stats', {
            'stats': 'season',
            'group': 'pitching',
            'season': year,
            'playerPool': 'All',
            'limit': 2000
        })
        rows = [s['stat'] | {'playerId': s['player']['id'], 'playerName': s['player']['fullName'], 'season': year}
                for s in data['stats'][0]['splits']]
        return pd.DataFrame(rows)