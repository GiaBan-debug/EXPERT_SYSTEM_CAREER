"""Định nghĩa schema cấu trúc cho Fact trong hệ chuyên gia (Thành viên 1).

Đại diện cho các sự kiện/dữ kiện đầu vào và dẫn xuất (derived) trong bộ nhớ làm việc (Working Memory).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Fact:
    """Một Fact đơn lẻ: attribute (tên thuộc tính), operator ('='), value (giá trị)."""
    attribute: str
    value: Any
    operator: str = "="
    source: str = "input"  # 'input' hoặc 'derived'
    label: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attribute": self.attribute,
            "operator": self.operator,
            "value": self.value,
            "source": self.source,
            "label": self.label or self.attribute,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fact":
        return cls(
            attribute=data["attribute"],
            value=data.get("value"),
            operator=data.get("operator", "="),
            source=data.get("source", "input"),
            label=data.get("label"),
        )
