"""Schema Pydantic cho dữ liệu Học sinh."""
from typing import Optional
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    fullName: str = Field(..., min_length=2, description="Họ và tên học sinh")
    grade: str = Field("12", description="Khối lớp (10, 11, 12)")
    school: Optional[str] = Field("", description="Trường THPT")
    region: Optional[str] = Field("south", description="Khu vực (north, central, south, abroad)")
    track: Optional[str] = Field("khoa_hoc_tu_nhien", description="Tổ hợp theo GDPT mới")


class StudentResponse(StudentCreate):
    id: Optional[str] = None
