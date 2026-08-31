import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_login_success_harish():
    response = client.post("/auth/login", data={"username": "harish", "password": "user123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "USER"
    assert data["username"] == "harish"

def test_login_success_admin():
    response = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "ADMIN"

def test_login_invalid_password():
    response = client.post("/auth/login", data={"username": "harish", "password": "wrongpassword"})
    assert response.status_code == 401

def test_get_me_with_token():
    login_resp = client.post("/auth/login", data={"username": "harish", "password": "user123"})
    token = login_resp.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "harish"
    assert data["role"] == "USER"

def test_admin_route_forbidden_for_regular_user():
    login_resp = client.post("/auth/login", data={"username": "harish", "password": "user123"})
    token = login_resp.json()["access_token"]

    response = client.post("/system/admin/refresh-forecast", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
