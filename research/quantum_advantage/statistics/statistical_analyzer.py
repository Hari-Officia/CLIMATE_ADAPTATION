import numpy as np
from typing import List, Dict, Any

class StatisticalAnalyzer:
    """
    Multi-Seed Statistical Analyzer for Quantum Advantage Evaluation (Protocol v2):
    - Filters strictly VALID QAOA runs (excludes INVALID_OR_INCOMPLETE).
    - Computes exact objective gaps without artificial clamping (np.maximum removed).
    - Calculates mean, median, std, percentiles, and 95% Bootstrap CIs.
    - Measures true empirical optimal bitstring sample probability.
    """

    @staticmethod
    def calculate_objective_gap(
        best_known_objective: float,
        qaoa_objective: float,
        direction: str = "MAXIMIZATION"
    ) -> float:
        """Calculates exact normalized objective gap for MAXIMIZATION or MINIMIZATION."""
        norm = max(abs(best_known_objective), 1.0)
        if direction.upper() == "MAXIMIZATION":
            raw_diff = best_known_objective - qaoa_objective
            if qaoa_objective > best_known_objective + 1e-4:
                # Anomaly detection: QAOA exceeds exact MILP
                print(f"[OBJECTIVE_VALIDATION_ANOMALY] QAOA obj ({qaoa_objective}) > MILP ({best_known_objective})")
            return float(raw_diff / norm)
        else:
            raw_diff = qaoa_objective - best_known_objective
            return float(raw_diff / norm)

    @staticmethod
    def analyze_runs(runs: List[Dict[str, Any]], classical_optimum: float) -> Dict[str, Any]:
        """Analyzes a series of stochastic QAOA experiment runs."""
        valid_runs = [r for r in runs if r.get("status") == "VALID" and r.get("best_objective") is not None]
        invalid_runs = [r for r in runs if r.get("status") != "VALID" or r.get("best_objective") is None]
        
        if not valid_runs:
            return {
                "n_samples": 0,
                "valid_runs": 0,
                "invalid_runs": len(invalid_runs),
                "classical_optimum": float(classical_optimum),
                "mean_objective": None,
                "std_objective": None,
                "min_objective": None,
                "max_objective": None,
                "mean_feasibility": 0.0,
                "mean_runtime_seconds": 0.0,
                "mean_objective_gap": None,
                "median_objective_gap": None,
                "gap_ci_95": None,
                "optimal_probability": 0.0,
                "mean_optimal_probability": 0.0,
                "cohens_d_vs_exact": None,
                "status": "ALL_RUNS_INVALID"
            }
            
        objectives = np.array([float(r["best_objective"]) for r in valid_runs])
        feasibilities = np.array([float(r.get("feasible_probability", 0.0)) for r in valid_runs])
        opt_probs = np.array([float(r.get("optimal_probability", 0.0)) for r in valid_runs])
        runtimes = np.array([float(r.get("runtime_seconds", 0.0)) for r in valid_runs])
        
        # Calculate objective gaps relative to classical_optimum without clamping
        gaps = np.array([
            StatisticalAnalyzer.calculate_objective_gap(classical_optimum, float(r["best_objective"]), "MAXIMIZATION")
            for r in valid_runs
        ])
        
        # 95% Bootstrap Confidence Intervals for Gap
        n_boot = 1000
        boot_means = []
        rng = np.random.RandomState(42)
        for _ in range(n_boot):
            sample = rng.choice(gaps, size=len(gaps), replace=True)
            boot_means.append(np.mean(sample))
        ci_lower, ci_upper = np.percentile(boot_means, [2.5, 97.5])
        
        return {
            "n_samples": len(valid_runs),
            "valid_runs": len(valid_runs),
            "invalid_runs": len(invalid_runs),
            "classical_optimum": float(classical_optimum),
            "mean_objective": float(np.mean(objectives)),
            "std_objective": float(np.std(objectives)),
            "min_objective": float(np.min(objectives)),
            "max_objective": float(np.max(objectives)),
            "mean_feasibility": float(np.mean(feasibilities)),
            "median_feasibility": float(np.median(feasibilities)),
            "mean_runtime_seconds": float(np.mean(runtimes)),
            "mean_objective_gap": float(np.mean(gaps)),
            "median_objective_gap": float(np.median(gaps)),
            "gap_ci_95": [float(ci_lower), float(ci_upper)],
            "optimal_probability": float(np.max(opt_probs)),
            "mean_optimal_probability": float(np.mean(opt_probs)),
            "cohens_d_vs_exact": float((np.mean(objectives) - classical_optimum) / (np.std(objectives) + 1e-8)),
            "status": "VALID"
        }
