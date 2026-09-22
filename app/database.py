import sqlite3
from datetime import datetime

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
            complaint_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migrate legacy tables (pre-existing DB without the new columns)
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(complaints)").fetchall()]
    if "complaint_id" not in cols:
        conn.execute("ALTER TABLE complaints ADD COLUMN complaint_id TEXT")
    if "updated_at" not in cols:
        conn.execute("ALTER TABLE complaints ADD COLUMN updated_at TEXT")

    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_complaints_complaint_id ON complaints(complaint_id)")

    # Backfill complaint_id/updated_at for rows created before this feature existed
    legacy_rows = conn.execute("SELECT id, created_at FROM complaints WHERE complaint_id IS NULL").fetchall()
    for r in legacy_rows:
        year = (r["created_at"] or "")[:4] or str(datetime.now().year)
        cid = f"CMP-{year}-{r['id']:05d}"
        conn.execute(
            "UPDATE complaints SET complaint_id = ?, updated_at = COALESCE(updated_at, created_at) WHERE id = ?",
            (cid, r["id"])
        )

    conn.commit()
    conn.close()

def insert_complaint(text, category, priority):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO complaints (complaint_text, category, priority, status) VALUES (?, ?, ?, 'Pending')",
        (text, category, priority)
    )
    new_id = cur.lastrowid

    year = datetime.now().year
    complaint_id = f"CMP-{year}-{new_id:05d}"
    conn.execute(
        "UPDATE complaints SET complaint_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (complaint_id, new_id)
    )
    conn.commit()

    row = conn.execute("SELECT * FROM complaints WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)

def get_all_complaints():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM complaints ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status(pk_id, status):
    conn = get_connection()
    cur = conn.execute(
        "UPDATE complaints SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, pk_id)
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0

def get_by_complaint_id(complaint_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT complaint_id, category, priority, status, created_at, updated_at FROM complaints WHERE complaint_id = ?",
        (complaint_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None
