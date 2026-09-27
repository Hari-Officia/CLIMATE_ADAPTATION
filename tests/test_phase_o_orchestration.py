"""
Comprehensive Phase O Test Suite
Tests multi-agent orchestrator, workflow state, stage progression, quality gates, idempotency, failure injection, cross-district isolation, REST APIs, and end-to-end golden decision scenarios.
"""

import json
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.orchestration.workflow_engine import MasterDecisionOrchestrator
from backend.services.orchestration.workflow_state import DecisionWorkflowState
from backend.services.orchestration.workflow_validator import WorkflowValidator
from backend.services.orchestration.idempotency_manager import IdempotencyManager
from backend.services.orchestration.observability_tracer import ObservabilityTracer

client = TestClient(app)

def test_group_a_b_c_orchestrator_and_state():
    orchestrator = MasterDecisionOrchestrator()
    res = orchestrator.execute_workflow("chennai")
    assert res["validation_status"] == "VERIFIED"
    assert res["district_id"] == "chennai"
    assert res["district_name"] == "Chennai"
    assert res["risk_score"] > 0
    assert res["priority_score"] > 0
    assert len(res["selected_strategies"]) > 0
    assert res["optimization_summary"]["quantum_advantage_claimed"] is False
    assert "context_hash" in res["provenance"]

def test_group_d_idempotency():
    mgr = IdempotencyManager()
    req = {"district_id": "coimbatore", "optimization_mode": "CLASSICAL"}
    key1 = mgr.compute_idempotency_key(req)
    key2 = mgr.compute_idempotency_key(req)
    assert key1 == key2
    assert len(key1) == 64

def test_group_e_quality_gates():
    validator = WorkflowValidator()
    state = DecisionWorkflowState("REQ-1", "WF-1", "DEC-1", "chennai")
    state.risk_context = {"composite_risk_score": 0.85}
    state.priority_context = {"priority_score": 0.88}
    state.strategy_candidates = ["STR-NBS-001"]
    state.classical_optimization_result = {"selected_strategy_ids": ["STR-NBS-001"]}
    state.evidence_packet = {
        "retrieved_evidence": [{"claim_id": "CLM-1"}],
        "citations": [{"citation_id": "CIT-1"}]
    }
    state.explanation = {"explanation": {"decision_summary": "Test Summary"}}
    state.context_hash = "hash_123"

    gate_res = validator.validate_workflow(state)
    assert gate_res["passed_all"] is True
    assert gate_res["status"] == "VERIFIED"

def test_group_f_failure_isolation():
    orchestrator = MasterDecisionOrchestrator()
    with pytest.raises(ValueError, match="District 'nonexistent_district' not found"):
        orchestrator.execute_workflow("nonexistent_district")

def test_group_h_observability():
    tracer = ObservabilityTracer()
    ev = tracer.log_event("TEST_EVENT", "WF-TEST-001", "TEST_STAGE", "SUCCESS", duration_ms=12.5)
    assert ev["service"] == "decision_orchestrator"
    assert ev["duration_ms"] == 12.5

def test_group_i_rest_api_endpoints():
    # Health check
    res_health = client.get("/api/v1/decision/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "HEALTHY"

    # Analyze decision endpoint
    res_analyze = client.post("/api/v1/decision/analyze", json={
        "district_id": "coimbatore",
        "optimization_mode": "CLASSICAL_PLUS_QAOA"
    })
    assert res_analyze.status_code == 200
    data = res_analyze.json()
    assert data["validation_status"] == "VERIFIED"
    assert data["district_id"] == "coimbatore"
    assert "decision_id" in data

    dec_id = data["decision_id"]

    # Fetch decision by ID
    res_fetch = client.get(f"/api/v1/decision/{dec_id}")
    assert res_fetch.status_code == 200
    assert res_fetch.json()["decision_id"] == dec_id

    # Fetch workflow by ID
    res_wf = client.get(f"/api/v1/decision/{dec_id}/workflow")
    assert res_wf.status_code == 200
    assert res_wf.json()["district_id"] == "coimbatore"

    # Fetch provenance
    res_prov = client.get(f"/api/v1/decision/{dec_id}/provenance")
    assert res_prov.status_code == 200
    assert "context_hash" in res_prov.json()

def test_group_j_cross_district_isolation():
    orchestrator = MasterDecisionOrchestrator()
    res_che = orchestrator.execute_workflow("chennai")
    res_coi = orchestrator.execute_workflow("coimbatore")

    assert res_che["district_id"] == "chennai"
    assert res_coi["district_id"] == "coimbatore"
    assert res_che["decision_id"] != res_coi["decision_id"]
    assert res_che["provenance"]["context_hash"] != res_coi["provenance"]["context_hash"]

def test_group_k_golden_scenarios():
    orchestrator = MasterDecisionOrchestrator()
    # Scenario 1: Coastal Flood District (Chennai)
    sc1 = orchestrator.execute_workflow("chennai", hazard_ids=["coastal_flooding"])
    assert sc1["validation_status"] == "VERIFIED"

    # Scenario 2: Inland Drought District (Nilgiris / Coimbatore)
    sc2 = orchestrator.execute_workflow("coimbatore", hazard_ids=["drought"])
    assert sc2["validation_status"] == "VERIFIED"
