"""Repository thao tác với bảng Careers & Career Categories."""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.models.career import Career, CareerCategory

CAREERS_FILE = Path(__file__).resolve().parents[4] / "DATABASE" / "data" / "career_details.json"
CATEGORIES_FILE = Path(__file__).resolve().parents[4] / "DATABASE" / "data" / "career_categories.json"


class CareerRepository:
    def __init__(self):
        self._careers_cache: Optional[List[Career]] = None
        self._categories_cache: Optional[List[CareerCategory]] = None

    def get_all(self) -> List[Career]:
        if self._careers_cache is None:
            if CAREERS_FILE.exists():
                with open(CAREERS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._careers_cache = [Career.from_dict(item) for item in data]
            else:
                self._careers_cache = []
        return self._careers_cache

    def get_by_id(self, career_id: str) -> Optional[Career]:
        all_careers = self.get_all()
        for c in all_careers:
            if c.id == career_id:
                return c
        return None

    def get_categories(self) -> List[CareerCategory]:
        if self._categories_cache is None:
            if CATEGORIES_FILE.exists():
                with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._categories_cache = [CareerCategory(**item) for item in data]
            else:
                self._categories_cache = []
        return self._categories_cache
