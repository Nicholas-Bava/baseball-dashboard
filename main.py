import duckdb
from app.constants.woba_weights import get_woba_weights

con = duckdb.connect()

# Judge across years
print("=== Aaron Judge ===")
for year in [2017, 2019, 2022, 2024]:
    df = con.execute(f"""
        SELECT playerName, season, avg_exit_velo, hard_hit_pct, 
               barrel_pct, xba, xwoba, xbacon, xwobacon
        FROM read_parquet('data/parquet/statcast_batting_agg_{year}.parquet')
        WHERE playerName = 'Aaron Judge'
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
    df = con.execute(f"""
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
    print(df.to_string())
    print()

