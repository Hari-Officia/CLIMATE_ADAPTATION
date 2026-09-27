"""
Phase J/K Classical Adaptation Strategy Optimization Unit Tests
"""

import pytest
from backend.services.optimization.solvers.exact_solver import ExactSolver
from backend.services.optimization.solvers.milp_solver import MILPSolver
from backend.services.optimization.solvers.greedy_solver import GreedySolver
from backend.services.optimization.optimization_service import OptimizationService
from backend.services.optimization.constraint_service import ConstraintService

@pytest.fixture
def exact_solver():
    return ExactSolver()

@pytest.fixture
def milp_solver():
    return MILPSolver()

@pytest.fixture
def greedy_solver():
    return GreedySolver()

@pytest.fixture
def opt_service():
    return OptimizationService()

def test_exact_solver_chennai(exact_solver):
    cand_ids = ["STR-DRN-001", "STR-DRN-002", "STR-WTR-001", "STR-NBS-001", "STR-CST-001"]
    res = exact_solver.solve(cand_ids, max_k=3)
    assert res["status"] == "OPTIMAL"
    assert len(res["selected_strategy_ids"]) <= 3
    assert res["objective_value"] > 0.0

def test_milp_exact_solver_agreement(exact_solver, milp_solver):
    cand_ids = ["STR-DRN-001", "STR-DRN-002", "STR-WTR-001", "STR-NBS-001", "STR-CST-001"]
    exact_res = exact_solver.solve(cand_ids, max_k=3)
    milp_res = milp_solver.solve(cand_ids, max_k=3)

    assert exact_res["status"] == "OPTIMAL"
    assert milp_res["status"] == "OPTIMAL"
    # Ground-truth exact objective includes quadratic pairwise interaction terms
    assert abs(exact_res["objective_value"] - milp_res["objective_value"]) <= 0.25

def test_greedy_solver_execution(greedy_solver):
    cand_ids = ["STR-DRN-001", "STR-DRN-002", "STR-WTR-001", "STR-NBS-001", "STR-CST-001"]
    res = greedy_solver.solve(cand_ids, max_k=3)
    assert res["status"] == "FEASIBLE"
    assert len(res["selected_strategy_ids"]) <= 3

def test_conflict_constraint_validation():
    constraint_service = ConstraintService()
    # Assume STR-DRN-001 and STR-DRN-002 are not directly in hard conflict, but test size & feasibility
    feas = constraint_service.validate_portfolio_feasibility(["STR-DRN-001", "STR-DRN-002"], max_k=1)
    assert feas["feasible"] is False
    assert len(feas["violations"]) > 0

def test_optimization_service_chennai_run(opt_service):
    res = opt_service.run_optimization("chennai", solver_id="MILP_HIGHS", max_k=4)
    assert res["status"] == "OPTIMAL"
    assert "portfolio" in res
    assert len(res["portfolio"]["selected_strategy_ids"]) <= 4
    assert res["portfolio"]["objective_value"] > 0.0

def test_optimization_service_coimbatore_run(opt_service):
    res = opt_service.run_optimization("coimbatore", solver_id="MILP_HIGHS", max_k=4)
    assert res["status"] == "OPTIMAL"
    # Coastal strategy STR-CST-001 must not be selected for inland Coimbatore
    assert "STR-CST-001" not in res["portfolio"]["selected_strategy_ids"]
