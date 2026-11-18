"""Integration test tích hợp toàn diện từ Facts -> Inference -> Ranking -> Explanation."""
from app.expert_system.facts.student_facts import student_to_facts
from app.expert_system.knowledge_base.rule_manager import RuleManager
from app.expert_system.inference.inference_engine import ForwardChainingEngine
from app.expert_system.explanation.explanation_generator import ExplanationGenerator
from app.services.consultation_service import ConsultationService


def test_end_to_end_consultation_flow():
    payload = {
        "student": {
            "fullName": "Trần Thị B",
            "grade": "12",
            "school": "THPT Marie Curie",
            "region": "south",
            "track": "khoa_hoc_tu_nhien"
        },
        "scores": {
            "math": 8.5,
            "biology": 9.0,
            "chemistry": 9.0,
            "physics": 7.0,
            "literature": 7.0,
            "english": 7.5,
            "informatics": 7.0,
            "history": 6.5
        },
        "riasec": {
            "R": 50,
            "I": 85,
            "A": 40,
            "S": 80,
            "E": 60,
            "C": 70
        },
        "preferences": {
            "environment": "medical",
            "tuition": "standard",
            "priority": "stability"
        }
    }

    service = ConsultationService()
    result = service.evaluate(payload)

    assert result["consultationId"].startswith("CONS-")
    assert len(result["recommendations"]) > 0

    top_rec = result["recommendations"][0]
    assert top_rec["career"]["category_id"] == "YDUOC"
    assert top_rec["career"]["id"] == "medical_doctor"
    assert "explanationSummary" in result
    assert result["explanationSummary"]["total_rules_fired"] > 0
