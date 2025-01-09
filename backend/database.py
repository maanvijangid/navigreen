import sqlite3

DB_NAME = "routes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY,
            origin TEXT,
            destination TEXT,
            fuel_efficiency REAL,
            vehicle_type TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_request(origin, destination, fuel_efficiency, vehicle_type, response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requests (origin, destination, fuel_efficiency, vehicle_type, response)
        VALUES (?, ?, ?, ?, ?)
    """, (origin, destination, fuel_efficiency, vehicle_type, str(response)))
    conn.commit()
    conn.close()
