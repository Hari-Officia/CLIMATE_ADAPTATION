import pytest
import os
import json
from backend.db.database import SessionLocal
from backend.db.models import District, DistrictProfile, PopulationExposureRecord, InfrastructureAssetRecord, DatasetRecord, SourceRecord
from backend.services.exposure_service import ExposureService
from backend.services.spatial_service import SpatialService

@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

def test_38_districts_exist_in_db(db_session):
    """A1: Verify all 38 canonical Tamil Nadu districts exist in PostGIS DB."""
    count = db_session.query(District).count()
    assert count == 38, f"Expected 38 districts, found {count}"

def test_district_spatial_pip_lookup(db_session):
    """A2: Test Point-in-Polygon spatial lookup for Chennai coordinates."""
    res = SpatialService.point_in_polygon_lookup(db_session, 13.0827, 80.2707)
    assert res["status"] == "MATCHED"
    assert res["district_id"] == "chennai"
    assert res["confidence"] == "HIGH"

def test_spatial_pip_out_of_scope(db_session):
    """Test Spatial PIP returns OUT_OF_SCOPE for coordinates outside Tamil Nadu (e.g. New Delhi)."""
    res = SpatialService.point_in_polygon_lookup(db_session, 28.6139, 77.2090)
    assert res["status"] == "OUT_OF_SCOPE"
    assert res["district_id"] is None

def test_source_and_dataset_provenance(db_session):
    """A6: Every active dataset has a verified source and checksum."""
    datasets = db_session.query(DatasetRecord).all()
    assert len(datasets) >= 4
    for d in datasets:
        assert d.source_id is not None
        assert d.checksum is not None
        source = db_session.query(SourceRecord).filter(SourceRecord.source_id == d.source_id).first()
        assert source is not None, f"Dataset {d.dataset_id} missing valid source"

def test_district_exposure_profile(db_session):
    """A11: Test population and built environment exposure profile calculation."""
    res = ExposureService.get_district_exposure(db_session, "chennai")
    assert res["status"] == "COMPLETE"
    assert res["district_id"] == "chennai"
    assert res["population_exposure"]["total_population"] == 7088403
    assert res["built_environment_exposure"]["built_up_area_km2"] == 426.0

def test_risk_exposure_profile_contract(db_session):
    """A13: Test RiskExposureProfile integrates risk and exposure without vulnerability scoring."""
    res = ExposureService.get_risk_exposure_profile(db_session, "chennai", "flood")
    assert res["district_id"] == "chennai"
    assert res["hazard_id"] == "flood"
    assert "risk_context" in res
    assert "exposure_context" in res
    assert "temporal_alignment" in res
    assert res["temporal_alignment"]["temporal_mismatch_flag"] is True
    assert res["data_governance"]["zero_imputation"] is False
    assert res["data_governance"]["rev_001_metric_status"] == "REQUIRES_REVIEW"

def test_no_orphan_exposure_records(db_session):
    """A5: Ensure no orphan exposure records exist without valid district references."""
    pop_recs = db_session.query(PopulationExposureRecord).all()
    for p in pop_recs:
        d = db_session.query(District).filter(District.district_id == p.district_id).first()
        assert d is not None, f"Orphan population exposure record found for district {p.district_id}"
