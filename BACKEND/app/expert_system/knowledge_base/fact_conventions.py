"""Đọc bảng quy ước Fact (DATABASE/data/fact_conventions.json).

Validator dùng bảng này để biết thuộc tính nào hợp lệ, kiểu gì, miền giá trị ra sao.
Khi Thành viên 1 chốt fact_schema.py, chỉ cần chỉnh file JSON này (không sửa code).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# .../BACKEND/app/expert_system/knowledge_base/fact_conventions.py -> parents[4] = thư mục gốc repo
REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONVENTIONS_PATH = REPO_ROOT / "DATABASE" / "data" / "fact_conventions.json"
DEFAULT_RULES_PATH = REPO_ROOT / "DATABASE" / "data" / "rules.json"

_REQUIRED_KEYS = ("operators_by_type", "priority_range", "confidence_range",
                  "attributes", "career_groups", "careers")


class ConventionsError(Exception):
    pass


class FactConventions:
    def __init__(self, data: Dict[str, Any]):
        missing = [k for k in _REQUIRED_KEYS if k not in data]
        if missing:
            raise ConventionsError(f"fact_conventions thiếu khóa: {', '.join(missing)}")
        self.version: str = data.get("version", "")
        self.operators_by_type: Dict[str, List[str]] = data["operators_by_type"]
        self.priority_range = tuple(data["priority_range"])
        self.confidence_range = tuple(data["confidence_range"])
        self.attributes: Dict[str, Dict[str, Any]] = data["attributes"]
        self.career_groups: Dict[str, str] = data["career_groups"]
        self.careers: Dict[str, str] = data["careers"]

    @classmethod
    def from_file(cls, path: Optional[Path] = None) -> "FactConventions":
        path = Path(path) if path else DEFAULT_CONVENTIONS_PATH
        try:
            with open(path, "r", encoding="utf-8") as f:
                return cls(json.load(f))
        except FileNotFoundError as e:
            raise ConventionsError(f"Không tìm thấy file quy ước: {path}") from e
        except json.JSONDecodeError as e:
            raise ConventionsError(f"File quy ước không phải JSON hợp lệ: {e}") from e

    def attribute(self, name: str) -> Optional[Dict[str, Any]]:
        return self.attributes.get(name)

    def is_derived(self, name: str) -> bool:
        spec = self.attributes.get(name)
        return bool(spec) and spec.get("source") == "derived"

    def allowed_operators(self, name: str) -> List[str]:
        spec = self.attributes.get(name)
        return list(self.operators_by_type.get(spec["type"], [])) if spec else []
