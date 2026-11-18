"""Repository lưu trữ và truy vấn lịch sử tư vấn (Consultations)."""
import json
import sqlite3
import uuid
from typing import Any, Dict, List, Optional
from app.database.db import get_db_connection


class ConsultationRepository:
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        self._conn = conn

    def _get_conn(self) -> sqlite3.Connection:
        return self._conn or get_db_connection()

    def save(self, data: Dict[str, Any]) -> str:
        conn = self._get_conn()
        cursor = conn.cursor()
        cid = data.get("consultationId") or str(uuid.uuid4())
        student_id = data.get("student", {}).get("id")

        cursor.execute(
            """
            INSERT INTO consultations (
                id, student_id, dominant_code, scores_json, riasec_json, 
                preferences_json, recommendations_json, explanation_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cid,
                student_id,
                data.get("dominantCode", ""),
                json.dumps(data.get("academicScores", {}), ensure_ascii=False),
                json.dumps(data.get("riasecScores", {}), ensure_ascii=False),
                json.dumps(data.get("preferences", {}), ensure_ascii=False),
                json.dumps(data.get("recommendations", []), ensure_ascii=False),
                json.dumps(data.get("explanationSummary", {}), ensure_ascii=False),
            )
        )
        conn.commit()
        return cid

    def get_all(self, limit: int = 50) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.*, s.full_name as student_name 
            FROM consultations c
            LEFT JOIN students s ON c.student_id = s.id
            ORDER BY c.created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        results = []
        for r in rows:
            recs = json.loads(r["recommendations_json"]) if r["recommendations_json"] else []
            top_career = recs[0].get("career", {}).get("name", "N/A") if recs else "N/A"
            match_rate = recs[0].get("matchScore", 0) if recs else 0
            results.append({
                "id": r["id"],
                "studentName": r["student_name"] or "Học sinh THPT",
                "dominantCode": r["dominant_code"],
                "targetCareer": top_career,
                "matchRate": match_rate,
                "createdAt": r["created_at"],
                "recommendations": recs,
            })
        return results

    def get_by_id(self, cid: str) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultations WHERE id = ?", (cid,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "dominantCode": row["dominant_code"],
            "scores": json.loads(row["scores_json"]) if row["scores_json"] else {},
            "riasec": json.loads(row["riasec_json"]) if row["riasec_json"] else {},
            "preferences": json.loads(row["preferences_json"]) if row["preferences_json"] else {},
            "recommendations": json.loads(row["recommendations_json"]) if row["recommendations_json"] else [],
            "explanationSummary": json.loads(row["explanation_json"]) if row["explanation_json"] else {},
            "createdAt": row["created_at"],
        }
