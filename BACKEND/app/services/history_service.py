"""Dịch vụ lịch sử tư vấn."""
from typing import Any, Dict, List, Optional
from app.database.repositories.consultation_repository import ConsultationRepository


class HistoryService:
    def __init__(self, consultation_repo: Optional[ConsultationRepository] = None):
        self.repo = consultation_repo or ConsultationRepository()

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.repo.get_all(limit=limit)

    def get_consultation_detail(self, cid: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(cid)
