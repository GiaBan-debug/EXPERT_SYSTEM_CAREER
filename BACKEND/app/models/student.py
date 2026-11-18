"""Mô hình dữ liệu Hồ sơ Học sinh (Student)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Student:
    id: Optional[str] = None
    full_name: str = ""
    grade: str = "12"
    school: str = ""
    region: str = "south"
    track: str = "khoa_hoc_tu_nhien"
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "grade": self.grade,
            "school": self.school,
            "region": self.region,
            "track": self.track,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Student":
        return cls(
            id=d.get("id"),
            full_name=d.get("full_name", d.get("fullName", "")),
            grade=str(d.get("grade", "12")),
            school=d.get("school", ""),
            region=d.get("region", "south"),
            track=d.get("track", "khoa_hoc_tu_nhien"),
            created_at=datetime.fromisoformat(d["created_at"]) if d.get("created_at") else None,
        )
