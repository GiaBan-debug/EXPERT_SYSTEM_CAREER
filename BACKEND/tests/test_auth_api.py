"""Unit test cho Authentication & Authorization."""
from fastapi.testclient import TestClient
from app import app
from app.services.auth_service import AuthService, hash_password, verify_password

client = TestClient(app)


def test_password_hash():
    pw = "secret123"
    h = hash_password(pw)
    assert verify_password(pw, h) is True
    assert verify_password("wrong", h) is False


def test_auth_login_admin():
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["role"] == "admin"
    assert "token" in data["data"]


def test_auth_login_wrong_password():
    res = client.post("/api/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert res.status_code == 401


def test_auth_register_and_login():
    import uuid
    rand_user = "student_" + uuid.uuid4().hex[:6]
    res_reg = client.post("/api/auth/register", json={
        "username": rand_user,
        "password": "password123",
        "fullName": "Học sinh thử nghiệm",
        "email": f"{rand_user}@gmail.com",
        "role": "user"
    })
    assert res_reg.status_code == 200
    reg_data = res_reg.json()
    assert reg_data["data"]["role"] == "user"

    # Đăng nhập lại
    res_login = client.post("/api/auth/login", json={"username": rand_user, "password": "password123"})
    assert res_login.status_code == 200
    assert res_login.json()["data"]["username"] == rand_user
