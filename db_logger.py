import sqlite3
from datetime import datetime


DATABASE_NAME = "database.db"


def initialize_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            severity TEXT,

            message TEXT
        )
    """)

    connection.commit()

    connection.close()


def log_to_database(severity, message):

    try:

        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO security_logs
            (timestamp, severity, message)

            VALUES (?, ?, ?)
        """, (
            timestamp,
            severity,
            message
        ))

        connection.commit()

        connection.close()

        print("[DATABASE] Security event stored.")

    except Exception as e:

        print(f"[DATABASE ERROR] {e}")