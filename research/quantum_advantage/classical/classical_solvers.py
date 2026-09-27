import time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from typing import Dict, Any, List, Tuple

class ClassicalSolvers:
    """
    Classical Baselines for Quantum Advantage Research Track:
    1. Exact Enumeration (Full binary search, feasible for N <= 20)
    2. HIGHS MILP (SciPy Branch-and-Cut MILP, Production Authoritative)
    3. Greedy Solver (Heuristic greedy ranking)
    4. Simulated Annealing (Metaheuristic QUBO solver)
    """

    @staticmethod
    def solve_exact(Q: np.ndarray, K: int) -> Dict[str, Any]:
        """Exact enumeration solver."""
        t0 = time.perf_counter()
        n = len(Q)
        best_obj = float('inf')
        best_x = None
        
        # Enumerate all 2^N bitstrings
        for i in range(1 << n):
            x = np.array([(i >> j) & 1 for j in range(n)])
            obj = float(x.T @ Q @ x)
            if obj < best_obj:
                best_obj = obj
                best_x = x
                
        t1 = time.perf_counter()
        feasible = (int(np.sum(best_x)) == K)
        
        return {
            "solver_name": "EXACT_ENUMERATION",
            "objective": float(best_obj),
            "bitstring": "".join(map(str, best_x)),
            "selected_variables": [int(idx) for idx, v in enumerate(best_x) if v == 1],
            "feasible": feasible,
            "runtime_seconds": t1 - t0
        }

    @staticmethod
    def solve_milp(c: np.ndarray, K: int) -> Dict[str, Any]:
        """SciPy HIGHS MILP exact solver (authoritative reference)."""
        t0 = time.perf_counter()
        n = len(c)
        # Minimize -c^T x subject to sum(x) == K
        c_cost = -c
        constraints = LinearConstraint(A=np.ones((1, n)), lb=K, ub=K)
        integrality = np.ones(n) # Binary
        bounds = Bounds(lb=0, ub=1)
        
        res = milp(c=c_cost, integrality=integrality, constraints=constraints, bounds=bounds)
        t1 = time.perf_counter()
        
        if res.success:
            x_sol = np.round(res.x).astype(int)
            # Original maximization objective = c^T x
            orig_obj = float(c @ x_sol)
            return {
                "solver_name": "HIGHS_MILP",
                "status": "OPTIMAL_EXACT",
                "objective": orig_obj,
                "bitstring": "".join(map(str, x_sol)),
                "selected_variables": [int(idx) for idx, v in enumerate(x_sol) if v == 1],
                "feasible": True,
                "optimality_gap": 0.0000,
                "runtime_seconds": t1 - t0
            }
        else:
            return {
                "solver_name": "HIGHS_MILP",
                "status": "FAILED",
                "objective": float('-inf'),
                "bitstring": "0" * n,
                "selected_variables": [],
                "feasible": False,
                "optimality_gap": 1.0,
                "runtime_seconds": t1 - t0
            }

    @staticmethod
    def solve_greedy(c: np.ndarray, K: int) -> Dict[str, Any]:
        """Greedy heuristic solver."""
        t0 = time.perf_counter()
        n = len(c)
        top_indices = np.argsort(-c)[:K]
        x_sol = np.zeros(n, dtype=int)
        x_sol[top_indices] = 1
        t1 = time.perf_counter()
        
        return {
            "solver_name": "GREEDY_HEURISTIC",
            "objective": float(c @ x_sol),
            "bitstring": "".join(map(str, x_sol)),
            "selected_variables": [int(idx) for idx in top_indices],
            "feasible": True,
            "runtime_seconds": t1 - t0
        }

    @staticmethod
    def solve_simulated_annealing(Q: np.ndarray, K: int, steps: int = 1000, seed: int = 42) -> Dict[str, Any]:
        """Simulated Annealing QUBO metaheuristic solver."""
        t0 = time.perf_counter()
        rng = np.random.RandomState(seed)
        n = len(Q)
        
        # Start with random bitstring
        x = rng.randint(0, 2, size=n)
        current_obj = float(x.T @ Q @ x)
        best_x = x.copy()
        best_obj = current_obj
        
        T = 100.0
        alpha = 0.99
        
        for step in range(steps):
            # Flip random bit
            idx = rng.randint(0, n)
            x_next = x.copy()
            x_next[idx] = 1 - x_next[idx]
            next_obj = float(x_next.T @ Q @ x_next)
            
            delta = next_obj - current_obj
            if delta < 0 or rng.rand() < np.exp(-delta / T):
                x = x_next
                current_obj = next_obj
                if current_obj < best_obj:
                    best_obj = current_obj
                    best_x = x.copy()
            T *= alpha
            
        t1 = time.perf_counter()
        feasible = (int(np.sum(best_x)) == K)
        
        return {
            "solver_name": "SIMULATED_ANNEALING",
            "objective": float(best_obj),
            "bitstring": "".join(map(str, best_x)),
            "selected_variables": [int(idx) for idx, v in enumerate(best_x) if v == 1],
            "feasible": feasible,
            "runtime_seconds": t1 - t0
        }
