import os
import json
import pytest
import numpy as np

from research.quantum_advantage.instances.canonical_model import CanonicalModelInstance
from research.quantum_advantage.warm_start.warm_start_qaoa import WarmStartQAOA
from research.quantum_advantage.independent_verification.independent_evaluator import IndependentEvaluator

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_aa")
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_AA")

def test_zero_noise_delta_audit():
    z_manifest = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_z", "PHASE_Z_BASELINE_MANIFEST.json")
    if os.path.exists(z_manifest):
        with open(z_manifest, "r") as f:
            data = json.load(f)
            assert data.get("preflight_status") == "PASS"

def test_circuit_metrics_audit():
    cm = CanonicalModelInstance("chennai", K=5, P=10.0)
    res_std = WarmStartQAOA.run_warm_start_trial(cm, p_depth=2, shots=1024, seed=42, method="STANDARD")
    assert res_std["circuit_depth"] == 10  # 4p + 2 = 10 for p=2
    assert res_std["two_qubit_gate_count"] == 20  # 10p = 20 for p=2

def test_classical_preprocessing_milp():
    cm = CanonicalModelInstance("coimbatore", K=5, P=10.0)
    class_res = WarmStartQAOA.get_classical_solution(cm, source="AA-MILP")
    assert class_res["source"] == "AA-MILP"
    assert len(class_res["solution_bitstring"]) == cm.N
    assert class_res["preprocessing_runtime_seconds"] >= 0.0

def test_parameter_warm_start_construction():
    p_ws = WarmStartQAOA.construct_parameter_warm_start("01010101010101", p_depth=3)
    assert p_ws["warm_start_type"] == "PARAMETER_WARM_START"
    assert len(p_ws["initial_gamma"]) == 3
    assert len(p_ws["initial_beta"]) == 3

def test_state_warm_start_construction():
    s_ws = WarmStartQAOA.construct_state_warm_start("01010101010101", p_depth=2)
    assert s_ws["warm_start_type"] == "STATE_WARM_START"
    assert "01010101010101" in s_ws["initial_state_probs"]
    assert s_ws["additional_circuit_depth"] == 2

def test_instance_and_qubo_identity():
    cm = CanonicalModelInstance("madurai", K=5, P=10.0)
    std_trial = WarmStartQAOA.run_warm_start_trial(cm, p_depth=1, seed=1000, method="STANDARD")
    par_trial = WarmStartQAOA.run_warm_start_trial(cm, p_depth=1, seed=1000, method="PARAMETER_WARM_START", warm_start_source="AA-MILP")
    
    assert std_trial["instance_hash"] == par_trial["instance_hash"]
    assert std_trial["qubo_hash"] == par_trial["qubo_hash"]

def test_end_to_end_cost_accounting():
    cm = CanonicalModelInstance("salem", K=5, P=10.0)
    par_trial = WarmStartQAOA.run_warm_start_trial(cm, p_depth=2, seed=1000, method="PARAMETER_WARM_START", warm_start_source="AA-MILP")
    
    assert par_trial["preprocessing_runtime_seconds"] > 0.0
    assert par_trial["end_to_end_runtime_seconds"] >= par_trial["preprocessing_runtime_seconds"] + par_trial["qaoa_runtime_seconds"]

def test_production_integrity_unmodified():
    prod_version_file = os.path.join(PROJECT_ROOT, "backend", "release_version.json")
    if os.path.exists(prod_version_file):
        with open(prod_version_file, "r") as f:
            data = json.load(f)
            assert data.get("version") in ["3.1.0", "3.0.0"]

def test_prohibited_terms_claim_audit():
    report_file = os.path.join(RESEARCH_DIR, "PHASE_AA_FINAL_REPORT.md")
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            content = f.read().lower()
            assert "quantum advantage" in content
            assert "not_established" in content
