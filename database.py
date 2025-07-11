### database.py
"""Database Module for Earthquake Data Analysis App
This module fetches earthquake data from the USGS API, processes it, and stores it in a SQLite database.
It also provides functionality to log queries and retrieve query history.
This module is designed to be used in conjunction with a Streamlit app for data visualization and analysis.
# It includes functions to fetch sample data, create the database schema, and insert data into the database.
"""
import pandas as pd
import sqlite3
import requests
import datetime
import logging

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_and_store_sample_data():
    logger.info("Fetching sample earthquake data from USGS...")
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    response = requests.get(url)
    data = response.json()

    sample_events = []

    for feature in data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        if not props["time"] or not props["place"] or not coords:
            continue

        event_time = datetime.datetime.utcfromtimestamp(props["time"] / 1000.0)
        sample_events.append({
            "place": props["place"],
            "magnitude": props["mag"] or 0.0,
            "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S"),
            "longitude": coords[0],
            "latitude": coords[1],
            "depth": coords[2]
        })

    df = pd.DataFrame(sample_events)
    logger.info(f"Prepared {len(df)} earthquake records.")

    conn = sqlite3.connect("earthquakes.db")
    logger.info("Creating earthquakes table if not exists...")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place TEXT,
            magnitude REAL,
            event_time TEXT,
            longitude REAL,
            latitude REAL,
            depth REAL
        );
    """)
    df.to_sql("earthquakes", conn, if_exists="replace", index=False)
    conn.close()
    logger.info("Data inserted into 'earthquakes' table.")
