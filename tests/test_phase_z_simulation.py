import os
import json
import pytest
import numpy as np
from research.quantum_advantage.noisy_qaoa.noise_simulator import NoiseSimulator
from research.quantum_advantage.independent_verification.independent_evaluator import IndependentEvaluator
from research.quantum_advantage.instances.canonical_model import CanonicalModelInstance

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(PROJECT_ROOT, "research", "quantum_advantage", "phase_z")
AUDIT_DIR = os.path.join(PROJECT_ROOT, "AUDIT", "PHASE_Z")

def test_noise_simulator_hash():
    h1 = NoiseSimulator.compute_noise_model_hash("Family Z-B", 0.001, 0.0)
    h2 = NoiseSimulator.compute_noise_model_hash("Family Z-B", 0.001, 0.0)
    h3 = NoiseSimulator.compute_noise_model_hash("Family Z-B", 0.005, 0.0)
    assert h1 == h2
    assert h1 != h3

def test_depolarizing_channel_decay():
    ideal = {"0000": 1.0, "1111": 0.0}
    noisy = NoiseSimulator.apply_depolarizing_channel(
        ideal, gate_error_rate=0.01, two_qubit_gate_count=20, single_qubit_gate_count=10, n_qubits=4
    )
    assert noisy["0000"] < 1.0
    assert noisy["1111"] > 0.0
    assert pytest.approx(sum(noisy.values()), 1e-6) == 1.0

def test_readout_channel_bitflip():
    ideal = {"0000": 1.0}
    noisy = NoiseSimulator.apply_readout_channel(ideal, readout_error_rate=0.02, n_qubits=4)
    assert noisy["0000"] < 1.0
    assert "0001" in noisy or "1000" in noisy
    assert pytest.approx(sum(noisy.values()), 1e-6) == 1.0

def test_raw_count_conservation():
    ideal = {"0101": 0.6, "1010": 0.4}
    res = NoiseSimulator.run_noisy_simulation(
        ideal, noise_family="Family Z-B", gate_error_rate=0.001, readout_error_rate=0.0,
        two_qubit_gate_count=20, single_qubit_gate_count=10, n_qubits=4, shots=1024, seed=42
    )
    assert res["status"] == "VALID"
    assert sum(res["raw_counts"].values()) == 1024

def test_family_ze_not_available_without_source():
    res = NoiseSimulator.run_noisy_simulation(
        {"0000": 1.0}, noise_family="Family Z-E", calibration_source=None
    )
    assert res["status"] == "NOT_AVAILABLE"

def test_independent_evaluator_decoupled_integrity():
    cm = CanonicalModelInstance("chennai", K=5, P=10.0)
    eval_res = IndependentEvaluator.evaluate_bitstring(cm, "01010101010101", 1.7500)
    assert "original_objective" in eval_res
    assert "feasible" in eval_res
    assert isinstance(eval_res["original_objective"], float)
    assert eval_res["original_objective"] >= 0.0

def test_production_integrity_unmodified():
    prod_version_file = os.path.join(PROJECT_ROOT, "backend", "release_version.json")
    if os.path.exists(prod_version_file):
        with open(prod_version_file, "r") as f:
            data = json.load(f)
            assert data.get("version") in ["3.1.0", "3.0.0"]

def test_prohibited_terms_claim_audit():
    if os.path.exists(RESEARCH_DIR):
        report_file = os.path.join(RESEARCH_DIR, "PHASE_Z_FINAL_REPORT.md")
        if os.path.exists(report_file):
            with open(report_file, "r") as f:
                content = f.read().lower()
                assert "quantum advantage" in content
                assert "not_established" in content
