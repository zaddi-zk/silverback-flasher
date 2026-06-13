import sqlite3
from datetime import datetime

DB_PATH = "silverback_orders.db"

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id TEXT UNIQUE NOT NULL,
    user_session TEXT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    tx_hash TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
)
"""

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._create_tables()

    def _create_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_ORDERS_TABLE)
            conn.commit()

    def execute(self, query: str, params: tuple = ()):  # pragma: no cover
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetchall(self, query: str, params: tuple = ()):  # pragma: no cover
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetchone(self, query: str, params: tuple = ()):  # pragma: no cover
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def create_order(self, payment_id: str, user_session: str, amount: float, currency: str, wallet_address: str, status: str = "pending"):
        self.execute(
            "INSERT INTO orders (payment_id, user_session, amount, currency, wallet_address, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (payment_id, user_session, amount, currency, wallet_address, status, datetime.utcnow().isoformat())
        )

    def update_order(self, payment_id: str, tx_hash: str, status: str):
        self.execute(
            "UPDATE orders SET tx_hash = ?, status = ? WHERE payment_id = ?",
            (tx_hash, status, payment_id)
        )

    def get_order(self, payment_id: str):
        row = self.fetchone("SELECT * FROM orders WHERE payment_id = ?", (payment_id,))
        return dict(row) if row else None

    def get_all_orders(self):
        rows = self.fetchall("SELECT * FROM orders ORDER BY created_at DESC")
        return [dict(row) for row in rows]
