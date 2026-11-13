
from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass
class Student:
    """
    Lưu trữ thông tin hồ sơ học sinh THPT.
    """

    student_id: str
    full_name: str
    grade: int

    # Điểm số các môn học (thang điểm 0-10)
    scores: dict[str, float] = field(default_factory=dict)

    # Năng lực của học sinh
    abilities: list[str] = field(default_factory=list)

    # Sở thích
    interests: list[str] = field(default_factory=list)

    # Kỹ năng
    skills: list[str] = field(default_factory=list)

    # Đặc điểm tính cách
    personality_traits: list[str] = field(default_factory=list)

    # Định hướng nghề nghiệp ban đầu
    career_orientation: list[str] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Student":
        """
        Chuyển dữ liệu dạng Dictionary thành đối tượng Student.
        Dữ liệu đầu vào cần được kiểm tra trước khi sử dụng.
        """
        return cls(
            student_id=data["student_id"],
            full_name=data["full_name"],
            grade=data["grade"],
            scores=dict(data.get("scores") or {}),
            abilities=list(data.get("abilities") or []),
            interests=list(data.get("interests") or []),
            skills=list(data.get("skills") or []),
            personality_traits=list(
                data.get("personality_traits") or []
            ),
            career_orientation=list(
                data.get("career_orientation") or []
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Chuyển đối tượng Student thành Dictionary.
        """
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "grade": self.grade,
            "scores": self.scores.copy(),
            "abilities": self.abilities.copy(),
            "interests": self.interests.copy(),
            "skills": self.skills.copy(),
            "personality_traits": self.personality_traits.copy(),
            "career_orientation": self.career_orientation.copy(),
        }
