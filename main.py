import duckdb
from app.constants.woba_weights import get_woba_weights

con = duckdb.connect()

# Judge across years
print("=== Aaron Judge ===")
for year in range(2017, 2026):
    df = con.execute(f"""
        SELECT playerName, season, avg_exit_velo, hard_hit_pct, 
               barrel_pct, xba, xwoba, xbacon, xwobacon, avg_launch_angle, ab, total_pa,
               whiff_pct, chase_pct, contact_pct
        FROM read_parquet('data/parquet/statcast_batting_agg_{year}.parquet')
        WHERE playerName = 'Steven Kwan'
    """).df()
    print(df.to_string())
    print()

# Alonso 2024
print("=== Pete Alonso 2024 ===")
df2 = con.execute("""
    SELECT playerName, season, avg_exit_velo, hard_hit_pct,
           barrel_pct, xba, xwoba
    FROM read_parquet('data/parquet/statcast_batting_agg_2024.parquet')
    WHERE playerName = 'Pete Alonso'
""").df()
print(df2.to_string())

for year in [2017, 2024]:
    df3 = con.execute(f"""
        SELECT 
            COUNT(*) as all_batted,
            COUNT(launch_speed) as tracked,
            COUNT(CASE WHEN woba_denom = 1 THEN 1 END) as woba_denom_1,
            SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) as barrels,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) / COUNT(launch_speed_angle), 1) as barrel_tracked,
            ROUND(100.0 * SUM(CASE WHEN launch_speed_angle = 6 THEN 1 ELSE 0 END) / COUNT(CASE WHEN woba_denom = 1 THEN 1 END), 1) as barrel_woba_denom
        FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 592450
        AND type = 'X'
        AND game_type = 'R'
    """).df()
    print(f"{year}:")
    print(df3.to_string())
    print()

# for year in [2017, 2024]:
#     df4 = con.execute(f"""
#         SELECT launch_speed FROM read_parquet('data/parquet/statcast_{year}.parquet')
#         WHERE batter = 592450
#         AND type = 'X'
#         AND game_type = 'R'
#     """).df()
#     print(f"{year} launch angle distribution:")
#     print(df4.to_string())
#     print()

years = [2023]
bid = 680757

for year in years:
    df4 = con.execute(f"""
        SELECT launch_angle, events FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = {bid}
        AND type = 'X'
        AND game_type = 'R'
        --AND launch_speed IS NULL OR launch_speed <= 0
        ORDER BY launch_angle ASC
    """).df()
    print(f"{year} launch angle distribution:")
    print(df4.to_string())
    print()

for year in years:
    df5 = con.execute(f"""
        SELECT events, COUNT(*) FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = {bid}
        --AND type = 'X'
        AND game_type = 'R'
        GROUP BY events
        ORDER BY COUNT(*) DESC
    """).df()
    print(f"{year}:")
    print(df5.to_string())
    print()

for year in years:
    df6 = con.execute(f"""
        SELECT events, COUNT(*) FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = {bid}
        AND type = 'X'
        AND game_type = 'R'
        AND launch_angle IS NOT NULL
        GROUP BY events
        --LIMIT 5
    """).df()
    print(f"{year}:")
    print(df6.to_string())
    print()

for year in years:
    df7 = con.execute(f"""
                      SELECT description, COUNT(*) FROM read_parquet('data/parquet/statcast_{year}.parquet')
                      WHERE batter = 621566
                      AND game_type = 'R'
                      GROUP BY description
                      ORDER BY COUNT(*) DESC
                    """).df()
    print(f"{year}:")
    print(df7.to_string())
    print()

# Check Judge 2024 zone breakdown
df = con.execute("""
    SELECT zone, batted_balls_in_zone, xbacon, xwobacon, 
           avg_exit_velo, barrel_pct, whiff_pct, swing_pct
    FROM read_parquet('data/parquet/statcast_zones_2024.parquet')
    WHERE playerId = 592450
    ORDER BY zone
""").df()

print(df.to_string())

from app.services.statcast_service import StatcastService

svc = StatcastService()

print("=== Judge 2024 Zone Data ===")
import json
data = svc.get_player_zone_data(592450, 2024)
print(json.dumps(data['zones'][:3], indent=2))

print("\n=== Judge 2024 Season Statcast ===")
season = svc.get_player_season_statcast(592450, 2024)
print(json.dumps({k: v for k, v in season.items() if k in ['xba', 'xwoba', 'barrel_pct', 'avg_exit_velo']}, indent=2))

print(json.dumps(svc.get_player_statcast_rankings(592450, 2024), indent=2))

df = con.execute("""
    SELECT playerId, playerName, season, avg_exit_velo, xba, xwoba
    FROM read_parquet('data/parquet/statcast_batting_agg_2022.parquet')
    WHERE playerId = 592450
""").df()

print(df.to_string())

print("=== 2024 zones for Judge ===")
df = con.execute("""
    SELECT zone, xbacon, xwobacon, avg_exit_velo
    FROM read_parquet('data/parquet/statcast_zones_2024.parquet')
    WHERE CAST(playerId AS INTEGER) = 592450
    ORDER BY zone
""").df()
print(df.to_string())

print("\n=== 2019 zones for Judge ===")
df2 = con.execute("""
    SELECT zone, xbacon, xwobacon, avg_exit_velo
    FROM read_parquet('data/parquet/statcast_zones_2019.parquet')
    WHERE CAST(playerId AS INTEGER) = 592450
    ORDER BY zone
""").df()
print(df2.to_string())

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1970.parquet')
                  """).df()
df4.to_csv("batting_1970.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1969.parquet')
                  """).df()
df4.to_csv("batting_1969.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1968.parquet')
                  """).df()
df4.to_csv("batting_1968.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1967.parquet')
                  """).df()
df4.to_csv("batting_1967.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1966.parquet')
                  """).df()
df4.to_csv("batting_1966.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1972.parquet')
                  """).df()
df4.to_csv("batting_1972.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1973.parquet')
                  """).df()
df4.to_csv("batting_1973.csv", index=False)

df4 = con.execute("""
                  SELECT * FROM read_parquet('data/parquet/batting_1974.parquet')
                  """).df()
df4.to_csv("batting_1974.csv", index=False)

