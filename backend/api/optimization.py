"""
Classical Optimization API Endpoints — Phase J/K
Provides REST API endpoints for running classical portfolio optimization, solver selection, and portfolio retrieval.
"""

import os
import json
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import OptimizationRunRecord, AdaptationPortfolioRecord
from backend.services.optimization.optimization_service import OptimizationService

router = APIRouter(prefix="/api/v1", tags=["Classical Strategy Optimization Baseline"])

optimization_service = OptimizationService()

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config", "master")

def load_master_json(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(CONFIG_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

class OptimizeRequest(BaseModel):
    district_id: str
    solver_id: Optional[str] = "MILP_HIGHS"
    scenario_id: Optional[str] = "BASELINE"
    max_k: Optional[int] = 5

@router.get("/optimization/solvers")
def get_optimization_solvers():
    """Retrieve registered classical optimization solvers."""
    return load_master_json("optimization_solvers.json")

@router.get("/optimization/scenarios")
def get_optimization_scenarios():
    """Retrieve registered optimization scenarios."""
    return load_master_json("optimization_scenarios.json")

@router.get("/optimization/methodologies")
def get_optimization_methodologies():
    """Retrieve active optimization methodology definitions."""
    return load_master_json("optimization_methodologies.json")

@router.get("/optimization/objectives")
def get_optimization_objectives():
    """Retrieve component optimization objectives."""
    return load_master_json("optimization_objectives.json")

@router.post("/districts/{district_id}/optimize")
def optimize_district_portfolio(district_id: str, req: Optional[OptimizeRequest] = None):
    """Run classical portfolio optimization for a district."""
    solver_id = req.solver_id if req and req.solver_id else "MILP_HIGHS"
    scenario_id = req.scenario_id if req and req.scenario_id else "BASELINE"
    max_k = req.max_k if req and req.max_k else 5
    
    return optimization_service.run_optimization(
        district_id=district_id.lower(),
        solver_id=solver_id,
        scenario_id=scenario_id,
        max_k=max_k
    )

@router.get("/districts/{district_id}/optimization/compare-solvers")
def compare_solvers_for_district(district_id: str, max_k: int = 5):
    """Compare Exact, MILP, and Greedy solvers on a district candidate set."""
    return optimization_service.compare_solvers_for_district(district_id.lower(), max_k=max_k)

@router.get("/optimization/runs/{run_id}")
def get_optimization_run(run_id: str, db: Session = Depends(get_db)):
    """Retrieve historical optimization run by ID."""
    rec = db.query(OptimizationRunRecord).filter(OptimizationRunRecord.optimization_run_id == run_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail=f"Optimization run '{run_id}' not found.")
    return {
        "optimization_run_id": rec.optimization_run_id,
        "district_id": rec.district_id,
        "candidate_set_id": rec.candidate_set_id,
        "methodology_id": rec.methodology_id,
        "solver_id": rec.solver_id,
        "scenario_id": rec.scenario_id,
        "status": rec.status,
        "problem_size": rec.problem_size,
        "best_objective": rec.best_objective,
        "optimality_gap": rec.optimality_gap,
        "runtime_ms": rec.runtime_ms,
        "created_at": rec.created_at.isoformat()
    }

@router.get("/optimization/runs/{run_id}/portfolio")
def get_optimization_run_portfolio(run_id: str, db: Session = Depends(get_db)):
    """Retrieve portfolio resulting from optimization run."""
    rec = db.query(AdaptationPortfolioRecord).filter(AdaptationPortfolioRecord.optimization_run_id == run_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail=f"Portfolio for optimization run '{run_id}' not found.")
    return {
        "portfolio_id": rec.portfolio_id,
        "optimization_run_id": rec.optimization_run_id,
        "district_id": rec.district_id,
        "selected_strategy_ids": rec.selected_strategy_ids,
        "objective_value": rec.objective_value,
        "feasibility_status": rec.feasibility_status,
        "hazard_coverage": rec.hazard_coverage,
        "domain_coverage": rec.domain_coverage,
        "sector_coverage": rec.sector_coverage,
        "created_at": rec.created_at.isoformat()
    }
