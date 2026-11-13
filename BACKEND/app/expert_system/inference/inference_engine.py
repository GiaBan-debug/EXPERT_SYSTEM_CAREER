"""Bộ máy suy diễn tiến (Forward Chaining) - Thành viên 3.

Đầu vào:
    - rules : luật của TV2 (RuleManager.active_rules() hoặc list dict từ rules.json)
    - facts : Facts của TV1 (student_to_fact_dicts(...) hoặc list Fact / dict)

Thuật toán:
    1. Working memory (WM) = Facts ban đầu.
    2. Mỗi chu kỳ: conflict set = luật BẬT, chưa bắn, điều kiện thỏa với WM.
    3. Chọn 1 luật (priority -> confidence -> số điều kiện -> id).
    4. Bắn luật:
         - kết luận type="fact"           -> ghi fact trung gian vào WM (có thể kích hoạt luật khác)
         - kết luận type="recommendation" -> ghi vào result.recommendations (đưa cho TV4 xử lý xung đột)
    5. Lặp tới khi conflict set rỗng (fixed point) hoặc chạm max_iterations.
Mỗi luật chỉ bắn tối đa 1 lần (refraction) => không lặp vô hạn.
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .condition_checker import check_condition, count_conditions, normalize_facts
from .inference_trace import FiredStep, InferenceResult


@dataclass
class InferenceRule:
    id: str
    condition: Any
    conclusions: List[Dict[str, Any]]
    priority: int = 0
    confidence: float = 1.0
    name: str = ""
    explanation: str = ""
    enabled: bool = True

    @classmethod
    def from_dict(cls, d: Any) -> "InferenceRule":
        if not isinstance(d, dict):          # đối tượng Rule của TV2
            d = d.to_dict()
        then = next((d[k] for k in ("conclusion", "then", "conclusions", "action") if k in d), [])
        if isinstance(then, dict):
            then = [then]
        cond = next((d[k] for k in ("conditions", "if", "condition", "when") if k in d), [])
        return cls(
            id=str(d["id"]),
            condition=cond,
            conclusions=list(then),
            priority=int(d.get("priority", 0)),
            confidence=float(d.get("confidence", 1.0)),
            name=d.get("name", ""),
            explanation=d.get("description", d.get("explanation", "")),
            enabled=bool(d.get("enabled", True)),
        )


Resolver = Callable[[List[InferenceRule]], InferenceRule]


def default_resolver(candidates: List[InferenceRule]) -> InferenceRule:
    """priority cao -> confidence cao -> nhiều điều kiện hơn -> id nhỏ."""
    return sorted(
        candidates,
        key=lambda r: (-r.priority, -r.confidence, -count_conditions(r.condition), r.id),
    )[0]


class ForwardChainingEngine:
    def __init__(
        self,
        rules: List[Any],
        resolver: Optional[Resolver] = None,
        max_iterations: int = 1000,
    ):
        parsed = [r if isinstance(r, InferenceRule) else InferenceRule.from_dict(r) for r in rules]
        ids = [r.id for r in parsed]
        if len(ids) != len(set(ids)):
            raise ValueError("Có luật trùng id trong tập luật")
        self.rules: List[InferenceRule] = [r for r in parsed if r.enabled]
        self.resolver = resolver or default_resolver
        self.max_iterations = max_iterations

    def run(self, initial_facts: Any) -> InferenceResult:
        wm: Dict[str, Any] = normalize_facts(initial_facts)
        fired: set = set()
        trace: List[FiredStep] = []
        derived: Dict[str, Any] = {}
        recommendations: List[Dict[str, Any]] = []
        reason = "fixed_point"

        for step in range(1, self.max_iterations + 1):
            conflict_set = [
                r for r in self.rules
                if r.id not in fired and check_condition(r.condition, wm)
            ]
            if not conflict_set:
                break

            rule = self.resolver(conflict_set)
            fired.add(rule.id)

            new_facts: Dict[str, Any] = {}
            updated: Dict[str, Any] = {}
            step_recs: List[Dict[str, Any]] = []

            for c in rule.conclusions:
                if c.get("type", "fact") == "recommendation":
                    rec = {
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "career_group": c.get("career_group"),
                        "careers": list(c.get("careers", [])),
                        "priority": rule.priority,
                        "confidence": rule.confidence,
                        "explanation": rule.explanation,
                    }
                    step_recs.append(rec)
                    recommendations.append(rec)
                    continue
                name = str(c.get("attribute", c.get("fact"))).strip().lower()
                value = c["value"]
                if name not in wm:
                    new_facts[name] = value
                elif wm[name] != value:
                    updated[name] = (wm[name], value)
                else:
                    continue
                wm[name] = value
                derived[name] = value

            trace.append(FiredStep(
                step=step, rule_id=rule.id, rule_name=rule.name,
                priority=rule.priority, confidence=rule.confidence,
                new_facts=new_facts, updated_facts=updated,
                recommendations=step_recs,
                conflict_set=[r.id for r in conflict_set],
                explanation=rule.explanation,
            ))
        else:
            reason = "max_iterations"

        return InferenceResult(
            facts=wm, derived_facts=derived, recommendations=recommendations,
            fired_rules=[s.rule_id for s in trace],
            trace=trace, iterations=len(trace), stopped_reason=reason,
        )


def run_inference(rules: List[Any], facts: Any, **kwargs) -> InferenceResult:
    """Tiện ích: tạo engine và chạy một lần."""
    return ForwardChainingEngine(rules, **kwargs).run(facts)
