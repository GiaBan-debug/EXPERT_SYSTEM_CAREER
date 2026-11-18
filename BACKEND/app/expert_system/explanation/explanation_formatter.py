"""Định dạng chuỗi văn bản giải thích tự nhiên cho người dùng (Thành viên 5)."""
from __future__ import annotations

from typing import Any, Dict, List
from app.expert_system.explanation.explanation_generator import ExplanationGenerator


class ExplanationFormatter:
    """Format lời giải thích thành text hoặc HTML thân thiện với học sinh THPT."""

    @staticmethod
    def format_to_bullet_points(generator: ExplanationGenerator) -> List[str]:
        summary = generator.generate_summary()
        bullets = []
        for step in summary["steps"]:
            expl = step["explanation"] or f"Kích hoạt luật {step['rule_id']}: {step['rule_name']}"
            bullets.append(f"• [Bước {step['step']}] {expl} (Độ tin cậy: {int(step['confidence'] * 100)}%)")
        return bullets

    @staticmethod
    def format_career_justification(career_name: str, career_expl: Dict[str, Any]) -> str:
        rules = career_expl.get("supporting_rules", [])
        if not rules:
            return f"Ngành {career_name} phù hợp với định hướng tổng quát của học sinh."
        reasons = [r.get("explanation") or r.get("rule_name") for r in rules]
        return f"Ngành {career_name} được đề xuất bởi vì: " + "; ".join(reasons) + "."
