"""Repository thao tác với bảng Users (Người dùng & Phân quyền)."""
import sqlite3
import uuid
from typing import Any, Dict, List, Optional
from app.database.db import get_db_connection
from app.models.user import User


class UserRepository:
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        self._conn = conn

    def _get_conn(self) -> sqlite3.Connection:
        return self._conn or get_db_connection()

    def get_by_username(self, username: str) -> Optional[User]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, username))
        row = cursor.fetchone()
        if row:
            return User.from_row(row)
        return None

    def get_by_id(self, user_id: str) -> Optional[User]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User.from_row(row)
        return None

    def create(self, username: str, password_hash: str, full_name: str, email: Optional[str] = None, role: str = "user") -> User:
        conn = self._get_conn()
        cursor = conn.cursor()
        user_id = "usr_" + uuid.uuid4().hex[:10]
        cursor.execute(
            """
            INSERT INTO users (id, username, password_hash, full_name, email, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, password_hash, full_name, email, role)
        )
        conn.commit()
        return self.get_by_id(user_id)

    def get_all(self, limit: int = 100) -> List[User]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [User.from_row(r) for r in rows]
