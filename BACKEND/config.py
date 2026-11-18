"""Cấu hình toàn cục cho ứng dụng Backend."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

APP_NAME = "Hệ Chuyên Gia Tư Vấn Chọn Ngành/Nghề THPT"
APP_VERSION = "1.0.0"

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*",
]
