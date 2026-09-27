import numpy as np
import scipy.optimize as opt
from typing import Dict, Any, List

class TrueMILPSolver:
    """
    True Binary Mixed-Integer Linear Programming (MILP) Solver:
    - Uses scipy.optimize.milp with explicit integrality = np.ones(N)
    - Enforces binary bounds [0, 1] and LinearConstraint sum(x) == K
    - Replaces prior continuous LP (scipy.optimize.linprog) usage to guarantee strict binary solutions.
    """

    @staticmethod
    def solve_binary_milp(c: List[float], K: int) -> Dict[str, Any]:
        c_arr = np.array(c, dtype=float)
        n_vars = len(c_arr)

        # scipy.optimize.milp minimizes c^T x, so negate c for maximization
        integrality = np.ones(n_vars)  # 1 indicates integer (binary) variable
        bounds = opt.Bounds(lb=np.zeros(n_vars), ub=np.ones(n_vars))
        constraint = opt.LinearConstraint(A=np.ones((1, n_vars)), lb=[K], ub=[K])

        res = opt.milp(c=-c_arr, integrality=integrality, bounds=bounds, constraints=constraint)

        if not res.success:
            return {
                "status": "FAILED",
                "milp_objective": 0.0,
                "selected_vector": [0] * n_vars,
                "feasible": False,
                "message": res.message
            }

        milp_obj = float(-res.fun)
        selected_vector = [int(round(x)) for x in res.x]
        feasible = (sum(selected_vector) == K)

        return {
            "status": "SUCCESS",
            "milp_objective": round(milp_obj, 4),
            "selected_vector": selected_vector,
            "feasible": feasible,
            "solver_type": "scipy.optimize.milp (HiGHS Integer Solver)"
        }
