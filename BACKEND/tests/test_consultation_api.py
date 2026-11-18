"""Unit test cho Consultation API (FastAPI TestClient)."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_check_api():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_careers_api():
    response = client.get("/api/careers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_evaluate_consultation_api():
    payload = {
        "student": {
            "fullName": "Nguyễn Minh Quân",
            "grade": "12",
            "school": "THPT Chuyên Lê Hồng Phong",
            "region": "south",
            "track": "khoa_hoc_tu_nhien"
        },
        "scores": {
            "math": 9.0,
            "physics": 8.5,
            "chemistry": 7.5,
            "biology": 7.0,
            "literature": 7.5,
            "english": 8.5,
            "informatics": 9.5,
            "history": 6.5
        },
        "riasec": {
            "R": 80,
            "I": 100,
            "A": 60,
            "S": 70,
            "E": 65,
            "C": 85
        },
        "preferences": {
            "environment": "tech",
            "tuition": "standard",
            "priority": "high_salary"
        }
    }
    response = client.post("/api/consultations/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "consultationId" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["career"]["category_id"] == "CNTT"
