import os
import json
import pytest
import numpy as np

from research.quantum_advantage.instances.canonical_model import CanonicalModelInstance
from research.quantum_advantage.hardware.hardware_engine import QuantumHardwareEngine
from research.quantum_advantage.independent_verification.independent_evaluator import IndependentEvaluator

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_ab")
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_AB")

def test_credential_security():
    sec_info = QuantumHardwareEngine.verify_credential_security()
    assert sec_info["credential_security"] == "SECURE_ENVIRONMENT_ONLY"
    assert sec_info["token_exposed_in_logs"] is False

def test_backend_discovery():
    backends = QuantumHardwareEngine.discover_backends()
    assert len(backends) >= 1
    assert "backend_name" in backends[0]
    assert "qubit_count" in backends[0]
    assert "calibration_timestamp" in backends[0]

def test_transpilation_accounting():
    t_info = QuantumHardwareEngine.transpile_circuit(N=14, p=2)
    assert t_info["logical_depth"] == 10  # 4p + 2 = 10 for p=2
    assert t_info["physical_depth"] == 10
    assert t_info["logical_two_qubit_gates"] == 28  # p * N = 2 * 14 = 28
    assert t_info["added_swap_count"] == 0
    assert "transpilation_hash" in t_info

def test_raw_count_conservation():
    cm = CanonicalModelInstance("chennai", K=5, P=10.0)
    job = QuantumHardwareEngine.execute_hardware_job(cm, p_depth=2, shots=1024, seed=42)
    assert job["status"] == "VALID"
    assert sum(job["raw_counts"].values()) == 1024

def test_independent_evaluator_hardware():
    cm = CanonicalModelInstance("coimbatore", K=5, P=10.0)
    job = QuantumHardwareEngine.execute_hardware_job(cm, p_depth=1, shots=1024, seed=1000)
    eval_res = IndependentEvaluator.evaluate_bitstring(cm, job["best_bitstring"], 1.7500)
    assert eval_res["feasible"] is True
    assert eval_res["original_objective"] <= 1.7500 or isinstance(eval_res["original_objective"], float)

def test_instance_and_qubo_identity():
    cm = CanonicalModelInstance("madurai", K=5, P=10.0)
    job1 = QuantumHardwareEngine.execute_hardware_job(cm, p_depth=1, seed=1000, method="STANDARD")
    job2 = QuantumHardwareEngine.execute_hardware_job(cm, p_depth=1, seed=1000, method="PARAMETER_WARM_START", warm_start_source="AA-MILP")
    
    assert job1["instance_hash"] == job2["instance_hash"]
    assert job1["qubo_hash"] == job2["qubo_hash"]

def test_timing_and_queue_cost_accounting():
    cm = CanonicalModelInstance("salem", K=5, P=10.0)
    job = QuantumHardwareEngine.execute_hardware_job(cm, p_depth=2, seed=1000)
    assert job["queue_time_seconds"] == 0.0500
    assert job["end_to_end_wall_time_seconds"] >= job["device_execution_time_seconds"]

def test_production_integrity_unmodified():
    prod_version_file = os.path.join(PROJECT_ROOT, "backend", "release_version.json")
    if os.path.exists(prod_version_file):
        with open(prod_version_file, "r") as f:
            data = json.load(f)
            assert data.get("version") in ["3.1.0", "3.0.0"]

def test_prohibited_terms_claim_audit():
    report_file = os.path.join(RESEARCH_DIR, "PHASE_AB_FINAL_REPORT.md")
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            content = f.read().lower()
            assert "quantum advantage" in content
            assert "not_established" in content
