# 🎵 Assignment 1 — Spotify Database  

## 📌 Project Description  
This project imports and analyzes Spotify data using PostgreSQL and Python.  
Five CSV files are imported into the database:  

- `spotify_artists`  
- `spotify_albums`  
- `spotify_tracks`  
- `spotify_features`  
- `spotify_data`  

The data is then analyzed using basic and analytical SQL queries.  

---

## 🛠 Tools Used  
- `PostgreSQL` — Database management system for data storage.  
- `Python` (`psycopg2`, `pandas`) — For importing CSV files into the database and executing SQL queries.  
- `SQL` — For data analysis (`LIMIT`, `WHERE + ORDER BY`, `GROUP BY`, `JOIN`, aggregations).  
- *(Optional)* `Apache Superset` — For visualization (not required in this project).  

---

## 🚀 How to Run  

1. Create the database in PostgreSQL:  
   ```sql
   CREATE DATABASE assignment1;
Install dependencies:
pip install pandas psycopg2
Run the script:
python dv.py
This will:
✔ Import CSV data into PostgreSQL  
✔ Execute 4 basic queries  
✔ Execute 10 analytical queries  
🔍 Queries Implemented  
🟢 Basic Queries    
LIMIT — First 10 albums.  
WHERE + ORDER BY — Top 20 tracks by popularity.  
GROUP BY — Average track popularity by album.  
JOIN — Number of tracks per album.  
🔵 Analytical Queries    
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
📂 Project Structure
📦 Assignment 1 - Spotify Database  
├── dv.py            # Main Python script (import + queries)  
├── queries.sql      # Collection of SQL queries  
├── Assignment1.pdf  # Assignment description  
└── *.csv            # Spotify dataset files  
✨ Done — ready to explore Spotify with SQL!
