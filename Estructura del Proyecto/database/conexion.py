import sqlite3

DB_NAME = "parking.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS placas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            fecha_hora TEXT
        )
    """)
    conn.commit()
    conn.close()
