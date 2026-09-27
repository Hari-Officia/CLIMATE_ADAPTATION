"""
Greedy Heuristic Solver — Phase J/K Classical Optimization
Iteratively selects strategy with highest marginal objective gain while respecting portfolio feasibility constraints.
"""

import time
from typing import Dict, Any, List
from backend.services.optimization.objective_service import ObjectiveService
from backend.services.optimization.constraint_service import ConstraintService

class GreedySolver:
    def __init__(self):
        self.objective_service = ObjectiveService()
        self.constraint_service = ConstraintService()

    def solve(self, candidate_strategy_ids: List[str], max_k: int = 5) -> Dict[str, Any]:
        """
        Greedy marginal gain strategy selection algorithm.
        """
        start_time = time.time()
        selected_ids = []
        remaining = list(candidate_strategy_ids)

        while len(selected_ids) < max_k and len(remaining) > 0:
            best_cand = None
            best_gain = -1.0

            curr_obj = self.objective_service.evaluate_portfolio_objective(selected_ids, candidate_strategy_ids)

            for cand in remaining:
                test_portfolio = selected_ids + [cand]
                feas = self.constraint_service.validate_portfolio_feasibility(test_portfolio, max_k=max_k)
                if feas["feasible"]:
                    test_obj = self.objective_service.evaluate_portfolio_objective(test_portfolio, candidate_strategy_ids)
                    gain = test_obj - curr_obj
                    if gain > best_gain:
                        best_gain = gain
                        best_cand = cand

            if best_cand is not None and best_gain > 0:
                selected_ids.append(best_cand)
                remaining.remove(best_cand)
            else:
                break

        runtime_ms = round((time.time() - start_time) * 1000, 2)
        obj_val = self.objective_service.evaluate_portfolio_objective(selected_ids, candidate_strategy_ids)

        return {
            "solver_id": "GREEDY_HEURISTIC",
            "selected_strategy_ids": selected_ids,
            "objective_value": round(obj_val, 4),
            "optimality_gap": None,
            "problem_size": len(candidate_strategy_ids),
            "runtime_ms": runtime_ms,
            "status": "FEASIBLE"
        }
