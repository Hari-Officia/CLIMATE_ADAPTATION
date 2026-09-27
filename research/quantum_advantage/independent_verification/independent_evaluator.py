import numpy as np
from typing import Dict, Any, List
from research.quantum_advantage.instances.canonical_model import CanonicalModelInstance

class IndependentEvaluator:
    """
    Independent Objective & Constraint Evaluator (Phase T):
    - Completely decoupled from QAOASolver, MILP, or StatisticalAnalyzer internal methods.
    - Decodes raw bitstrings directly using CanonicalModelInstance.
    - Evaluates original climate adaptation objective (MAXIMIZATION).
    - Checks feasibility constraints (sum(x) == K).
    - Calculates two-sided un-clamped objective gap: (MILP - QAOA) / MILP.
    """

    @staticmethod
    def evaluate_bitstring(
        canonical_instance: CanonicalModelInstance,
        raw_bitstring: str,
        milp_objective: float
    ) -> Dict[str, Any]:
        c = canonical_instance.linear_weights
        Q = canonical_instance.qubo_matrix
        K = canonical_instance.K
        n_vars = canonical_instance.N
        
        candidate_bits = raw_bitstring[:n_vars]
        x = np.array([int(b) for b in candidate_bits])
        
        selected_ids = [canonical_instance.strategy_ids[i] for i, b in enumerate(x) if b == 1]
        selected_count = int(np.sum(x))
        feasible = (selected_count == K)
        
        orig_obj = float(c @ x)
        qubo_energy = float(x.T @ Q @ x)
        
        norm = max(abs(milp_objective), 1.0)
        raw_diff = milp_objective - orig_obj
        gap = float(raw_diff / norm)
        
        is_opt = feasible and abs(orig_obj - milp_objective) < 1e-4
        
        return {
            "instance_hash": canonical_instance.instance_hash,
            "raw_bitstring": raw_bitstring,
            "selected_strategy_ids": selected_ids,
            "selected_count": selected_count,
            "feasible": feasible,
            "original_objective": orig_obj,
            "qubo_energy": qubo_energy,
            "milp_objective": milp_objective,
            "objective_gap": gap,
            "is_optimal": is_opt,
            "status": "VALID" if feasible else "FEASIBILITY_VIOLATED"
        }
