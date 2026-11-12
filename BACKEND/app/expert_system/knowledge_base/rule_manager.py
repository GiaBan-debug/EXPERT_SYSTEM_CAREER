"""Quản lý tập luật: tra cứu, thêm, cập nhật, bật/tắt, xóa, lưu (Thành viên 2).

Mọi thao tác thay đổi đều được kiểm tra bằng RuleValidator trước khi áp dụng;
nếu không hợp lệ sẽ raise RuleValidationError và tập luật KHÔNG bị thay đổi.
"""
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from app.expert_system.knowledge_base.fact_conventions import DEFAULT_RULES_PATH, FactConventions
from app.expert_system.knowledge_base.rule_loader import LoadReport, RuleLoader
from app.expert_system.knowledge_base.rule_validator import RuleValidator, ValidationIssue
from app.models.rule import CONCLUSION_FACT, CONCLUSION_RECOMMENDATION, Rule


class RuleNotFoundError(KeyError):
    pass


class RuleValidationError(ValueError):
    def __init__(self, issues: List[ValidationIssue]):
        super().__init__("; ".join(str(i) for i in issues))
        self.issues = issues


class RuleManager:
    def __init__(self, rules: Optional[List[Rule]] = None,
                 conventions: Optional[FactConventions] = None):
        self.validator = RuleValidator(conventions)
        self._rules: Dict[str, Rule] = {}
        for r in rules or []:
            self._rules[r.id] = r
        self.last_report: Optional[LoadReport] = None

    # ------------------------------------------------------------------ khởi tạo
    @classmethod
    def from_file(cls, path: Union[str, Path, None] = None, strict: bool = False,
                  conventions: Optional[FactConventions] = None,
                  min_rules: Optional[int] = None) -> "RuleManager":
        loader = RuleLoader(conventions)
        report = loader.load_from_file(path, strict=strict, min_rules=min_rules)
        mgr = cls(report.rules, conventions or loader.validator.conventions)
        mgr.last_report = report
        return mgr

    # ------------------------------------------------------------------ truy vấn
    def get(self, rule_id: str) -> Rule:
        try:
            return self._rules[rule_id]
        except KeyError:
            raise RuleNotFoundError(f"Không có luật {rule_id}") from None

    def all_rules(self) -> List[Rule]:
        return list(self._rules.values())

    def active_rules(self) -> List[Rule]:
        """Các luật đang BẬT - đây là tập mà bộ suy diễn (Thành viên 3) sử dụng."""
        return [r for r in self._rules.values() if r.enabled]

    def find_by_conclusion_group(self, career_group: str) -> List[Rule]:
        return [r for r in self._rules.values()
                if r.conclusion.type == CONCLUSION_RECOMMENDATION and r.conclusion.career_group == career_group]

    def __len__(self) -> int:
        return len(self._rules)

    def __contains__(self, rule_id: str) -> bool:
        return rule_id in self._rules

    # ------------------------------------------------------------------ thay đổi
    def add_rule(self, rule: Union[Rule, Dict[str, Any]]) -> Rule:
        data = rule.to_dict() if isinstance(rule, Rule) else copy.deepcopy(rule)
        issues = self.validator.validate_against(data, self._rules.values())
        if issues:
            raise RuleValidationError(issues)
        new_rule = Rule.from_dict(data)
        self._rules[new_rule.id] = new_rule
        return new_rule

    def update_rule(self, rule_id: str, changes: Dict[str, Any]) -> Rule:
        """Cập nhật một phần luật. Không được đổi 'id'."""
        current = self.get(rule_id)
        if "id" in changes and changes["id"] != rule_id:
            raise RuleValidationError([ValidationIssue(rule_id, "id", "Không được đổi mã luật")])
        data = current.to_dict()
        data.update(copy.deepcopy(changes))
        issues = self.validator.validate_against(data, self._rules.values(), ignore_id=rule_id)
        if issues:
            raise RuleValidationError(issues)
        updated = Rule.from_dict(data)
        self._rules[rule_id] = updated
        return updated

    def enable_rule(self, rule_id: str) -> Rule:
        rule = self.get(rule_id)
        rule.enabled = True
        return rule

    def disable_rule(self, rule_id: str) -> Rule:
        rule = self.get(rule_id)
        rule.enabled = False
        return rule

    def remove_rule(self, rule_id: str) -> Rule:
        rule = self.get(rule_id)
        del self._rules[rule_id]
        return rule

    # ------------------------------------------------------------------ kiểm tra / thống kê / lưu
    def validate_all(self, min_rules: Optional[int] = None):
        """Kiểm tra lại toàn bộ tập luật hiện tại (kể cả cảnh báo Fact trung gian không với tới được)."""
        return self.validator.validate_ruleset([r.to_dict() for r in self._rules.values()], min_rules=min_rules)

    def stats(self) -> Dict[str, Any]:
        rules = self.all_rules()
        return {
            "total": len(rules),
            "enabled": sum(r.enabled for r in rules),
            "disabled": sum(not r.enabled for r in rules),
            "fact_rules": sum(r.conclusion.type == CONCLUSION_FACT for r in rules),
            "recommendation_rules": sum(r.conclusion.type == CONCLUSION_RECOMMENDATION for r in rules),
            "by_group": dict(Counter(r.conclusion.career_group for r in rules
                                     if r.conclusion.type == CONCLUSION_RECOMMENDATION)),
        }

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._rules.values()]

    def save(self, path: Union[str, Path, None] = None) -> Path:
        path = Path(path) if path else DEFAULT_RULES_PATH
        payload = {"version": "1.0", "rules": self.to_dicts()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return path
