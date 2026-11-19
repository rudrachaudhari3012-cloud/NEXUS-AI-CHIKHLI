
import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "nexus_infinity.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():

    with connect() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS river_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level_m REAL,
                source TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level_m REAL,
                threshold_m REAL,
                message TEXT,
                source TEXT
            )
        """)

        conn.commit()


def save_reading(level, source="SIMULATED"):

    with connect() as conn:

        conn.execute("""
            INSERT INTO river_readings
            (timestamp, level_m, source)
            VALUES (?, ?, ?)
        """, (
            datetime.now().astimezone().isoformat(),
            float(level),
            source
        ))

        conn.commit()


def get_readings():

    with connect() as conn:

        df = pd.read_sql_query(
            "SELECT timestamp, level_m, source "
            "FROM river_readings ORDER BY timestamp",
            conn
        )

    if not df.empty:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )
        df["level_m"] = pd.to_numeric(
            df["level_m"], errors="coerce"
        )
        df = df.dropna(subset=["timestamp", "level_m"])

    return df


def save_alert(level, threshold, message, source):

    with connect() as conn:

        conn.execute("""
            INSERT INTO alerts
            (timestamp, level_m, threshold_m, message, source)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().astimezone().isoformat(),
            float(level),
            float(threshold),
            str(message),
            str(source)
        ))

        conn.commit()


def get_alerts():

    with connect() as conn:

        return pd.read_sql_query(
            "SELECT timestamp, level_m, threshold_m, "
            "message, source FROM alerts ORDER BY id DESC",
            conn
        )


def clear_alerts():

    with connect() as conn:

        conn.execute("DELETE FROM alerts")
        conn.commit()
