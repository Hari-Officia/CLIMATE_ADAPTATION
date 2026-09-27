import os
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_X")
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_x")

def test_phase_x_status_file():
    status_path = os.path.join(RESEARCH_DIR, "PHASE_X_STATUS.json")
    assert os.path.exists(status_path), "PHASE_X_STATUS.json missing"
    with open(status_path, "r") as f:
        data = json.load(f)
    assert data["phase_status"] == "PASS"
    assert data["unique_qaoa_runs"] == 1900
    assert data["shots_per_run"] == 1024
    assert data["statistical_unit"] == "RUN (district x depth x seed)"
    assert data["primary_outcome"] == "un_clamped_objective_gap"
    assert data["gap_recalculation"] == "PASS"
    assert data["missing_data"] == "0"
    assert data["quantum_advantage"] == "NOT_ESTABLISHED"
    assert data["phase_y_authorized"] is False

def test_phase_x_protocol_file():
    path = os.path.join(RESEARCH_DIR, "PHASE_X_STATISTICAL_PROTOCOL.json")
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = json.load(f)
    assert data["protocol_id"] == "PHASE_X_STATISTICAL_PROTOCOL_V1"
    assert data["bootstrap_replicates"] == 10000

def test_phase_x_experimental_units():
    path = os.path.join(RESEARCH_DIR, "PHASE_X_EXPERIMENTAL_UNITS.json")
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = json.load(f)
    assert data["level_2_qaoa_run"]["count"] == 1900
    assert data["level_1_measurement_shot"]["count"] == 1945600

def test_phase_x_bootstrap_results():
    path = os.path.join(RESEARCH_DIR, "PHASE_X_BOOTSTRAP_RESULTS.json")
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = json.load(f)
    assert "naive_run_level_95_ci" in data
    assert "district_clustered_95_ci" in data

def test_phase_x_audit_reports_exist():
    expected_files = [
        "00_STATISTICAL_PROTOCOL.md", "01_EXPERIMENTAL_UNITS.md",
        "02_GAP_DISTRIBUTION.md", "03_CI_RECONCILIATION.md",
        "04_BOOTSTRAP_METHODS.md", "05_SEED_ROBUSTNESS.md",
        "06_DISTRICT_ROBUSTNESS.md", "07_DEPTH_ROBUSTNESS.md",
        "08_PAIRED_DEPTH_ANALYSIS.md", "09_MULTIPLE_COMPARISONS.md",
        "10_EFFECT_SIZES.md", "11_FEASIBILITY_STATISTICS.md",
        "12_OPTIMAL_PROBABILITY.md", "13_OPTIMALITY_DEFINITION.md",
        "14_RUNTIME_STATISTICS.md", "15_CIRCUIT_RESOURCE_STATISTICS.md",
        "16_OUTLIER_AUDIT.md", "17_MISSING_DATA.md",
        "18_AGGREGATION_SENSITIVITY.md", "19_REPRODUCIBILITY.md",
        "20_CLASSICAL_REFERENCE_CHECK.md", "21_CLAIM_AUDIT.md",
        "22_SECURITY.md", "23_FINAL_PHASE_X_CERTIFICATION.md"
    ]
    for fname in expected_files:
        p = os.path.join(AUDIT_DIR, fname)
        assert os.path.exists(p), f"Missing audit report: {fname}"
