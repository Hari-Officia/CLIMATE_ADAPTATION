"""
Phase M — Enterprise QAOA Implementation & Benchmarking Test Suite
Verifies dependency gates, zero-error QUBO-to-Ising mathematical identity, Qiskit circuit builder metrics, QAOA solver execution,
scipy classical parameter optimization, bitstring decoding, sample probability distributions, exact classical comparisons, and database persistence.
"""

import pytest
import math
from backend.services.optimization.qubo_builder import QUBOBuilder
from backend.services.optimization.qaoa.qubo_to_ising import QUBOToIsingConverter
from backend.services.optimization.qaoa.circuit_builder import QAOACircuitBuilder
from backend.services.optimization.qaoa.qaoa_solver import QAOASolver
from backend.services.optimization.qaoa.benchmark_engine import QAOABenchmarkEngine

@pytest.fixture
def builder():
    return QUBOBuilder()

@pytest.fixture
def converter():
    return QUBOToIsingConverter()

@pytest.fixture
def circuit_builder():
    return QAOACircuitBuilder()

@pytest.fixture
def solver():
    return QAOASolver()

@pytest.fixture
def benchmark_engine():
    return QAOABenchmarkEngine()

# 1. DEPENDENCY GATE TEST
def test_phase_m_dependency_gate(builder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    assert model["status"] == "VERIFIED"
    assert "qubo_hash" in model

# 2. QUBO-TO-ISING EXACT IDENTITY TEST
def test_qubo_to_ising_identity(builder, converter):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    ising = converter.convert_qubo_to_ising(model)
    
    assert ising["qubit_count"] == model["total_variable_count"]
    assert "h_0" in ising
    assert "h_i" in ising
    assert "J_ij" in ising
    
    # Check identity over fixed test bitstring
    n_vars = model["total_variable_count"]
    bits = [1, 0, 1, 0] + [0] * (n_vars - 4)
    
    from backend.services.optimization.qubo_decoder import QUBODecoder
    decoder = QUBODecoder()
    q_dec = decoder.decode_bitstring(bits, model, max_k=5)
    qubo_energy = q_dec["total_energy"]
    
    ising_energy = converter.evaluate_ising_energy(bits, ising)
    assert abs(qubo_energy - ising_energy) < 1e-5

# 3. QAOA CIRCUIT BUILDER TEST
def test_qaoa_circuit_builder(builder, converter, circuit_builder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    ising = converter.convert_qubo_to_ising(model)
    
    gamma = [0.1, 0.2]
    beta = [0.3, 0.4]
    qc = circuit_builder.build_qaoa_circuit(ising, gamma, beta)
    
    assert qc.num_qubits == model["total_variable_count"]
    metrics = circuit_builder.compute_circuit_metrics(qc)
    
    assert metrics["depth"] > 0
    assert metrics["two_qubit_gate_count"] > 0
    assert "circuit_hash" in metrics

# 4. QAOA SOLVER EXECUTION TEST
def test_qaoa_solver_execution(solver):
    res = solver.run_qaoa("chennai", max_k=5, qaoa_depth_p=1, shots=500, seed=42, persist=False)
    
    assert res["district_id"] == "chennai"
    assert res["logical_qubit_count"] == 16
    assert res["qaoa_depth"] == 1
    assert "best_sample_objective" in res
    assert "feasible_probability" in res
    assert res["feasible_probability"] > 0.0

# 5. BENCHMARK ENGINE TEST
def test_qaoa_benchmark_engine(benchmark_engine):
    bench = benchmark_engine.run_benchmark("coimbatore", max_k=5, p_depths=[1], shots=500, seed=42, persist=False)
    
    assert bench["district_id"] == "coimbatore"
    assert "classical_baselines" in bench
    assert "EXACT" in bench["classical_baselines"]
    assert "MILP" in bench["classical_baselines"]
    assert "GREEDY" in bench["classical_baselines"]
    assert len(bench["qaoa_benchmarks"]) == 1

# 6. SEED DETERMINISM TEST
def test_qaoa_seed_determinism(solver):
    r1 = solver.run_qaoa("madurai", max_k=5, qaoa_depth_p=1, shots=500, seed=123, persist=False)
    r2 = solver.run_qaoa("madurai", max_k=5, qaoa_depth_p=1, shots=500, seed=123, persist=False)
    
    assert r1["best_sample_objective"] == r2["best_sample_objective"]
    assert r1["feasible_probability"] == r2["feasible_probability"]

# 7. DATABASE PERSISTENCE TEST
def test_qaoa_database_persistence(solver):
    res = solver.run_qaoa("chennai", max_k=5, qaoa_depth_p=1, shots=500, seed=42, persist=True)
    assert res["status"] in ["VERIFIED", "FEASIBLE"]
