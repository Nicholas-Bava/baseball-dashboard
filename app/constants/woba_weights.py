# app/constants/woba_weights.py
# FanGraphs wOBA linear weights by season
# Source: https://www.fangraphs.com/guts.aspx?type=cn
# These weights reflect the run value of each offensive
# outcome in that season's run environment

WOBA_WEIGHTS = {
    1990: {'wBB': 0.707, 'wHBP': 0.739, 'w1B': 0.908, 'w2B': 1.298, 'w3B': 1.648, 'wHR': 2.137, 'wOBAScale': 1.299},
    1991: {'wBB': 0.707, 'wHBP': 0.739, 'w1B': 0.908, 'w2B': 1.297, 'w3B': 1.647, 'wHR': 2.133, 'wOBAScale': 1.297},
    1992: {'wBB': 0.706, 'wHBP': 0.739, 'w1B': 0.912, 'w2B': 1.311, 'w3B': 1.670, 'wHR': 2.178, 'wOBAScale': 1.330},
    1993: {'wBB': 0.713, 'wHBP': 0.744, 'w1B': 0.905, 'w2B': 1.278, 'w3B': 1.613, 'wHR': 2.063, 'wOBAScale': 1.240},
    1994: {'wBB': 0.716, 'wHBP': 0.745, 'w1B': 0.899, 'w2B': 1.254, 'w3B': 1.573, 'wHR': 1.988, 'wOBAScale': 1.182},
    1995: {'wBB': 0.718, 'wHBP': 0.748, 'w1B': 0.903, 'w2B': 1.263, 'w3B': 1.587, 'wHR': 2.011, 'wOBAScale': 1.199},
    1996: {'wBB': 0.719, 'wHBP': 0.748, 'w1B': 0.901, 'w2B': 1.252, 'w3B': 1.568, 'wHR': 1.975, 'wOBAScale': 1.171},
    1997: {'wBB': 0.714, 'wHBP': 0.744, 'w1B': 0.900, 'w2B': 1.260, 'w3B': 1.585, 'wHR': 2.013, 'wOBAScale': 1.201},
    1998: {'wBB': 0.713, 'wHBP': 0.742, 'w1B': 0.898, 'w2B': 1.257, 'w3B': 1.580, 'wHR': 2.007, 'wOBAScale': 1.197},
    1999: {'wBB': 0.723, 'wHBP': 0.752, 'w1B': 0.902, 'w2B': 1.249, 'w3B': 1.561, 'wHR': 1.959, 'wOBAScale': 1.156},
    2000: {'wBB': 0.722, 'wHBP': 0.751, 'w1B': 0.900, 'w2B': 1.244, 'w3B': 1.554, 'wHR': 1.947, 'wOBAScale': 1.147},
    2001: {'wBB': 0.704, 'wHBP': 0.733, 'w1B': 0.887, 'w2B': 1.242, 'w3B': 1.561, 'wHR': 1.982, 'wOBAScale': 1.182},
    2002: {'wBB': 0.704, 'wHBP': 0.735, 'w1B': 0.892, 'w2B': 1.255, 'w3B': 1.582, 'wHR': 2.021, 'wOBAScale': 1.211},
    2003: {'wBB': 0.706, 'wHBP': 0.736, 'w1B': 0.891, 'w2B': 1.249, 'w3B': 1.572, 'wHR': 2.000, 'wOBAScale': 1.194},
    2004: {'wBB': 0.707, 'wHBP': 0.737, 'w1B': 0.890, 'w2B': 1.244, 'w3B': 1.563, 'wHR': 1.983, 'wOBAScale': 1.180},
    2005: {'wBB': 0.703, 'wHBP': 0.733, 'w1B': 0.890, 'w2B': 1.252, 'w3B': 1.578, 'wHR': 2.017, 'wOBAScale': 1.208},
    2006: {'wBB': 0.708, 'wHBP': 0.737, 'w1B': 0.890, 'w2B': 1.241, 'w3B': 1.557, 'wHR': 1.970, 'wOBAScale': 1.170},
    2007: {'wBB': 0.711, 'wHBP': 0.741, 'w1B': 0.896, 'w2B': 1.253, 'w3B': 1.575, 'wHR': 1.999, 'wOBAScale': 1.192},
    2008: {'wBB': 0.708, 'wHBP': 0.739, 'w1B': 0.896, 'w2B': 1.259, 'w3B': 1.587, 'wHR': 2.024, 'wOBAScale': 1.211},
    2009: {'wBB': 0.707, 'wHBP': 0.737, 'w1B': 0.895, 'w2B': 1.258, 'w3B': 1.585, 'wHR': 2.023, 'wOBAScale': 1.210},
    2010: {'wBB': 0.701, 'wHBP': 0.732, 'w1B': 0.895, 'w2B': 1.270, 'w3B': 1.608, 'wHR': 2.072, 'wOBAScale': 1.251},
    2011: {'wBB': 0.694, 'wHBP': 0.726, 'w1B': 0.890, 'w2B': 1.270, 'w3B': 1.611, 'wHR': 2.086, 'wOBAScale': 1.264},
    2012: {'wBB': 0.691, 'wHBP': 0.722, 'w1B': 0.884, 'w2B': 1.257, 'w3B': 1.593, 'wHR': 2.058, 'wOBAScale': 1.245},
    2013: {'wBB': 0.690, 'wHBP': 0.722, 'w1B': 0.888, 'w2B': 1.271, 'w3B': 1.616, 'wHR': 2.101, 'wOBAScale': 1.277},
    2014: {'wBB': 0.689, 'wHBP': 0.722, 'w1B': 0.892, 'w2B': 1.283, 'w3B': 1.635, 'wHR': 2.135, 'wOBAScale': 1.304},
    2015: {'wBB': 0.687, 'wHBP': 0.718, 'w1B': 0.881, 'w2B': 1.256, 'w3B': 1.594, 'wHR': 2.065, 'wOBAScale': 1.251},
    2016: {'wBB': 0.691, 'wHBP': 0.721, 'w1B': 0.878, 'w2B': 1.242, 'w3B': 1.569, 'wHR': 2.015, 'wOBAScale': 1.212},
    2017: {'wBB': 0.693, 'wHBP': 0.723, 'w1B': 0.877, 'w2B': 1.232, 'w3B': 1.552, 'wHR': 1.980, 'wOBAScale': 1.185},
    2018: {'wBB': 0.690, 'wHBP': 0.720, 'w1B': 0.880, 'w2B': 1.247, 'w3B': 1.578, 'wHR': 2.031, 'wOBAScale': 1.226},
    2019: {'wBB': 0.690, 'wHBP': 0.719, 'w1B': 0.870, 'w2B': 1.217, 'w3B': 1.529, 'wHR': 1.940, 'wOBAScale': 1.157},
    2020: {'wBB': 0.699, 'wHBP': 0.728, 'w1B': 0.883, 'w2B': 1.238, 'w3B': 1.558, 'wHR': 1.979, 'wOBAScale': 1.185},
    2021: {'wBB': 0.692, 'wHBP': 0.722, 'w1B': 0.879, 'w2B': 1.242, 'w3B': 1.568, 'wHR': 2.007, 'wOBAScale': 1.209},
    2022: {'wBB': 0.689, 'wHBP': 0.720, 'w1B': 0.884, 'w2B': 1.261, 'w3B': 1.601, 'wHR': 2.072, 'wOBAScale': 1.259},
    2023: {'wBB': 0.696, 'wHBP': 0.726, 'w1B': 0.883, 'w2B': 1.244, 'w3B': 1.569, 'wHR': 2.004, 'wOBAScale': 1.204},
    2024: {'wBB': 0.689, 'wHBP': 0.720, 'w1B': 0.882, 'w2B': 1.254, 'w3B': 1.590, 'wHR': 2.050, 'wOBAScale': 1.242},
    2025: {'wBB': 0.691, 'wHBP': 0.722, 'w1B': 0.882, 'w2B': 1.252, 'w3B': 1.584, 'wHR': 2.037, 'wOBAScale': 1.232},
}

def get_woba_weights(season: int) -> dict:
    """
    Returns the wOBA linear weights for a given season.
    Falls back to most recent year if season not found.
    """
    if season in WOBA_WEIGHTS:
        return WOBA_WEIGHTS[season]
    # Fall back to closest available year
    available = sorted(WOBA_WEIGHTS.keys())
    closest = min(available, key=lambda x: abs(x - season))
    return WOBA_WEIGHTS[closest]