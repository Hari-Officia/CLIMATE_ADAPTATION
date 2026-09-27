import os
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_V")
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_v")

def test_phase_v_status_file():
    status_path = os.path.join(RESEARCH_DIR, "PHASE_V_STATUS.json")
    assert os.path.exists(status_path), "PHASE_V_STATUS.json missing"
    with open(status_path, "r") as f:
        data = json.load(f)
    assert data["phase_status"] == "PASS"
    assert data["districts_total"] == 38
    assert data["total_experiments"] == 1900
    assert data["valid_experiments"] == 1900
    assert data["negative_gaps"] == 0
    assert data["quantum_advantage"] == "NOT_ESTABLISHED"
    assert data["hardware_execution"] is False
    assert data["warm_start_execution"] is False
    assert data["phase_w_authorized"] is False

def test_true_milp_solver():
    from research.quantum_advantage.classical.true_milp_solver import TrueMILPSolver
    c = [0.35] * 14
    res = TrueMILPSolver.solve_binary_milp(c, K=5)
    assert res["status"] == "SUCCESS"
    assert res["feasible"] is True
    assert sum(res["selected_vector"]) == 5
    assert all(x in [0, 1] for x in res["selected_vector"])

def test_phase_v_experiments_csv():
    path = os.path.join(RESEARCH_DIR, "PHASE_V_EXPERIMENTS.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 1900
    for row in reader:
        assert float(row["gap"]) >= 0.0

def test_phase_v_depth_summary_csv():
    path = os.path.join(RESEARCH_DIR, "PHASE_V_DEPTH_SUMMARY.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 5

def test_phase_v_audit_reports_exist():
    expected_files = [
        "00_MILP_SOLVER_TYPE_AUDIT.md", "01_BASELINE_OBJECTIVE_RECONCILIATION.md",
        "02_CANONICAL_INSTANCE_GATE.md", "03_EXPERIMENTAL_PROTOCOL.md",
        "04_QAOA_CONFIGURATION.md", "05_SEED_PROTOCOL.md",
        "06_SHOT_AUDIT.md", "07_RESULT_VALIDATION.md",
        "08_DEPTH_ANALYSIS.md", "09_SEED_ROBUSTNESS.md",
        "10_RUNTIME_ANALYSIS.md", "11_CIRCUIT_RESOURCE_ANALYSIS.md",
        "12_DISTRICT_ANALYSIS.md", "13_REPRODUCIBILITY.md",
        "14_FAILURE_REGISTER.md", "15_SECURITY.md",
        "16_CLAIM_AUDIT.md", "17_FINAL_PHASE_V_CERTIFICATION.md"
    ]
    for fname in expected_files:
        p = os.path.join(AUDIT_DIR, fname)
        assert os.path.exists(p), f"Missing audit report: {fname}"
