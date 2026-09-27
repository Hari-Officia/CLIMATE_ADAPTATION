"""
Phase I Adaptation Strategy Intelligence & Applicability Engine Unit Tests
"""

import pytest
from backend.services.strategy_applicability_service import StrategyApplicabilityService
from backend.services.strategy_candidate_service import StrategyCandidateService

@pytest.fixture
def applicability_service():
    return StrategyApplicabilityService()

@pytest.fixture
def candidate_service():
    return StrategyCandidateService()

def test_strategy_master_registry_loading(applicability_service):
    strategies = applicability_service.strategies
    assert len(strategies) >= 14
    for strat in strategies:
        assert "strategy_id" in strat
        assert "canonical_name" in strat
        assert "domain_id" in strat
        assert "primary_hazard_id" in strat

def test_coastal_strategy_applicability_chennai(applicability_service):
    # Chennai is coastal -> STR-CST-001 should be ELIGIBLE
    res = applicability_service.evaluate_strategy_applicability("chennai", "STR-CST-001")
    assert res["applicable"] is True
    assert res["eligibility_status"] == "ELIGIBLE"
    assert "CND-CST-001: Coastal Exposure Satisfied" in res["satisfied_conditions"]

def test_coastal_strategy_ineligible_coimbatore(applicability_service):
    # Coimbatore is inland -> STR-CST-001 should be INELIGIBLE
    res = applicability_service.evaluate_strategy_applicability("coimbatore", "STR-CST-001")
    assert res["applicable"] is False
    assert res["eligibility_status"] == "INELIGIBLE"
    assert any("Coastal Exposure Required" in f for f in res["failed_conditions"])

def test_candidate_set_generation_chennai(candidate_service):
    candidate_set = candidate_service.generate_candidate_set("chennai")
    assert "candidate_set_id" in candidate_set
    assert candidate_set["district_id"] == "chennai"
    assert len(candidate_set["strategy_ids"]) > 0
    assert "STR-CST-001" in candidate_set["strategy_ids"]

def test_candidate_set_generation_coimbatore(candidate_service):
    candidate_set = candidate_service.generate_candidate_set("coimbatore")
    assert candidate_set["district_id"] == "coimbatore"
    assert "STR-CST-001" not in candidate_set["strategy_ids"]
    assert "STR-CST-001" in candidate_set["excluded_strategy_ids"]

def test_review_required_strategy_flag(applicability_service):
    # STR-BLD-001 (Cool Roof) is flagged REQUIRES_REVIEW
    res = applicability_service.evaluate_strategy_applicability("chennai", "STR-BLD-001")
    assert res["eligibility_status"] == "REQUIRES_REVIEW"
