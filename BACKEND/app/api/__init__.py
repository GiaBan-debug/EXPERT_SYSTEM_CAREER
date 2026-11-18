"""Khởi tạo và gộp các router API."""
from fastapi import APIRouter
from app.api.health_routes import router as health_router
from app.api.career_routes import router as career_router
from app.api.consultation_routes import router as consultation_router
from app.api.history_routes import router as history_router
from app.api.admin_routes import router as admin_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(career_router)
api_router.include_router(consultation_router)
api_router.include_router(history_router)
api_router.include_router(admin_router)

__all__ = ["api_router"]
