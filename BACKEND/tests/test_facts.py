"""Unit test cho Facts & Validator (Thành viên 1)."""
import pytest
from app.expert_system.facts import Fact, FactValidator, student_to_facts


def test_create_fact():
    f = Fact(attribute="score.math", value=8.5)
    assert f.attribute == "score.math"
    assert f.value == 8.5
    assert f.operator == "="
    assert f.source == "input"


def test_student_to_facts():
    payload = {
        "student": {"fullName": "Nguyễn Văn A", "grade": "12", "track": "khoa_hoc_tu_nhien"},
        "scores": {"math": 9.0, "physics": 8.0},
        "riasec": {"R": 70, "I": 90},
        "preferences": {"environment": "tech"}
    }
    facts = student_to_facts(payload)
    fact_dict = {f.attribute: f.value for f in facts}

    assert fact_dict["score.math"] == 9.0
    assert fact_dict["score.physics"] == 8.0
    assert fact_dict["riasec.I"] == 90.0
    assert fact_dict["student.track"] == "khoa_hoc_tu_nhien"
    assert fact_dict["pref.environment"] == "tech"


def test_fact_validator():
    validator = FactValidator()
    valid_fact = Fact(attribute="score.math", value=8.0)
    errors = validator.validate_fact(valid_fact)
    assert len(errors) == 0

    invalid_fact = Fact(attribute="score.math", value=15.0)
    errors = validator.validate_fact(invalid_fact)
    assert len(errors) > 0
