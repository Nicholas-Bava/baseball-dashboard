# app/constants/qualifiers.py

# ============================================
# MLB STATISTICAL QUALIFIERS
# These thresholds determine which players are
# included in league average and rate stat
# calculations. Based on official MLB rules.
# ============================================

# Games played per season by year
# Used to calculate all other qualifiers dynamically
GAMES_PER_SEASON = {
    1995: 144,  # Strike shortened - started April 25
    2020: 60,  # COVID shortened
    # All other seasons default to 162
}
DEFAULT_GAMES = 162

def get_games(season: int) -> int:
    """Returns the number of games played in a given season."""
    return GAMES_PER_SEASON.get(season, DEFAULT_GAMES)


# ============================================
# BATTING QUALIFIERS
# ============================================

# Official MLB batting title qualifier
# 3.1 plate appearances per team game
BATTING_PA_PER_GAME = 3.1

def get_batting_qualifier(season: int) -> int:
    """
    Returns the minimum plate appearances to qualify
    for batting rate stats (AVG, OBP, SLG, OPS) in a given season.
    Based on the official MLB batting title rule.
    Example: 162 games × 3.1 = 502 PA
    """
    return round(get_games(season) * BATTING_PA_PER_GAME)


# ============================================
# PITCHING QUALIFIERS
# ============================================

# Official MLB ERA title qualifier for starting pitchers
# 1.0 inning pitched per team game
STARTER_IP_PER_GAME = 1.0

def get_starter_qualifier(season: int) -> float:
    """
    Returns minimum IP for starting pitcher rate stat qualification.
    Official MLB ERA title rule: 1.0 IP per team game.
    Example: 162 games → 162 IP
    """
    return get_games(season) * STARTER_IP_PER_GAME

# Minimum IP for relievers to qualify for rate stat rankings
# 81 IP (official 0.5 × 162) would exclude most real relievers
# 40 IP captures closers, setup men, and regular middle relievers
# while filtering out specialists and low-usage arms
RELIEVER_MIN_IP = 40

def get_reliever_qualifier(season: int) -> float:
    """
    Returns minimum IP for relief pitcher rate stat qualification.
    Scales proportionally for shortened seasons.
    Example: 162 games → 40 IP, 60 games → ~15 IP
    """
    return round(RELIEVER_MIN_IP * (get_games(season) / DEFAULT_GAMES))

STATCAST_PA_PER_GAME = 2.1

def get_statcast_qualifier(season: int) -> int:
    """
    Returns minimum PA for Statcast metric qualification.
    Based on Baseball Savant's standard of 2.1 PA per team game.
    """
    return round(get_games(season) * STATCAST_PA_PER_GAME)


# ============================================
# COUNTING STAT QUALIFIERS
# ============================================

# Counting stats (HR, RBI, Strikeouts, Saves) have no
# official minimum - the leader is simply whoever has
# the most. These minimums just filter out garbage
# appearances from the league AVERAGE calculation.

# Minimum PA to be included in counting stat averages
# Filters out pitchers and cup-of-coffee players
COUNTING_STAT_MIN_PA = 100

# Minimum IP to be included in pitcher counting stat averages
COUNTING_STAT_MIN_IP = 20

# Statcast aggregation filters
# Only batted ball events (type = 'X') are included
STATCAST_BATTED_BALL_TYPE = 'X'

# Minimum exit velocity to be included in contact quality metrics
# Null exit velocities (~2%) are excluded - tracking system failures
STATCAST_MIN_EXIT_VELO = 0  # just checking IS NOT NULL

# Hard hit threshold - Baseball Savant standard
STATCAST_HARD_HIT_MPH = 95.0

# Barrel classification uses launch_speed_angle = 6
# This is Baseball Savant's barrel classification code
STATCAST_BARREL_CODE = 6

# xBA/xSLG/xwOBA nulls are excluded naturally via AVG()
# Some batted balls lack expected stats (sac flies, bunts,
# extreme exit velo/angle combinations outside model range)

# Statcast game type filters
GAME_TYPE_REGULAR = 'R'
GAME_TYPE_SPRING = 'S'
GAME_TYPE_POSTSEASON = ('F', 'D', 'L', 'W')
GAME_TYPE_ALL = ('R', 'S', 'F', 'D', 'L', 'W')