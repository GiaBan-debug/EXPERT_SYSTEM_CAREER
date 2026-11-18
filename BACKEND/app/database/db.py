"""Quản lý kết nối cơ sở dữ liệu SQLite/SQLAlchemy."""
import os
import sqlite3
from pathlib import Path
from typing import Generator

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "DATABASE" / "career_system.db"
SCHEMA_PATH = BASE_DIR / "DATABASE" / "schema.sql"
SEED_PATH = BASE_DIR / "DATABASE" / "seed.sql"


def get_db_connection() -> sqlite3.Connection:
    """Tạo kết nối SQLite có hỗ trợ truy xuất theo tên cột (Row factory)."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Dependency injection cho FastAPI routes."""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
