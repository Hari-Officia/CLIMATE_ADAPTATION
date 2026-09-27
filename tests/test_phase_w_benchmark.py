import os
import json
import csv
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_W")
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_w")

def test_phase_w_status_file():
    status_path = os.path.join(RESEARCH_DIR, "PHASE_W_STATUS.json")
    assert os.path.exists(status_path), "PHASE_W_STATUS.json missing"
    with open(status_path, "r") as f:
        data = json.load(f)
    assert data["phase_status"] == "PASS"
    assert data["total_unique_experiments"] == 1900
    assert data["exact_reference_status"] == "PASS"
    assert data["milp_reference_status"] == "PASS"
    assert data["milp_integer_valid"] is True
    assert data["greedy_status"] == "PASS"
    assert data["sa_status"] == "PASS"
    assert data["qaoa_status"] == "PASS"
    assert data["common_evaluator"] == "PASS"
    assert data["negative_gaps"] == 0
    assert data["quantum_advantage"] == "NOT_ESTABLISHED"
    assert data["hardware_execution"] is False
    assert data["warm_start_execution"] is False
    assert data["phase_x_authorized"] is False
    assert data["phase_y_authorized"] is False

def test_greedy_solver():
    from research.quantum_advantage.classical.greedy_solver import GreedySolver
    c = [0.35] * 14
    res = GreedySolver.solve(c, K=5)
    assert res["status"] == "SUCCESS"
    assert res["feasible"] is True
    assert sum(res["selected_vector"]) == 5

def test_simulated_annealing_solver():
    from research.quantum_advantage.classical.simulated_annealing_solver import SimulatedAnnealingSolver
    c = [0.35] * 14
    res = SimulatedAnnealingSolver.solve(c, K=5, seed=1000)
    assert res["status"] == "SUCCESS"
    assert res["feasible"] is True
    assert sum(res["selected_vector"]) == 5

def test_phase_w_solver_comparison_csv():
    path = os.path.join(RESEARCH_DIR, "PHASE_W_SOLVER_COMPARISON.csv")
    assert os.path.exists(path)
    with open(path, "r") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) > 0
    for row in reader:
        assert float(row["gap"]) >= 0.0

def test_phase_w_audit_reports_exist():
    expected_files = [
        "00_EXPERIMENT_COUNT_RECONCILIATION.md", "01_FEASIBILITY_DEFINITION.md",
        "02_REPRODUCIBILITY_TERMINOLOGY.md", "03_BENCHMARK_PROTOCOL.md",
        "04_CANONICAL_INSTANCE_EQUALITY.md", "05_EXACT_BASELINE.md",
        "06_MILP_BASELINE.md", "07_GREEDY_BASELINE.md",
        "08_SIMULATED_ANNEALING.md", "09_QAOA_REFERENCE.md",
        "10_COMMON_EVALUATOR.md", "11_RUNTIME_PROTOCOL.md",
        "12_TIME_TO_SOLUTION.md", "13_RESOURCE_COMPARISON.md",
        "14_DISTRICT_ANALYSIS.md", "15_SOLVER_ANALYSIS.md",
        "16_QAOA_DEPTH_COMPARISON.md", "17_STATISTICS.md",
        "18_BOOTSTRAP.md", "19_EFFECT_SIZE.md",
        "20_REPRODUCIBILITY.md", "21_SECURITY.md",
        "22_CLAIM_AUDIT.md", "23_PRODUCTION_INTEGRITY.md",
        "24_FINAL_PHASE_W_CERTIFICATION.md"
    ]
    for fname in expected_files:
        p = os.path.join(AUDIT_DIR, fname)
        assert os.path.exists(p), f"Missing audit report: {fname}"
