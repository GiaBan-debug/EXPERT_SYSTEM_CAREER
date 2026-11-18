"""Khởi tạo module Hệ chuyên gia."""
from app.expert_system.facts import Fact, student_to_facts, student_to_fact_dicts
from app.expert_system.knowledge_base.rule_manager import RuleManager
from app.expert_system.inference.inference_engine import ForwardChainingEngine, run_inference
from app.expert_system.conflict_resolution.conflict_detector import ConflictDetector
from app.expert_system.conflict_resolution.conflict_resolver import ConflictResolver
from app.expert_system.conflict_resolution.ranking_engine import RankingEngine
from app.expert_system.explanation.explanation_generator import ExplanationGenerator

__all__ = [
    "Fact",
    "student_to_facts",
    "student_to_fact_dicts",
    "RuleManager",
    "ForwardChainingEngine",
    "run_inference",
    "ConflictDetector",
    "ConflictResolver",
    "RankingEngine",
    "ExplanationGenerator",
]
