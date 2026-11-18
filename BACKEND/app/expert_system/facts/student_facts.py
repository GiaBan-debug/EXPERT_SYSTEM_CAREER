"""Chuyển đổi dữ liệu học sinh thành danh sách Facts chuẩn cho bộ máy suy diễn (Thành viên 1).

Đầu vào tương ứng payload từ Frontend hoặc API:
{
    "student": {"fullName": "...", "grade": "12", "track": "khoa_hoc_tu_nhien", "region": "south"},
    "scores": {"math": 8.5, "physics": 8.0, ...},
    "riasec": {"R": 80, "I": 90, ...},
    "preferences": {"environment": "tech", "tuition": "standard", "priority": "high_salary"}
}
"""
from __future__ import annotations

from typing import Any, Dict, List, Union
from app.expert_system.facts.fact_schema import Fact


def student_to_facts(data: Dict[str, Any]) -> List[Fact]:
    """Chuyển đổi dữ liệu học sinh thành danh sách các đối tượng Fact."""
    facts: List[Fact] = []

    # 1. Điểm số (scores)
    scores = data.get("scores", {})
    for subject, score in scores.items():
        if score is not None:
            attr_name = f"score.{subject}"
            try:
                val = float(score)
                facts.append(Fact(attribute=attr_name, value=val, source="input"))
            except (ValueError, TypeError):
                continue

    # 2. Điểm RIASEC
    riasec = data.get("riasec", {})
    for letter, score in riasec.items():
        if score is not None:
            attr_name = f"riasec.{letter.upper()}"
            try:
                val = float(score)
                facts.append(Fact(attribute=attr_name, value=val, source="input"))
            except (ValueError, TypeError):
                continue

    # 3. Thông tin học sinh (student)
    student = data.get("student", {})
    if "track" in student:
        facts.append(Fact(attribute="student.track", value=str(student["track"]), source="input"))
    if "grade" in student:
        facts.append(Fact(attribute="student.grade", value=str(student["grade"]), source="input"))
    if "region" in student:
        facts.append(Fact(attribute="student.region", value=str(student["region"]), source="input"))

    # 4. Nguyện vọng & sở thích (preferences)
    prefs = data.get("preferences", {})
    if "environment" in prefs:
        facts.append(Fact(attribute="pref.environment", value=str(prefs["environment"]), source="input"))
    if "tuition" in prefs:
        facts.append(Fact(attribute="pref.tuition", value=str(prefs["tuition"]), source="input"))
    if "priority" in prefs:
        facts.append(Fact(attribute="pref.priority", value=str(prefs["priority"]), source="input"))

    return facts


def student_to_fact_dicts(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Chuyển đổi dữ liệu học sinh thành list dict {attribute, operator, value}."""
    return [f.to_dict() for f in student_to_facts(data)]
