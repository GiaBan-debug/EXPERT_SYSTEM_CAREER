"""Schema Pydantic cho dữ liệu đầu ra kết quả tư vấn (Result Response)."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class CareerMatchDetail(BaseModel):
    id: str
    code: str
    name: str
    category: str
    description: str
    riasec_code: str
    required_blocks: List[str]
    top_universities: List[str]
    average_salary: str
    market_trend: str
    icon: Optional[str] = "fa-briefcase"


class RecommendationItem(BaseModel):
    career: CareerMatchDetail
    matchScore: int
    academicMatch: int
    personalityMatch: int
    marketMatch: int
    rulesFired: List[str]
    priority: Optional[int] = 5
    confidence: Optional[float] = 1.0


class ConsultationResponse(BaseModel):
    consultationId: str
    createdAt: str
    student: Dict[str, Any]
    dominantCode: str
    riasecScores: Dict[str, float]
    academicScores: Dict[str, float]
    recommendations: List[RecommendationItem]
    explanationSummary: Optional[Dict[str, Any]] = None
