"""
QAOA Circuit Builder — Phase M Enterprise QAOA
Builds parameterized QAOA quantum circuits using Qiskit 2.5+ for p layers of cost U_C(gamma) and mixer U_M(beta) evolution.
Computes exact gate counts, CNOT counts, circuit depth, and transpiled metrics.
"""

import hashlib
import json
from typing import Dict, Any, List, Tuple
import numpy as np

import qiskit
from qiskit import QuantumCircuit
from qiskit.compiler import transpile

class QAOACircuitBuilder:
    def __init__(self):
        pass

    def build_qaoa_circuit(self, ising_model: Dict[str, Any], gamma: List[float], beta: List[float]) -> QuantumCircuit:
        """
        Construct parameterized QAOA circuit for p layers.
        gamma = [gamma_1, ..., gamma_p]
        beta = [beta_1, ..., beta_p]
        """
        p = len(gamma)
        if len(beta) != p:
            raise ValueError(f"Gamma length ({p}) does not match Beta length ({len(beta)}).")

        n_qubits = ising_model["qubit_count"]
        h_i = ising_model["h_i"]
        J_ij = ising_model["J_ij"]

        qc = QuantumCircuit(n_qubits, n_qubits)

        # 1. Hadamard initial superposition state |+>^N
        qc.h(range(n_qubits))

        # 2. Apply p layers of Cost Unitary U_C(gamma) and Mixer Unitary U_M(beta)
        for layer in range(p):
            g = float(gamma[layer])
            b = float(beta[layer])

            # Cost Unitary U_C(gamma) = exp(-i * gamma * H_C)
            # Single-qubit Z terms: exp(-i * gamma * h_i * Z_i) -> RZ(2 * gamma * h_i)
            for i_str, h_val in h_i.items():
                i = int(i_str)
                angle = 2.0 * g * float(h_val)
                qc.rz(angle, i)

            # Two-qubit ZZ terms: exp(-i * gamma * J_ij * Z_i * Z_j) -> CX(i, j), RZ(2 * gamma * J_ij, j), CX(i, j)
            for pair_str, j_val in J_ij.items():
                i_str, j_str = pair_str.split(",")
                i, j = int(i_str), int(j_str)
                angle = 2.0 * g * float(j_val)
                qc.cx(i, j)
                qc.rz(angle, j)
                qc.cx(i, j)

            # Mixer Unitary U_M(beta) = exp(-i * beta * sum X_i) -> RX(2 * beta) on all qubits
            for i in range(n_qubits):
                qc.rx(2.0 * b, i)

        # 3. Measurement
        qc.measure(range(n_qubits), range(n_qubits))
        return qc

    def compute_circuit_metrics(self, qc: QuantumCircuit) -> Dict[str, Any]:
        """
        Extract total gate count, CNOT count, circuit depth, and deterministic hash.
        """
        depth = qc.depth()
        dict_ops = qc.count_ops()
        total_gates = sum(dict_ops.values()) - dict_ops.get("measure", 0)
        cnot_count = dict_ops.get("cx", 0)

        # Compute circuit hash
        qasm_str = str(qc)
        circuit_hash = hashlib.sha256(qasm_str.encode("utf-8")).hexdigest()

        return {
            "qubit_count": qc.num_qubits,
            "depth": depth,
            "gate_count": total_gates,
            "two_qubit_gate_count": cnot_count,
            "ops": dict(dict_ops),
            "circuit_hash": circuit_hash
        }
