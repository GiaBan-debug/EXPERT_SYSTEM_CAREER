
import pytest
from pydantic import ValidationError

from app.models.student import Student
from app.schemas.student_schema import StudentCreateSchema
from app.expert_system.facts.fact_schema import Fact
from app.expert_system.facts.fact_validator import (
    FactValidationError,
    validate_fact,
    validate_facts,
)
from app.expert_system.facts.student_facts import (
    student_to_facts,
    student_to_fact_dicts,
)


@pytest.fixture
def valid_student_data():
    return {
        "student_id": "HS001",
        "full_name": "Nguyen Van A",
        "grade": 12,
        "scores": {
            "math": 8.5,
            "english": 7.5,
        },
        "abilities": ["Logical thinking"],
        "interests": ["Technology"],
        "skills": ["Programming"],
        "personality_traits": ["Creative"],
        "career_orientation": ["Information Technology"],
    }


def test_create_valid_student(valid_student_data):
    student = StudentCreateSchema.model_validate(valid_student_data)

    assert student.student_id == "HS001"
    assert student.grade == 12
    assert student.scores["math"] == 8.5


def test_reject_score_above_10(valid_student_data):
    valid_student_data["scores"]["math"] = 15

    with pytest.raises(ValidationError):
        StudentCreateSchema.model_validate(valid_student_data)


def test_reject_score_below_0(valid_student_data):
    valid_student_data["scores"]["math"] = -1

    with pytest.raises(ValidationError):
        StudentCreateSchema.model_validate(valid_student_data)


def test_reject_invalid_grade(valid_student_data):
    valid_student_data["grade"] = 9

    with pytest.raises(ValidationError):
        StudentCreateSchema.model_validate(valid_student_data)


def test_reject_missing_student_name(valid_student_data):
    valid_student_data.pop("full_name")

    with pytest.raises(ValidationError):
        StudentCreateSchema.model_validate(valid_student_data)


def test_convert_student_to_facts(valid_student_data):
    student = StudentCreateSchema.model_validate(valid_student_data)

    facts = student_to_facts(student)

    attributes = {fact.attribute for fact in facts}

    assert "grade" in attributes
    assert "scores.math" in attributes
    assert "scores.english" in attributes
    assert "interests" in attributes
    assert "skills" in attributes


def test_all_input_facts_use_equal_operator(valid_student_data):
    facts = student_to_facts(valid_student_data)

    assert all(fact.operator == "=" for fact in facts)


def test_student_identity_not_in_facts(valid_student_data):
    facts = student_to_facts(valid_student_data)

    attributes = {fact.attribute for fact in facts}

    assert "student_id" not in attributes
    assert "full_name" not in attributes


def test_reject_unknown_attribute():
    with pytest.raises(FactValidationError):
        validate_fact({
            "attribute": "unknown",
            "operator": "=",
            "value": "abc",
        })


def test_reject_invalid_score_fact():
    with pytest.raises(FactValidationError):
        validate_fact({
            "attribute": "scores.math",
            "operator": "=",
            "value": 15,
        })


def test_reject_wrong_operator_for_input_fact():
    with pytest.raises(FactValidationError):
        validate_fact({
            "attribute": "grade",
            "operator": ">=",
            "value": 12,
        })


def test_reject_duplicate_facts():
    facts = [
        Fact(
            attribute="grade",
            operator="=",
            value=12,
        ),
        Fact(
            attribute="grade",
            operator="=",
            value=11,
        ),
    ]

    with pytest.raises(FactValidationError):
        validate_facts(facts)


def test_convert_student_to_fact_dicts(valid_student_data):
    facts = student_to_fact_dicts(valid_student_data)

    assert isinstance(facts, list)
    assert all(isinstance(fact, dict) for fact in facts)
    assert facts[0]["attribute"] == "grade"


def test_student_model_conversion(valid_student_data):
    student = Student.from_mapping(valid_student_data)

    facts = student_to_facts(student)

    assert any(
        fact.attribute == "scores.math"
        for fact in facts
    )
