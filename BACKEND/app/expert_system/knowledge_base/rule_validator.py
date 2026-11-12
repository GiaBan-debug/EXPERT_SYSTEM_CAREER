"""Kiểm tra cấu trúc và nội dung luật (Thành viên 2).

Kiểm tra cho TỪNG luật:
    - đủ trường bắt buộc, không có trường lạ, đúng kiểu dữ liệu;
    - id đúng định dạng (vd GRP-01);
    - thuộc tính trong điều kiện có trong bảng quy ước Fact;
    - toán tử phù hợp kiểu thuộc tính; giá trị nằm trong miền cho phép;
    - điều kiện không tự mâu thuẫn (vd math >= 8 và math < 5);
    - kết luận hợp lệ (fact trung gian chỉ được gán cho thuộc tính "derived");
    - priority nguyên trong khoảng, confidence trong (0, 1].
Kiểm tra cho CẢ TẬP luật:
    - trùng id, trùng nội dung (cùng điều kiện + kết luận);
    - cảnh báo (warning) điều kiện dùng Fact trung gian mà không luật nào sinh ra.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence

from app.expert_system.knowledge_base.fact_conventions import FactConventions
from app.models.rule import (
    CONCLUSION_FACT, CONCLUSION_RECOMMENDATION, CONCLUSION_TYPES, Rule, rule_signature,
)

RULE_ID_PATTERN = re.compile(r"^[A-Z]{2,5}-\d{2,3}$")

REQUIRED_FIELDS = ("id", "name", "conditions", "conclusion", "priority", "confidence")
OPTIONAL_FIELDS = ("description", "category", "enabled")
ALLOWED_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


@dataclass
class ValidationIssue:
    rule_id: str
    field: str
    message: str
    severity: str = "error"  # "error" | "warning"

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.rule_id} · {self.field}: {self.message}"


@dataclass
class RulesetValidation:
    valid_indices: List[int] = field(default_factory=list)
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


class RuleValidator:
    def __init__(self, conventions: Optional[FactConventions] = None):
        self.conventions = conventions or FactConventions.from_file()

    # ------------------------------------------------------------------ một luật
    def validate_rule(self, rule: Any, index: Optional[int] = None) -> List[ValidationIssue]:
        """Trả về danh sách lỗi của một luật (dạng dict). Rỗng = hợp lệ."""
        if not isinstance(rule, dict):
            return [ValidationIssue(self._label(None, index), "(luật)", "Mỗi luật phải là một object JSON")]

        rid = rule.get("id") if isinstance(rule.get("id"), str) and rule.get("id") else None
        label = self._label(rid, index)
        issues: List[ValidationIssue] = []
        err = lambda f, m: issues.append(ValidationIssue(label, f, m))  # noqa: E731

        for f in REQUIRED_FIELDS:
            if f not in rule:
                err(f, "Thiếu trường bắt buộc")
        for f in rule:
            if f not in ALLOWED_FIELDS:
                err(f, f"Trường không được hỗ trợ (chỉ gồm: {', '.join(ALLOWED_FIELDS)})")

        if "id" in rule and not (isinstance(rule["id"], str) and RULE_ID_PATTERN.match(rule["id"])):
            err("id", "Mã luật phải có dạng 'AAA-01' (2-5 chữ HOA, gạch ngang, 2-3 chữ số)")
        if "name" in rule and not (isinstance(rule["name"], str) and rule["name"].strip()):
            err("name", "Tên luật phải là chuỗi không rỗng")
        for f in ("description", "category"):
            if f in rule and not isinstance(rule[f], str):
                err(f, "Phải là chuỗi")
        if "enabled" in rule and not isinstance(rule["enabled"], bool):
            err("enabled", "Phải là true/false")

        if "priority" in rule:
            p, (lo, hi) = rule["priority"], self.conventions.priority_range
            if not (isinstance(p, int) and not isinstance(p, bool)):
                err("priority", "Phải là số nguyên")
            elif not lo <= p <= hi:
                err("priority", f"Phải nằm trong khoảng {lo}..{hi} (được {p})")
        if "confidence" in rule:
            c, (lo, hi) = rule["confidence"], self.conventions.confidence_range
            if not _is_number(c):
                err("confidence", "Phải là số")
            elif not (lo < c <= hi):
                err("confidence", f"Phải nằm trong khoảng ({lo}, {hi}] (được {c})")

        if "conditions" in rule:
            self._check_conditions(rule["conditions"], label, issues)
        if "conclusion" in rule:
            self._check_conclusion(rule["conclusion"], label, issues)
        return issues

    # ------------------------------------------------------------------ điều kiện
    def _check_conditions(self, conds: Any, label: str, issues: List[ValidationIssue]) -> None:
        if not isinstance(conds, list) or not conds:
            issues.append(ValidationIssue(label, "conditions", "Phải là danh sách có ít nhất 1 điều kiện"))
            return
        clean: List[Dict[str, Any]] = []
        for i, c in enumerate(conds):
            field_name = f"conditions[{i}]"
            n_before = len(issues)
            self._check_one_condition(c, label, field_name, issues)
            if len(issues) == n_before:
                clean.append(c)
        self._check_contradiction(clean, label, issues)

    def _check_one_condition(self, c: Any, label: str, fname: str, issues: List[ValidationIssue]) -> None:
        err = lambda m: issues.append(ValidationIssue(label, fname, m))  # noqa: E731
        if not isinstance(c, dict):
            return err("Điều kiện phải là object {attribute, operator, value}")
        missing = [k for k in ("attribute", "operator", "value") if k not in c]
        if missing:
            return err(f"Thiếu: {', '.join(missing)}")
        extra = [k for k in c if k not in ("attribute", "operator", "value")]
        if extra:
            return err(f"Trường lạ: {', '.join(extra)}")

        attr, op, val = c["attribute"], c["operator"], c["value"]
        spec = self.conventions.attribute(attr) if isinstance(attr, str) else None
        if spec is None:
            return err(f"Thuộc tính '{attr}' không có trong bảng quy ước Fact")
        allowed = self.conventions.allowed_operators(attr)
        if op not in allowed:
            return err(f"Toán tử '{op}' không hợp lệ cho '{attr}' (kiểu {spec['type']}; cho phép: {', '.join(allowed)})")

        if spec["type"] == "number":
            if not _is_number(val):
                return err(f"Giá trị của '{attr}' phải là số")
            if not spec["min"] <= val <= spec["max"]:
                return err(f"Giá trị {val} ngoài miền [{spec['min']}, {spec['max']}] của '{attr}'")
        else:  # enum
            if op in ("in", "not_in"):
                if not isinstance(val, list) or not val:
                    return err(f"Toán tử '{op}' cần một danh sách không rỗng")
                if len(set(map(str, val))) != len(val):
                    return err("Danh sách giá trị bị lặp phần tử")
                bad = [v for v in val if v not in spec["values"]]
                if bad:
                    return err(f"Giá trị {bad} ngoài miền {spec['values']} của '{attr}'")
            else:
                if isinstance(val, list) or val not in spec["values"]:
                    return err(f"Giá trị {val!r} ngoài miền {spec['values']} của '{attr}'")

    def _check_contradiction(self, conds: Sequence[Dict[str, Any]], label: str,
                             issues: List[ValidationIssue]) -> None:
        """Phát hiện điều kiện cùng thuộc tính không thể đồng thời đúng."""
        by_attr: Dict[str, List[Dict[str, Any]]] = {}
        for c in conds:
            by_attr.setdefault(c["attribute"], []).append(c)
        for attr, cs in by_attr.items():
            if len(cs) < 2:
                continue
            spec = self.conventions.attribute(attr)
            if spec["type"] == "number":
                lo, lo_strict, hi, hi_strict = float("-inf"), False, float("inf"), False
                eqs, nes = [], []
                for c in cs:
                    op, v = c["operator"], c["value"]
                    if op == ">=" and v > lo:
                        lo, lo_strict = v, False
                    elif op == ">" and v >= lo:
                        lo, lo_strict = v, True
                    elif op == "<=" and v < hi:
                        hi, hi_strict = v, False
                    elif op == "<" and v <= hi:
                        hi, hi_strict = v, True
                    elif op == "==":
                        eqs.append(v)
                    elif op == "!=":
                        nes.append(v)
                bad = lo > hi or (lo == hi and (lo_strict or hi_strict))
                if len(set(eqs)) > 1:
                    bad = True
                for e in eqs:
                    if e < lo or e > hi or (e == lo and lo_strict) or (e == hi and hi_strict) or e in nes:
                        bad = True
                if bad:
                    issues.append(ValidationIssue(label, "conditions",
                                                  f"Các điều kiện trên '{attr}' mâu thuẫn, không thể cùng đúng"))
            else:
                possible = set(spec["values"])
                for c in cs:
                    op, v = c["operator"], c["value"]
                    if op == "==":
                        possible &= {v}
                    elif op == "!=":
                        possible -= {v}
                    elif op == "in":
                        possible &= set(v)
                    elif op == "not_in":
                        possible -= set(v)
                if not possible:
                    issues.append(ValidationIssue(label, "conditions",
                                                  f"Các điều kiện trên '{attr}' mâu thuẫn, không thể cùng đúng"))

    # ------------------------------------------------------------------ kết luận
    def _check_conclusion(self, concl: Any, label: str, issues: List[ValidationIssue]) -> None:
        err = lambda m: issues.append(ValidationIssue(label, "conclusion", m))  # noqa: E731
        if not isinstance(concl, dict):
            return err("Kết luận phải là object")
        ctype = concl.get("type")
        if ctype not in CONCLUSION_TYPES:
            return err(f"'type' phải là một trong {list(CONCLUSION_TYPES)}")

        if ctype == CONCLUSION_FACT:
            allowed = {"type", "attribute", "value"}
            extra = [k for k in concl if k not in allowed]
            if extra:
                return err(f"Kết luận loại 'fact' có trường lạ: {', '.join(extra)}")
            attr, val = concl.get("attribute"), concl.get("value")
            spec = self.conventions.attribute(attr) if isinstance(attr, str) else None
            if spec is None:
                return err(f"Thuộc tính '{attr}' không có trong bảng quy ước Fact")
            if not self.conventions.is_derived(attr):
                return err(f"'{attr}' là dữ kiện đầu vào, luật không được kết luận ra nó (chỉ gán cho thuộc tính 'derived')")
            if spec["type"] == "enum" and val not in spec["values"]:
                return err(f"Giá trị {val!r} ngoài miền {spec['values']} của '{attr}'")
        else:  # recommendation
            allowed = {"type", "career_group", "careers"}
            extra = [k for k in concl if k not in allowed]
            if extra:
                return err(f"Kết luận loại 'recommendation' có trường lạ: {', '.join(extra)}")
            group = concl.get("career_group")
            if group not in self.conventions.career_groups:
                return err(f"Nhóm ngành {group!r} không có trong bảng quy ước "
                           f"({', '.join(self.conventions.career_groups)})")
            careers = concl.get("careers", [])
            if not isinstance(careers, list):
                return err("'careers' phải là danh sách mã ngành")
            for car in careers:
                if car not in self.conventions.careers:
                    err(f"Mã ngành {car!r} không có trong bảng quy ước")
                elif self.conventions.careers[car] != group:
                    err(f"Ngành {car!r} thuộc nhóm {self.conventions.careers[car]}, không thuộc {group}")

    # ------------------------------------------------------------------ cả tập luật
    def validate_ruleset(self, raw_rules: Sequence[Any], min_rules: Optional[int] = None) -> RulesetValidation:
        """Kiểm tra cả tập. Luật trùng id/nội dung xuất hiện SAU bị loại; luật đầu tiên được giữ."""
        result = RulesetValidation()
        seen_ids: Dict[str, int] = {}
        seen_sigs: Dict[str, str] = {}

        for idx, raw in enumerate(raw_rules):
            issues = self.validate_rule(raw, index=idx)
            if not issues:
                rid = raw["id"]
                sig = rule_signature(raw)
                if rid in seen_ids:
                    issues.append(ValidationIssue(rid, "id", f"Trùng mã luật (đã dùng ở vị trí #{seen_ids[rid]})"))
                elif sig in seen_sigs:
                    issues.append(ValidationIssue(rid, "(nội dung)",
                                                  f"Trùng nội dung với luật {seen_sigs[sig]} (cùng điều kiện và kết luận)"))
                else:
                    seen_ids[rid] = idx
                    seen_sigs[sig] = rid
            if issues:
                result.errors.extend(issues)
            else:
                result.valid_indices.append(idx)

        accepted = [raw_rules[i] for i in result.valid_indices]
        result.warnings.extend(self.find_unreachable_conditions(accepted))
        if min_rules is not None and len(accepted) < min_rules:
            result.errors.append(ValidationIssue("(bộ luật)", "số lượng",
                                                 f"Cần tối thiểu {min_rules} luật hợp lệ, hiện có {len(accepted)}"))
        return result

    def validate_against(self, candidate: Any, existing: Iterable[Rule],
                         ignore_id: Optional[str] = None) -> List[ValidationIssue]:
        """Kiểm tra một luật mới/được sửa so với tập luật đang có (dùng cho RuleManager)."""
        issues = self.validate_rule(candidate)
        if issues:
            return issues
        sig = rule_signature(candidate)
        for r in existing:
            if r.id == ignore_id:
                continue
            if r.id == candidate["id"]:
                issues.append(ValidationIssue(candidate["id"], "id", "Trùng mã luật"))
            elif r.signature() == sig:
                issues.append(ValidationIssue(candidate["id"], "(nội dung)",
                                              f"Trùng nội dung với luật {r.id}"))
        return issues

    def find_unreachable_conditions(self, raw_rules: Sequence[Dict[str, Any]]) -> List[ValidationIssue]:
        """Cảnh báo điều kiện dùng Fact trung gian mà không luật BẬT nào có thể sinh ra giá trị đó."""
        produced: Dict[str, set] = {}
        for r in raw_rules:
            if r.get("enabled", True) and r["conclusion"]["type"] == CONCLUSION_FACT:
                produced.setdefault(r["conclusion"]["attribute"], set()).add(r["conclusion"]["value"])
        out: List[ValidationIssue] = []
        for r in raw_rules:
            for c in r["conditions"]:
                if not self.conventions.is_derived(c["attribute"]):
                    continue
                vals, op, v = produced.get(c["attribute"], set()), c["operator"], c["value"]
                ok = {
                    "==": lambda: v in vals, "!=": lambda: any(x != v for x in vals),
                    "in": lambda: bool(vals & set(v)), "not_in": lambda: bool(vals - set(v)),
                }[op]()
                if not ok:
                    out.append(ValidationIssue(
                        r["id"], "conditions",
                        f"Điều kiện {c['attribute']} {op} {v} không bao giờ thỏa vì không luật nào sinh ra giá trị đó",
                        severity="warning"))
        return out

    @staticmethod
    def _label(rid: Optional[str], index: Optional[int]) -> str:
        if rid:
            return rid
        return f"(luật #{index})" if index is not None else "(luật)"
