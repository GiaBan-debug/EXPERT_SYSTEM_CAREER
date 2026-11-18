"""Mô hình dữ liệu Ngành nghề (Career & Category)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Career:
    id: str
    code: str
    name: str
    category: str
    category_id: str
    description: str
    riasec_code: str
    riasec_primary: str
    required_blocks: List[str]
    top_universities: List[str]
    average_salary: str
    market_trend: str
    icon: str = "fa-briefcase"
    rules: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "category_id": self.category_id,
            "description": self.description,
            "riasec_code": self.riasec_code,
            "riasec_primary": self.riasec_primary,
            "required_blocks": self.required_blocks,
            "top_universities": self.top_universities,
            "average_salary": self.average_salary,
            "market_trend": self.market_trend,
            "icon": self.icon,
            "rules": self.rules,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Career":
        return cls(
            id=d["id"],
            code=d["code"],
            name=d["name"],
            category=d.get("category", ""),
            category_id=d.get("category_id", ""),
            description=d.get("description", ""),
            riasec_code=d.get("riasec_code", ""),
            riasec_primary=d.get("riasec_primary", ""),
            required_blocks=d.get("required_blocks", []),
            top_universities=d.get("top_universities", []),
            average_salary=d.get("average_salary", ""),
            market_trend=d.get("market_trend", ""),
            icon=d.get("icon", "fa-briefcase"),
            rules=d.get("rules", []),
        )


@dataclass
class CareerCategory:
    id: str
    name: str
    description: str = ""
    icon: str = "fa-folder"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
        }
