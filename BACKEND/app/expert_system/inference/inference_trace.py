"""Cấu trúc dữ liệu ghi vết suy diễn (Thành viên 3).

FiredStep       : một lần bắn luật (dùng cho Explanation Trace của TV5).
InferenceResult : kết quả toàn bộ phiên suy diễn (đầu vào cho TV4 và TV5).
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FiredStep:
    step: int
    rule_id: str
    rule_name: str
    priority: int
    confidence: float
    new_facts: Dict[str, Any]
    updated_facts: Dict[str, Any]          # {attribute: (cũ, mới)}
    recommendations: List[Dict[str, Any]]  # gợi ý sinh ra ở bước này
    conflict_set: List[str]                # các luật cùng kích hoạt ở chu kỳ này
    explanation: str = ""


@dataclass
class InferenceResult:
    facts: Dict[str, Any]                   # working memory cuối cùng
    derived_facts: Dict[str, Any]           # chỉ các fact suy ra được
    recommendations: List[Dict[str, Any]]   # gợi ý nhóm ngành (đầu vào cho TV4)
    fired_rules: List[str]
    trace: List[FiredStep] = field(default_factory=list)
    iterations: int = 0
    stopped_reason: str = "fixed_point"     # fixed_point | max_iterations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "facts": self.facts,
            "derived_facts": self.derived_facts,
            "recommendations": self.recommendations,
            "fired_rules": self.fired_rules,
            "iterations": self.iterations,
            "stopped_reason": self.stopped_reason,
            "trace": [s.__dict__ for s in self.trace],
        }
