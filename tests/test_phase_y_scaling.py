import os
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_Y")
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_y")

def test_phase_y_status_file():
    status_path = os.path.join(RESEARCH_DIR, "PHASE_Y_STATUS.json")
    assert os.path.exists(status_path), "PHASE_Y_STATUS.json missing"
    with open(status_path, "r") as f:
        data = json.load(f)
    assert data["phase_status"] == "PASS"
    assert data["real_instances_count"] == 38
    assert data["n_range"] == "N=4..20"
    assert data["exact_scaling_limit"] == 18
    assert data["quantum_advantage"] == "NOT_ESTABLISHED"
    assert data["phase_z_authorized"] is False
    assert data["hardware_authorized"] is False

def test_phase_y_denominator_reconciliation():
    path = os.path.join(RESEARCH_DIR, "PHASE_Y_DENOMINATOR_RECONCILIATION.json")
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = json.load(f)
    assert data["valid_p2_runs"] == 350
    assert data["exact_hit_runs"] == 50

def test_phase_y_scaling_master_table():
    path = os.path.join(RESEARCH_DIR, "PHASE_Y_SCALING_MASTER_TABLE.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) > 0
    for row in reader:
        assert float(row["gap"]) >= 0.0

def test_phase_y_solver_boundaries():
    path = os.path.join(RESEARCH_DIR, "PHASE_Y_SOLVER_BOUNDARIES.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 5

def test_phase_y_audit_reports_exist():
    expected_files = [
        "00_PHASE_X_DENOMINATOR_RECONCILIATION.md", "01_REPRODUCIBILITY_TERMINOLOGY.md",
        "02_SCALING_PROTOCOL.md", "03_REAL_VS_SYNTHETIC_POLICY.md",
        "04_INSTANCE_GENERATION.md", "05_INSTANCE_HASHING.md",
        "06_OBJECTIVE_NORMALIZATION.md", "07_CONSTRAINT_SCALING.md",
        "08_PENALTY_SCALING.md", "09_EXACT_SCALING.md",
        "10_MILP_SCALING.md", "11_GREEDY_SCALING.md",
        "12_SA_SCALING.md", "13_QUBO_SCALING.md",
        "14_QAOA_SCALING.md", "15_RESOURCE_SCALING.md",
        "16_RUNTIME_SCALING.md", "17_MEMORY_SCALING.md",
        "18_DEPTH_X_SCALE.md", "19_SOLVER_BOUNDARIES.md",
        "20_REPLICATION.md", "21_STATISTICS.md",
        "22_REPRODUCIBILITY.md", "23_REAL_DATA_LIMITATIONS.md",
        "24_CLAIM_AUDIT.md", "25_SECURITY.md",
        "26_PRODUCTION_INTEGRITY.md", "27_FINAL_PHASE_Y_CERTIFICATION.md"
    ]
    for fname in expected_files:
        p = os.path.join(AUDIT_DIR, fname)
        assert os.path.exists(p), f"Missing audit report: {fname}"
