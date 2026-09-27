import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_phase_p_dependency_gate_and_api_contract():
    """Verify backend decision analysis API schema meets Phase P UI requirements."""
    response = client.post("/api/v1/decision/analyze", json={
        "district_id": "chennai",
        "optimization_mode": "CLASSICAL_PLUS_QAOA",
        "qaoa_p_depth": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert "decision_id" in data
    assert "district_id" in data
    assert data["district_id"].lower() == "chennai" or data["district_id"] == "TN-001"
    assert "risk_score" in data
    assert "priority_score" in data
    assert "selected_strategies" in data
    assert "optimization_summary" in data
    
    opt = data["optimization_summary"]
    assert "quantum_advantage_claimed" in opt
    # Enforce quantum advantage guardrail (False when gap > 0)
    assert opt["quantum_advantage_claimed"] is False
    assert opt["objective_gap"] > 0

def test_phase_p_gis_districts_endpoint():
    """Verify GIS district endpoint returns 38 canonical Tamil Nadu districts."""
    response = client.get("/districts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 38
    district_ids = {d.get("district_id") or d.get("district_name") for d in data}
    assert any("chennai" in str(did).lower() or "tn-001" in str(did).lower() for did in district_ids)

def test_phase_p_cross_district_isolation():
    """Verify selecting District A and District B returns isolated decision states."""
    resp_a = client.post("/api/v1/decision/analyze", json={"district_id": "chennai"})
    resp_b = client.post("/api/v1/decision/analyze", json={"district_id": "coimbatore"})
    assert resp_a.status_code == 200
    assert resp_b.status_code == 200
    data_a = resp_a.json()
    data_b = resp_b.json()
    assert data_a["district_id"] != data_b["district_id"]
    assert data_a["decision_id"] != data_b["decision_id"]
