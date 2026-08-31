from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class HazardScore(BaseModel):
    probability: float
    risk_level: str  # 'LOW', 'MEDIUM', 'HIGH'
    threshold_applied: float
    confidence_note: Optional[str] = None

class DailyRiskAssessment(BaseModel):
    date: str
    flood: HazardScore
    heatwave: HazardScore
    drought: HazardScore
    overall_hazard_level: str
    features_summary: Optional[Dict[str, float]] = None

class DistrictRiskResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    district_id: str
    district_name: str
    date: str
    spatial_resolution: str = "District-level (Administrative ADM2)"
    model_status: str = "Verified XGBoost Ensemble (53 features)"
    assessment: DailyRiskAssessment
    climatological_context: Optional[Dict[str, Any]] = None
    demographic_exposure: Optional[Dict[str, Any]] = None
    data_quality: Optional[Dict[str, Any]] = None

class TimelineRiskResponse(BaseModel):
    district_id: str
    district_name: str
    spatial_resolution: str = "District-level"
    timeline: List[DailyRiskAssessment]
