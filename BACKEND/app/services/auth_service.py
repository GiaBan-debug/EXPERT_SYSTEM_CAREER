"""Dịch vụ Xác thực và Phân quyền người dùng (Authentication & Authorization)."""
import hashlib
import time
from typing import Any, Dict, Optional
import jwt
from app.database.repositories.user_repository import UserRepository
from app.models.user import User

SECRET_KEY = "EduCareerAI_SecretKey_ExpertSystem_2026"
ALGORITHM = "HS256"
TOKEN_EXPIRE_SECONDS = 7 * 24 * 3600  # 7 ngày


def hash_password(password: str) -> str:
    """Băm mật khẩu bằng SHA-256 an toàn và nhất quán."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_access_token(user_id: str, username: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "exp": int(time.time()) + TOKEN_EXPIRE_SECONDS
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None


class AuthService:
    def __init__(self, user_repo: Optional[UserRepository] = None):
        self.user_repo = user_repo or UserRepository()

    def register(self, username: str, password: str, full_name: str, email: Optional[str] = None, role: str = "user") -> Dict[str, Any]:
        existing = self.user_repo.get_by_username(username)
        if existing:
            raise ValueError(f"Tên đăng nhập hoặc email '{username}' đã tồn tại")

        # Chuẩn hóa role
        clean_role = "admin" if role == "admin" else "user"
        pw_hash = hash_password(password)
        user = self.user_repo.create(
            username=username,
            password_hash=pw_hash,
            full_name=full_name,
            email=email,
            role=clean_role
        )
        token = create_access_token(user.id, user.username, user.role)
        return {
            "id": user.id,
            "username": user.username,
            "fullName": user.full_name,
            "email": user.email,
            "role": user.role,
            "token": token
        }

    def login(self, username: str, password: str) -> Dict[str, Any]:
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Tên đăng nhập hoặc mật khẩu không chính xác")

        token = create_access_token(user.id, user.username, user.role)
        return {
            "id": user.id,
            "username": user.username,
            "fullName": user.full_name,
            "email": user.email,
            "role": user.role,
            "token": token
        }

    def get_current_user(self, token: str) -> Optional[User]:
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            return None
        return self.user_repo.get_by_id(payload["sub"])
