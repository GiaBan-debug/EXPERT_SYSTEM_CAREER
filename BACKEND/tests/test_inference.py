"""Unit test cho bộ máy suy diễn tiến (Thành viên 3).

Chạy từ thư mục BACKEND:
    python -m pytest tests/test_inference.py -v
"""
import pytest

from app.expert_system.inference import (
    ForwardChainingEngine,
    check_condition,
    run_inference,
)


# ----------------------------------------------------------------- dữ liệu mẫu
def fact(attribute, value):
    """Fact đầu vào dạng TV1: {attribute, operator '=', value}."""
    return {"attribute": attribute, "operator": "=", "value": value}


def cond(attribute, operator, value):
    return {"attribute": attribute, "operator": operator, "value": value}


def fact_rule(rid, conditions, attribute, value, priority=5, confidence=0.9, **extra):
    return {
        "id": rid, "name": rid, "priority": priority, "confidence": confidence,
        "conditions": conditions,
        "conclusion": {"type": "fact", "attribute": attribute, "value": value},
        **extra,
    }


def rec_rule(rid, conditions, group, careers=(), priority=5, confidence=0.9, **extra):
    return {
        "id": rid, "name": rid, "priority": priority, "confidence": confidence,
        "conditions": conditions,
        "conclusion": {"type": "recommendation", "career_group": group, "careers": list(careers)},
        **extra,
    }


@pytest.fixture
def facts():
    return [
        fact("grade", 12),
        fact("scores.math", 8.5),
        fact("scores.physics", 7.5),
        fact("interests", ["Lap trinh", "Toan"]),
        fact("skills", ["tu duy logic"]),
    ]


# ----------------------------------------------------------------- kiểm tra điều kiện
class TestConditionChecker:
    WM = {
        "grade": 12,
        "scores.math": 8.5,
        "interests": ["lap trinh", "toan"],
        "stem": "high",
    }

    @pytest.mark.parametrize("c, expected", [
        (cond("scores.math", ">=", 8), True),
        (cond("scores.math", ">=", 9), False),
        (cond("scores.math", ">", 8.5), False),
        (cond("scores.math", "<=", 8.5), True),
        (cond("scores.math", "<", 9), True),
        (cond("grade", "=", 12), True),
        (cond("grade", "==", 12), True),
        (cond("grade", "!=", 11), True),
        (cond("grade", "in", [11, 12]), True),
        (cond("grade", "not_in", [10, 11]), True),
        (cond("grade", "not_in", [12]), False),
        (cond("interests", "contains", "Lap Trinh"), True),       # không phân biệt hoa thường
        (cond("interests", "contains", "ve"), False),
        (cond("interests", "intersects", ["ve", "toan"]), True),
        (cond("interests", "intersects", ["ve", "hat"]), False),
        (cond("stem", "==", "high"), True),
    ])
    def test_operators(self, c, expected):
        assert check_condition(c, self.WM) is expected

    def test_missing_fact_is_not_satisfied(self):
        assert check_condition(cond("scores.chemistry", ">=", 5), self.WM) is False
        assert check_condition(cond("scores.chemistry", "!=", 5), self.WM) is False

    def test_type_mismatch_is_not_satisfied(self):
        assert check_condition(cond("stem", ">=", 5), self.WM) is False

    def test_condition_list_is_and(self):
        ok = [cond("grade", "=", 12), cond("scores.math", ">=", 8)]
        bad = [cond("grade", "=", 12), cond("scores.math", ">=", 9)]
        assert check_condition(ok, self.WM) is True
        assert check_condition(bad, self.WM) is False

    def test_any_all_not(self):
        assert check_condition({"any": [cond("grade", "=", 10), cond("grade", "=", 12)]}, self.WM)
        assert not check_condition({"all": [cond("grade", "=", 10), cond("grade", "=", 12)]}, self.WM)
        assert check_condition({"not": cond("grade", "=", 10)}, self.WM)

    def test_accepts_list_of_facts(self, facts):
        assert check_condition(cond("scores.math", ">=", 8), facts)


# ----------------------------------------------------------------- suy diễn
class TestInference:
    def test_rule_fires_when_condition_met(self, facts):
        rules = [fact_rule("INT-01", [cond("scores.math", ">=", 8)], "stem", "high")]
        r = run_inference(rules, facts)
        assert r.fired_rules == ["INT-01"]
        assert r.derived_facts == {"stem": "high"}
        assert r.facts["stem"] == "high"
        assert r.stopped_reason == "fixed_point"

    def test_no_rule_fires(self, facts):
        rules = [fact_rule("INT-01", [cond("scores.math", ">=", 9.5)], "stem", "high")]
        r = run_inference(rules, facts)
        assert r.fired_rules == []
        assert r.derived_facts == {}
        assert r.recommendations == []
        assert r.iterations == 0

    def test_empty_ruleset(self, facts):
        r = run_inference([], facts)
        assert r.fired_rules == [] and r.iterations == 0

    def test_original_facts_are_kept(self, facts):
        r = run_inference([], facts)
        assert r.facts["grade"] == 12
        assert r.facts["scores.math"] == 8.5

    def test_multi_step_chain(self, facts):
        """INT-01 -> INT-02 -> GRP-01: mỗi luật dùng kết quả của luật trước."""
        rules = [
            # cố ý đặt ngược thứ tự để chứng minh engine không phụ thuộc thứ tự luật
            rec_rule("GRP-01", [cond("career_fit", "==", "strong")], "CNTT", ["SE", "AI"]),
            fact_rule("INT-02", [cond("stem", "==", "high"), cond("skills", "contains", "tu duy logic")],
                      "career_fit", "strong"),
            fact_rule("INT-01", [cond("scores.math", ">=", 8), cond("scores.physics", ">=", 7)],
                      "stem", "high"),
        ]
        r = run_inference(rules, facts)
        assert r.fired_rules == ["INT-01", "INT-02", "GRP-01"]
        assert r.derived_facts == {"stem": "high", "career_fit": "strong"}
        assert [x["career_group"] for x in r.recommendations] == ["CNTT"]
        assert r.iterations == 3

    def test_recommendation_is_not_written_to_working_memory(self, facts):
        rules = [rec_rule("GRP-01", [cond("grade", "=", 12)], "CNTT", ["SE"])]
        r = run_inference(rules, facts)
        rec = r.recommendations[0]
        assert rec["rule_id"] == "GRP-01"
        assert rec["careers"] == ["SE"]
        assert rec["confidence"] == 0.9 and rec["priority"] == 5
        assert "CNTT" not in r.facts.values()
        assert r.derived_facts == {}

    def test_missing_fact_does_not_fire_and_does_not_crash(self):
        rules = [rec_rule("GRP-01", [cond("scores.math", ">=", 8)], "CNTT")]
        r = run_inference(rules, [fact("grade", 12)])
        assert r.fired_rules == []

    def test_disabled_rule_is_skipped(self, facts):
        rules = [
            fact_rule("INT-01", [cond("grade", "=", 12)], "a", 1, enabled=False),
            fact_rule("INT-02", [cond("grade", "=", 12)], "b", 1),
        ]
        r = run_inference(rules, facts)
        assert r.fired_rules == ["INT-02"]
        assert "a" not in r.facts

    def test_each_rule_fires_at_most_once(self, facts):
        rules = [fact_rule("INT-01", [cond("grade", "=", 12)], "x", 1)]
        r = run_inference(rules, facts)
        assert r.fired_rules.count("INT-01") == 1

    def test_cyclic_rules_terminate(self, facts):
        """A -> B và B -> A: không được lặp vô hạn."""
        rules = [
            fact_rule("CYC-01", [cond("grade", "=", 12)], "a", 1),
            fact_rule("CYC-02", [cond("a", "==", 1)], "b", 1),
            fact_rule("CYC-03", [cond("b", "==", 1)], "a", 1),
        ]
        r = run_inference(rules, facts)
        assert sorted(r.fired_rules) == ["CYC-01", "CYC-02", "CYC-03"]
        assert r.stopped_reason == "fixed_point"

    def test_self_triggering_rule_terminates(self):
        rules = [fact_rule("LOOP-01", [cond("n", ">=", 0)], "n", 1)]
        r = run_inference(rules, [fact("n", 0)])
        assert r.fired_rules == ["LOOP-01"]

    def test_max_iterations_guard(self, facts):
        rules = [
            fact_rule("INT-01", [cond("grade", "=", 12)], "a", 1),
            fact_rule("INT-02", [cond("a", "==", 1)], "b", 1),
            fact_rule("INT-03", [cond("b", "==", 1)], "c", 1),
        ]
        r = run_inference(rules, facts, max_iterations=2)
        assert r.iterations == 2
        assert r.stopped_reason == "max_iterations"

    def test_duplicate_rule_id_raises(self):
        rules = [
            fact_rule("INT-01", [cond("grade", "=", 12)], "a", 1),
            fact_rule("INT-01", [cond("grade", "=", 12)], "b", 1),
        ]
        with pytest.raises(ValueError):
            ForwardChainingEngine(rules)

    def test_engine_is_reusable_and_does_not_mutate_input(self, facts):
        rules = [fact_rule("INT-01", [cond("grade", "=", 12)], "x", 1)]
        engine = ForwardChainingEngine(rules)
        r1, r2 = engine.run(facts), engine.run(facts)
        assert r1.fired_rules == r2.fired_rules == ["INT-01"]
        assert all(f["attribute"] != "x" for f in facts)      # facts gốc không bị sửa

    def test_accepts_dict_facts(self):
        rules = [fact_rule("INT-01", [cond("grade", "=", 12)], "x", 1)]
        assert run_inference(rules, {"grade": 12}).fired_rules == ["INT-01"]

    def test_accepts_object_with_to_dict(self, facts):
        """RuleManager.active_rules() trả về đối tượng Rule có to_dict()."""
        class FakeRule:
            def __init__(self, d): self._d = d
            def to_dict(self): return self._d
        rules = [FakeRule(fact_rule("INT-01", [cond("grade", "=", 12)], "x", 1))]
        assert run_inference(rules, facts).fired_rules == ["INT-01"]


# ----------------------------------------------------------------- chọn luật & trace
class TestOrderingAndTrace:
    def test_priority_decides_firing_order(self, facts):
        rules = [
            rec_rule("GRP-01", [cond("grade", "=", 12)], "A", priority=1),
            rec_rule("GRP-02", [cond("grade", "=", 12)], "B", priority=9),
            rec_rule("GRP-03", [cond("grade", "=", 12)], "C", priority=5),
        ]
        assert run_inference(rules, facts).fired_rules == ["GRP-02", "GRP-03", "GRP-01"]

    def test_confidence_breaks_priority_tie(self, facts):
        rules = [
            rec_rule("GRP-01", [cond("grade", "=", 12)], "A", priority=5, confidence=0.6),
            rec_rule("GRP-02", [cond("grade", "=", 12)], "B", priority=5, confidence=0.9),
        ]
        assert run_inference(rules, facts).fired_rules == ["GRP-02", "GRP-01"]

    def test_more_specific_rule_wins_when_priority_and_confidence_tie(self, facts):
        rules = [
            rec_rule("GRP-01", [cond("grade", "=", 12)], "A"),
            rec_rule("GRP-02", [cond("grade", "=", 12), cond("scores.math", ">=", 8)], "B"),
        ]
        assert run_inference(rules, facts).fired_rules == ["GRP-02", "GRP-01"]

    def test_custom_resolver(self, facts):
        rules = [
            rec_rule("GRP-01", [cond("grade", "=", 12)], "A"),
            rec_rule("GRP-02", [cond("grade", "=", 12)], "B"),
        ]
        last_id_first = lambda cands: sorted(cands, key=lambda r: r.id, reverse=True)[0]
        r = run_inference(rules, facts, resolver=last_id_first)
        assert r.fired_rules == ["GRP-02", "GRP-01"]

    def test_trace_records_each_step(self, facts):
        rules = [
            fact_rule("INT-01", [cond("scores.math", ">=", 8)], "stem", "high",
                      description="Toan tot nen co nang luc STEM"),
            rec_rule("GRP-01", [cond("stem", "==", "high")], "CNTT", ["SE"]),
            rec_rule("GRP-02", [cond("grade", "=", 12)], "KT", priority=1),
        ]
        r = run_inference(rules, facts)
        assert [s.step for s in r.trace] == [1, 2, 3]
        first = r.trace[0]
        assert first.rule_id == "INT-01"
        assert first.new_facts == {"stem": "high"}
        assert set(first.conflict_set) == {"INT-01", "GRP-02"}      # cùng kích hoạt ở chu kỳ 1
        assert first.explanation == "Toan tot nen co nang luc STEM"
        assert r.trace[1].rule_id == "GRP-01"
        assert r.trace[1].recommendations[0]["career_group"] == "CNTT"

    def test_trace_records_overwritten_fact(self):
        rules = [
            fact_rule("INT-01", [cond("x", "=", 1)], "level", "low", priority=9),
            fact_rule("INT-02", [cond("level", "==", "low")], "level", "high", priority=5),
        ]
        r = run_inference(rules, [fact("x", 1)])
        assert r.facts["level"] == "high"
        assert r.trace[1].updated_facts == {"level": ("low", "high")}

    def test_to_dict_is_serializable(self, facts):
        import json
        rules = [rec_rule("GRP-01", [cond("grade", "=", 12)], "CNTT", ["SE"])]
        data = run_inference(rules, facts).to_dict()
        json.dumps(data, default=str)
        assert data["fired_rules"] == ["GRP-01"]
