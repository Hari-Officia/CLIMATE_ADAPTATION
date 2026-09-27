import numpy as np
from typing import Dict, Any, List

class GreedySolver:
    """
    Deterministic Greedy Portfolio Optimization Solver:
    - Selects the top K strategies with highest linear objective coefficients c_i.
    - Used as a fast classical heuristic baseline for Phase W comparison.
    """

    @staticmethod
    def solve(c: List[float], K: int = 5) -> Dict[str, Any]:
        c_arr = np.array(c, dtype=float)
        n_vars = len(c_arr)

        # Sort indices by coefficient descending
        sorted_indices = np.argsort(-c_arr)
        top_k_indices = sorted_indices[:K]

        x = [0] * n_vars
        for idx in top_k_indices:
            x[idx] = 1

        obj = float(np.sum(c_arr[top_k_indices]))
        feasible = (sum(x) == K)

        return {
            "status": "SUCCESS",
            "objective": round(obj, 4),
            "selected_vector": x,
            "feasible": feasible,
            "solver_type": "Deterministic Greedy Selector"
        }
