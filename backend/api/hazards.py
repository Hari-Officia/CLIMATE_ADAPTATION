from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import District, DistrictProfile, User
from backend.api.auth import get_current_user, require_admin
from backend.agents.climate_data_agent import ClimateDataAgent
from backend.hazards.registry import HazardRegistry
from backend.hazards.risk_engine import RiskEngine
from backend.risk.feature_contract import TRAINING_DISTRIBUTIONS, FLOOD_CONTRACT, DROUGHT_CONTRACT, HEATWAVE_CONTRACT, FeatureContractValidator
from backend.services.feature_engineering import FeatureEngineeringService

router = APIRouter(tags=["Hazards & Multi-Hazard Risk Engine"])

@router.get("/hazards", summary="List all registered climate hazards")
def list_hazards() -> List[Dict[str, Any]]:
    """Returns metadata for all 10 registered hazard modules."""
    registry = HazardRegistry.get_instance()
    return registry.list_all()

@router.get("/hazards/{hazard_id}", summary="Get metadata for a single hazard")
def get_hazard_metadata(hazard_id: str) -> Dict[str, Any]:
    registry = HazardRegistry.get_instance()
    h = registry.get(hazard_id)
    if not h:
        raise HTTPException(status_code=404, detail=f"Hazard '{hazard_id}' not found in registry.")
    return {
        "id": h.hazard_id,
        "name": h.hazard_name,
        "engine_type": h.engine_type,
        "description": h.description,
        "temporal_resolution": h.temporal_resolution,
        "spatial_resolution": h.spatial_resolution
    }

@router.get("/risk/{district_id}/hazards", summary="Comprehensive multi-hazard evaluation")
async def get_district_hazards(
    district_id: str,
    day: int = Query(0, ge=0, le=6, description="Forecast day index (0=Today, 6=Day 7)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Executes full multi-hazard evaluation (Type A ML models, Type B rules, Type C external sources)
    for a district with failure isolation.
    """
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    profile_obj = db.query(DistrictProfile).filter(DistrictProfile.district_id == district.district_id).first()
    profile = {
        "population": profile_obj.population if profile_obj else 1000000,
        "urban_percentage": profile_obj.urban_percentage if profile_obj else 40.0,
        "coastal": profile_obj.coastal if profile_obj else False,
        "elevation_m": profile_obj.elevation_m if profile_obj else 50.0
    }

    # Fetch weather forecast
    forecast = await ClimateDataAgent.get_forecast(district.latitude, district.longitude, district.district_id)

    # Fetch Air Quality and Marine data where applicable
    extra_data = {}
    try:
        aq = await ClimateDataAgent.get_air_quality(district.latitude, district.longitude)
        extra_data["air_quality"] = aq
    except Exception:
        pass

    if profile.get("coastal"):
        try:
            marine = await ClimateDataAgent.get_marine_data(district.latitude, district.longitude)
            extra_data["marine"] = marine
        except Exception:
            pass

    engine = RiskEngine.get_instance()
    result = engine.calculate_all(
        district_name=district.district_name,
        day_index=day,
        forecast_daily=forecast.get("raw_daily", forecast.get("daily", {})),
        forecast_hourly=forecast.get("raw_hourly", forecast.get("hourly", {})),
        district_profile=profile,
        historical_baseline=None,
        extra_data=extra_data
    )

    result["district_id"] = district.district_id
    result["coordinates"] = {"latitude": district.latitude, "longitude": district.longitude}
    result["demographic_exposure"] = profile

    return result

@router.get("/risk/{district_id}/hazard/{hazard_id}", summary="Single hazard evaluation")
async def get_district_single_hazard(
    district_id: str,
    hazard_id: str,
    day: int = Query(0, ge=0, le=6),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    profile_obj = db.query(DistrictProfile).filter(DistrictProfile.district_id == district.district_id).first()
    profile = {
        "coastal": profile_obj.coastal if profile_obj else False,
        "population": profile_obj.population if profile_obj else 1000000
    }

    forecast = await ClimateDataAgent.get_forecast(district.latitude, district.longitude, district.district_id)
    extra_data = {}
    if hazard_id == "air_quality":
        extra_data["air_quality"] = await ClimateDataAgent.get_air_quality(district.latitude, district.longitude)
    elif hazard_id == "coastal" and profile.get("coastal"):
        extra_data["marine"] = await ClimateDataAgent.get_marine_data(district.latitude, district.longitude)

    engine = RiskEngine.get_instance()
    res = engine.calculate_single(
        hazard_id=hazard_id,
        district_name=district.district_name,
        day_index=day,
        forecast_daily=forecast.get("raw_daily", forecast.get("daily", {})),
        forecast_hourly=forecast.get("raw_hourly", forecast.get("hourly", {})),
        district_profile=profile,
        historical_baseline=None,
        extra_data=extra_data
    )

    if not res:
        raise HTTPException(status_code=404, detail=f"Hazard '{hazard_id}' not found.")

    return res

@router.get("/system/debug", summary="Admin Debug Inspection Mode")
async def get_system_debug(
    district_id: str = Query("chennai"),
    day: int = Query(0, ge=0, le=6),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """
    ADMIN ONLY: Comprehensive debug endpoint exposing raw forecast values,
    53 derived features, training distribution min/max comparisons,
    and contract validation status.
    """
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()
    if not district:
        district = db.query(District).first()

    forecast = await ClimateDataAgent.get_forecast(district.latitude, district.longitude, district.district_id)
    fe_service = FeatureEngineeringService()
    res = fe_service.build_feature_vector(
        district_name=district.district_name,
        day_index=day,
        daily_forecast=forecast.get("raw_daily", forecast.get("daily", {})),
        hourly_forecast=forecast.get("raw_hourly", forecast.get("hourly", {}))
    )

    feat_dict = res["features_dict"]

    # Compare features against training distributions
    comparison = []
    for k, v in feat_dict.items():
        if k in TRAINING_DISTRIBUTIONS:
            dist = TRAINING_DISTRIBUTIONS[k]
            is_out = (v < dist["min"]) or (v > dist["max"]) if v is not None else False
            comparison.append({
                "feature": k,
                "forecast_value": v,
                "training_min": dist["min"],
                "training_max": dist["max"],
                "training_mean": dist["mean"],
                "out_of_distribution": is_out
            })

    # Validate contracts
    v_flood, r_flood, _ = FeatureContractValidator.validate(FLOOD_CONTRACT, feat_dict)
    v_drought, r_drought, _ = FeatureContractValidator.validate(DROUGHT_CONTRACT, feat_dict)
    v_heat, r_heat, _ = FeatureContractValidator.validate(HEATWAVE_CONTRACT, feat_dict)

    return {
        "district": district.district_name,
        "day_index": day,
        "raw_forecast_current": forecast.get("current"),
        "features_comparison": comparison,
        "contracts": {
            "flood": {"valid": v_flood, "reason": r_flood},
            "drought": {"valid": v_drought, "reason": r_drought},
            "heatwave": {"valid": v_heat, "reason": r_heat}
        },
        "training_bounds": TRAINING_DISTRIBUTIONS
    }

@router.get("/risk/{district_id}/diagnostics", summary="Feature Contract Diagnostics (Admin)")
async def get_district_diagnostics(
    district_id: str,
    day: int = Query(0, ge=0, le=6),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """ADMIN ONLY: Diagnostic report comparing model input and distributions."""
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    forecast = await ClimateDataAgent.get_forecast(district.latitude, district.longitude, district.district_id)
    fe_service = FeatureEngineeringService()
    res = fe_service.build_feature_vector(
        district_name=district.district_name,
        day_index=day,
        daily_forecast=forecast.get("raw_daily", forecast.get("daily", {})),
        hourly_forecast=forecast.get("raw_hourly", forecast.get("hourly", {}))
    )

    diag_flood = FeatureContractValidator.diagnose_prediction(
        model_name="flood_xgboost",
        feature_dict=res["features_dict"],
        raw_probability=0.0004,
        predicted_class="LOW",
        contract=FLOOD_CONTRACT
    )

    return {
        "district": district.district_name,
        "flood_diagnostics": diag_flood,
        "training_distributions": TRAINING_DISTRIBUTIONS
    }
