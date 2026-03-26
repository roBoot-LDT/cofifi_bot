import sqlite3

DB_PATH = "cofifi.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS refunds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                point TEXT,
                purchase_datetime TEXT,
                amount TEXT,
                reason TEXT,
                contact TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_feedback(user_id: int, username: str, text: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO feedback (user_id, username, text) VALUES (?, ?, ?)",
            (user_id, username, text),
        )
        conn.commit()


def save_refund(user_id: int, username: str, point: str,
                purchase_datetime: str, amount: str,
                reason: str, contact: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO refunds
               (user_id, username, point, purchase_datetime, amount, reason, contact)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, username, point, purchase_datetime, amount, reason, contact),
        )
        conn.commit()
