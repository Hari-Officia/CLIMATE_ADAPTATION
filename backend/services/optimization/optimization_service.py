"""
Optimization Service — Phase J/K Classical Optimization
Orchestrates classical portfolio optimization, solver selection, portfolio payload generation, and immutable database persistence.
"""

import os
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime

from backend.db.database import get_db_context
from backend.db.models import OptimizationRunRecord, OptimizationResultRecord, AdaptationPortfolioRecord, PortfolioStrategyRecord
from backend.services.strategy_candidate_service import StrategyCandidateService
from backend.services.optimization.portfolio_service import PortfolioService
from backend.services.optimization.solvers.exact_solver import ExactSolver
from backend.services.optimization.solvers.milp_solver import MILPSolver
from backend.services.optimization.solvers.greedy_solver import GreedySolver

class OptimizationService:
    def __init__(self):
        self.candidate_service = StrategyCandidateService()
        self.portfolio_service = PortfolioService()
        self.exact_solver = ExactSolver()
        self.milp_solver = MILPSolver()
        self.greedy_solver = GreedySolver()

    def run_optimization(self, district_id: str, solver_id: str = "MILP_HIGHS", scenario_id: str = "BASELINE", max_k: int = 5) -> Dict[str, Any]:
        """
        Run classical optimization for a district candidate set and persist immutable run record.
        """
        district_id = district_id.lower()
        cand_set = self.candidate_service.generate_candidate_set(district_id)
        candidate_strategy_ids = cand_set["strategy_ids"]

        opt_run_id = f"OPTRUN-{district_id.upper()}-{uuid.uuid4().hex[:8]}"

        # Select Solver
        solver_id_upper = solver_id.upper()
        if solver_id_upper == "EXACT" or (len(candidate_strategy_ids) <= 15 and solver_id_upper == "EXACT"):
            solve_res = self.exact_solver.solve(candidate_strategy_ids, max_k=max_k)
        elif solver_id_upper in ["GREEDY", "GREEDY_HEURISTIC"]:
            solve_res = self.greedy_solver.solve(candidate_strategy_ids, max_k=max_k)
        else:
            solve_res = self.milp_solver.solve(candidate_strategy_ids, max_k=max_k)

        selected_ids = solve_res["selected_strategy_ids"]

        # Build Portfolio payload
        portfolio_payload = self.portfolio_service.build_portfolio_payload(
            optimization_run_id=opt_run_id,
            district_id=district_id,
            selected_strategy_ids=selected_ids,
            candidate_strategy_ids=candidate_strategy_ids,
            max_k=max_k
        )

        # Store immutable OptimizationRunRecord, AdaptationPortfolioRecord, and OptimizationResultRecord
        with get_db_context() as db:
            run_rec = OptimizationRunRecord(
                optimization_run_id=opt_run_id,
                district_id=district_id,
                candidate_set_id=cand_set["candidate_set_id"],
                methodology_id="MTH-OPT-TN-001",
                solver_id=solver_id_upper,
                scenario_id=scenario_id,
                status=solve_res["status"],
                problem_size=len(candidate_strategy_ids),
                best_objective=solve_res["objective_value"],
                optimality_gap=solve_res.get("optimality_gap"),
                runtime_ms=solve_res["runtime_ms"],
                created_at=datetime.utcnow()
            )
            db.add(run_rec)
            db.flush()

            port_rec = AdaptationPortfolioRecord(
                portfolio_id=portfolio_payload["portfolio_id"],
                optimization_run_id=opt_run_id,
                district_id=district_id,
                selected_strategy_ids=selected_ids,
                objective_value=solve_res["objective_value"],
                feasibility_status=portfolio_payload["feasibility_status"],
                hazard_coverage=portfolio_payload["hazard_coverage"],
                domain_coverage=portfolio_payload["domain_coverage"],
                sector_coverage=portfolio_payload["sector_coverage"],
                created_at=datetime.utcnow()
            )
            db.add(port_rec)
            db.flush()

            for order_idx, sid in enumerate(selected_ids, 1):
                p_strat = PortfolioStrategyRecord(
                    portfolio_id=portfolio_payload["portfolio_id"],
                    strategy_id=sid,
                    selection_order=order_idx,
                    selection_reason="Selected by classical optimizer maximizing objective function under hard constraints."
                )
                db.add(p_strat)
                
                res_rec = OptimizationResultRecord(
                    result_id=f"OPTRES-{uuid.uuid4().hex[:8]}",
                    optimization_run_id=opt_run_id,
                    strategy_id=sid,
                    selected=True,
                    objective_contribution=0.0
                )
                db.add(res_rec)

            db.commit()

        return {
            "optimization_run_id": opt_run_id,
            "district_id": district_id,
            "candidate_set_id": cand_set["candidate_set_id"],
            "methodology_id": "MTH-OPT-TN-001",
            "solver_id": solver_id_upper,
            "status": solve_res["status"],
            "runtime_ms": solve_res["runtime_ms"],
            "best_objective": solve_res["objective_value"],
            "optimality_gap": solve_res.get("optimality_gap"),
            "portfolio": portfolio_payload,
            "created_at": datetime.utcnow().isoformat()
        }

    def compare_solvers_for_district(self, district_id: str, max_k: int = 5) -> Dict[str, Any]:
        """Compare Exact, MILP, and Greedy solvers on identical district candidate set instance."""
        cand_set = self.candidate_service.generate_candidate_set(district_id.lower())
        cand_ids = cand_set["strategy_ids"]

        exact_res = self.exact_solver.solve(cand_ids, max_k=max_k)
        milp_res = self.milp_solver.solve(cand_ids, max_k=max_k)
        greedy_res = self.greedy_solver.solve(cand_ids, max_k=max_k)

        return {
            "district_id": district_id.lower(),
            "candidate_count": len(cand_ids),
            "solvers": {
                "EXACT": exact_res,
                "MILP_HIGHS": milp_res,
                "GREEDY_HEURISTIC": greedy_res
            }
        }
