"""Khởi tạo ứng dụng FastAPI và cấu hình CORS Middleware."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.database.init_db import initialize_database
from config import APP_NAME, APP_VERSION, CORS_ORIGINS


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description="Backend API Hệ Chuyên Gia Tư Vấn Chọn Ngành/Nghề Cho Học Sinh THPT",
    )

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Đăng ký các router với tiền tố /api
    app.include_router(api_router, prefix="/api")

    # Khởi tạo CSDL khi khởi động
    @app.on_event("startup")
    def on_startup():
        initialize_database()

    return app


app = create_app()
