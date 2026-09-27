from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="USER", nullable=False)  # 'USER' or 'ADMIN'
    full_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. "chennai"
    district_name = Column(String(100), unique=True, nullable=False)         # e.g. "Chennai"
    district_code = Column(String(20), nullable=True)                         # e.g. "IND-TN-CHE"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geojson_properties = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    profile = relationship("DistrictProfile", back_populates="district", uselist=False)
    forecasts = relationship("ForecastData", back_populates="district")
    risks = relationship("RiskResult", back_populates="district")

class DistrictProfile(Base):
    __tablename__ = "district_profiles"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), unique=True, nullable=False)
    district_name = Column(String(100), nullable=False)
    population = Column(Integer, nullable=False)
    area_km2 = Column(Float, nullable=False)
    population_density = Column(Float, nullable=False)
    urban_percentage = Column(Float, nullable=False)
    coastal = Column(Boolean, default=False)
    elevation_m = Column(Float, nullable=True)
    source = Column(String(200), default="Census of India & Tamil Nadu DES")
    source_year = Column(Integer, default=2021)
    updated_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="profile")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=True)
    category = Column(String(50), default="landmark")  # 'landmark', 'town', 'station'
    created_at = Column(DateTime, default=datetime.utcnow)

class ForecastRun(Base):
    __tablename__ = "forecast_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50), default="Open-Meteo API")
    status = Column(String(20), default="SUCCESS")  # 'SUCCESS', 'FAILED'
    districts_updated = Column(Integer, default=0)
    details = Column(JSON, nullable=True)

class ForecastData(Base):
    __tablename__ = "forecast_data"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), index=True, nullable=False)
    date = Column(String(20), index=True, nullable=False)  # 'YYYY-MM-DD'
    temp_max = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    soil_wetness = Column(Float, nullable=True)
    hourly_payload = Column(JSON, nullable=True)
    daily_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="forecasts")

class RiskResult(Base):
    __tablename__ = "risk_results"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), index=True, nullable=False)
    date = Column(String(20), index=True, nullable=False)  # 'YYYY-MM-DD'
    
    flood_prob = Column(Float, nullable=False)
    flood_risk = Column(String(10), nullable=False)  # 'LOW', 'MEDIUM', 'HIGH'
    
    heatwave_prob = Column(Float, nullable=False)
    heatwave_risk = Column(String(10), nullable=False)
    
    drought_prob = Column(Float, nullable=False)
    drought_risk = Column(String(10), nullable=False)
    
    features_json = Column(JSON, nullable=True)  # Snapshot of 53 features used
    data_quality = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="risks")

class ModelRegistryRecord(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    hazard = Column(String(50), unique=True, nullable=False)  # 'flood', 'drought', 'heatwave'
    model_name = Column(String(100), nullable=False)
    model_path = Column(String(255), nullable=False)
    framework = Column(String(50), default="XGBoost")
    n_features = Column(Integer, default=53)
    roc_auc = Column(Float, nullable=True)
    pr_auc = Column(Float, nullable=True)
    status = Column(String(20), default="ACTIVE")
    loaded_at = Column(DateTime, default=datetime.utcnow)

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String(20), default="INFO")  # 'INFO', 'WARN', 'ERROR'
    component = Column(String(50), nullable=False) # 'ClimateAgent', 'RiskAgent', 'Auth', etc.
    message = Column(Text, nullable=False)
    details_json = Column(JSON, nullable=True)

# Phase F — Provenance & Source Registry Models
class SourceRecord(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(50), unique=True, index=True, nullable=False)
    source_name = Column(String(150), nullable=False)
    organization = Column(String(150), nullable=False)
    source_type = Column(String(50), nullable=False)  # government, national_agency, international, satellite, reanalysis, open_data, research
    official_url = Column(String(255), nullable=True)
    license = Column(String(100), default="GOVT_OPEN")
    authority_level = Column(String(30), default="AUTHORITATIVE") # AUTHORITATIVE, HIGH, MEDIUM, COMMUNITY
    geographic_scope = Column(String(50), default="TAMIL_NADU")
    temporal_scope = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    verification_status = Column(String(30), default="VERIFIED")
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatasetRecord(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String(50), unique=True, index=True, nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=False)
    dataset_name = Column(String(150), nullable=False)
    dataset_version = Column(String(30), default="1.0.0")
    description = Column(Text, nullable=True)
    data_type = Column(String(50), nullable=False)  # raster, vector_polygon, vector_point, tabular
    format = Column(String(30), nullable=False)     # geojson, postgis, csv, parquet, tif
    spatial_resolution = Column(String(50), nullable=True)
    geographic_scope = Column(String(50), default="TAMIL_NADU")
    temporal_start = Column(String(20), nullable=True)
    temporal_end = Column(String(20), nullable=True)
    crs = Column(String(20), default="EPSG:4326")
    checksum = Column(String(64), nullable=True)    # SHA-256
    row_count = Column(Integer, default=0)
    quality_status = Column(String(30), default="VALIDATED")
    current_status = Column(String(30), default="ACTIVE")    # ACTIVE, DEPRECATED, PENDING_ACQUISITION
    created_at = Column(DateTime, default=datetime.utcnow)

class DatasetVersionRecord(Base):
    __tablename__ = "dataset_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(String(60), unique=True, index=True, nullable=False)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    version_tag = Column(String(30), nullable=False)
    checksum = Column(String(64), nullable=False)
    created_by = Column(String(50), default="INGESTION_PIPELINE")
    change_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatasetLineageRecord(Base):
    __tablename__ = "lineage"

    id = Column(Integer, primary_key=True, index=True)
    lineage_id = Column(String(60), unique=True, index=True, nullable=False)
    parent_dataset_id = Column(String(50), nullable=False)
    derived_dataset_id = Column(String(50), nullable=False)
    transformation_method = Column(String(100), nullable=False)
    parameters_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase F — Data Quality Models
class DataQualityCheckRecord(Base):
    __tablename__ = "data_quality_checks"

    id = Column(Integer, primary_key=True, index=True)
    check_id = Column(String(60), unique=True, index=True, nullable=False)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    check_type = Column(String(50), nullable=False)  # completeness, uniqueness, spatial_validity, range_validity
    status = Column(String(20), nullable=False)      # PASS, FAIL, WARNING, NOT_APPLICABLE
    records_checked = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    failure_rate = Column(Float, default=0.0)
    details_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DataQualityIssueRecord(Base):
    __tablename__ = "data_quality_issues"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(String(60), unique=True, index=True, nullable=False)
    dataset_id = Column(String(50), nullable=False)
    issue_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="WARNING")  # CRITICAL, WARNING, INFO
    description = Column(Text, nullable=False)
    status = Column(String(30), default="REQUIRES_REVIEW")  # REQUIRES_REVIEW, MISSING, UNAVAILABLE, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase F — Spatial Governance Models
class SpatialLayerRecord(Base):
    __tablename__ = "spatial_layers"

    id = Column(Integer, primary_key=True, index=True)
    layer_id = Column(String(50), unique=True, index=True, nullable=False)
    layer_name = Column(String(100), nullable=False)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    geometry_type = Column(String(30), nullable=False)  # MultiPolygon, Polygon, Point, LineString
    crs = Column(String(20), default="EPSG:4326")
    feature_count = Column(Integer, default=0)
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

class SpatialLayerVersionRecord(Base):
    __tablename__ = "layer_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(String(60), unique=True, index=True, nullable=False)
    layer_id = Column(String(50), ForeignKey("spatial_layers.layer_id"), nullable=False)
    version = Column(String(30), nullable=False)
    valid_from = Column(String(20), nullable=False)
    valid_to = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase F — Infrastructure Asset Model
class InfrastructureAssetRecord(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String(50), unique=True, index=True, nullable=False)
    asset_type = Column(String(50), nullable=False)   # healthcare, education, emergency, power, water, transport
    asset_name = Column(String(150), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=False)
    criticality = Column(String(20), default="HIGH")   # HIGH, MEDIUM, LOW
    operational_status = Column(String(30), default="OPERATIONAL")
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase F — Exposure Models
class PopulationExposureRecord(Base):
    __tablename__ = "population_exposure"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    district_name = Column(String(100), nullable=False)
    total_population = Column(Integer, nullable=False)
    urban_population = Column(Integer, nullable=True)
    rural_population = Column(Integer, nullable=True)
    vulnerable_age_group = Column(Integer, nullable=True)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    dataset_year = Column(Integer, default=2020)
    created_at = Column(DateTime, default=datetime.utcnow)

class InfrastructureExposureRecord(Base):
    __tablename__ = "infrastructure_exposure"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    hazard_id = Column(String(50), nullable=False)     # flood, drought, heatwave
    total_assets = Column(Integer, default=0)
    exposed_assets = Column(Integer, default=0)
    healthcare_exposed = Column(Integer, default=0)
    power_water_exposed = Column(Integer, default=0)
    transport_exposed = Column(Integer, default=0)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    exposure_status = Column(String(30), default="EXPOSED") # EXPOSED, NOT_EXPOSED, UNKNOWN, UNAVAILABLE
    created_at = Column(DateTime, default=datetime.utcnow)

class BuiltEnvironmentExposureRecord(Base):
    __tablename__ = "built_environment_exposure"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    total_area_km2 = Column(Float, nullable=False)
    built_up_area_km2 = Column(Float, nullable=True)
    impervious_surface_fraction = Column(Float, nullable=True)
    urban_density_category = Column(String(30), nullable=True)
    dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExposureRecord(Base):
    __tablename__ = "exposure_records"

    id = Column(Integer, primary_key=True, index=True)
    exposure_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    hazard_id = Column(String(50), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=True)
    metric_unit = Column(String(30), nullable=False)
    source_dataset_id = Column(String(50), ForeignKey("datasets.dataset_id"), nullable=False)
    spatial_method = Column(String(50), default="SPATIAL_OVERLAY")
    quality_status = Column(String(30), default="VALIDATED")
    confidence = Column(String(20), default="HIGH")
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase F — Audit & Processing Models
class DataConflictRecord(Base):
    __tablename__ = "data_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    conflict_id = Column(String(60), unique=True, index=True, nullable=False)
    dataset_a_id = Column(String(50), nullable=False)
    dataset_b_id = Column(String(50), nullable=False)
    field_name = Column(String(100), nullable=False)
    value_a = Column(String(255), nullable=True)
    value_b = Column(String(255), nullable=True)
    resolution_status = Column(String(30), default="UNRESOLVED") # UNRESOLVED, RESOLVED, DISCARDED
    created_at = Column(DateTime, default=datetime.utcnow)

class ProcessingRunRecord(Base):
    __tablename__ = "processing_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(60), unique=True, index=True, nullable=False)
    pipeline_name = Column(String(100), default="PHASE_F_EXPOSURE_PIPELINE")
    pipeline_version = Column(String(30), default="1.0.0")
    status = Column(String(20), default="COMPLETED")
    records_processed = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.utcnow)

# Phase H — Adaptation Priority Engine Models
class PriorityMethodologyRecord(Base):
    __tablename__ = "priority_methodologies"

    id = Column(Integer, primary_key=True, index=True)
    methodology_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. "MTH-PRIORITY-TN-001"
    name = Column(String(150), nullable=False)
    version = Column(String(30), default="1.0.0")
    framework = Column(String(100), default="Multi-Criteria Climate Decision Analysis (MCDA)")
    description = Column(Text, nullable=True)
    status = Column(String(30), default="ACTIVE") # DRAFT, UNDER_REVIEW, APPROVED, ACTIVE, DEPRECATED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class PriorityProfileRecord(Base):
    __tablename__ = "priority_profiles"

    id = Column(Integer, primary_key=True, index=True)
    priority_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    hazard_id = Column(String(50), nullable=False)
    methodology_id = Column(String(50), ForeignKey("priority_methodologies.methodology_id"), nullable=False)
    priority_status = Column(String(50), nullable=False) # REQUIRES_PRIORITY_ATTENTION, MODERATE_PRIORITY, MONITORING_ONLY, UNCERTAIN
    priority_horizon = Column(String(30), default="SHORT_TERM") # IMMEDIATE, SHORT_TERM, MEDIUM_TERM, LONG_TERM
    uncertainty_status = Column(String(30), default="LOW")
    data_quality_status = Column(String(30), default="PASS")
    generated_at = Column(DateTime, default=datetime.utcnow)

class PriorityComponentRecord(Base):
    __tablename__ = "priority_components"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(String(60), unique=True, index=True, nullable=False)
    priority_id = Column(String(60), ForeignKey("priority_profiles.priority_id"), nullable=False)
    component_type = Column(String(50), nullable=False) # RISK, EXPOSURE, VULNERABILITY, RESILIENCE_GAP
    raw_status = Column(String(50), nullable=False)
    normalized_value = Column(Float, nullable=True)
    contribution_weight = Column(Float, nullable=True)
    source_dataset_id = Column(String(50), nullable=True)

class PriorityDriverRecord(Base):
    __tablename__ = "priority_drivers"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(String(60), unique=True, index=True, nullable=False)
    priority_id = Column(String(60), ForeignKey("priority_profiles.priority_id"), nullable=False)
    driver_type = Column(String(50), nullable=False) # HIGH_HAZARD_RISK, HIGH_POPULATION_EXPOSURE, HIGH_SENSITIVITY, LOW_ADAPTIVE_CAPACITY, RESILIENCE_GAP
    evidence_summary = Column(Text, nullable=False)
    source_reference = Column(String(150), nullable=True)

class PriorityUncertaintyRecord(Base):
    __tablename__ = "priority_uncertainty"

    id = Column(Integer, primary_key=True, index=True)
    uncertainty_id = Column(String(60), unique=True, index=True, nullable=False)
    priority_id = Column(String(60), ForeignKey("priority_profiles.priority_id"), nullable=False)
    uncertainty_source = Column(String(100), nullable=False) # TEMPORAL_MISMATCH, DATA_GAP, METHODOLOGICAL_LIMITATION
    impact_level = Column(String(30), default="MEDIUM")

class PrioritySnapshotRecord(Base):
    __tablename__ = "priority_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(String(60), unique=True, index=True, nullable=False)
    priority_id = Column(String(60), ForeignKey("priority_profiles.priority_id"), nullable=False)
    snapshot_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PriorityValidationRecord(Base):
    __tablename__ = "priority_validations"

    id = Column(Integer, primary_key=True, index=True)
    validation_id = Column(String(60), unique=True, index=True, nullable=False)
    priority_id = Column(String(60), ForeignKey("priority_profiles.priority_id"), nullable=False)
    validation_type = Column(String(50), default="FACE_VALIDITY")
    result_status = Column(String(30), default="PASSED")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PrioritySensitivityRunRecord(Base):
    __tablename__ = "priority_sensitivity_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(60), unique=True, index=True, nullable=False)
    methodology_id = Column(String(50), nullable=False)
    variation_type = Column(String(50), nullable=False) # WEIGHT_PERTURBATION, THRESHOLD_PERTURBATION
    robustness_status = Column(String(30), default="ROBUST")
    details_json = Column(JSON, nullable=True)
    run_at = Column(DateTime, default=datetime.utcnow)

# Phase I — Enterprise Adaptation Strategy Intelligence Models
class StrategyDomainRecord(Base):
    __tablename__ = "strategy_domains"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. "DOM-DRN"
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

class StrategyRecord(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. "STR-DRN-001"
    canonical_name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(150), nullable=False)
    short_description = Column(Text, nullable=True)
    long_description = Column(Text, nullable=True)
    domain_id = Column(String(50), ForeignKey("strategy_domains.domain_id"), nullable=False)
    measure_type = Column(String(50), default="STRUCTURAL")
    primary_hazard_id = Column(String(50), nullable=False)
    sector_ids = Column(JSON, nullable=True)
    planning_horizon = Column(String(30), default="SHORT_TERM")
    evidence_status = Column(String(30), default="VERIFIED")
    evidence_strength = Column(String(30), default="STRONG")
    uncertainty_level = Column(String(30), default="LOW")
    status = Column(String(30), default="ACTIVE")
    aliases = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class StrategyHazardRecord(Base):
    __tablename__ = "strategy_hazards"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    hazard_id = Column(String(50), nullable=False)
    relationship_type = Column(String(30), default="PRIMARY") # PRIMARY, SECONDARY, CO_BENEFIT

class StrategySectorRecord(Base):
    __tablename__ = "strategy_sectors"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    sector_id = Column(String(50), nullable=False)
    relationship_type = Column(String(30), default="PRIMARY")

class StrategyConditionRecord(Base):
    __tablename__ = "strategy_conditions"

    id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(String(50), unique=True, index=True, nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    condition_type = Column(String(50), nullable=False) # HAZARD, EXPOSURE, VULNERABILITY, COASTAL, SPATIAL
    feature_name = Column(String(100), nullable=False)
    operator = Column(String(30), default="EQUALS")
    threshold = Column(Float, nullable=True)
    required_value = Column(String(100), nullable=True)
    hard_or_soft = Column(String(20), default="HARD") # HARD, SOFT
    notes = Column(Text, nullable=True)

class StrategyRelationshipRecord(Base):
    __tablename__ = "strategy_relationships"

    id = Column(Integer, primary_key=True, index=True)
    strategy_a = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    strategy_b = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    relationship_type = Column(String(40), nullable=False) # COMPLEMENTARY, SYNERGISTIC, ALTERNATIVE, REDUNDANT, CONFLICTING, DEPENDENT
    reason = Column(Text, nullable=True)
    severity = Column(String(20), default="INFO")
    hard_or_soft = Column(String(20), default="SOFT")

class EvidenceClaimRecord(Base):
    __tablename__ = "evidence_claims"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String(60), unique=True, index=True, nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    claim_type = Column(String(50), nullable=False)
    claim_text = Column(Text, nullable=False)
    source_tier = Column(String(30), default="TIER_1")
    document_reference = Column(String(200), nullable=True)
    page_section = Column(String(100), nullable=True)
    evidence_strength = Column(String(30), default="STRONG")

class StrategyApplicabilityRecord(Base):
    __tablename__ = "strategy_district_applicability"

    id = Column(Integer, primary_key=True, index=True)
    applicability_id = Column(String(60), unique=True, index=True, nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    hazard_id = Column(String(50), nullable=False)
    applicable = Column(Boolean, default=True)
    eligibility_status = Column(String(40), default="ELIGIBLE") # ELIGIBLE, INELIGIBLE, CONDITIONALLY_ELIGIBLE, INSUFFICIENT_DATA, REQUIRES_REVIEW, NOT_APPLICABLE
    satisfied_conditions = Column(JSON, nullable=True)
    failed_conditions = Column(JSON, nullable=True)
    missing_data = Column(JSON, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

class StrategyCandidateSetRecord(Base):
    __tablename__ = "strategy_candidate_sets"

    id = Column(Integer, primary_key=True, index=True)
    candidate_set_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    priority_id = Column(String(60), nullable=False)
    hazard_ids = Column(JSON, nullable=True)
    strategy_ids = Column(JSON, nullable=False)
    excluded_strategy_ids = Column(JSON, nullable=True)
    review_required_strategy_ids = Column(JSON, nullable=True)
    insufficient_data_strategy_ids = Column(JSON, nullable=True)
    evidence_summary = Column(Text, nullable=True)
    version = Column(String(30), default="1.0.0")
    generated_at = Column(DateTime, default=datetime.utcnow)

class StrategyCandidateRecord(Base):
    __tablename__ = "strategy_candidates"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String(60), unique=True, index=True, nullable=False)
    candidate_set_id = Column(String(60), ForeignKey("strategy_candidate_sets.candidate_set_id"), nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    eligibility_status = Column(String(40), default="ELIGIBLE")

class StrategyReviewQueueRecord(Base):
    __tablename__ = "strategy_review_queue"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String(60), unique=True, index=True, nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    reason = Column(String(100), nullable=False) # WEAK_EVIDENCE, CONFLICTING_EVIDENCE, MISSING_LOCAL_EVIDENCE, REQUIRES_FIELD_AUDIT
    priority = Column(String(30), default="MEDIUM")
    status = Column(String(30), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase J/K — Classical Adaptation Strategy Optimization Foundation Models
class OptimizationMethodologyRecord(Base):
    __tablename__ = "optimization_methodologies"

    id = Column(Integer, primary_key=True, index=True)
    methodology_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. "MTH-OPT-TN-001"
    name = Column(String(150), nullable=False)
    version = Column(String(30), default="1.0.0")
    description = Column(Text, nullable=True)
    status = Column(String(30), default="ACTIVE")

class OptimizationRunRecord(Base):
    __tablename__ = "optimization_runs"

    id = Column(Integer, primary_key=True, index=True)
    optimization_run_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    candidate_set_id = Column(String(60), ForeignKey("strategy_candidate_sets.candidate_set_id"), nullable=False)
    methodology_id = Column(String(50), ForeignKey("optimization_methodologies.methodology_id"), nullable=False)
    solver_id = Column(String(50), nullable=False) # EXACT, MILP_HIGHS, GREEDY_HEURISTIC
    scenario_id = Column(String(50), default="BASELINE")
    status = Column(String(30), default="READY") # DRAFT, READY, RUNNING, OPTIMAL, FEASIBLE, INFEASIBLE, ERROR
    problem_size = Column(Integer, default=0)
    best_objective = Column(Float, nullable=True)
    best_bound = Column(Float, nullable=True)
    optimality_gap = Column(Float, nullable=True)
    runtime_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class OptimizationResultRecord(Base):
    __tablename__ = "optimization_results"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(String(60), unique=True, index=True, nullable=False)
    optimization_run_id = Column(String(60), ForeignKey("optimization_runs.optimization_run_id"), nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    selected = Column(Boolean, default=False)
    objective_contribution = Column(Float, default=0.0)

class AdaptationPortfolioRecord(Base):
    __tablename__ = "adaptation_portfolios"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(String(60), unique=True, index=True, nullable=False)
    optimization_run_id = Column(String(60), ForeignKey("optimization_runs.optimization_run_id"), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    selected_strategy_ids = Column(JSON, nullable=False)
    objective_value = Column(Float, nullable=False)
    feasibility_status = Column(String(30), default="FEASIBLE") # FEASIBLE, INFEASIBLE, CONDITIONAL
    hazard_coverage = Column(JSON, nullable=True)
    domain_coverage = Column(JSON, nullable=True)
    sector_coverage = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PortfolioStrategyRecord(Base):
    __tablename__ = "portfolio_strategies"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(String(60), ForeignKey("adaptation_portfolios.portfolio_id"), nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    selection_order = Column(Integer, default=1)
    selection_reason = Column(Text, nullable=True)

class OptimizationScenarioRecord(Base):
    __tablename__ = "optimization_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    max_portfolio_size = Column(Integer, default=5)
    description = Column(Text, nullable=True)

class OptimizationSensitivityRecord(Base):
    __tablename__ = "optimization_sensitivity_runs"

    id = Column(Integer, primary_key=True, index=True)
    sensitivity_run_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), nullable=False)
    stability_score = Column(Float, default=1.0)
    details_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class OptimizationBenchmarkRecord(Base):
    __tablename__ = "optimization_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    benchmark_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), nullable=False)
    solver_id = Column(String(50), nullable=False)
    candidate_count = Column(Integer, nullable=False)
    objective_value = Column(Float, nullable=False)
    runtime_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase L — Enterprise QUBO Formulation & Mathematical Bridge Models
class QUBOMethodologyRecord(Base):
    __tablename__ = "qubo_methodologies"

    id = Column(Integer, primary_key=True, index=True)
    methodology_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    version = Column(String(30), default="1.0.0")
    objective_sign_convention = Column(String(50), default="MINIMIZE_NEGATED_OBJECTIVE")
    matrix_convention = Column(String(50), default="FULL_SYMMETRIC")
    slack_encoding = Column(String(50), default="BINARY_EXPONENTIAL_SLACK")
    status = Column(String(30), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

class QUBOModelRecord(Base):
    __tablename__ = "qubo_models"

    id = Column(Integer, primary_key=True, index=True)
    qubo_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    candidate_set_id = Column(String(60), ForeignKey("strategy_candidate_sets.candidate_set_id"), nullable=False)
    optimization_run_id = Column(String(60), ForeignKey("optimization_runs.optimization_run_id"), nullable=True)
    classical_model_hash = Column(String(64), nullable=False)
    qubo_hash = Column(String(64), unique=True, index=True, nullable=False)
    methodology_id = Column(String(50), ForeignKey("qubo_methodologies.methodology_id"), nullable=False)
    methodology_version = Column(String(30), default="1.0.0")
    objective_version = Column(String(30), default="1.0.0")
    constraint_version = Column(String(30), default="1.0.0")
    candidate_variable_count = Column(Integer, nullable=False)
    slack_variable_count = Column(Integer, default=0)
    total_variable_count = Column(Integer, nullable=False)
    linear_term_count = Column(Integer, default=0)
    quadratic_term_count = Column(Integer, default=0)
    constant_offset = Column(Float, default=0.0)
    matrix_format = Column(String(30), default="SPARSE_DICT")
    coefficient_scale = Column(Float, default=1.0)
    precision = Column(String(30), default="FLOAT64")
    status = Column(String(30), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)

class QUBOVariableRecord(Base):
    __tablename__ = "qubo_variables"

    id = Column(Integer, primary_key=True, index=True)
    variable_id = Column(String(60), unique=True, index=True, nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    index = Column(Integer, nullable=False)
    variable_name = Column(String(100), nullable=False)
    variable_type = Column(String(30), default="STRATEGY")
    candidate_id = Column(String(60), nullable=True)
    strategy_id = Column(String(50), nullable=True)
    slack_constraint_id = Column(String(60), nullable=True)
    slack_bit = Column(Integer, nullable=True)
    meaning = Column(Text, nullable=True)

class QUBOTermRecord(Base):
    __tablename__ = "qubo_terms"

    id = Column(Integer, primary_key=True, index=True)
    term_id = Column(String(60), unique=True, index=True, nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    variable_i = Column(Integer, nullable=False)
    variable_j = Column(Integer, nullable=False)
    term_type = Column(String(30), nullable=False)
    coefficient = Column(Float, nullable=False)
    source_type = Column(String(50), nullable=True)
    source_id = Column(String(100), nullable=True)
    provenance = Column(Text, nullable=True)

class QUBOConstraintRecord(Base):
    __tablename__ = "qubo_constraints"

    id = Column(Integer, primary_key=True, index=True)
    constraint_id = Column(String(60), unique=True, index=True, nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    constraint_type = Column(String(50), nullable=False)
    original_expression = Column(Text, nullable=False)
    qubo_expression = Column(Text, nullable=False)
    slack_variables = Column(JSON, nullable=True)
    penalty_value = Column(Float, nullable=False)
    penalty_method = Column(String(50), default="DYNAMIC_UPPER_BOUND")
    verification_status = Column(String(30), default="VERIFIED")

class QUBOPenaltyRecord(Base):
    __tablename__ = "qubo_penalties"

    id = Column(Integer, primary_key=True, index=True)
    penalty_id = Column(String(60), unique=True, index=True, nullable=False)
    constraint_id = Column(String(60), ForeignKey("qubo_constraints.constraint_id"), nullable=False)
    objective_bound = Column(Float, nullable=False)
    minimum_required_penalty = Column(Float, nullable=False)
    selected_penalty = Column(Float, nullable=False)
    safety_margin = Column(Float, default=2.0)
    derivation = Column(Text, nullable=False)
    validation_status = Column(String(30), default="VERIFIED")

class QUBOCertificateRecord(Base):
    __tablename__ = "qubo_certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(60), unique=True, index=True, nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    classical_model_hash = Column(String(64), nullable=False)
    qubo_hash = Column(String(64), nullable=False)
    candidate_set_version = Column(String(30), default="v1.0")
    district_id = Column(String(50), nullable=False)
    variable_count = Column(Integer, nullable=False)
    tested_state_count = Column(Integer, nullable=False)
    classical_optimum = Column(Float, nullable=False)
    qubo_optimum = Column(Float, nullable=False)
    decoded_objective = Column(Float, nullable=False)
    objective_difference = Column(Float, default=0.0)
    feasibility_match = Column(Boolean, default=True)
    optimality_match = Column(Boolean, default=True)
    penalty_validated = Column(Boolean, default=True)
    status = Column(String(30), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)

class QUBOValidationRecord(Base):
    __tablename__ = "qubo_validations"

    id = Column(Integer, primary_key=True, index=True)
    validation_id = Column(String(60), unique=True, index=True, nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    validation_type = Column(String(50), default="EXHAUSTIVE_BITSTRING_SEARCH")
    result_status = Column(String(30), default="PASSED")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class QUBOExportRecord(Base):
    __tablename__ = "qubo_exports"

    id = Column(Integer, primary_key=True, index=True)
    export_id = Column(String(60), unique=True, index=True, nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    format = Column(String(30), default="JSON")
    export_payload = Column(JSON, nullable=False)
    exported_at = Column(DateTime, default=datetime.utcnow)

# Phase M — Enterprise QAOA Implementation & Benchmarking Models
class QAOAExperimentRecord(Base):
    __tablename__ = "qaoa_experiments"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(60), unique=True, index=True, nullable=False)
    run_id = Column(String(60), nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    qubo_hash = Column(String(64), nullable=False)
    classical_model_hash = Column(String(64), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    candidate_count = Column(Integer, nullable=False)
    slack_count = Column(Integer, default=0)
    logical_qubit_count = Column(Integer, nullable=False)
    qaoa_depth = Column(Integer, default=1)
    optimizer = Column(String(50), default="COBYLA")
    optimizer_config = Column(JSON, nullable=True)
    initialization_method = Column(String(50), default="ZERO_AND_RANDOM_HYBRID")
    seed = Column(Integer, default=42)
    shots = Column(Integer, default=1000)
    backend = Column(String(80), default="aer_simulator_statevector")
    backend_type = Column(String(50), default="EXACT_STATEVECTOR")
    noise_model = Column(String(50), default="NONE")
    transpiler_config = Column(JSON, nullable=True)
    initial_parameters = Column(JSON, nullable=True)
    final_parameters = Column(JSON, nullable=True)
    final_expectation = Column(Float, nullable=True)
    best_sample_energy = Column(Float, nullable=True)
    best_sample_objective = Column(Float, nullable=True)
    classical_optimum_objective = Column(Float, nullable=True)
    objective_gap = Column(Float, nullable=True)
    relative_objective_gap = Column(Float, nullable=True)
    feasible_probability = Column(Float, default=0.0)
    optimal_probability = Column(Float, default=0.0)
    near_optimal_probability = Column(Float, default=0.0)
    constraint_violation_rate = Column(Float, default=0.0)
    circuit_depth_pre_transpile = Column(Integer, nullable=True)
    circuit_depth_post_transpile = Column(Integer, nullable=True)
    gate_count = Column(Integer, nullable=True)
    two_qubit_gate_count = Column(Integer, nullable=True)
    transpilation_time = Column(Float, default=0.0)
    optimization_time = Column(Float, default=0.0)
    sampling_time = Column(Float, default=0.0)
    total_time = Column(Float, default=0.0)
    convergence_status = Column(String(30), default="OPTIMAL")
    created_at = Column(DateTime, default=datetime.utcnow)

class QAOASampleRecord(Base):
    __tablename__ = "qaoa_samples"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String(60), unique=True, index=True, nullable=False)
    experiment_id = Column(String(60), ForeignKey("qaoa_experiments.experiment_id"), nullable=False)
    bitstring = Column(String(100), nullable=False)
    probability = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    decoded_strategy_ids = Column(JSON, nullable=False)
    decoded_slack_values = Column(JSON, nullable=True)
    qubo_energy = Column(Float, nullable=False)
    original_objective = Column(Float, nullable=False)
    is_feasible = Column(Boolean, default=True)
    is_optimal = Column(Boolean, default=False)
    is_near_optimal = Column(Boolean, default=False)
    constraint_violations = Column(JSON, nullable=True)

class QAOACircuitRecord(Base):
    __tablename__ = "qaoa_circuits"

    id = Column(Integer, primary_key=True, index=True)
    circuit_id = Column(String(60), unique=True, index=True, nullable=False)
    experiment_id = Column(String(60), ForeignKey("qaoa_experiments.experiment_id"), nullable=False)
    qubit_count = Column(Integer, nullable=False)
    qaoa_depth = Column(Integer, nullable=False)
    gate_count = Column(Integer, nullable=False)
    two_qubit_gate_count = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    transpiled_depth = Column(Integer, nullable=True)
    basis_gates = Column(JSON, nullable=True)
    backend = Column(String(80), nullable=False)
    circuit_hash = Column(String(64), nullable=False)

class QAOACertificateRecord(Base):
    __tablename__ = "qaoa_certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(60), unique=True, index=True, nullable=False)
    experiment_id = Column(String(60), ForeignKey("qaoa_experiments.experiment_id"), nullable=False)
    qubo_id = Column(String(60), ForeignKey("qubo_models.qubo_id"), nullable=False)
    qubo_hash = Column(String(64), nullable=False)
    classical_hash = Column(String(64), nullable=False)
    district_id = Column(String(50), nullable=False)
    best_bitstring = Column(String(100), nullable=False)
    best_energy = Column(Float, nullable=False)
    best_original_objective = Column(Float, nullable=False)
    classical_optimum = Column(Float, nullable=False)
    objective_gap = Column(Float, nullable=False)
    feasibility_status = Column(String(30), default="FEASIBLE")
    optimality_status = Column(String(30), default="OPTIMAL")
    circuit_hash = Column(String(64), nullable=False)
    status = Column(String(30), default="VERIFIED")
    timestamp = Column(DateTime, default=datetime.utcnow)

class QAOABenchmarkRecord(Base):
    __tablename__ = "qaoa_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    benchmark_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), nullable=False)
    qubo_id = Column(String(60), nullable=False)
    qubit_count = Column(Integer, nullable=False)
    classical_method = Column(String(50), nullable=False)
    qaoa_p = Column(Integer, nullable=False)
    shots = Column(Integer, nullable=False)
    seed = Column(Integer, nullable=False)
    classical_objective = Column(Float, nullable=False)
    qaoa_objective = Column(Float, nullable=False)
    objective_gap = Column(Float, nullable=False)
    feasible_probability = Column(Float, nullable=False)
    optimal_probability = Column(Float, nullable=False)
    runtime_ms = Column(Float, nullable=False)
    circuit_depth = Column(Integer, nullable=False)
    two_qubit_gates = Column(Integer, nullable=False)
    status = Column(String(30), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase N — Enterprise RAG, Evidence Integration & Decision Explanation Models
class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(60), unique=True, index=True, nullable=False)
    source_id = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    organization = Column(String(150), nullable=False)
    source_tier = Column(String(30), default="Tier 1")
    publication_year = Column(Integer, nullable=True)
    version = Column(String(30), default="1.0.0")
    geographic_scope = Column(String(100), default="Tamil Nadu")
    file_hash = Column(String(64), nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)

class DocumentVersionRecord(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(String(60), unique=True, index=True, nullable=False)
    document_id = Column(String(60), ForeignKey("documents.document_id"), nullable=False)
    version_number = Column(String(30), nullable=False)
    file_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EvidenceLinkRecord(Base):
    __tablename__ = "evidence_links"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(String(60), unique=True, index=True, nullable=False)
    strategy_id = Column(String(50), ForeignKey("strategies.strategy_id"), nullable=False)
    claim_id = Column(String(60), nullable=False)
    relationship_type = Column(String(40), default="SUPPORTS")
    support_strength = Column(String(30), default="STRONG")
    geographic_relevance = Column(String(50), default="STATE")
    hazard_relevance = Column(String(50), nullable=True)
    sector_relevance = Column(String(50), nullable=True)
    review_status = Column(String(30), default="VERIFIED")

class EvidenceConflictRecord(Base):
    __tablename__ = "evidence_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    conflict_id = Column(String(60), unique=True, index=True, nullable=False)
    claim_a_id = Column(String(60), nullable=False)
    claim_b_id = Column(String(60), nullable=False)
    source_a_id = Column(String(50), nullable=False)
    source_b_id = Column(String(50), nullable=False)
    conflict_type = Column(String(50), default="QUALITATIVE_DISAGREEMENT")
    resolution_status = Column(String(40), default="CONTEXTUALIZED")
    context_notes = Column(Text, nullable=True)

class CitationRecord(Base):
    __tablename__ = "citation_records"

    id = Column(Integer, primary_key=True, index=True)
    citation_id = Column(String(60), unique=True, index=True, nullable=False)
    source_id = Column(String(50), nullable=False)
    document_id = Column(String(60), nullable=False)
    chunk_id = Column(String(60), nullable=True)
    claim_id = Column(String(60), nullable=True)
    title = Column(String(255), nullable=False)
    organization = Column(String(150), nullable=False)
    year = Column(Integer, nullable=True)
    page = Column(Integer, nullable=True)
    section = Column(String(100), nullable=True)
    url = Column(String(255), nullable=True)
    source_tier = Column(String(30), default="Tier 1")
    created_at = Column(DateTime, default=datetime.utcnow)

class RAGQueryRecord(Base):
    __tablename__ = "rag_queries"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), nullable=True)
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50), default="STRATEGY_EVIDENCE")
    top_k = Column(Integer, default=5)
    retrieved_chunk_count = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class RAGResultRecord(Base):
    __tablename__ = "rag_results"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(String(60), unique=True, index=True, nullable=False)
    query_id = Column(String(60), ForeignKey("rag_queries.query_id"), nullable=False)
    chunk_id = Column(String(60), nullable=False)
    citation_id = Column(String(60), nullable=False)
    similarity_score = Column(Float, nullable=False)
    rerank_score = Column(Float, nullable=True)

class ExplanationRecord(Base):
    __tablename__ = "explanation_records"

    id = Column(Integer, primary_key=True, index=True)
    explanation_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    optimization_run_id = Column(String(60), nullable=True)
    qaoa_experiment_id = Column(String(60), nullable=True)
    model = Column(String(80), nullable=False)
    model_version = Column(String(30), default="1.0.0")
    prompt_version = Column(String(30), default="1.0.0")
    retrieval_version = Column(String(30), default="1.0.0")
    knowledge_base_version = Column(String(30), default="v1.0.0_verified")
    context_hash = Column(String(64), nullable=False)
    evidence_packet_hash = Column(String(64), nullable=False)
    decision_summary = Column(Text, nullable=False)
    explanation_payload = Column(JSON, nullable=False)
    validation_status = Column(String(30), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)

class ExplanationClaimRecord(Base):
    __tablename__ = "explanation_claims"

    id = Column(Integer, primary_key=True, index=True)
    explanation_claim_id = Column(String(60), unique=True, index=True, nullable=False)
    explanation_id = Column(String(60), ForeignKey("explanation_records.explanation_id"), nullable=False)
    claim_text = Column(Text, nullable=False)
    claim_type = Column(String(50), default="FACTUAL")
    citation_ids = Column(JSON, nullable=False)
    support_status = Column(String(30), default="SUPPORTED")

class HumanReviewRecord(Base):
    __tablename__ = "human_reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String(60), unique=True, index=True, nullable=False)
    explanation_id = Column(String(60), ForeignKey("explanation_records.explanation_id"), nullable=False)
    issue_type = Column(String(50), nullable=False)
    reviewer = Column(String(100), default="SYSTEM_AUDITOR")
    decision = Column(String(30), default="APPROVED")
    comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeBaseVersionRecord(Base):
    __tablename__ = "knowledge_base_versions"

    id = Column(Integer, primary_key=True, index=True)
    kb_version_id = Column(String(60), unique=True, index=True, nullable=False)
    version = Column(String(30), nullable=False)
    document_count = Column(Integer, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    claim_count = Column(Integer, nullable=False)
    checksum = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Phase O — Enterprise Decision Intelligence API & Multi-Agent Orchestration Models
class DecisionRequestRecord(Base):
    __tablename__ = "decision_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(60), unique=True, index=True, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    hazard_ids = Column(JSON, nullable=True)
    optimization_mode = Column(String(40), default="CLASSICAL")
    qaoa_p_depth = Column(Integer, default=2)
    explanation_mode = Column(String(40), default="STRICT_GROUNDED")
    idempotency_key = Column(String(100), index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionWorkflowRecord(Base):
    __tablename__ = "decision_workflows"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String(60), unique=True, index=True, nullable=False)
    request_id = Column(String(60), ForeignKey("decision_requests.request_id"), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    status = Column(String(30), default="RUNNING") # RUNNING, COMPLETED, FAILED, CANCELLED, DEGRADED
    current_stage = Column(String(50), default="DISTRICT_RESOLUTION")
    stage_history = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class WorkflowEventRecord(Base):
    __tablename__ = "workflow_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(60), unique=True, index=True, nullable=False)
    workflow_id = Column(String(60), ForeignKey("decision_workflows.workflow_id"), nullable=False)
    stage = Column(String(50), nullable=False)
    event_type = Column(String(50), nullable=False) # STAGE_STARTED, STAGE_COMPLETED, STAGE_FAILED, STAGE_RETRIED
    duration_ms = Column(Float, default=0.0)
    status = Column(String(30), default="SUCCESS")
    event_metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WorkflowCheckpointRecord(Base):
    __tablename__ = "workflow_checkpoints"

    id = Column(Integer, primary_key=True, index=True)
    checkpoint_id = Column(String(60), unique=True, index=True, nullable=False)
    workflow_id = Column(String(60), ForeignKey("decision_workflows.workflow_id"), nullable=False)
    stage = Column(String(50), nullable=False)
    state_payload = Column(JSON, nullable=False)
    context_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionResultRecord(Base):
    __tablename__ = "decision_results"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(String(60), unique=True, index=True, nullable=False)
    request_id = Column(String(60), ForeignKey("decision_requests.request_id"), nullable=False)
    workflow_id = Column(String(60), ForeignKey("decision_workflows.workflow_id"), nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    risk_score = Column(Float, nullable=False)
    priority_score = Column(Float, nullable=False)
    selected_strategy_ids = Column(JSON, nullable=False)
    optimization_run_id = Column(String(60), nullable=True)
    qaoa_experiment_id = Column(String(60), nullable=True)
    explanation_id = Column(String(60), nullable=True)
    context_hash = Column(String(64), nullable=False)
    evidence_packet_hash = Column(String(64), nullable=False)
    result_payload = Column(JSON, nullable=False)
    validation_status = Column(String(30), default="VERIFIED")
    schema_version = Column(String(30), default="1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionProvenanceRecord(Base):
    __tablename__ = "decision_provenance"

    id = Column(Integer, primary_key=True, index=True)
    provenance_id = Column(String(60), unique=True, index=True, nullable=False)
    decision_id = Column(String(60), ForeignKey("decision_results.decision_id"), nullable=False)
    context_hash = Column(String(64), nullable=False)
    evidence_packet_hash = Column(String(64), nullable=False)
    system_versions = Column(JSON, nullable=False)
    snapshots = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionErrorRecord(Base):
    __tablename__ = "decision_errors"

    id = Column(Integer, primary_key=True, index=True)
    error_id = Column(String(60), unique=True, index=True, nullable=False)
    workflow_id = Column(String(60), nullable=False)
    stage = Column(String(50), nullable=False)
    error_code = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    retryable = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class HumanOverrideRecord(Base):
    __tablename__ = "human_overrides"

    id = Column(Integer, primary_key=True, index=True)
    override_id = Column(String(60), unique=True, index=True, nullable=False)
    decision_id = Column(String(60), ForeignKey("decision_results.decision_id"), nullable=False)
    actor = Column(String(100), nullable=False)
    override_type = Column(String(50), nullable=False)
    original_value = Column(JSON, nullable=False)
    new_value = Column(JSON, nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)








