"""
QUBO to Ising Converter — Phase M Enterprise QAOA
Converts QUBO models Q(x) into Pauli-Z Ising Hamiltonians H(Z) = h_0 + sum h_i Z_i + sum J_ij Z_i Z_j.
Uses the exact algebraic identity x_i = (1 - Z_i)/2 to ensure zero conversion error.
"""

from typing import Dict, Any, Tuple, List

class QUBOToIsingConverter:
    @staticmethod
    def convert_qubo_to_ising(qubo_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert QUBO model into Ising Hamiltonian coefficients (h_0, h_i, J_ij).
        """
        total_vars = qubo_model["total_variable_count"]
        linear_terms = qubo_model["linear_terms"] # {str(i): float}
        quadratic_terms = qubo_model["quadratic_terms"] # {"i,j": float}
        constant_offset = qubo_model["constant_offset"]

        # Parse numeric keys
        a_coeffs: Dict[int, float] = {int(k): float(v) for k, v in linear_terms.items()}
        b_coeffs: Dict[Tuple[int, int], float] = {}
        for pair_str, val in quadratic_terms.items():
            i_str, j_str = pair_str.split(",")
            i, j = int(i_str), int(j_str)
            u, v = (i, j) if i < j else (j, i)
            b_coeffs[(u, v)] = float(val)

        # 1. Compute h_0 (Ising constant offset)
        h_0 = float(constant_offset)
        for i in range(total_vars):
            h_0 += 0.5 * a_coeffs.get(i, 0.0)

        for (i, j), b_ij in b_coeffs.items():
            h_0 += 0.25 * b_ij

        # 2. Compute h_i (single-qubit Z coefficients)
        h_i: Dict[int, float] = {}
        for i in range(total_vars):
            h_val = -0.5 * a_coeffs.get(i, 0.0)
            
            # Contribution from b_ij where i < j
            for j in range(i + 1, total_vars):
                if (i, j) in b_coeffs:
                    h_val -= 0.25 * b_coeffs[(i, j)]
            
            # Contribution from b_ji where j < i
            for j in range(0, i):
                if (j, i) in b_coeffs:
                    h_val -= 0.25 * b_coeffs[(j, i)]
            
            if abs(h_val) > 1e-12:
                h_i[i] = round(h_val, 8)

        # 3. Compute J_ij (two-qubit ZZ coupling coefficients)
        J_ij: Dict[Tuple[int, int], float] = {}
        for (i, j), b_val in b_coeffs.items():
            j_val = 0.25 * b_val
            if abs(j_val) > 1e-12:
                J_ij[(i, j)] = round(j_val, 8)

        return {
            "qubo_id": qubo_model["qubo_id"],
            "district_id": qubo_model["district_id"],
            "qubit_count": total_vars,
            "h_0": round(h_0, 8),
            "h_i": h_i,
            "J_ij": {f"{k[0]},{k[1]}": v for k, v in J_ij.items()},
            "convention": "PAULI_Z_EIGENVALUE_1_MINUS_2X"
        }

    @staticmethod
    def evaluate_ising_energy(bitstring: List[int], ising_model: Dict[str, Any]) -> float:
        """
        Evaluate Ising energy H(Z) for bitstring x in {0, 1}^N where Z_i = 1 - 2*x_i.
        """
        h_0 = ising_model["h_0"]
        h_i = ising_model["h_i"]
        J_ij = ising_model["J_ij"]

        # Z_i = 1 - 2*x_i -> bit 0 gives Z_i = +1, bit 1 gives Z_i = -1
        Z = [1.0 - 2.0 * float(b) for b in bitstring]

        energy = h_0
        for i_str, h_val in h_i.items():
            i = int(i_str)
            energy += h_val * Z[i]

        for pair_str, j_val in J_ij.items():
            i_str, j_str = pair_str.split(",")
            i, j = int(i_str), int(j_str)
            energy += j_val * Z[i] * Z[j]

        return round(energy, 8)
