"""Mô hình dữ liệu Phiên Tư vấn (Consultation)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.models.student import Student


@dataclass
class Consultation:
    id: str
    student: Student
    scores: Dict[str, float]
    riasec: Dict[str, float]
    preferences: Dict[str, Any]
    dominant_code: str
    recommendations: List[Dict[str, Any]]
    explanation_summary: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student": self.student.to_dict(),
            "scores": self.scores,
            "riasec": self.riasec,
            "preferences": self.preferences,
            "dominant_code": self.dominant_code,
            "recommendations": self.recommendations,
            "explanation_summary": self.explanation_summary,
            "created_at": self.created_at.isoformat(),
        }
