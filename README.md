Assignment 1 — Spotify Database
Project Description

As part of this assignment, a project was prepared to load and analyze Spotify data.
Five CSV files (spotify_artists, spotify_albums, spotify_tracks, spotify_features, spotify_data) are imported into PostgreSQL.
Based on the data, both basic and analytical SQL queries are executed.

Tools Used

PostgreSQL — Database management system for data storage.

Python (psycopg2, pandas) — For importing CSV files into the database and running SQL queries.

SQL — For data analysis (LIMIT, WHERE + ORDER BY, GROUP BY, JOIN, aggregations).

(Optional per assignment: Apache Superset can be used for visualization, but this project focuses on SQL queries only).

How to Run

Create a PostgreSQL database named assignment1.

Install dependencies:

pip install pandas psycopg2


Run the script:

python dv.py


The script will import CSV data into PostgreSQL and execute 4 basic + 10 analytical queries.

Queries Implemented
Basic Queries

LIMIT — first 10 albums.

WHERE + ORDER BY — top 20 tracks by popularity.

GROUP BY — average track popularity by album.

JOIN — number of tracks per album.

Analytical Queries

Top 10 artists by number of followers.

Top albums by total track popularity.

Most energetic tracks.

Top albums by danceability.

Distribution of track duration (0–10 minutes).

Fast and popular tracks (tempo + popularity).

Artists ranked by number of tracks.

Top explicit tracks by popularity.

Number of tracks by release year.

Average energy by release year.

Project Structure

dv.py — Main Python script (import + queries).

queries.sql — Collection of SQL queries (for direct use in psql/pgAdmin).

Assignment1.pdf — Assignment description.

*.csv — Source datasets.
