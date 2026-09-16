import sqlite3

DB_NAME = "multiplex_bookings.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_id TEXT NOT NULL,
            grand_total TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_booking(show_id: str, grand_total: str):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (show_id, grand_total) VALUES (?, ?)", (show_id, grand_total))
    conn.commit()
    conn.close()

def fetch_bookings():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, show_id, grand_total, timestamp FROM bookings ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows