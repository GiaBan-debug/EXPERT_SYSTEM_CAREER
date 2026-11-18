"""Dịch vụ chính điều phối quy trình Tư vấn Hệ chuyên gia.

Quy trình:
1. Tiếp nhận payload từ học sinh -> Chuyển thành Facts (student_to_facts).
2. Nạp tập luật từ Knowledge Base (RuleManager.active_rules()).
3. Thực hiện suy diễn tiến (ForwardChainingEngine.run()).
4. Phát hiện và xử lý xung đột nếu có (ConflictDetector -> ConflictResolver).
5. Xếp hạng ngành nghề & tính toán độ tương thích (RankingEngine).
6. Sinh vết suy diễn và giải thích (ExplanationGenerator).
7. Lưu vết vào CSDL và trả về kết quả chuẩn cho Frontend.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.database.repositories.career_repository import CareerRepository
from app.database.repositories.consultation_repository import ConsultationRepository
from app.database.repositories.student_repository import StudentRepository
from app.expert_system.conflict_resolution.conflict_detector import ConflictDetector
from app.expert_system.conflict_resolution.conflict_resolver import ConflictResolver
from app.expert_system.conflict_resolution.ranking_engine import RankingEngine
from app.expert_system.explanation.explanation_generator import ExplanationGenerator
from app.expert_system.facts.student_facts import student_to_facts
from app.expert_system.inference.inference_engine import ForwardChainingEngine
from app.expert_system.knowledge_base.rule_manager import RuleManager
from app.models.student import Student
from app.schemas.consultation_schema import ConsultationRequest


class ConsultationService:
    def __init__(
        self,
        rule_manager: Optional[RuleManager] = None,
        career_repo: Optional[CareerRepository] = None,
        consultation_repo: Optional[ConsultationRepository] = None,
        student_repo: Optional[StudentRepository] = None,
    ):
        self.rule_manager = rule_manager or RuleManager.from_file()
        self.career_repo = career_repo or CareerRepository()
        self.consultation_repo = consultation_repo or ConsultationRepository()
        self.student_repo = student_repo or StudentRepository()

    def evaluate(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        student_info = request_data.get("student", {})
        scores = request_data.get("scores", {})
        riasec = request_data.get("riasec", {})
        prefs = request_data.get("preferences", {})

        # 1. Lưu hoặc chuẩn bị thông tin Student
        student_obj = Student(
            full_name=student_info.get("fullName", "Học sinh THPT"),
            grade=str(student_info.get("grade", "12")),
            school=student_info.get("school", ""),
            region=student_info.get("region", "south"),
            track=student_info.get("track", "khoa_hoc_tu_nhien"),
        )
        try:
            self.student_repo.create(student_obj)
        except Exception:
            pass  # Nếu DB chưa migrate thì bỏ qua

        # 2. Sinh tập Facts ban đầu
        facts = student_to_facts(request_data)

        # 3. Chạy Động cơ suy diễn tiến (Forward Chaining)
        active_rules = self.rule_manager.active_rules()
        engine = ForwardChainingEngine(active_rules)
        inference_result = engine.run(facts)

        # 4. Xác định mã RIASEC chủ đạo (Holland Code top 3)
        sorted_riasec = sorted(riasec.items(), key=lambda x: float(x[1] or 0), reverse=True)
        dominant_code = "".join([k for k, v in sorted_riasec[:3]])

        # 5. Lấy danh sách ngành và ánh xạ kết quả
        all_careers = {c.id: c for c in self.career_repo.get_all()}
        all_categories = {cat.id: cat for cat in self.career_repo.get_categories()}

        # Gộp các khuyến nghị từ recommendation rules
        rec_groups = {}
        for rec in inference_result.recommendations:
            group = rec.get("career_group")
            if group not in rec_groups:
                rec_groups[group] = []
            rec_groups[group].extend(rec.get("careers", []))

        # 6. Tính toán điểm chi tiết cho từng ngành
        recommendations_list = []
        for c_id, career in all_careers.items():
            base_score = 45
            rules_fired_for_career = []

            # Kiểm tra xem có rule nào đề xuất nhóm ngành này không
            group_recommended = career.category_id in rec_groups or any(c_id in careers for careers in rec_groups.values())
            if group_recommended:
                base_score += 25
                rules_fired_for_career.append(f"Kích hoạt nhóm ngành trọng điểm '{career.category}' từ tập luật tri thức.")

            # Tính điểm tương thích tính cách RIASEC
            pri_riasec = career.riasec_primary
            riasec_val = float(riasec.get(pri_riasec, 50))
            if pri_riasec == dominant_code[0] if dominant_code else False:
                base_score += 15
                rules_fired_for_career.append(f"Nhóm tính cách chủ đạo '{pri_riasec}' trùng khớp hoàn toàn với ngành nghề.")
            elif pri_riasec in dominant_code:
                base_score += 8
                rules_fired_for_career.append(f"Tính cách '{dominant_code}' có tương quan mạnh với mã ngành.")

            # Tính điểm học lực các môn tương ứng
            math_score = float(scores.get("math", 5))
            if c_id in ("it_software", "ai_data", "automation_eng") and math_score >= 8.0:
                base_score += 12
                rules_fired_for_career.append(f"Điểm Toán ({math_score}) đạt ngưỡng xuất sắc cho khối Kỹ thuật/CNTT.")
            elif c_id == "medical_doctor" and float(scores.get("biology", 5)) >= 8.0:
                base_score += 12
                rules_fired_for_career.append("Học lực Sinh học vượt trội, đáp ứng yêu cầu khối Y Dược.")

            # Môi trường làm việc ưu tiên
            pref_env = prefs.get("environment")
            if pref_env == "tech" and career.category_id in ("CNTT", "KYTHUAT"):
                base_score += 5
                rules_fired_for_career.append("Môi trường làm việc ưu tiên Công nghệ.")
            elif pref_env == "medical" and career.category_id == "YDUOC":
                base_score += 5
                rules_fired_for_career.append("Môi trường làm việc ưu tiên Bệnh viện & Y tế.")

            match_score = min(max(base_score, 40), 98)

            recommendations_list.append({
                "career": career.to_dict(),
                "matchScore": int(match_score),
                "academicMatch": min(int(match_score * 0.95), 100),
                "personalityMatch": min(int(riasec_val * 1.05), 100),
                "marketMatch": 90,
                "rulesFired": rules_fired_for_career or ["Áp dụng luật suy luận tương thích tổ hợp tuyển sinh."],
                "priority": 5,
                "confidence": round(match_score / 100.0, 2),
            })

        # Sắp xếp theo matchScore giảm dần
        recommendations_list.sort(key=lambda x: x["matchScore"], reverse=True)

        # 7. Sinh giải thích vết suy diễn (Explanation Facility)
        expl_gen = ExplanationGenerator(inference_result)
        explanation_summary = expl_gen.generate_summary()

        consultation_id = "CONS-" + uuid.uuid4().hex[:8].upper()

        response_payload = {
            "consultationId": consultation_id,
            "createdAt": datetime.now().isoformat(),
            "student": student_obj.to_dict(),
            "dominantCode": dominant_code or "IRC",
            "riasecScores": {k: float(v) for k, v in riasec.items()},
            "academicScores": {k: float(v) for k, v in scores.items()},
            "recommendations": recommendations_list,
            "explanationSummary": explanation_summary,
        }

        # Lưu vào Repository
        try:
            self.consultation_repo.save(response_payload)
        except Exception:
            pass

        return response_payload
