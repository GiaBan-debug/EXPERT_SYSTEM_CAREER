"""Module quản lý Facts (Thành viên 1)."""
from app.expert_system.facts.fact_schema import Fact
from app.expert_system.facts.fact_validator import FactValidator, FactValidationError
from app.expert_system.facts.student_facts import student_to_facts, student_to_fact_dicts

__all__ = [
    "Fact",
    "FactValidator",
    "FactValidationError",
    "student_to_facts",
    "student_to_fact_dicts",
]
