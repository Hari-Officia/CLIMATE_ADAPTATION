"""
QAOA Benchmark Engine — Phase M Enterprise QAOA
Executes multi-algorithm benchmarking (Exact, MILP, Greedy vs QAOA p=1,2,3) across representative districts of Tamil Nadu.
Measures objective values, optimality gaps, feasibility probabilities, execution runtimes, gate counts, and persists benchmark metrics.
"""

import time
import uuid
from typing import Dict, Any, List
from datetime import datetime

from backend.db.database import get_db_context
from backend.db.models import QAOABenchmarkRecord
from backend.services.optimization.solvers.exact_solver import ExactSolver
from backend.services.optimization.solvers.milp_solver import MILPSolver
from backend.services.optimization.solvers.greedy_solver import GreedySolver
from backend.services.optimization.qaoa.qaoa_solver import QAOASolver

class QAOABenchmarkEngine:
    def __init__(self):
        self.exact_solver = ExactSolver()
        self.milp_solver = MILPSolver()
        self.greedy_solver = GreedySolver()
        self.qaoa_solver = QAOASolver()

    def run_benchmark(
        self,
        district_id: str,
        max_k: int = 5,
        p_depths: List[int] = [1, 2, 3],
        shots: int = 1000,
        seed: int = 42,
        persist: bool = True
    ) -> Dict[str, Any]:
        """
        Run multi-algorithm classical-vs-QAOA benchmark on candidate instance.
        """
        district_id = district_id.lower()
        cand_set = self.qaoa_solver.qubo_builder.candidate_service.generate_candidate_set(district_id)
        cand_ids = sorted(cand_set["strategy_ids"])

        # 1. Classical Baselines
        exact_res = self.exact_solver.solve(cand_ids, max_k=max_k)
        milp_res = self.milp_solver.solve(cand_ids, max_k=max_k)
        greedy_res = self.greedy_solver.solve(cand_ids, max_k=max_k)

        classical_best_obj = exact_res["objective_value"]

        # 2. QAOA Depths Benchmarks
        qaoa_results = []
        for p in p_depths:
            qaoa_res = self.qaoa_solver.run_qaoa(
                district_id=district_id,
                max_k=max_k,
                qaoa_depth_p=p,
                shots=shots,
                seed=seed,
                persist=persist
            )

            bench_id = f"BM-{district_id.upper()}-P{p}-{uuid.uuid4().hex[:6]}"
            bench_summary = {
                "benchmark_id": bench_id,
                "district_id": district_id,
                "qubo_id": qaoa_res["qubo_id"],
                "logical_qubits": qaoa_res["logical_qubit_count"],
                "qaoa_depth_p": p,
                "shots": shots,
                "seed": seed,
                "exact_objective": classical_best_obj,
                "milp_objective": milp_res["objective_value"],
                "greedy_objective": greedy_res["objective_value"],
                "qaoa_objective": qaoa_res["best_sample_objective"],
                "objective_gap": qaoa_res["objective_gap"],
                "relative_gap": qaoa_res["relative_objective_gap"],
                "feasible_probability": qaoa_res["feasible_probability"],
                "optimal_probability": qaoa_res["optimal_probability"],
                "exact_runtime_ms": exact_res["runtime_ms"],
                "milp_runtime_ms": milp_res["runtime_ms"],
                "greedy_runtime_ms": greedy_res["runtime_ms"],
                "qaoa_total_time_sec": qaoa_res["total_time_sec"],
                "circuit_depth": qaoa_res["circuit_metrics"]["depth"],
                "two_qubit_gates": qaoa_res["circuit_metrics"]["two_qubit_gate_count"],
                "status": "VERIFIED"
            }

            qaoa_results.append(bench_summary)

            if persist:
                with get_db_context() as db:
                    bm_rec = QAOABenchmarkRecord(
                        benchmark_id=bench_id,
                        district_id=district_id,
                        qubo_id=qaoa_res["qubo_id"],
                        qubit_count=qaoa_res["logical_qubit_count"],
                        classical_method="EXACT_ENUMERATION",
                        qaoa_p=p,
                        shots=shots,
                        seed=seed,
                        classical_objective=classical_best_obj,
                        qaoa_objective=qaoa_res["best_sample_objective"],
                        objective_gap=qaoa_res["objective_gap"],
                        feasible_probability=qaoa_res["feasible_probability"],
                        optimal_probability=qaoa_res["optimal_probability"],
                        runtime_ms=round(qaoa_res["total_time_sec"] * 1000.0, 2),
                        circuit_depth=qaoa_res["circuit_metrics"]["depth"],
                        two_qubit_gates=qaoa_res["circuit_metrics"]["two_qubit_gate_count"],
                        status="VERIFIED"
                    )
                    db.add(bm_rec)
                    db.commit()

        return {
            "district_id": district_id,
            "candidate_count": len(cand_ids),
            "classical_baselines": {
                "EXACT": exact_res,
                "MILP": milp_res,
                "GREEDY": greedy_res
            },
            "qaoa_benchmarks": qaoa_results
        }
