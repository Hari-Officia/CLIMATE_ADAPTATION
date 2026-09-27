"""
Continuous Operations & Periodic Re-Certification Test Suite
Verifies operating state machine, monitoring schedules, 38-district health drills, and decision diff engine.
"""

import pytest
import json
import os
from pathlib import Path

from scripts.monitor_drift import run_drift_monitoring
from scripts.enforce_policies import enforce_all_policies
from scripts.verify_decision_reproducibility import verify_decision_reproducibility
from scripts.scan_secrets import scan_repository

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_c01_operating_state_machine():
    """Verify operating state machine baseline configuration."""
    state_file = PROJECT_ROOT / "lifecycle" / "status" / "operating_state.json"
    assert state_file.exists()
    with open(state_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["release_version"] == "3.0.0-certified"
        assert data["current_state"] in data["allowed_states"]
        assert data["quantum_advantage_status"] == "NOT ESTABLISHED"

def test_c02_monitoring_schedule_policy():
    """Verify monitoring schedule frequencies."""
    sched_file = PROJECT_ROOT / "config" / "governance" / "monitoring_schedule.json"
    assert sched_file.exists()
    with open(sched_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "DAILY" in data["frequencies"]
        assert "ANNUALLY" in data["frequencies"]

def test_c03_monthly_operations_report():
    """Verify September 2026 monthly operations report exists."""
    rep_file = PROJECT_ROOT / "REPORTS" / "OPERATIONS" / "monthly" / "MONTHLY_OPERATIONS_REPORT_2026_09.md"
    assert rep_file.exists()

def test_c04_district_health_drill():
    """Verify 38-district operational health coverage."""
    drift_rep = run_drift_monitoring()
    assert drift_rep["district_count"] == 38
    assert drift_rep["data_freshness"]["status"] == "CURRENT"

def test_c05_decision_reproducibility_drill():
    """Verify 100% deterministic decision reconstruction."""
    rep = verify_decision_reproducibility("chennai")
    assert rep["reproducible"] is True
    assert rep["provenance_status"] == "VERIFIED"

def test_c06_policy_enforcement_drill():
    """Verify continuous policy compliance."""
    summary = enforce_all_policies()
    assert summary["overall_status"] == "COMPLIANT"

def test_c07_secret_scan_drill():
    """Verify zero hardcoded API secrets in codebase."""
    findings = scan_repository()
    assert len(findings) == 0

def test_c08_qaoa_guardrail():
    """Verify QAOA experimental guardrail status label."""
    reg_file = PROJECT_ROOT / "config" / "quantum" / "qaoa_registry.json"
    assert reg_file.exists()
    with open(reg_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["experiment_baseline"]["status_label"] == "Quantum Advantage: Not Established"
