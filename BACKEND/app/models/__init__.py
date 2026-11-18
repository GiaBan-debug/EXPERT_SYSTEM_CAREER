"""Khởi tạo models."""
from app.models.rule import Rule, Condition, Conclusion
from app.models.career import Career, CareerCategory
from app.models.student import Student
from app.models.consultation import Consultation

__all__ = [
    "Rule",
    "Condition",
    "Conclusion",
    "Career",
    "CareerCategory",
    "Student",
    "Consultation",
]
