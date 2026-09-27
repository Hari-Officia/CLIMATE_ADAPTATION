import os
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_U")
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_u")

def test_phase_u_status_file():
    status_path = os.path.join(RESEARCH_DIR, "PHASE_U_STATUS.json")
    assert os.path.exists(status_path), "PHASE_U_STATUS.json missing"
    with open(status_path, "r") as f:
        data = json.load(f)
    assert data["phase_status"] == "PASS"
    assert data["districts_verified"] == 38
    assert data["experiments_verified"] == 190
    assert data["negative_gaps_remaining"] == 0
    assert data["quantum_advantage"] == "NOT_ESTABLISHED"
    assert data["phase_v_authorized"] is False

def test_phase_u_district_registry():
    path = os.path.join(RESEARCH_DIR, "PHASE_U_DISTRICT_REGISTRY.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 38

def test_phase_u_strategy_mapping():
    path = os.path.join(RESEARCH_DIR, "PHASE_U_STRATEGY_BIT_MAPPING.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 14

def test_phase_u_190_experiments():
    path = os.path.join(RESEARCH_DIR, "PHASE_U_190_EXPERIMENT_CERTIFICATION.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 190
    for row in reader:
        assert float(row["independent_gap"]) >= 0.0

def test_phase_u_audit_reports_exist():
    expected_files = [
        "00_INPUT_FREEZE.md", "01_PRODUCTION_INTEGRITY.md", "02_SLACK_CERTIFICATION.md",
        "03_QUBO_GLOBAL_OPTIMUM_CERTIFICATION.md", "04_INDEPENDENT_DECODING.md",
        "05_INDEPENDENT_OBJECTIVE.md", "06_INDEPENDENT_FEASIBILITY.md",
        "07_INDEPENDENT_QUBO_ENERGY.md", "08_GAP_CERTIFICATION.md",
        "09_OPTIMAL_PROBABILITY.md", "10_SHOT_AUDIT.md",
        "11_38_DISTRICT_CERTIFICATION.md", "12_190_EXPERIMENT_CERTIFICATION.md",
        "13_STATISTICAL_CROSSCHECK.md", "14_REPRODUCIBILITY.md",
        "15_PROVENANCE.md", "16_SECURITY.md", "17_TEST_REPORT.md",
        "18_CLAIM_AUDIT.md", "19_FINAL_PHASE_U_CERTIFICATION.md"
    ]
    for fname in expected_files:
        p = os.path.join(AUDIT_DIR, fname)
        assert os.path.exists(p), f"Missing audit report: {fname}"
