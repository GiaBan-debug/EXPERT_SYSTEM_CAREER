"""Mô hình dữ liệu Người dùng & Tài khoản."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class User:
    id: str
    username: str
    password_hash: str
    full_name: str
    email: Optional[str] = None
    role: str = "user"  # 'admin' hoặc 'user'
    created_at: Optional[datetime] = None

    def to_dict(self, include_hash: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_hash:
            data["password_hash"] = self.password_hash
        return data

    @classmethod
    def from_row(cls, row: Any) -> "User":
        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            full_name=row["full_name"],
            email=row["email"],
            role=row["role"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
        )
