import numpy as np
import random
from typing import Dict, Any, List

class SimulatedAnnealingSolver:
    """
    Simulated Annealing (SA) Solver for Portfolio Optimization:
    - Performs stochastic search with exponential temperature decay.
    - Evaluates portfolio objectives under constraint K (swap neighborhood moves).
    - Driven by predetermined random seeds for strict Phase W comparability.
    """

    @staticmethod
    def solve(c: List[float], K: int = 5, seed: int = 42, max_iter: int = 500) -> Dict[str, Any]:
        c_arr = np.array(c, dtype=float)
        n_vars = len(c_arr)

        rng = random.Random(seed)
        np_rng = np.random.RandomState(seed)

        # Initial random K-valid solution
        initial_indices = rng.sample(range(n_vars), K)
        current_x = np.zeros(n_vars, dtype=int)
        current_x[initial_indices] = 1
        current_obj = float(c_arr @ current_x)

        best_x = np.copy(current_x)
        best_obj = current_obj

        temp = 2.0
        cooling_rate = 0.95

        for _ in range(max_iter):
            # Swap move: pick one 1-bit and one 0-bit
            ones = np.where(current_x == 1)[0]
            zeros = np.where(current_x == 0)[0]

            if len(ones) == 0 or len(zeros) == 0:
                break

            idx_out = rng.choice(ones)
            idx_in = rng.choice(zeros)

            neighbor_x = np.copy(current_x)
            neighbor_x[idx_out] = 0
            neighbor_x[idx_in] = 1

            neighbor_obj = float(c_arr @ neighbor_x)
            delta = neighbor_obj - current_obj

            # Accept if better or with Metropolis probability
            if delta > 0 or np_rng.rand() < np.exp(delta / max(temp, 1e-6)):
                current_x = neighbor_x
                current_obj = neighbor_obj

                if current_obj > best_obj:
                    best_x = np.copy(current_x)
                    best_obj = current_obj

            temp *= cooling_rate

        feasible = (int(np.sum(best_x)) == K)

        return {
            "status": "SUCCESS",
            "objective": round(best_obj, 4),
            "selected_vector": best_x.tolist(),
            "feasible": feasible,
            "seed": seed,
            "iterations": max_iter,
            "solver_type": "Simulated Annealing (Swap Neighborhood)"
        }
