"""API Routes cho Đăng nhập, Đăng ký và Thông tin tài khoản."""
from fastapi import APIRouter, Header, HTTPException
from app.schemas.user_schema import UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register")
def register(payload: UserRegisterRequest):
    """Đăng ký tài khoản mới (học sinh hoặc admin)."""
    try:
        user_info = auth_service.register(
            username=payload.username.strip(),
            password=payload.password,
            full_name=payload.fullName.strip(),
            email=payload.email.strip() if payload.email else None,
            role=payload.role or "user"
        )
        return {
            "success": True,
            "message": "Đăng ký tài khoản thành công",
            "data": user_info
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đăng ký: {str(e)}")


@router.post("/login")
def login(payload: UserLoginRequest):
    """Đăng nhập hệ thống và cấp mã JWT Token cùng Role."""
    try:
        user_info = auth_service.login(
            username=payload.username.strip(),
            password=payload.password
        )
        return {
            "success": True,
            "message": "Đăng nhập thành công",
            "data": user_info
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đăng nhập: {str(e)}")


@router.get("/me")
def get_me(authorization: str = Header(None)):
    """Lấy thông tin người dùng hiện tại dựa trên Token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Chưa cung cấp token xác thực")
    token = authorization.replace("Bearer ", "").strip()
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc đã hết hạn")
    return {
        "success": True,
        "data": user.to_dict()
    }
