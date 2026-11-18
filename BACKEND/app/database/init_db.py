"""Khởi tạo cấu trúc bảng và nạp dữ liệu mẫu vào CSDL."""
import os
from app.database.db import DB_PATH, SCHEMA_PATH, SEED_PATH, get_db_connection


def initialize_database():
    """Tạo bảng và seed dữ liệu nếu DB chưa tồn tại."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    if SEED_PATH.exists():
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Khởi tạo cơ sở dữ liệu thành công tại: {DB_PATH}")
