"""Unit test cho Conflict Resolution (Thành viên 4)."""
from app.expert_system.conflict_resolution.conflict_detector import ConflictDetector
from app.expert_system.conflict_resolution.conflict_resolver import ConflictResolver
from app.expert_system.conflict_resolution.ranking_engine import RankingEngine


def test_conflict_detection():
    rules = [
        {"id": "R1", "conclusion": "CNTT", "confidence": 0.85, "priority": 5},
        {"id": "R2", "conclusion": "CNTT", "confidence": 0.95, "priority": 6},
        {"id": "R3", "conclusion": "YDUOC", "confidence": 0.80, "priority": 4},
    ]
    detector = ConflictDetector(rules)
    conflicts = detector.detect_conflicts()

    assert "CNTT" in conflicts
    assert len(conflicts["CNTT"]) == 2
    assert "YDUOC" in conflicts
    assert len(conflicts["YDUOC"]) == 1


def test_conflict_resolver():
    conflict_groups = {
        "CNTT": [
            {"id": "R1", "conclusion": "CNTT", "confidence": 0.85, "priority": 5},
            {"id": "R2", "conclusion": "CNTT", "confidence": 0.95, "priority": 6},
        ]
    }
    resolver = ConflictResolver(conflict_groups)
    resolved = resolver.resolve()

    assert len(resolved) == 1
    assert resolved[0]["id"] == "R2"


def test_ranking_engine():
    resolved_rules = [
        {"id": "R1", "conclusion": "CNTT", "confidence": 0.95, "priority": 6},
        {"id": "R2", "conclusion": "YDUOC", "confidence": 0.80, "priority": 4},
    ]
    ranking = RankingEngine(resolved_rules)
    ranked = ranking.rank_careers()

    assert len(ranked) == 2
    assert ranked[0]["rank"] == 1
    assert ranked[0]["career"] == "CNTT"
    assert ranked[1]["rank"] == 2
    assert ranked[1]["career"] == "YDUOC"
