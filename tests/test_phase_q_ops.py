import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings

client = TestClient(app)

def test_phase_q_liveness_probe():
    """Verify liveness probe returns HTTP 200 ALIVE."""
    response = client.get("/api/v1/decision/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ALIVE"

def test_phase_q_readiness_probe():
    """Verify readiness probe checks database connectivity."""
    response = client.get("/api/v1/decision/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert data["dependencies"]["database"] == "UP"

def test_phase_q_configuration_validation():
    """Verify settings validation rules."""
    assert settings.ENVIRONMENT in ["development", "testing", "staging", "production"]
    assert settings.DATABASE_URL is not None
    assert settings.CHROMA_PERSIST_DIR is not None

def test_phase_q_model_registry_file():
    """Verify ML model registry JSON configuration."""
    import os, json
    path = "config/models/model_registry.json"
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = json.load(f)
    assert "models" in data
    assert len(data["models"]) >= 3
