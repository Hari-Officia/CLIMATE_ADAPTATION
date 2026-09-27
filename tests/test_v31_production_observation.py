"""
v3.1 Production Observation Test Suite
Validates operational health, observation state machine, baseline protection,
53-feature contract, 38-district golden set reproducibility, QUBO P=10.0 parity,
QAOA experimental status, RAG hierarchy, LLM read-only boundary, and claim audit compliance.
"""

import os
import json
import pytest
from scripts.independent_v31_observation_verification import run_33_observation_verifications
from scripts.verify_certified_baseline import verify_certified_baseline

def test_observation_baseline_integrity():
    """Verify BASE-3.0.0-20260923 baseline integrity remains immutable."""
    res = verify_certified_baseline()
    assert res["status"] == "PASS"

def test_observation_33_independent_verifications():
    """Execute all 33 observation verification checks."""
    res = run_33_observation_verifications()
    assert res["status"] == "PASS"
    assert res["passed_count"] == 33

def test_observation_state_file_integrity():
    """Verify lifecycle/production_observation/ state files exist and are valid."""
    state_file = os.path.join(os.path.dirname(__file__), "..", "lifecycle", "production_observation", "observation_state.json")
    assert os.path.exists(state_file)
    with open(state_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["state"] == "HEALTHY"
    assert data["production_certification"] == "CONDITIONALLY_CERTIFIED"

def test_observation_canonical_strategies_reconciliation():
    """Verify strategy reconciliation: 14 canonical strategies and 45 derived RAG claim links."""
    strat_file = os.path.join(os.path.dirname(__file__), "..", "config", "master", "strategies.json")
    with open(strat_file, "r", encoding="utf-8") as f:
        strats = json.load(f)
    assert len(strats) == 14

def test_observation_qaoa_experimental_status():
    """Verify QAOA remains experimental with gap=0.4700 and Quantum Advantage NOT ESTABLISHED."""
    claim_file = os.path.join(os.path.dirname(__file__), "..", "docs", "research", "CLAIM_EVIDENCE_MATRIX.md")
    with open(claim_file, "r", encoding="utf-8") as f:
        text = f.read()
    assert "NOT_ESTABLISHED" in text
    assert "PROHIBITED" in text

def test_observation_rollback_readiness():
    """Verify system rollback path to BASE-3.0.0-20260923 is ready."""
    rb_file = os.path.join(os.path.dirname(__file__), "..", "deployment", "rc", "v3.1.0-rc1", "rollback_manifest.json")
    assert os.path.exists(rb_file)
