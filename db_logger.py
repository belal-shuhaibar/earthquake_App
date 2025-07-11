# db_logger.py

import sqlite3
from datetime import datetime
import pandas as pd

# Create the SQLite table if it doesn't exist
def init_db():
    conn = sqlite3.connect("query_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date TEXT,
            end_date TEXT,
            min_magnitude REAL,
            result_count INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Log each query to the database
def log_query(start_date, end_date, min_magnitude, result_count):
    conn = sqlite3.connect("query_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO query_log (start_date, end_date, min_magnitude, result_count, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        str(start_date),
        str(end_date),
        float(min_magnitude),
        int(result_count),
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

# Retrieve all query logs
def get_query_history():
    conn = sqlite3.connect("query_logs.db")
    df = pd.read_sql_query("SELECT * FROM query_log ORDER BY timestamp DESC", conn)
    conn.close()
    return df
