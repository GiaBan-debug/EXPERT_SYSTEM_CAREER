"""API Routes truy vấn lịch sử tư vấn."""
from fastapi import APIRouter
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["History"])
history_service = HistoryService()


@router.get("")
def get_history(limit: int = 50):
    return history_service.get_history(limit=limit)


@router.get("/{consultation_id}")
def get_history_detail(consultation_id: str):
    detail = history_service.get_consultation_detail(consultation_id)
    if not detail:
        return {"error": "Not found"}
    return detail
