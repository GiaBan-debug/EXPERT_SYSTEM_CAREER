"""Unit test cho Explanation Generator & Formatter (Thành viên 5)."""
from app.expert_system.explanation.explanation_generator import ExplanationGenerator
from app.expert_system.explanation.explanation_formatter import ExplanationFormatter
from app.expert_system.inference.inference_trace import FiredStep, InferenceResult


def test_explanation_generator():
    step1 = FiredStep(
        step=1,
        rule_id="ABL-01",
        rule_name="Logic cao",
        priority=5,
        confidence=0.9,
        new_facts={"ability.logic": "high"},
        updated_facts={},
        recommendations=[],
        conflict_set=["ABL-01"],
        explanation="Toán >= 8.0 và Tin học >= 7.5"
    )
    result = InferenceResult(
        facts={"ability.logic": "high"},
        derived_facts={"ability.logic": "high"},
        recommendations=[{"career_group": "CNTT", "careers": ["it_software"]}],
        fired_rules=["ABL-01"],
        trace=[step1],
        iterations=1
    )

    gen = ExplanationGenerator(result)
    summary = gen.generate_summary()

    assert summary["total_rules_fired"] == 1
    assert len(summary["steps"]) == 1
    assert summary["steps"][0]["rule_id"] == "ABL-01"

    bullets = ExplanationFormatter.format_to_bullet_points(gen)
    assert len(bullets) == 1
    assert "Toán >= 8.0" in bullets[0]
