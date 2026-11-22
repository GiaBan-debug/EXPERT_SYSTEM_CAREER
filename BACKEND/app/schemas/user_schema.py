"""Schema Pydantic cho Đăng ký, Đăng nhập và Thông tin User."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Tên đăng nhập")
    password: str = Field(..., min_length=6, description="Mật khẩu tối thiểu 6 ký tự")
    fullName: str = Field(..., min_length=2, description="Họ và tên người dùng")
    email: Optional[str] = Field(None, description="Địa chỉ email")
    role: Optional[str] = Field("user", description="Quyền người dùng ('user' hoặc 'admin')")


class UserLoginRequest(BaseModel):
    username: str = Field(..., description="Tên đăng nhập hoặc email")
    password: str = Field(..., description="Mật khẩu")


class UserResponse(BaseModel):
    id: str
    username: str
    fullName: str
    email: Optional[str] = None
    role: str
    token: Optional[str] = None
