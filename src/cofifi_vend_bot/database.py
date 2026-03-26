import aiosqlite

DB_PATH = "cofifi.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
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
        await db.commit()


async def save_feedback(user_id: int, username: str, text: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO feedback (user_id, username, text) VALUES (?, ?, ?)",
            (user_id, username, text),
        )
        await db.commit()


async def save_refund(user_id: int, username: str, point: str,
                      purchase_datetime: str, amount: str,
                      reason: str, contact: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO refunds
               (user_id, username, point, purchase_datetime, amount, reason, contact)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, username, point, purchase_datetime, amount, reason, contact),
        )
        await db.commit()
