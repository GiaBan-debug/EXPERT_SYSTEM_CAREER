
from typing import Any, Iterable
import re

from pydantic import ValidationError

from app.expert_system.facts.fact_schema import Fact


class FactValidationError(ValueError):
    """Lỗi khi dữ liệu Fact không hợp lệ."""


LIST_ATTRIBUTES = {
    "abilities",
    "interests",
    "skills",
    "personality_traits",
    "career_orientation",
}


def validate_fact(fact: Fact | dict[str, Any]) -> Fact:
    """Kiểm tra một Fact đầu vào của học sinh."""

    try:
        if not isinstance(fact, Fact):
            fact = Fact.model_validate(fact)

    except ValidationError as exc:
        raise FactValidationError(
            f"Fact không hợp lệ: {exc}"
        ) from exc

    attribute = fact.attribute
    operator = fact.operator
    value = fact.value

    # Fact đầu vào của học sinh phải dùng toán tử =
    if operator != "=":
        raise FactValidationError(
            "Fact đầu vào của học sinh phải sử dụng toán tử '='"
        )

    # Kiểm tra thuộc tính khối lớp
    if attribute == "grade":
        if not isinstance(value, int) or isinstance(value, bool):
            raise FactValidationError(
                "Khối lớp phải là số nguyên"
            )

        if value not in (10, 11, 12):
            raise FactValidationError(
                "Khối lớp chỉ được là 10, 11 hoặc 12"
            )

    # Kiểm tra điểm từng môn học
    elif attribute.startswith("scores."):
        parts = attribute.split(".")

        if len(parts) != 2 or not re.fullmatch(
            r"[a-z0-9_]+", parts[1]
        ):
            raise FactValidationError(
                "Thuộc tính điểm phải có dạng scores.ten_mon_hoc"
            )

        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            raise FactValidationError(
                "Điểm môn học phải là số"
            )

        if not 0 <= value <= 10:
            raise FactValidationError(
                "Điểm môn học phải nằm trong khoảng 0-10"
            )

    # Kiểm tra các thuộc tính dạng danh sách
    elif attribute in LIST_ATTRIBUTES:
        if not isinstance(value, list):
            raise FactValidationError(
                f"{attribute} phải có dạng danh sách"
            )

        if not all(isinstance(item, str) for item in value):
            raise FactValidationError(
                f"Các phần tử trong {attribute} phải là chuỗi"
            )

    else:
        raise FactValidationError(
            f"Thuộc tính không được hỗ trợ: {attribute}"
        )

    return fact


def validate_facts(
    facts: Iterable[Fact | dict[str, Any]]
) -> list[Fact]:
    """Kiểm tra danh sách Facts và phát hiện thuộc tính bị trùng."""

    validated_facts = []
    seen_attributes = set()

    for item in facts:
        fact = validate_fact(item)

        if fact.attribute in seen_attributes:
            raise FactValidationError(
                f"Fact bị trùng thuộc tính: {fact.attribute}"
            )

        seen_attributes.add(fact.attribute)
        validated_facts.append(fact)

    return validated_facts
