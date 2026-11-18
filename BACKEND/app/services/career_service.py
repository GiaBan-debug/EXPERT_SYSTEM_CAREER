"""Dịch vụ tra cứu danh mục và chi tiết Ngành nghề."""
from typing import List, Optional
from app.database.repositories.career_repository import CareerRepository
from app.models.career import Career, CareerCategory


class CareerService:
    def __init__(self, career_repo: Optional[CareerRepository] = None):
        self.repo = career_repo or CareerRepository()

    def get_all_careers(self) -> List[Career]:
        return self.repo.get_all()

    def get_career_by_id(self, career_id: str) -> Optional[Career]:
        return self.repo.get_by_id(career_id)

    def get_categories(self) -> List[CareerCategory]:
        return self.repo.get_categories()
