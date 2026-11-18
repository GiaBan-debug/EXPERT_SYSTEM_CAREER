"""Repository thao tác với bảng Rules."""
from typing import List, Optional
from app.expert_system.knowledge_base.rule_manager import RuleManager
from app.models.rule import Rule


class RuleRepository:
    def __init__(self, rule_manager: Optional[RuleManager] = None):
        self.rule_manager = rule_manager or RuleManager.from_file()

    def get_all(self) -> List[Rule]:
        return self.rule_manager.all_rules()

    def get_active(self) -> List[Rule]:
        return self.rule_manager.active_rules()

    def get_by_id(self, rule_id: str) -> Optional[Rule]:
        try:
            return self.rule_manager.get(rule_id)
        except KeyError:
            return None
