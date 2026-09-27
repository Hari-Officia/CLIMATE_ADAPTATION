import pytest
from backend.db.database import SessionLocal
from backend.db.models import District, PriorityMethodologyRecord
from backend.services.priority_service import PriorityService

@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

def test_priority_methodology_active(db_session):
    """GATE H5: Active Priority Methodology MTH-PRIORITY-TN-001 exists."""
    mth = db_session.query(PriorityMethodologyRecord).filter(PriorityMethodologyRecord.methodology_id == "MTH-PRIORITY-TN-001").first()
    assert mth is not None
    assert mth.status == "ACTIVE"

def test_district_priority_profile_generation(db_session):
    """GATE H6: Priority Profile generation for Chennai."""
    profile = PriorityService.get_priority_profile(db_session, "chennai", "flood")
    assert profile["district_id"] == "chennai"
    assert profile["hazard_id"] == "flood"
    assert profile["methodology_id"] == "MTH-PRIORITY-TN-001"
    assert profile["priority_status"] == "REQUIRES_PRIORITY_ATTENTION"
    assert profile["priority_horizon"] in ["IMMEDIATE", "SHORT_TERM", "MEDIUM_TERM", "LONG_TERM"]

def test_no_unverified_composite_priority_score(db_session):
    """GATE H11/H13: Ensure priority_score remains NULL to prevent fake composite scores."""
    profile = PriorityService.get_priority_profile(db_session, "chennai", "flood")
    assert profile["priority_score"] is None
    assert profile["data_governance"]["zero_imputation_applied"] is False

def test_priority_driver_extraction(db_session):
    """GATE H14: Priority drivers extracted deterministically."""
    profile = PriorityService.get_priority_profile(db_session, "chennai", "flood")
    drivers = profile["priority_drivers"]
    assert len(drivers) >= 1
    driver_types = [d["driver_type"] for d in drivers]
    assert "HIGH_POPULATION_EXPOSURE" in driver_types or "HIGH_SENSITIVITY" in driver_types

def test_temporal_gap_barrier_extraction(db_session):
    """GATE H7: Temporal gap triggers TEMPORAL_MISMATCH barrier."""
    profile = PriorityService.get_priority_profile(db_session, "chennai", "flood")
    barriers = profile["priority_barriers"]
    barrier_types = [b["barrier_type"] for b in barriers]
    assert "TEMPORAL_MISMATCH" in barrier_types

def test_all_38_districts_priority_evaluable(db_session):
    """GATE H29: Evaluate priority across all 38 canonical Tamil Nadu districts."""
    districts = db_session.query(District).all()
    assert len(districts) == 38
    for d in districts:
        profile = PriorityService.get_priority_profile(db_session, d.district_id, "flood")
        assert profile["priority_status"] in ["REQUIRES_PRIORITY_ATTENTION", "MODERATE_PRIORITY", "MONITORING_ONLY", "UNCERTAIN"]
