import duckdb
from app.constants.woba_weights import get_woba_weights

con = duckdb.connect()

# Judge across years
print("=== Aaron Judge ===")
for year in range(2017, 2026):
    df = con.execute(f"""
        SELECT playerName, season, avg_exit_velo, hard_hit_pct, 
               barrel_pct, xba, xwoba, xbacon, xwobacon, avg_launch_angle, ab, total_pa
        FROM read_parquet('data/parquet/statcast_batting_agg_{year}.parquet')
        WHERE playerName = 'Juan Soto'
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

for year in [2024]:
    df4 = con.execute(f"""
        SELECT launch_speed, events FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 665742
        AND type = 'X'
        AND game_type = 'R'
        --AND launch_speed IS NULL OR launch_speed <= 0
        ORDER BY launch_speed ASC
    """).df()
    print(f"{year} launch angle distribution:")
    print(df4.to_string())
    print()

for year in [2024]:
    df5 = con.execute(f"""
        SELECT events, COUNT(*) FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 665742
        --AND type = 'X'
        AND game_type = 'R'
        GROUP BY events
        ORDER BY COUNT(*) DESC
    """).df()
    print(f"{year}:")
    print(df5.to_string())
    print()

for year in [2024]:
    df6 = con.execute(f"""
        SELECT events, COUNT(*) FROM read_parquet('data/parquet/statcast_{year}.parquet')
        WHERE batter = 665742
        AND type = 'X'
        AND game_type = 'R'
        AND launch_speed IS NOT NULL
        GROUP BY events
        --LIMIT 5
    """).df()
    print(f"{year}:")
    print(df6.to_string())
    print()