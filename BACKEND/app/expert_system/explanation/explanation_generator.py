"""Xây dựng và định dạng lời giải thích suy diễn (Explanation Facility - Thành viên 5)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.expert_system.inference.inference_trace import FiredStep, InferenceResult


class ExplanationGenerator:
    """Sinh lời giải thích từ vết suy diễn (InferenceResult & FiredSteps)."""

    def __init__(self, inference_result: InferenceResult):
        self.result = inference_result

    def generate_step_explanations(self) -> List[Dict[str, Any]]:
        """Tạo danh sách chi tiết các bước giải thích từ trace."""
        steps = []
        for step in self.result.trace:
            steps.append({
                "step": step.step,
                "rule_id": step.rule_id,
                "rule_name": step.rule_name,
                "priority": step.priority,
                "confidence": step.confidence,
                "explanation": step.explanation,
                "new_facts": step.new_facts,
                "conflict_set_size": len(step.conflict_set),
            })
        return steps

    def generate_career_explanation(self, career_id: str, career_group: str) -> Dict[str, Any]:
        """Giải thích vì sao một ngành nghề/nhóm ngành được đề xuất."""
        supporting_rules = []
        for step in self.result.trace:
            for rec in step.recommendations:
                if rec.get("career_group") == career_group or career_id in rec.get("careers", []):
                    supporting_rules.append({
                        "rule_id": step.rule_id,
                        "rule_name": step.rule_name,
                        "explanation": step.explanation,
                        "confidence": step.confidence,
                    })

        return {
            "career_id": career_id,
            "career_group": career_group,
            "supporting_rules": supporting_rules,
            "summary": f"Đề xuất dựa trên {len(supporting_rules)} luật thỏa mãn trong quá trình suy diễn.",
        }

    def generate_summary(self) -> Dict[str, Any]:
        """Tạo báo cáo tổng kết vết suy diễn."""
        return {
            "total_rules_fired": len(self.result.fired_rules),
            "iterations": self.result.iterations,
            "stopped_reason": self.result.stopped_reason,
            "derived_facts": self.result.derived_facts,
            "fired_rule_ids": self.result.fired_rules,
            "steps": self.generate_step_explanations(),
        }
