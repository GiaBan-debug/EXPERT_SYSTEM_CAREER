
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class StudentCreateSchema(BaseModel):
    """
    Schema kiểm tra và chuẩn hóa dữ liệu học sinh đầu vào.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    student_id: str = Field(
        min_length=1,
        max_length=40,
        description="Mã học sinh",
    )

    full_name: str = Field(
        min_length=2,
        max_length=120,
        description="Họ và tên học sinh",
    )

    grade: Annotated[int, Field(strict=True, ge=10, le=12)]

    scores: dict[str, float] = Field(default_factory=dict)

    abilities: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    personality_traits: list[str] = Field(default_factory=list)
    career_orientation: list[str] = Field(default_factory=list)

    @field_validator("scores")
    @classmethod
    def validate_scores(cls, scores):
        normalized = {}

        for subject, score in scores.items():
            subject = subject.strip().lower()

            if not subject:
                raise ValueError("Tên môn học không được để trống")

            if isinstance(score, bool) or not 0 <= score <= 10:
                raise ValueError(
                    f"Điểm môn {subject} phải nằm trong khoảng 0-10"
                )

            if subject in normalized:
                raise ValueError(
                    f"Môn học bị trùng: {subject}"
                )

            normalized[subject] = score

        return normalized

    @field_validator(
        "abilities",
        "interests",
        "skills",
        "personality_traits",
        "career_orientation",
    )
    @classmethod
    def normalize_string_lists(cls, values):
        result = []
        seen = set()

        for value in values:
            value = value.strip()

            if not value:
                continue

            key = value.casefold()

            if key not in seen:
                result.append(value)
                seen.add(key)

        return result


class StudentResponseSchema(StudentCreateSchema):
    """
    Schema dữ liệu học sinh trả về sau khi xử lý.
    """
    pass
