import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_full_pipeline_flow():
    # 1. Login
    login_res = client.post("/auth/login", data={"username": "harish", "password": "user123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Search for landmark "Marina Beach"
    search_res = client.get("/locations/search?q=Marina+Beach", headers=headers)
    assert search_res.status_code == 200
    results = search_res.json()
    assert len(results) > 0
    first_hit = results[0]
    assert first_hit["district_id"] == "chennai"

    # 3. Get district details & profile
    dist_res = client.get("/districts/chennai", headers=headers)
    assert dist_res.status_code == 200
    assert dist_res.json()["district_name"] == "Chennai"

    # 4. Get district risk assessment
    risk_res = client.get("/risk/district/chennai?day=0", headers=headers)
    assert risk_res.status_code == 200
    risk_data = risk_res.json()
    assert risk_data["district_id"] == "chennai"
    assert "flood" in risk_data["assessment"]
    assert "heatwave" in risk_data["assessment"]
    assert "drought" in risk_data["assessment"]
    assert risk_data["spatial_resolution"] == "District-level (Administrative ADM2)"

    # 5. Get system status
    sys_res = client.get("/system/status", headers=headers)
    assert sys_res.status_code == 200
    assert sys_res.json()["status"] == "HEALTHY"
    assert sys_res.json()["districts_count"] == 38
