"""Unit test cho Knowledge Base (Thành viên 2). Chạy: cd BACKEND && python -m pytest tests/test_knowledge_base.py -v"""
import copy
import json

import pytest

from app.expert_system.knowledge_base import (
    FactConventions, RuleLoadError, RuleLoader, RuleManager, RuleNotFoundError,
    RuleValidationError, RuleValidator,
)
from app.expert_system.knowledge_base.fact_conventions import ConventionsError
from app.models.rule import Rule


def make_rule(**over):
    """Một luật hợp lệ mẫu; ghi đè trường bằng over."""
    base = {
        "id": "TST-01",
        "name": "Luật kiểm thử",
        "conditions": [{"attribute": "score.math", "operator": ">=", "value": 8}],
        "conclusion": {"type": "fact", "attribute": "ability.logic", "value": "high"},
        "priority": 5,
        "confidence": 0.9,
    }
    base.update(over)
    return base


@pytest.fixture(scope="module")
def validator():
    return RuleValidator()


def errors_of(validator, rule):
    return [str(i) for i in validator.validate_rule(rule)]


# ----------------------------------------------------------------- bộ luật thật
class TestRealRuleBase:
    def test_loads_without_errors(self):
        report = RuleLoader().load_from_file(min_rules=25)
        assert report.ok, [str(e) for e in report.errors]
        assert report.warnings == []

    def test_at_least_25_rules(self):
        assert len(RuleLoader().load_from_file().rules) >= 25

    def test_every_rule_has_priority_and_confidence(self):
        for r in RuleLoader().load_from_file().rules:
            assert 1 <= r.priority <= 10
            assert 0 < r.confidence <= 1
            assert r.conditions and r.name

    def test_ids_unique(self):
        ids = [r.id for r in RuleLoader().load_from_file().rules]
        assert len(ids) == len(set(ids))

    def test_covers_all_career_groups(self):
        mgr = RuleManager.from_file()
        conv = FactConventions.from_file()
        for group in conv.career_groups:
            assert mgr.find_by_conclusion_group(group), f"Chưa có luật cho nhóm {group}"

    def test_has_both_fact_and_recommendation_rules(self):
        s = RuleManager.from_file().stats()
        assert s["fact_rules"] > 0 and s["recommendation_rules"] > 0

    def test_strict_mode_ok_on_real_file(self):
        RuleLoader().load_from_file(strict=True, min_rules=25)  # không raise


# ----------------------------------------------------------------- validator: cấu trúc
class TestValidatorStructure:
    def test_valid_rule_passes(self, validator):
        assert validator.validate_rule(make_rule()) == []

    @pytest.mark.parametrize("missing", ["id", "name", "conditions", "conclusion", "priority", "confidence"])
    def test_missing_required_field(self, validator, missing):
        rule = make_rule()
        del rule[missing]
        assert any(missing in e and "Thiếu" in e for e in errors_of(validator, rule))

    def test_unknown_field_rejected(self, validator):
        assert any("xyz" in e for e in errors_of(validator, make_rule(xyz=1)))

    def test_not_a_dict(self, validator):
        assert validator.validate_rule("không phải object")

    @pytest.mark.parametrize("bad_id", ["abc", "GRP1", "grp-01", "", 5])
    def test_bad_id_format(self, validator, bad_id):
        assert any("id" in e for e in errors_of(validator, make_rule(id=bad_id)))

    def test_empty_conditions(self, validator):
        assert any("conditions" in e for e in errors_of(validator, make_rule(conditions=[])))

    def test_enabled_must_be_bool(self, validator):
        assert any("enabled" in e for e in errors_of(validator, make_rule(enabled="yes")))

    @pytest.mark.parametrize("p", [0, 11, 5.5, "5", True])
    def test_bad_priority(self, validator, p):
        assert any("priority" in e for e in errors_of(validator, make_rule(priority=p)))

    @pytest.mark.parametrize("c", [0, 0.0, 1.5, -0.1, "0.9", None])
    def test_bad_confidence(self, validator, c):
        assert any("confidence" in e for e in errors_of(validator, make_rule(confidence=c)))

    def test_confidence_one_is_allowed(self, validator):
        assert validator.validate_rule(make_rule(confidence=1)) == []


# ----------------------------------------------------------------- validator: điều kiện
class TestValidatorConditions:
    def cond(self, a, o, v):
        return make_rule(conditions=[{"attribute": a, "operator": o, "value": v}])

    def test_unknown_attribute(self, validator):
        assert any("không có trong bảng quy ước" in e for e in errors_of(validator, self.cond("score.art", ">=", 5)))

    def test_bad_operator_for_number(self, validator):
        assert any("Toán tử" in e for e in errors_of(validator, self.cond("score.math", "in", [1, 2])))

    def test_bad_operator_for_enum(self, validator):
        assert any("Toán tử" in e for e in errors_of(validator, self.cond("pref.environment", ">", "tech")))

    @pytest.mark.parametrize("v", [0, 10.5, 11])
    def test_score_out_of_range(self, validator, v):
        assert any("ngoài miền" in e for e in errors_of(validator, self.cond("score.math", ">=", v)))

    def test_riasec_out_of_range(self, validator):
        assert any("ngoài miền" in e for e in errors_of(validator, self.cond("riasec.I", ">=", 101)))

    def test_number_value_must_be_number(self, validator):
        assert any("phải là số" in e for e in errors_of(validator, self.cond("score.math", ">=", "8")))

    def test_bool_is_not_a_number(self, validator):
        assert errors_of(validator, self.cond("score.math", ">=", True))

    def test_enum_value_out_of_domain(self, validator):
        assert any("ngoài miền" in e for e in errors_of(validator, self.cond("pref.environment", "==", "space")))

    def test_in_requires_nonempty_list(self, validator):
        assert errors_of(validator, self.cond("ability.logic", "in", "high"))
        assert errors_of(validator, self.cond("ability.logic", "in", []))

    def test_in_with_valid_list(self, validator):
        assert validator.validate_rule(self.cond("ability.logic", "in", ["medium", "high"])) == []

    def test_in_with_duplicates(self, validator):
        assert errors_of(validator, self.cond("ability.logic", "in", ["high", "high"]))

    def test_condition_missing_key(self, validator):
        assert errors_of(validator, make_rule(conditions=[{"attribute": "score.math", "operator": ">="}]))

    def test_contradictory_numeric_range(self, validator):
        conds = [{"attribute": "score.math", "operator": ">=", "value": 8},
                 {"attribute": "score.math", "operator": "<", "value": 5}]
        assert any("mâu thuẫn" in e for e in errors_of(validator, make_rule(conditions=conds)))

    def test_contradictory_strict_boundary(self, validator):
        conds = [{"attribute": "score.math", "operator": ">", "value": 8},
                 {"attribute": "score.math", "operator": "<=", "value": 8}]
        assert any("mâu thuẫn" in e for e in errors_of(validator, make_rule(conditions=conds)))

    def test_contradictory_enum(self, validator):
        conds = [{"attribute": "pref.environment", "operator": "==", "value": "tech"},
                 {"attribute": "pref.environment", "operator": "==", "value": "medical"}]
        assert any("mâu thuẫn" in e for e in errors_of(validator, make_rule(conditions=conds)))

    def test_valid_range_on_same_attribute(self, validator):
        conds = [{"attribute": "score.math", "operator": ">=", "value": 5},
                 {"attribute": "score.math", "operator": "<", "value": 8}]
        assert validator.validate_rule(make_rule(conditions=conds)) == []


# ----------------------------------------------------------------- validator: kết luận
class TestValidatorConclusion:
    def test_cannot_conclude_input_fact(self, validator):
        concl = {"type": "fact", "attribute": "score.math", "value": 9}
        assert any("dữ kiện đầu vào" in e for e in errors_of(validator, make_rule(conclusion=concl)))

    def test_fact_value_out_of_domain(self, validator):
        concl = {"type": "fact", "attribute": "ability.logic", "value": "super"}
        assert errors_of(validator, make_rule(conclusion=concl))

    def test_unknown_conclusion_type(self, validator):
        assert errors_of(validator, make_rule(conclusion={"type": "magic"}))

    def test_recommendation_ok(self, validator):
        concl = {"type": "recommendation", "career_group": "CNTT", "careers": ["it_software"]}
        assert validator.validate_rule(make_rule(conclusion=concl)) == []

    def test_unknown_group(self, validator):
        concl = {"type": "recommendation", "career_group": "XYZ"}
        assert any("Nhóm ngành" in e for e in errors_of(validator, make_rule(conclusion=concl)))

    def test_unknown_career(self, validator):
        concl = {"type": "recommendation", "career_group": "CNTT", "careers": ["astronaut"]}
        assert errors_of(validator, make_rule(conclusion=concl))

    def test_career_not_in_group(self, validator):
        concl = {"type": "recommendation", "career_group": "CNTT", "careers": ["medical_doctor"]}
        assert any("không thuộc" in e for e in errors_of(validator, make_rule(conclusion=concl)))

    def test_fact_conclusion_with_extra_field(self, validator):
        concl = {"type": "fact", "attribute": "ability.logic", "value": "high", "career_group": "CNTT"}
        assert errors_of(validator, make_rule(conclusion=concl))


# ----------------------------------------------------------------- validator: cả tập luật
class TestValidatorRuleset:
    def test_duplicate_id_rejected_first_kept(self, validator):
        a = make_rule()
        b = make_rule(name="khác", conclusion={"type": "fact", "attribute": "ability.logic", "value": "low"},
                      conditions=[{"attribute": "score.math", "operator": "<", "value": 5}])
        res = validator.validate_ruleset([a, b])
        assert res.valid_indices == [0]
        assert any("Trùng mã" in str(e) for e in res.errors)

    def test_duplicate_content_rejected(self, validator):
        a = make_rule(id="TST-01")
        b = make_rule(id="TST-02")  # cùng điều kiện + kết luận
        res = validator.validate_ruleset([a, b])
        assert res.valid_indices == [0]
        assert any("Trùng nội dung" in str(e) for e in res.errors)

    def test_duplicate_content_ignores_condition_order(self, validator):
        c1 = {"attribute": "score.math", "operator": ">=", "value": 8}
        c2 = {"attribute": "score.physics", "operator": ">=", "value": 8}
        a = make_rule(id="TST-01", conditions=[c1, c2])
        b = make_rule(id="TST-02", conditions=[c2, c1])
        assert validator.validate_ruleset([a, b]).valid_indices == [0]

    def test_min_rules_enforced(self, validator):
        res = validator.validate_ruleset([make_rule()], min_rules=25)
        assert any("tối thiểu 25" in str(e) for e in res.errors)

    def test_unreachable_derived_condition_warns(self, validator):
        needs = make_rule(id="GRP-01",
                          conditions=[{"attribute": "ability.logic", "operator": "==", "value": "high"}],
                          conclusion={"type": "recommendation", "career_group": "CNTT"})
        res = validator.validate_ruleset([needs])  # không luật nào sinh ability.logic
        assert res.valid_indices == [0]
        assert len(res.warnings) == 1 and res.warnings[0].severity == "warning"

    def test_reachable_derived_condition_no_warning(self, validator):
        produce = make_rule(id="ABL-01")
        needs = make_rule(id="GRP-01",
                          conditions=[{"attribute": "ability.logic", "operator": "==", "value": "high"}],
                          conclusion={"type": "recommendation", "career_group": "CNTT"})
        assert validator.validate_ruleset([produce, needs]).warnings == []

    def test_disabled_producer_does_not_count(self, validator):
        produce = make_rule(id="ABL-01", enabled=False)
        needs = make_rule(id="GRP-01",
                          conditions=[{"attribute": "ability.logic", "operator": "==", "value": "high"}],
                          conclusion={"type": "recommendation", "career_group": "CNTT"})
        assert len(validator.validate_ruleset([produce, needs]).warnings) == 1


# ----------------------------------------------------------------- loader
class TestLoader:
    def test_invalid_rules_rejected_valid_loaded(self):
        data = {"rules": [make_rule(id="TST-01"), make_rule(id="bad"), make_rule(id="TST-03", priority=99)]}
        report = RuleLoader().load_from_data(data)
        assert [r.id for r in report.rules] == ["TST-01"]
        assert report.total == 3 and len(report.errors) == 2 and not report.ok

    def test_strict_raises_with_issues(self):
        with pytest.raises(RuleLoadError) as exc:
            RuleLoader().load_from_data([make_rule(id="bad")], strict=True)
        assert exc.value.issues

    def test_accepts_bare_list(self):
        assert len(RuleLoader().load_from_data([make_rule()]).rules) == 1

    def test_rejects_non_list_payload(self):
        with pytest.raises(RuleLoadError):
            RuleLoader().load_from_data({"rules": "nope"})

    def test_file_not_found(self, tmp_path):
        with pytest.raises(RuleLoadError, match="Không tìm thấy"):
            RuleLoader().load_from_file(tmp_path / "none.json")

    def test_invalid_json(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{ not json", encoding="utf-8")
        with pytest.raises(RuleLoadError, match="JSON"):
            RuleLoader().load_from_file(p)

    def test_loaded_rule_fields(self):
        rule = RuleLoader().load_from_data([make_rule(enabled=False)]).rules[0]
        assert isinstance(rule, Rule) and rule.enabled is False
        assert rule.conditions[0].attribute == "score.math"


# ----------------------------------------------------------------- conventions
class TestConventions:
    def test_missing_keys(self):
        with pytest.raises(ConventionsError):
            FactConventions({})

    def test_missing_file(self, tmp_path):
        with pytest.raises(ConventionsError):
            FactConventions.from_file(tmp_path / "x.json")

    def test_input_vs_derived(self):
        conv = FactConventions.from_file()
        assert not conv.is_derived("score.math") and conv.is_derived("ability.logic")

    def test_every_career_maps_to_known_group(self):
        conv = FactConventions.from_file()
        assert set(conv.careers.values()) <= set(conv.career_groups)


# ----------------------------------------------------------------- manager
@pytest.fixture
def mgr():
    return RuleManager.from_file()


class TestManager:
    def test_get_and_missing(self, mgr):
        assert mgr.get("ABL-01").id == "ABL-01"
        with pytest.raises(RuleNotFoundError):
            mgr.get("NOPE-99")

    def test_disable_and_enable(self, mgr):
        n = len(mgr.active_rules())
        mgr.disable_rule("GRP-01")
        assert len(mgr.active_rules()) == n - 1 and "GRP-01" in mgr
        mgr.enable_rule("GRP-01")
        assert len(mgr.active_rules()) == n

    def test_add_valid_rule(self, mgr):
        n = len(mgr)
        mgr.add_rule(make_rule(id="TST-01", conditions=[{"attribute": "score.math", "operator": ">=", "value": 9.5}]))
        assert len(mgr) == n + 1

    def test_add_duplicate_id_rejected_and_unchanged(self, mgr):
        n = len(mgr)
        with pytest.raises(RuleValidationError):
            mgr.add_rule(make_rule(id="ABL-01"))
        assert len(mgr) == n

    def test_add_duplicate_content_rejected(self, mgr):
        dup = mgr.get("ABL-01").to_dict()
        dup["id"] = "TST-09"
        with pytest.raises(RuleValidationError, match="Trùng nội dung"):
            mgr.add_rule(dup)

    def test_add_invalid_rejected(self, mgr):
        with pytest.raises(RuleValidationError):
            mgr.add_rule(make_rule(id="TST-01", priority=0))

    def test_update_priority_and_confidence(self, mgr):
        mgr.update_rule("GRP-01", {"priority": 10, "confidence": 0.99})
        r = mgr.get("GRP-01")
        assert r.priority == 10 and r.confidence == 0.99

    def test_update_invalid_leaves_rule_untouched(self, mgr):
        before = mgr.get("GRP-01").to_dict()
        with pytest.raises(RuleValidationError):
            mgr.update_rule("GRP-01", {"confidence": 5})
        assert mgr.get("GRP-01").to_dict() == before

    def test_update_cannot_change_id(self, mgr):
        with pytest.raises(RuleValidationError):
            mgr.update_rule("GRP-01", {"id": "GRP-99"})

    def test_update_unknown_rule(self, mgr):
        with pytest.raises(RuleNotFoundError):
            mgr.update_rule("NOPE-99", {"priority": 3})

    def test_update_to_duplicate_content_rejected(self, mgr):
        other = mgr.get("ABL-02")
        with pytest.raises(RuleValidationError, match="Trùng nội dung"):
            mgr.update_rule("ABL-01", {"conditions": [c.to_dict() for c in other.conditions]})

    def test_remove(self, mgr):
        mgr.remove_rule("GRP-20")
        assert "GRP-20" not in mgr

    def test_validate_all_warns_when_producer_removed(self, mgr):
        for rid in ("ABL-01", "ABL-02"):
            mgr.disable_rule(rid)
        assert any("ability.logic" in w.message for w in mgr.validate_all().warnings)

    def test_stats(self, mgr):
        s = mgr.stats()
        assert s["total"] == s["fact_rules"] + s["recommendation_rules"]
        assert sum(s["by_group"].values()) == s["recommendation_rules"]

    def test_save_roundtrip(self, mgr, tmp_path):
        mgr.disable_rule("GRP-02")
        mgr.update_rule("GRP-03", {"priority": 8})
        path = mgr.save(tmp_path / "out.json")
        again = RuleManager.from_file(path, strict=True)
        assert [r.to_dict() for r in again.all_rules()] == mgr.to_dicts()
        assert again.get("GRP-02").enabled is False and again.get("GRP-03").priority == 8

    def test_saved_file_is_utf8_readable_json(self, mgr, tmp_path):
        path = mgr.save(tmp_path / "out.json")
        assert "Tư duy logic" in path.read_text(encoding="utf-8")
        assert json.loads(path.read_text(encoding="utf-8"))["rules"]

    def test_rule_dict_roundtrip(self):
        original = make_rule(description="d", category="c", enabled=False)
        assert Rule.from_dict(original).to_dict() == {**original}

    def test_manager_does_not_share_input_dict(self, mgr):
        data = make_rule(id="TST-05", conditions=[{"attribute": "score.math", "operator": ">=", "value": 9.9}])
        snapshot = copy.deepcopy(data)
        mgr.add_rule(data)
        mgr.update_rule("TST-05", {"priority": 2})
        assert data == snapshot


# ----------------------------------------------------------------- tương thích Thành viên 4
class TestActivationDict:
    def test_recommendation_flat_conclusion_is_hashable_string(self):
        d = RuleManager.from_file().get("GRP-01").to_activation_dict()
        assert d["conclusion"] == "CNTT" and d["priority"] == 9 and d["confidence"] == 0.95
        hash(d["conclusion"])

    def test_fact_flat_conclusion(self):
        d = RuleManager.from_file().get("ABL-01").to_activation_dict()
        assert d["conclusion"] == "ability.logic=high" and d["conclusion_type"] == "fact"

    def test_works_with_conflict_detector(self):
        from app.expert_system.conflict_resolution import ConflictDetector
        rules = [r.to_activation_dict() for r in RuleManager.from_file().active_rules()
                 if r.id in ("GRP-01", "GRP-02", "GRP-16")]
        groups = ConflictDetector(rules).detect_conflicts()
        assert set(groups) == {"CNTT", "KYTHUAT"} and len(groups["CNTT"]) == 2
