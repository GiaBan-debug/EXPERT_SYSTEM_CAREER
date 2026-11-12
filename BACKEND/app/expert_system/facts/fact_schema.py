
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


FactOperator = Literal[
    "=",
    "!=",
    ">",
    ">=",
    "<",
    "<=",
    "contains",
    "in",
    "intersects",
]


class Fact(BaseModel):
    """
    Biểu diễn một sự kiện (Fact) trong hệ chuyên gia.

    Fact gồm:
    - attribute: Thuộc tính cần xét.
    - operator: Toán tử so sánh.
    - value: Giá trị tương ứng.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    attribute: str = Field(
        min_length=1,
        description="Tên thuộc tính",
    )

    operator: FactOperator = Field(
        description="Toán tử của Fact",
    )

    value: Any = Field(
        description="Giá trị của Fact",
    )

    @field_validator("attribute")
    @classmethod
    def normalize_attribute(cls, value: str) -> str:
        return value.strip().lower()
