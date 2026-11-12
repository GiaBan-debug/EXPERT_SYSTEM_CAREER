
from typing import Any, Mapping

from app.models.student import Student
from app.schemas.student_schema import StudentCreateSchema
from app.expert_system.facts.fact_schema import Fact
from app.expert_system.facts.fact_validator import validate_facts


def student_to_facts(
    student: Student | StudentCreateSchema | Mapping[str, Any],
) -> list[Fact]:
    """
    Chuyển hồ sơ học sinh thành danh sách Facts phục vụ suy luận.

    Thông tin định danh (student_id, full_name) được giữ trong
    hồ sơ nhưng không đưa vào hệ thống suy luận.
    """

    # Chuẩn hóa và kiểm tra dữ liệu đầu vào
    if isinstance(student, Student):
        data = student.to_dict()

    elif isinstance(student, StudentCreateSchema):
        data = student.model_dump()

    elif isinstance(student, Mapping):
        data = StudentCreateSchema.model_validate(
            student
        ).model_dump()

    else:
        raise TypeError(
            "student phải là Student, StudentCreateSchema hoặc Mapping"
        )

    facts = []

    # Fact về khối lớp
    facts.append(
        Fact(
            attribute="grade",
            operator="=",
            value=data["grade"],
        )
    )

    # Fact về điểm số từng môn học
    for subject, score in data.get("scores", {}).items():
        facts.append(
            Fact(
                attribute=f"scores.{subject}",
                operator="=",
                value=score,
            )
        )

    # Fact về năng lực, sở thích, kỹ năng và tính cách
    list_attributes = [
        "abilities",
        "interests",
        "skills",
        "personality_traits",
        "career_orientation",
    ]

    for attribute in list_attributes:
        values = data.get(attribute, [])

        if values:
            facts.append(
                Fact(
                    attribute=attribute,
                    operator="=",
                    value=values,
                )
            )

    # Kiểm tra toàn bộ Facts trước khi trả về
    return validate_facts(facts)


def student_to_fact_dicts(
    student: Student | StudentCreateSchema | Mapping[str, Any],
) -> list[dict[str, Any]]:
    """
    Chuyển hồ sơ học sinh thành danh sách Dictionary Facts.
    Phù hợp khi truyền dữ liệu qua API hoặc JSON.
    """

    facts = student_to_facts(student)

    return [
        fact.model_dump()
        for fact in facts
    ]
