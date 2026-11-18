"""Unit test cho Admin API Routes."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_admin_stats():
    res = client.get("/api/admin/stats")
    assert res.status_code == 200
    data = res.json()
    assert "rules" in data
    assert "totalCareers" in data
    assert data["rules"]["total"] >= 35


def test_admin_get_rules():
    res = client.get("/api/admin/rules")
    assert res.status_code == 200
    rules = res.json()
    assert isinstance(rules, list)
    assert len(rules) >= 35


def test_admin_toggle_rule():
    res = client.patch("/api/admin/rules/ABL-01/toggle")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    # Bật lại để không ảnh hưởng dữ liệu gốc
    res_back = client.patch("/api/admin/rules/ABL-01/toggle")
    assert res_back.status_code == 200
    assert res_back.json()["enabled"] is True
