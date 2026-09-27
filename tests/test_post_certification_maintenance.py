"""
Post-Certification Maintenance & Governance Test Suite
Verifies baseline snapshots, change control frameworks, drift engines, policy compliance, and 38-district health drills.
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

def test_m01_baseline_manifest_exists():
    """Verify master baseline manifest existence and release version."""
    base_file = PROJECT_ROOT / "lifecycle" / "baselines" / "release_3_0_0_baseline.json"
    assert base_file.exists()
    with open(base_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["release_version"] == "3.0.0-certified"
        assert data["quantum_advantage_status"] == "NOT ESTABLISHED"

def test_m02_change_classification_exists():
    """Verify change classification documentation exists."""
    doc = PROJECT_ROOT / "lifecycle" / "change_management" / "CHANGE_CLASSIFICATION.md"
    assert doc.exists()

def test_m03_qaoa_registry_exists():
    """Verify QAOA experiment registry exists and claims zero quantum advantage."""
    reg_file = PROJECT_ROOT / "lifecycle" / "qaoa" / "qaoa_experiment_registry.json"
    assert reg_file.exists()
    with open(reg_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["experiment_baseline"]["quantum_advantage_established"] is False

def test_m04_research_gap_registry_exists():
    """Verify research gap registry documentation exists."""
    doc = PROJECT_ROOT / "docs" / "research" / "RESEARCH_GAP_REGISTRY.md"
    assert doc.exists()

def test_m05_policy_compliance():
    """Verify policy compliance engine passes cleanly."""
    summary = enforce_all_policies()
    assert summary["overall_status"] == "COMPLIANT"

def test_m06_drift_monitoring():
    """Verify continuous data and model drift monitoring."""
    rep = run_drift_monitoring()
    assert rep["district_count"] == 38
    assert rep["data_freshness"]["status"] == "CURRENT"

def test_m07_decision_reproducibility():
    """Verify 100% deterministic decision reconstruction for chennai."""
    rep = verify_decision_reproducibility("chennai")
    assert rep["reproducible"] is True

def test_m08_secret_scan():
    """Verify zero hardcoded API secrets in codebase."""
    findings = scan_repository()
    assert len(findings) == 0
