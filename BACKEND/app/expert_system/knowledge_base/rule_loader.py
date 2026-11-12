"""Nạp luật từ JSON (Thành viên 2).

Luật hợp lệ được nạp; luật sai cấu trúc bị TỪ CHỐI (không nạp) và được báo lỗi rõ ràng.
    strict=False (mặc định): bỏ qua luật lỗi, trả về báo cáo để ghi log.
    strict=True            : có bất kỳ lỗi nào thì raise RuleLoadError.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Union

from app.expert_system.knowledge_base.fact_conventions import DEFAULT_RULES_PATH, FactConventions
from app.expert_system.knowledge_base.rule_validator import RuleValidator, ValidationIssue
from app.models.rule import Rule


class RuleLoadError(Exception):
    def __init__(self, message: str, issues: Optional[List[ValidationIssue]] = None):
        super().__init__(message)
        self.issues = issues or []


@dataclass
class LoadReport:
    rules: List[Rule] = field(default_factory=list)
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    source: str = ""
    total: int = 0  # tổng số luật đọc được trong file

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        return (f"{self.source}: nạp {len(self.rules)}/{self.total} luật, "
                f"{len(self.errors)} lỗi, {len(self.warnings)} cảnh báo")


class RuleLoader:
    def __init__(self, conventions: Optional[FactConventions] = None,
                 validator: Optional[RuleValidator] = None):
        self.validator = validator or RuleValidator(conventions)

    def load_from_file(self, path: Union[str, Path, None] = None, strict: bool = False,
                       min_rules: Optional[int] = None) -> LoadReport:
        path = Path(path) if path else DEFAULT_RULES_PATH
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise RuleLoadError(f"Không tìm thấy file luật: {path}") from e
        except json.JSONDecodeError as e:
            raise RuleLoadError(f"File luật không phải JSON hợp lệ ({path.name}): {e}") from e
        return self.load_from_data(data, source=str(path.name), strict=strict, min_rules=min_rules)

    def load_from_data(self, data: Any, source: str = "<memory>", strict: bool = False,
                       min_rules: Optional[int] = None) -> LoadReport:
        """Chấp nhận {"rules": [...]} hoặc trực tiếp một danh sách luật."""
        raw = data.get("rules") if isinstance(data, dict) else data
        if not isinstance(raw, list):
            raise RuleLoadError(f"{source}: dữ liệu luật phải là danh sách hoặc object có khóa 'rules'")

        validation = self.validator.validate_ruleset(raw, min_rules=min_rules)
        report = LoadReport(
            rules=[Rule.from_dict(raw[i]) for i in validation.valid_indices],
            errors=validation.errors,
            warnings=validation.warnings,
            source=source,
            total=len(raw),
        )
        if strict and report.errors:
            raise RuleLoadError(f"{report.summary()}", report.errors)
        return report
