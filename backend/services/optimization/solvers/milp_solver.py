"""
HiGHS MILP Solver — Phase J/K Classical Optimization
Solves mixed-integer linear programming portfolio optimization using scipy.optimize.milp.
"""

import time
import numpy as np
from typing import Dict, Any, List
from scipy.optimize import milp, LinearConstraint, Bounds
from backend.services.optimization.objective_service import ObjectiveService
from backend.services.optimization.constraint_service import ConstraintService

class MILPSolver:
    def __init__(self):
        self.objective_service = ObjectiveService()
        self.constraint_service = ConstraintService()

    def solve(self, candidate_strategy_ids: List[str], max_k: int = 5) -> Dict[str, Any]:
        """
        Formulate MILP and solve using scipy.optimize.milp (HiGHS backend).
        """
        start_time = time.time()
        n = len(candidate_strategy_ids)
        if n == 0:
            return {
                "solver_id": "MILP_HIGHS",
                "selected_strategy_ids": [],
                "objective_value": 0.0,
                "optimality_gap": 0.0,
                "problem_size": 0,
                "runtime_ms": 0.0,
                "status": "FEASIBLE"
            }

        # 1. Objective Vector c (scipy milp minimizes c^T x, so negate for maximization)
        c_vals = self.objective_service.build_objective_coefficients(candidate_strategy_ids)
        c = -np.array(c_vals, dtype=float)

        # 2. Variable Bounds (0 <= x_i <= 1) and Integrality (1 = integer/binary)
        bounds = Bounds(0, 1)
        integrality = np.ones(n, dtype=int)

        # 3. Build Constraints Matrix
        # Constraint 1: sum(x_i) <= K
        A_rows = [np.ones(n, dtype=float)]
        lb_rows = [0.0]
        ub_rows = [float(max_k)]

        # Constraint 2: Conflicts x_i + x_j <= 1
        conflicts = self.constraint_service.get_conflict_pairs(candidate_strategy_ids)
        for i, j in conflicts:
            row = np.zeros(n, dtype=float)
            row[i] = 1.0
            row[j] = 1.0
            A_rows.append(row)
            lb_rows.append(-np.inf)
            ub_rows.append(1.0)

        # Constraint 3: Dependencies x_A - x_B <= 0
        dependencies = self.constraint_service.get_dependency_pairs(candidate_strategy_ids)
        for idx_a, idx_b in dependencies:
            row = np.zeros(n, dtype=float)
            row[idx_a] = 1.0
            row[idx_b] = -1.0
            A_rows.append(row)
            lb_rows.append(-np.inf)
            ub_rows.append(0.0)

        A_mat = np.vstack(A_rows)
        constraints = LinearConstraint(A_mat, lb_rows, ub_rows)

        # 4. Solve MILP
        res = milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints)
        runtime_ms = round((time.time() - start_time) * 1000, 2)

        if res.success:
            x_sol = np.round(res.x).astype(int)
            selected_ids = [candidate_strategy_ids[i] for i in range(n) if x_sol[i] == 1]
            
            # Recalculate exact objective with pairwise bonuses
            exact_obj = self.objective_service.evaluate_portfolio_objective(selected_ids, candidate_strategy_ids)

            return {
                "solver_id": "MILP_HIGHS",
                "selected_strategy_ids": selected_ids,
                "objective_value": round(exact_obj, 4),
                "optimality_gap": 0.0,
                "problem_size": n,
                "runtime_ms": runtime_ms,
                "status": "OPTIMAL"
            }
        else:
            return {
                "solver_id": "MILP_HIGHS",
                "selected_strategy_ids": [],
                "objective_value": 0.0,
                "optimality_gap": None,
                "problem_size": n,
                "runtime_ms": runtime_ms,
                "status": "INFEASIBLE"
            }
