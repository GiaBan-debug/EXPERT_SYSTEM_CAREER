"""Kiểm tra tính hợp lệ của Fact dựa trên fact_conventions.json (Thành viên 1)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.expert_system.knowledge_base.fact_conventions import FactConventions
from app.expert_system.facts.fact_schema import Fact


class FactValidationError(ValueError):
    def __init__(self, errors: List[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


class FactValidator:
    def __init__(self, conventions: Optional[FactConventions] = None):
        self.conventions = conventions or FactConventions.from_file()

    def validate_fact(self, fact: Fact) -> List[str]:
        errors = []
        spec = self.conventions.attribute(fact.attribute)
        if not spec:
            errors.append(f"Thuộc tính không xác định trong quy ước: {fact.attribute}")
            return errors

        attr_type = spec.get("type")
        val = fact.value

        if attr_type == "number":
            if not isinstance(val, (int, float)):
                errors.append(f"Thuộc tính '{fact.attribute}' phải là số, nhận được: {type(val).__name__}")
            else:
                min_v = spec.get("min")
                max_v = spec.get("max")
                if min_v is not None and val < min_v:
                    errors.append(f"Thuộc tính '{fact.attribute}' nhỏ hơn giá trị tối thiểu {min_v}")
                if max_v is not None and val > max_v:
                    errors.append(f"Thuộc tính '{fact.attribute}' lớn hơn giá trị tối đa {max_v}")
        elif attr_type == "enum":
            allowed_vals = spec.get("values", [])
            if val not in allowed_vals:
                errors.append(f"Giá trị '{val}' không hợp lệ cho thuộc tính '{fact.attribute}'. Giá trị hợp lệ: {allowed_vals}")

        return errors

    def validate_facts(self, facts: List[Fact]) -> List[str]:
        all_errors = []
        for f in facts:
            all_errors.extend(self.validate_fact(f))
        return all_errors
