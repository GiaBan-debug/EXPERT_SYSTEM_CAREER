"""API Routes thực hiện Tư vấn và Suy diễn Hệ chuyên gia."""
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from app.schemas.consultation_schema import ConsultationRequest
from app.services.consultation_service import ConsultationService

router = APIRouter(prefix="/consultations", tags=["Consultations"])
consultation_service = ConsultationService()


@router.post("/evaluate")
def evaluate_consultation(payload: Dict[str, Any]):
    """Nhận thông tin học sinh, điểm môn, RIASEC và trả về kết quả suy diễn tiến."""
    try:
        result = consultation_service.evaluate(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi suy diễn: {str(e)}")
