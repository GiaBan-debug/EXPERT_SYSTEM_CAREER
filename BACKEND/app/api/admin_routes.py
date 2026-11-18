"""API Routes dành cho Quản trị viên (Admin & Knowledge Base Management)."""
from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.expert_system.knowledge_base.rule_manager import RuleManager, RuleNotFoundError, RuleValidationError
from app.database.repositories.consultation_repository import ConsultationRepository
from app.database.repositories.career_repository import CareerRepository
from app.database.db import get_db_connection

router = APIRouter(prefix="/admin", tags=["Admin"])

# Khởi tạo instance dùng chung
rule_manager = RuleManager.from_file()
consultation_repo = ConsultationRepository()
career_repo = CareerRepository()


class RuleCreateRequest(BaseModel):
    id: str = Field(..., description="Mã luật duy nhất, ví dụ: GRP-99")
    name: str = Field(..., description="Tên luật")
    description: Optional[str] = Field("", description="Mô tả lý do")
    category: Optional[str] = Field("career_group", description="Phân loại: ability, interest, career_group")
    conditions: list = Field(..., description="Danh sách các điều kiện IF")
    conclusion: dict = Field(..., description="Kết luận THEN (fact hoặc recommendation)")
    priority: int = Field(5, ge=1, le=10, description="Độ ưu tiên 1-10")
    confidence: float = Field(1.0, gt=0.0, le=1.0, description="Độ tin cậy (0, 1]")
    enabled: bool = Field(True, description="Trạng thái bật/tắt")


class RuleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    conditions: Optional[list] = None
    conclusion: Optional[dict] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    confidence: Optional[float] = Field(None, gt=0.0, le=1.0)
    enabled: Optional[bool] = None


@router.get("/stats")
def get_admin_dashboard_stats():
    """Lấy dữ liệu thống kê tổng quan cho Dashboard Admin."""
    rule_stats = rule_manager.stats()
    careers = career_repo.get_all()
    history = consultation_repo.get_all(limit=100)

    # Đếm số lần các ngành nghề được đề xuất cao nhất
    top_careers_count: Dict[str, int] = {}
    for item in history:
        target = item.get("targetCareer")
        if target and target != "N/A":
            top_careers_count[target] = top_careers_count.get(target, 0) + 1

    # Đếm số học sinh trong CSDL
    total_students = 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        row = cursor.fetchone()
        if row:
            total_students = row[0]
        conn.close()
    except Exception:
        total_students = len(history)

    return {
        "rules": rule_stats,
        "totalCareers": len(careers),
        "totalConsultations": len(history),
        "totalStudents": total_students,
        "topRecommendedCareers": top_careers_count,
        "recentConsultations": history[:10],
    }


@router.get("/rules")
def get_all_rules(
    category: Optional[str] = Query(None, description="Lọc theo category"),
    enabled: Optional[bool] = Query(None, description="Lọc theo enabled")
):
    """Lấy toàn bộ danh sách luật có thể lọc."""
    rules = [r.to_dict() for r in rule_manager.all_rules()]
    if category:
        rules = [r for r in rules if r.get("category") == category]
    if enabled is not None:
        rules = [r for r in rules if r.get("enabled") == enabled]
    return rules


@router.get("/rules/{rule_id}")
def get_rule_detail(rule_id: str):
    """Xem chi tiết một luật."""
    try:
        rule = rule_manager.get(rule_id)
        return rule.to_dict()
    except RuleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy luật {rule_id}")


@router.patch("/rules/{rule_id}/toggle")
def toggle_rule(rule_id: str):
    """Bật hoặc tắt trạng thái của một luật."""
    try:
        rule = rule_manager.get(rule_id)
        if rule.enabled:
            updated = rule_manager.disable_rule(rule_id)
        else:
            updated = rule_manager.enable_rule(rule_id)
        rule_manager.save()
        return {
            "success": True,
            "rule_id": rule_id,
            "enabled": updated.enabled,
            "message": f"Đã {'bật' if updated.enabled else 'tắt'} luật {rule_id}"
        }
    except RuleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy luật {rule_id}")


@router.post("/rules")
def create_rule(payload: RuleCreateRequest):
    """Thêm luật mới vào cơ sở tri thức (tự động validate tính hợp lệ)."""
    try:
        new_rule = rule_manager.add_rule(payload.model_dump())
        rule_manager.save()
        return {
            "success": True,
            "message": f"Tạo luật {new_rule.id} thành công",
            "rule": new_rule.to_dict()
        }
    except RuleValidationError as e:
        raise HTTPException(status_code=400, detail=[str(issue) for issue in e.issues])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/rules/{rule_id}")
def update_rule(rule_id: str, payload: RuleUpdateRequest):
    """Cập nhật thông tin của một luật."""
    changes = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        updated = rule_manager.update_rule(rule_id, changes)
        rule_manager.save()
        return {
            "success": True,
            "message": f"Cập nhật luật {rule_id} thành công",
            "rule": updated.to_dict()
        }
    except RuleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy luật {rule_id}")
    except RuleValidationError as e:
        raise HTTPException(status_code=400, detail=[str(issue) for issue in e.issues])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: str):
    """Xóa một luật khỏi cơ sở tri thức."""
    try:
        rule_manager.remove_rule(rule_id)
        rule_manager.save()
        return {
            "success": True,
            "message": f"Đã xóa thành công luật {rule_id}"
        }
    except RuleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy luật {rule_id}")
