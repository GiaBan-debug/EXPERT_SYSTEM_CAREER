"""Kiểm tra điều kiện IF của luật so với working memory (tập Facts).

Facts đầu vào (từ TV1, student_to_fact_dicts) là danh sách:
    [{"attribute": "scores.toan", "operator": "=", "value": 8.5},
     {"attribute": "interests", "operator": "=", "value": ["lap trinh", "toan"]}]
-> được chuyển thành working memory dạng dict {attribute: value}.

Điều kiện của luật (cùng dạng với Fact):
    {"attribute": "scores.toan", "operator": ">=", "value": 8}
    {"attribute": "interests", "operator": "intersects", "value": ["lap trinh", "may tinh"]}
Nhóm điều kiện: {"all": [...]}, {"any": [...]}, {"not": cond}; list = AND.

Toán tử: =, !=, >, >=, <, <=, contains, in, intersects (+ exists, not_exists).
Fact chưa có trong working memory -> điều kiện không thỏa (không ném lỗi).
"""
from typing import Any, Dict, Iterable, List, Union

Condition = Union[Dict[str, Any], List[Any]]
_MISSING = object()


class ConditionError(ValueError):
    """Điều kiện sai cấu trúc (thiếu khóa, toán tử không hỗ trợ...)."""


def _as_list(x: Any) -> list:
    return list(x) if isinstance(x, (list, tuple, set)) else [x]


def _norm(x: Any) -> Any:
    """Chuẩn hóa chuỗi (strip + lower) để so sánh không phân biệt hoa thường."""
    if isinstance(x, str):
        return x.strip().lower()
    if isinstance(x, (list, tuple, set)):
        return [_norm(i) for i in x]
    return x


def _eq(a, b) -> bool:
    a, b = _norm(a), _norm(b)
    if isinstance(a, list) and not isinstance(b, list):
        return b in a                      # fact dạng list, so với 1 giá trị
    if isinstance(a, list) and isinstance(b, list):
        return sorted(map(str, a)) == sorted(map(str, b))
    return a == b


def _contains(a, b) -> bool:
    a, b = _norm(a), _norm(b)
    if isinstance(a, str) and isinstance(b, str):
        return b in a
    items = _as_list(a)
    return all(i in items for i in _as_list(b))


def _in(a, b) -> bool:
    a, b = _norm(a), _norm(b)
    allowed = _as_list(b)
    return all(i in allowed for i in _as_list(a))


def _not_in(a, b) -> bool:
    allowed = _as_list(_norm(b))
    return not any(i in allowed for i in _as_list(_norm(a)))


def _intersects(a, b) -> bool:
    return bool(set(map(str, _as_list(_norm(a)))) & set(map(str, _as_list(_norm(b)))))


_OPERATORS = {
    "=": _eq,
    "==": _eq,
    "!=": lambda a, b: not _eq(a, b),
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "contains": _contains,
    "in": _in,
    "not_in": _not_in,
    "intersects": _intersects,
}


def normalize_facts(facts: Any) -> Dict[str, Any]:
    """Chuyển Facts (dict, list dict, list Fact của TV1) thành dict {attribute: value}."""
    if isinstance(facts, dict):
        return {str(k).strip().lower(): v for k, v in facts.items()}
    wm: Dict[str, Any] = {}
    for f in facts:
        if isinstance(f, dict):
            name, value = f.get("attribute", f.get("fact")), f.get("value")
        else:  # đối tượng Fact (pydantic)
            name, value = f.attribute, f.value
        wm[str(name).strip().lower()] = value
    return wm


def check_condition(cond: Condition, facts: Any) -> bool:
    """True nếu `cond` thỏa với `facts` (dict hoặc list Facts)."""
    wm = facts if isinstance(facts, dict) else normalize_facts(facts)

    if isinstance(cond, list):
        return all(check_condition(c, wm) for c in cond)
    if not isinstance(cond, dict):
        raise ConditionError(f"Điều kiện không hợp lệ: {cond!r}")

    if "all" in cond:
        return all(check_condition(c, wm) for c in cond["all"])
    if "any" in cond:
        return any(check_condition(c, wm) for c in cond["any"])
    if "not" in cond:
        return not check_condition(cond["not"], wm)

    name = cond.get("attribute", cond.get("fact"))
    op = cond.get("operator", cond.get("op"))
    if name is None or op is None:
        raise ConditionError(f"Điều kiện thiếu 'attribute' hoặc 'operator': {cond!r}")

    actual = wm.get(str(name).strip().lower(), _MISSING)
    if op == "exists":
        return actual is not _MISSING
    if op == "not_exists":
        return actual is _MISSING
    if op not in _OPERATORS:
        raise ConditionError(f"Toán tử không hỗ trợ: {op!r}")
    if actual is _MISSING:
        return False
    if "value" not in cond:
        raise ConditionError(f"Điều kiện thiếu 'value': {cond!r}")
    try:
        return bool(_OPERATORS[op](actual, cond["value"]))
    except TypeError:
        return False  # so sánh khác kiểu -> không thỏa


def collect_fact_names(cond: Condition) -> List[str]:
    """Các attribute được dùng trong điều kiện (phục vụ giải thích)."""
    if isinstance(cond, list):
        return [n for c in cond for n in collect_fact_names(c)]
    if "all" in cond or "any" in cond:
        items: Iterable = cond.get("all", cond.get("any"))
        return [n for c in items for n in collect_fact_names(c)]
    if "not" in cond:
        return collect_fact_names(cond["not"])
    return [cond.get("attribute", cond.get("fact"))]


def count_conditions(cond: Condition) -> int:
    """Số điều kiện nguyên tử – dùng làm độ đặc hiệu (specificity)."""
    return len(collect_fact_names(cond))
