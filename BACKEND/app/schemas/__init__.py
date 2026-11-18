"""Khởi tạo schemas."""
from app.schemas.student_schema import StudentCreate, StudentResponse
from app.schemas.consultation_schema import (
    ConsultationRequest,
    SubjectScores,
    RiasecScores,
    StudentPreferences,
)
from app.schemas.result_schema import (
    ConsultationResponse,
    RecommendationItem,
    CareerMatchDetail,
)

__all__ = [
    "StudentCreate",
    "StudentResponse",
    "ConsultationRequest",
    "SubjectScores",
    "RiasecScores",
    "StudentPreferences",
    "ConsultationResponse",
    "RecommendationItem",
    "CareerMatchDetail",
]
