"""API Routes kiểm tra trạng thái hoạt động của hệ thống."""
from fastapi import APIRouter
from app.utils.response_handler import success_response

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return success_response(
        data={"status": "healthy", "service": "Career Expert System Backend"},
        message="Hệ thống hoạt động bình thường"
    )
