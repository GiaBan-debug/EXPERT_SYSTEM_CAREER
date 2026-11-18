"""Schema Pydantic cho dữ liệu đầu vào tư vấn (Consultation Request)."""
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.schemas.student_schema import StudentCreate


class SubjectScores(BaseModel):
    math: float = Field(..., ge=1.0, le=10.0, description="Điểm Toán")
    physics: Optional[float] = Field(5.0, ge=1.0, le=10.0)
    chemistry: Optional[float] = Field(5.0, ge=1.0, le=10.0)
    biology: Optional[float] = Field(5.0, ge=1.0, le=10.0)
    literature: Optional[float] = Field(5.0, ge=1.0, le=10.0)
    english: Optional[float] = Field(5.0, ge=1.0, le=10.0)
    informatics: Optional[float] = Field(5.0, ge=1.0, le=10.0)
    history: Optional[float] = Field(5.0, ge=1.0, le=10.0)


class RiasecScores(BaseModel):
    R: float = Field(50.0, ge=0.0, le=100.0)
    I: float = Field(50.0, ge=0.0, le=100.0)
    A: float = Field(50.0, ge=0.0, le=100.0)
    S: float = Field(50.0, ge=0.0, le=100.0)
    E: float = Field(50.0, ge=0.0, le=100.0)
    C: float = Field(50.0, ge=0.0, le=100.0)


class StudentPreferences(BaseModel):
    environment: Optional[str] = "tech"
    tuition: Optional[str] = "standard"
    priority: Optional[str] = "high_salary"


class ConsultationRequest(BaseModel):
    student: StudentCreate
    scores: SubjectScores
    riasec: RiasecScores
    preferences: Optional[StudentPreferences] = Field(default_factory=StudentPreferences)
