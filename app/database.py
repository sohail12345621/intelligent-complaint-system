import sqlite3

DB_PATH = "complaints.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_text TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_complaint(text, category, priority):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO complaints (complaint_text, category, priority, status) VALUES (?, ?, ?, 'Pending')",
        (text, category, priority)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_all_complaints():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM complaints ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status(complaint_id, status):
    conn = get_connection()
    cur = conn.execute("UPDATE complaints SET status = ? WHERE id = ?", (status, complaint_id))
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0
