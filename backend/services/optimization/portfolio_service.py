"""
Portfolio Service — Phase J/K Classical Optimization
Formats AdaptationPortfolio payloads, calculates domain/sector/hazard coverage, and builds structured explanation objects.
"""

import os
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime
from backend.services.optimization.objective_service import ObjectiveService
from backend.services.optimization.constraint_service import ConstraintService

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "master")

class PortfolioService:
    def __init__(self):
        self.objective_service = ObjectiveService()
        self.constraint_service = ConstraintService()
        self.strategies = self._load_json("strategies.json")

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        path = os.path.join(CONFIG_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def build_portfolio_payload(self, optimization_run_id: str, district_id: str, selected_strategy_ids: List[str], candidate_strategy_ids: List[str], max_k: int = 5) -> Dict[str, Any]:
        """Build full contract-compliant AdaptationPortfolio object."""
        obj_val = self.objective_service.evaluate_portfolio_objective(selected_strategy_ids, candidate_strategy_ids)
        feas_res = self.constraint_service.validate_portfolio_feasibility(selected_strategy_ids, max_k=max_k)

        hazard_coverage = set()
        domain_coverage = set()
        sector_coverage = set()

        for sid in selected_strategy_ids:
            strat = next((s for s in self.strategies if s["strategy_id"] == sid), None)
            if strat:
                hazard_coverage.add(strat.get("primary_hazard_id", "HAZ-FLD"))
                domain_coverage.add(strat.get("domain_id", "DOM-DRN"))
                for sec in strat.get("sector_ids", []):
                    sector_coverage.add(sec)

        portfolio_id = f"PORT-{district_id.upper()}-{uuid.uuid4().hex[:8]}"

        return {
            "portfolio_id": portfolio_id,
            "optimization_run_id": optimization_run_id,
            "district_id": district_id.lower(),
            "selected_strategy_ids": selected_strategy_ids,
            "objective_value": round(obj_val, 4),
            "feasibility_status": "FEASIBLE" if feas_res["feasible"] else "INFEASIBLE",
            "hazard_coverage": sorted(list(hazard_coverage)),
            "domain_coverage": sorted(list(domain_coverage)),
            "sector_coverage": sorted(list(sector_coverage)),
            "violations": feas_res["violations"],
            "created_at": datetime.utcnow().isoformat()
        }
