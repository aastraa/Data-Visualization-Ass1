import os, io
import pandas as pd
import psycopg2

# --- настройки ---
DB = dict(dbname="assignment1", user="postgres", password="230806", host="localhost", port="5432")
DL = "/Users/adilkhanmaratov/Downloads"
CSV = {
    "spotify_artists":  os.path.join(DL, "spotify_artists.csv"),
    "spotify_albums":   os.path.join(DL, "spotify_albums.csv"),
    "spotify_tracks":   os.path.join(DL, "spotify_tracks.csv"),
    "spotify_features": os.path.join(DL, "spotify_features.csv"),
    "spotify_data":     os.path.join(DL, "spotify_data.csv"),
}

def import_csv(cur, table, path):
    df = pd.read_csv(path, low_memory=False)
    cols = ", ".join([f'"{c}" TEXT' for c in df.columns])
    cur.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
    cur.execute(f'CREATE TABLE "{table}" ({cols});')
    buf = io.StringIO(); df.to_csv(buf, index=False, header=False); buf.seek(0)
    cur.copy_expert(f'COPY "{table}" ({", ".join([f"""\"{c}\"""" for c in df.columns])}) FROM STDIN WITH CSV', buf)

def run(cur, title, sql):
    print(f"\n-- {title} --")
    cur.execute(sql)
    rows = cur.fetchall()
    if not rows: print("(пусто)"); return
    for r in rows[:10]: print(r)

def main():
    with psycopg2.connect(**DB) as conn, conn.cursor() as cur:
        # импорт
        for t, p in CSV.items():
            if os.path.exists(p): import_csv(cur, t, p)
        conn.commit()

        # базовые 4
        run(cur, "albums LIMIT 10", "SELECT * FROM spotify_albums LIMIT 10;")
        run(cur, "ТОП-20 треков по популярности", """
            SELECT d.track_id, d.track_name, st.track_popularity::INT AS popularity
            FROM spotify_data d
            JOIN spotify_tracks st ON st.id = d.track_id
            WHERE st.track_popularity ~ '^[0-9]+$'
            ORDER BY st.track_popularity::INT DESC
            LIMIT 20;""")
        run(cur, "средняя популярность по альбомам", """
            SELECT d.album_id, d.album_name,
                   AVG(st.track_popularity::INT)::NUMERIC(10,2) AS avg_pop,
                   COUNT(*) AS n_tracks
            FROM spotify_data d
            JOIN spotify_tracks st ON st.id = d.track_id
            WHERE st.track_popularity ~ '^[0-9]+$'
            GROUP BY d.album_id, d.album_name
            ORDER BY avg_pop DESC
            LIMIT 15;""")
        run(cur, "альбомы и кол-во треков (JOIN)", """
            SELECT a.album_id, a.album_name, COUNT(d.track_id) AS tracks_count
            FROM spotify_albums a
            JOIN spotify_data d ON d.album_id = a.album_id
            GROUP BY a.album_id, a.album_name
            ORDER BY tracks_count DESC
            LIMIT 15;""")

        # 10 аналитических
        run(cur, "A1. топ артистов по подписчикам", """
            SELECT name, followers::INT AS followers
            FROM spotify_artists
            WHERE followers ~ '^[0-9]+$'
            ORDER BY followers::INT DESC
            LIMIT 10;""")

        run(cur, "A2. топ альбомов по сумме популярности", """
            SELECT d.album_id, d.album_name, SUM(st.track_popularity::INT) AS sum_pop
            FROM spotify_data d
            JOIN spotify_tracks st ON st.id = d.track_id
            WHERE st.track_popularity ~ '^[0-9]+$'
            GROUP BY d.album_id, d.album_name
            ORDER BY sum_pop DESC
            LIMIT 20;""")

        run(cur, "A3. самые энергичные треки", """
            SELECT track_id, track_name, energy::NUMERIC AS energy
            FROM spotify_data
            WHERE energy ~ '^[0-9.]+$'
            ORDER BY energy::NUMERIC DESC
            LIMIT 20;""")

        run(cur, "A4. альбомы по танцевальности", """
            SELECT album_id, album_name,
                   AVG(danceability::NUMERIC)::NUMERIC(10,3) AS avg_dance
            FROM spotify_data
            WHERE danceability ~ '^[0-9.]+$'
            GROUP BY album_id, album_name
            ORDER BY avg_dance DESC
            LIMIT 20;""")

        run(cur, "A5. распределение длительностей (0–10 минут)", """
            SELECT width_bucket(
                       (COALESCE(NULLIF(d.duration_ms,''), f.duration_ms))::INT/60000.0,
                       0, 10, 10
                   ) AS duration_bin_min,
                   COUNT(*) AS n
            FROM spotify_data d
            LEFT JOIN spotify_features f ON f.id = d.track_id
            WHERE COALESCE(NULLIF(d.duration_ms,''), f.duration_ms) ~ '^[0-9]+$'
            GROUP BY duration_bin_min
            ORDER BY duration_bin_min;""")

        run(cur, "A6. быстрые и популярные (tempo, pop>=50)", """
            SELECT d.track_id, d.track_name, d.tempo::NUMERIC AS tempo
            FROM spotify_data d
            JOIN spotify_tracks st ON st.id = d.track_id
            WHERE d.tempo ~ '^[0-9.]+$'
              AND st.track_popularity ~ '^[0-9]+$'
              AND st.track_popularity::INT >= 50
            ORDER BY d.tempo::NUMERIC DESC
            LIMIT 30;""")

        run(cur, "A7. исполнители по количеству треков", """
            SELECT name AS artist, COUNT(*) AS n_tracks
            FROM spotify_data
            WHERE name IS NOT NULL AND name <> ''
            GROUP BY name
            ORDER BY n_tracks DESC
            LIMIT 20;""")

        run(cur, "A8. explicit-треки по популярности", """
            SELECT d.track_id, d.track_name, st.track_popularity::INT AS popularity
            FROM spotify_data d
            JOIN spotify_tracks st ON st.id = d.track_id
            WHERE st.explicit = 'True' AND st.track_popularity ~ '^[0-9]+$'
            ORDER BY st.track_popularity::INT DESC
            LIMIT 10;""")

        run(cur, "A9. треки по годам релиза", """
            WITH yrs AS (
              SELECT
                CASE
                  WHEN d.release_year ~ '^[0-9]+(\\.[0-9]+)?$'
                    THEN (NULLIF(d.release_year,'')::NUMERIC)::INT
                  WHEN a.release_date ~ '^[0-9]{4}'
                    THEN SUBSTRING(a.release_date FROM '^[0-9]{4}')::INT
                  ELSE NULL
                END AS year
              FROM spotify_data d
              LEFT JOIN spotify_albums a ON a.album_id = d.album_id
            )
            SELECT year, COUNT(*) AS n_tracks
            FROM yrs
            WHERE year IS NOT NULL
            GROUP BY year
            ORDER BY year;""")

        run(cur, "A10. средняя энергия по годам релиза", """
            WITH yrs AS (
              SELECT
                CASE
                  WHEN d.release_year ~ '^[0-9]+(\\.[0-9]+)?$'
                    THEN (NULLIF(d.release_year,'')::NUMERIC)::INT
                  WHEN a.release_date ~ '^[0-9]{4}'
                    THEN SUBSTRING(a.release_date FROM '^[0-9]{4}')::INT
                  ELSE NULL
                END AS year,
                d.energy
              FROM spotify_data d
              LEFT JOIN spotify_albums a ON a.album_id = d.album_id
              WHERE d.energy ~ '^[0-9.]+$'
            )
            SELECT year, AVG(energy::NUMERIC)::NUMERIC(10,3) AS avg_energy, COUNT(*) AS n
            FROM yrs
            WHERE year IS NOT NULL
            GROUP BY year
            ORDER BY year;""")

    print("\nГотово")

if __name__ == "__main__":
    main()
