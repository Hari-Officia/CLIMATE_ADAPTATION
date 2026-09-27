"""
Phase R Platform Governance & Continuous Evaluation Test Suite
"""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient

from backend.main import app
from scripts.monitor_drift import run_drift_monitoring, calculate_psi
from scripts.verify_decision_reproducibility import verify_decision_reproducibility
from scripts.enforce_policies import enforce_all_policies

client = TestClient(app)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_governance_status_endpoint():
    """Test read-only /api/v1/governance/status endpoint."""
    response = client.get("/api/v1/governance/status")
    assert response.status_code == 200
    data = response.json()
    assert data["phase"] == "R"
    assert data["scope"] == "CLIMATE ADAPTATION ONLY"
    assert data["district_count"] == 38
    assert data["quantum_advantage_status"] == "NOT ESTABLISHED"
    assert data["qaoa_objective_gap_benchmark"] == 0.4700

def test_governance_models_endpoint():
    """Test read-only /api/v1/governance/models endpoint."""
    response = client.get("/api/v1/governance/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data or "models_registered" in data

def test_governance_datasets_endpoint():
    """Test read-only /api/v1/governance/datasets endpoint."""
    response = client.get("/api/v1/governance/datasets")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLIANT"
    assert len(data["datasets"]) > 0

def test_governance_knowledge_endpoint():
    """Test read-only /api/v1/governance/knowledge endpoint."""
    response = client.get("/api/v1/governance/knowledge")
    assert response.status_code == 200
    data = response.json()
    assert "knowledge_base_version" in data or "sources" in data

def test_governance_decisions_endpoint():
    """Test read-only /api/v1/governance/decisions endpoint."""
    response = client.get("/api/v1/governance/decisions?district=TN-001")
    assert response.status_code == 200
    data = response.json()
    assert data["lineage_node_count"] == 19
    assert data["provenance_status"] == "VERIFIED"

def test_governance_incidents_endpoint():
    """Test read-only /api/v1/governance/incidents endpoint."""
    response = client.get("/api/v1/governance/incidents")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"

def test_governance_changes_endpoint():
    """Test read-only /api/v1/governance/changes endpoint."""
    response = client.get("/api/v1/governance/changes")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CONTROLLED"

def test_governance_security_endpoint():
    """Test read-only /api/v1/governance/security endpoint."""
    response = client.get("/api/v1/governance/security")
    assert response.status_code == 200
    data = response.json()
    assert data["secret_scan_status"] == "CLEAN"

def test_governance_backups_endpoint():
    """Test read-only /api/v1/governance/backups endpoint."""
    response = client.get("/api/v1/governance/backups")
    assert response.status_code == 200
    data = response.json()
    assert data["rpo_compliant"] is True
    assert data["rto_compliant"] is True

def test_governance_slo_endpoint():
    """Test read-only /api/v1/governance/slo endpoint."""
    response = client.get("/api/v1/governance/slo")
    assert response.status_code == 200
    data = response.json()
    assert "slos" in data

def test_psi_calculation():
    """Test PSI drift calculation utility."""
    base = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    target = [0.11, 0.21, 0.31, 0.41, 0.51, 0.61, 0.71, 0.81, 0.91, 0.99]
    psi = calculate_psi(base, target)
    assert psi >= 0.0
    assert psi < 0.1 # Slight perturbation = low PSI

def test_drift_monitoring_execution():
    """Test drift monitoring engine script."""
    report = run_drift_monitoring()
    assert report["district_count"] == 38
    assert report["data_freshness"]["status"] == "CURRENT"
    assert report["optimization_integrity"]["quantum_advantage_status"] == "NOT ESTABLISHED"

def test_policy_enforcement_execution():
    """Test policy compliance engine script."""
    summary = enforce_all_policies()
    assert summary["overall_status"] == "COMPLIANT"
    assert summary["compliant_count"] == summary["total_policies"]

def test_decision_reproducibility_execution():
    """Test decision reproducibility verification script."""
    rep = verify_decision_reproducibility("chennai")
    assert rep["reproducible"] is True
    assert rep["provenance_status"] == "VERIFIED"
