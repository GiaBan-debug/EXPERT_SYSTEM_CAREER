"""Chuẩn hóa cấu trúc phản hồi HTTP JSON."""
from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse


def success_response(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        }
    )


def error_response(message: str = "Error", status_code: int = 400, errors: Optional[Any] = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors or [],
        }
    )
