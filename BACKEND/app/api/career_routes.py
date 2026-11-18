"""API Routes cho Danh mục & Chi tiết Ngành nghề."""
from fastapi import APIRouter, HTTPException
from app.services.career_service import CareerService

router = APIRouter(prefix="/careers", tags=["Careers"])
career_service = CareerService()


@router.get("")
def get_all_careers():
    careers = career_service.get_all_careers()
    return [c.to_dict() for c in careers]


@router.get("/categories")
def get_categories():
    categories = career_service.get_categories()
    return [c.to_dict() for c in categories]


@router.get("/{career_id}")
def get_career_by_id(career_id: str):
    career = career_service.get_career_by_id(career_id)
    if not career:
        raise HTTPException(status_code=404, detail="Không tìm thấy ngành nghề")
    return career.to_dict()
