"""Mô hình dữ liệu của một luật IF-THEN (Tv 2).

Một luật gồm:
    IF   conditions (danh sách điều kiện, nối bằng AND)
    THEN conclusion (một kết luận)
cùng với siêu dữ liệu: id, priority (độ ưu tiên), confidence (độ tin cậy), enabled.

Quy ước (xem DOCUMENTATION/08_knowledge_base.md):
    - confidence : số thực (0, 1], mức tin cậy của kết luận. Là tiêu chí CHÍNH khi
                   giải quyết xung đột (cao hơn thắng).
    - priority   : số nguyên 1..10, độ ưu tiên do người xây dựng tri thức quy định.
                   Là tiêu chí PHỤ: chỉ quyết định khi confidence bằng nhau.
Thứ tự so sánh khi xung đột: confidence -> priority (khớp với ConflictResolver/RankingEngine
của Tv 4).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

OPERATORS: Tuple[str, ...] = ("==", "!=", ">=", "<=", ">", "<", "in", "not_in")

CONCLUSION_FACT = "fact"                      # THEN thêm một Fact trung gian (derived)
CONCLUSION_RECOMMENDATION = "recommendation"  # THEN đề xuất một nhóm ngành
CONCLUSION_TYPES: Tuple[str, ...] = (CONCLUSION_FACT, CONCLUSION_RECOMMENDATION)


@dataclass
class Condition:
    """Một điều kiện: thuộc_tính - toán_tử - giá_trị (cùng dạng với Fact)."""

    attribute: str
    operator: str
    value: Any

    def to_dict(self) -> Dict[str, Any]:
        return {"attribute": self.attribute, "operator": self.operator, "value": self.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Condition":
        return cls(attribute=data["attribute"], operator=data["operator"], value=data["value"])


@dataclass
class Conclusion:
    """Kết luận THEN.

    type == "fact"           -> dùng attribute + value (Fact trung gian).
    type == "recommendation" -> dùng career_group (+ careers tùy chọn).
    """

    type: str
    attribute: Optional[str] = None
    value: Any = None
    career_group: Optional[str] = None
    careers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        if self.type == CONCLUSION_FACT:
            return {"type": self.type, "attribute": self.attribute, "value": self.value}
        out: Dict[str, Any] = {"type": self.type, "career_group": self.career_group}
        if self.careers:
            out["careers"] = list(self.careers)
        return out

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conclusion":
        return cls(
            type=data["type"],
            attribute=data.get("attribute"),
            value=data.get("value"),
            career_group=data.get("career_group"),
            careers=list(data.get("careers", [])),
        )


@dataclass
class Rule:
    id: str
    name: str
    conditions: List[Condition]
    conclusion: Conclusion
    priority: int
    confidence: float
    description: str = ""
    category: str = ""
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "conditions": [c.to_dict() for c in self.conditions],
            "conclusion": self.conclusion.to_dict(),
            "priority": self.priority,
            "confidence": self.confidence,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rule":
        """Chỉ gọi với dữ liệu ĐÃ qua RuleValidator."""
        return cls(
            id=data["id"],
            name=data["name"],
            conditions=[Condition.from_dict(c) for c in data["conditions"]],
            conclusion=Conclusion.from_dict(data["conclusion"]),
            priority=data["priority"],
            confidence=float(data["confidence"]),
            description=data.get("description", ""),
            category=data.get("category", ""),
            enabled=data.get("enabled", True),
        )

    def to_activation_dict(self) -> Dict[str, Any]:
        """Dạng dict PHẲNG cho bộ xử lý xung đột / xếp hạng (Thành viên 4).

        `conclusion` là một chuỗi (hashable): mã nhóm ngành với luật đề xuất,
        hoặc "thuộc_tính=giá_trị" với luật sinh Fact trung gian.
        """
        c = self.conclusion
        flat_conclusion = (c.career_group if c.type == CONCLUSION_RECOMMENDATION
                           else f"{c.attribute}={c.value}")
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "conclusion": flat_conclusion,
            "conclusion_type": c.type,
            "career_group": c.career_group,
            "careers": list(c.careers),
            "priority": self.priority,
            "confidence": self.confidence,
        }

    def signature(self) -> str:
        """Chữ ký nội dung (điều kiện + kết luận), không phụ thuộc id/thứ tự điều kiện.

        Hai luật có cùng signature là luật trùng nhau.
        """
        return rule_signature(self.to_dict())


def rule_signature(rule_dict: Dict[str, Any]) -> str:
    conds = sorted(
        json.dumps(
            {"a": c.get("attribute"), "o": c.get("operator"), "v": _norm(c.get("value"))},
            sort_keys=True, ensure_ascii=False,
        )
        for c in rule_dict.get("conditions", [])
        if isinstance(c, dict)
    )
    concl = rule_dict.get("conclusion", {})
    concl_norm = {k: _norm(v) for k, v in concl.items()} if isinstance(concl, dict) else concl
    return json.dumps({"if": conds, "then": concl_norm}, sort_keys=True, ensure_ascii=False)


def _norm(value: Any) -> Any:
    """Chuẩn hóa để so sánh: list -> list đã sắp xếp, số nguyên/thực -> float."""
    if isinstance(value, list):
        return sorted((_norm(v) for v in value), key=lambda x: json.dumps(x, ensure_ascii=False))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return value
