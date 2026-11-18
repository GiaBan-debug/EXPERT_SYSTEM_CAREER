"""Repository thao tác với bảng Students."""
import sqlite3
import uuid
from typing import List, Optional
from app.database.db import get_db_connection
from app.models.student import Student


class StudentRepository:
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        self._conn = conn

    def _get_conn(self) -> sqlite3.Connection:
        return self._conn or get_db_connection()

    def create(self, student: Student) -> Student:
        conn = self._get_conn()
        if not student.id:
            student.id = str(uuid.uuid4())
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO students (id, full_name, grade, school, region, track)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (student.id, student.full_name, student.grade, student.school, student.region, student.track)
        )
        conn.commit()
        return student

    def get_by_id(self, student_id: str) -> Optional[Student]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        if row:
            return Student(
                id=row["id"],
                full_name=row["full_name"],
                grade=row["grade"],
                school=row["school"],
                region=row["region"],
                track=row["track"],
            )
        return None
