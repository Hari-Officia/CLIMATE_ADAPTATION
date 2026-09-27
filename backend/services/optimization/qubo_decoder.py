"""
QUBO Decoder — Phase L Classical-to-Quantum Mathematical Bridge
Decodes binary bitstrings into strategy selections, evaluates QUBO energy Q(x, s), evaluates decoded classical objective F(x), and checks feasibility using Phase J/K ConstraintService.
"""

from typing import Dict, Any, List, Tuple
from backend.services.optimization.objective_service import ObjectiveService
from backend.services.optimization.constraint_service import ConstraintService

class QUBODecoder:
    def __init__(self):
        self.objective_service = ObjectiveService()
        self.constraint_service = ConstraintService()

    def decode_bitstring(self, bitstring: List[int], qubo_model: Dict[str, Any], max_k: int = 5) -> Dict[str, Any]:
        """
        Decode a binary bitstring [x_0, x_1, ... x_{N-1}, s_0, s_1, s_2] and calculate QUBO energy, classical objective, and feasibility.
        """
        variables = qubo_model["variable_mapping"]
        n_candidates = qubo_model["candidate_variable_count"]
        
        if len(bitstring) != len(variables):
            raise ValueError(f"Bitstring length ({len(bitstring)}) does not match variable count ({len(variables)}).")

        strategy_vars = []
        selected_strategy_ids = []
        
        for idx in range(n_candidates):
            bit = bitstring[idx]
            var_info = variables[idx]
            sid = var_info["strategy_id"]
            if bit == 1:
                strategy_vars.append(idx)
                selected_strategy_ids.append(sid)

        # Slack bit decoding
        slack_bits = bitstring[n_candidates:]
        slack_value = sum(b * (2**i) for i, b in enumerate(slack_bits))

        # 1. Calculate raw QUBO energy: Q(x, s) = sum linear_i * x_i + sum quad_{i,j} * x_i * x_j
        linear_terms = qubo_model["linear_terms"]
        quadratic_terms = qubo_model["quadratic_terms"]
        constant_offset = qubo_model["constant_offset"]

        raw_energy = 0.0
        for i_str, c_val in linear_terms.items():
            i = int(i_str)
            if bitstring[i] == 1:
                raw_energy += c_val

        for pair_str, q_val in quadratic_terms.items():
            i_str, j_str = pair_str.split(",")
            i, j = int(i_str), int(j_str)
            if bitstring[i] == 1 and bitstring[j] == 1:
                raw_energy += q_val

        total_energy = round(raw_energy + constant_offset, 6)

        # 2. Evaluate decoded classical objective F(x) from original Phase J/K ObjectiveService
        # Note: qubo_model candidate list is sorted strategy_ids
        candidate_strategy_ids = [v["strategy_id"] for v in variables[:n_candidates]]
        decoded_classical_objective = self.objective_service.evaluate_portfolio_objective(
            selected_strategy_ids=selected_strategy_ids,
            candidate_strategy_ids=candidate_strategy_ids
        )

        # 3. Evaluate feasibility using original Phase J/K ConstraintService
        feas_res = self.constraint_service.validate_portfolio_feasibility(
            selected_strategy_ids=selected_strategy_ids,
            max_k=max_k
        )

        # 4. Penalty value = Total Energy - (-F(x)) = Total Energy + F(x)
        calculated_penalty = round(total_energy + decoded_classical_objective, 6)
        if abs(calculated_penalty) < 1e-5:
            calculated_penalty = 0.0

        return {
            "bitstring": bitstring,
            "selected_strategy_ids": selected_strategy_ids,
            "selected_count": len(selected_strategy_ids),
            "slack_value": slack_value,
            "raw_energy": round(raw_energy, 6),
            "constant_offset": round(constant_offset, 6),
            "total_energy": total_energy,
            "decoded_classical_objective": decoded_classical_objective,
            "penalty_value": calculated_penalty,
            "feasible": feas_res["feasible"],
            "violations": feas_res["violations"]
        }
