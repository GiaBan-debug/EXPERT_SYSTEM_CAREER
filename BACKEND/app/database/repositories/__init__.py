"""Khởi tạo repositories."""
from app.database.repositories.career_repository import CareerRepository
from app.database.repositories.rule_repository import RuleRepository
from app.database.repositories.student_repository import StudentRepository
from app.database.repositories.consultation_repository import ConsultationRepository

__all__ = [
    "CareerRepository",
    "RuleRepository",
    "StudentRepository",
    "ConsultationRepository",
]
