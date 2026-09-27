import logging
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

logger = logging.getLogger("hazards_api")

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
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

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
    except Exception as e:
        logger.warning(f"[DATA] Air Quality unavailable for {district.district_name}: {e}")

    if profile.get("coastal"):
        try:
            marine = await ClimateDataAgent.get_marine_data(district.latitude, district.longitude)
            extra_data["marine"] = marine
        except Exception as e:
            logger.warning(f"[DATA] Marine API unavailable for {district.district_name}: {e}")

    engine = RiskEngine.get_instance()
    raw_daily = forecast.get("raw_daily", forecast.get("daily", {}))
    raw_hourly = forecast.get("raw_hourly", forecast.get("hourly", {}))

    eval_result = engine.calculate_all(
        district_name=district.district_name,
        day_index=day,
        forecast_daily=raw_daily,
        forecast_hourly=raw_hourly,
        district_profile=profile,
        extra_data=extra_data
    )

    logger.info(f"[RISK] Multi-hazard evaluation completed for {district.district_name} (Day {day}): Threat Level = {eval_result.get('overall_threat_level')}")

    return {
        "district_id": district.district_id,
        "district_name": district.district_name,
        "day_index": day,
        "overall_threat_level": eval_result["overall_threat_level"],
        "hazards": eval_result["hazards"],
        "demographic_exposure": profile,
        "forecast_current": forecast.get("current", {})
    }

@router.get("/risk/{district_id}/hazard/{hazard_id}", summary="Single hazard evaluation")
async def get_single_hazard(
    district_id: str,
    hazard_id: str,
    day: int = Query(0, ge=0, le=6),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    registry = HazardRegistry.get_instance()
    hazard_mod = registry.get(hazard_id)
    if not hazard_mod:
        raise HTTPException(status_code=404, detail=f"Hazard '{hazard_id}' not found in registry.")

    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()

    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    profile_obj = db.query(DistrictProfile).filter(DistrictProfile.district_id == district.district_id).first()
    profile = {
        "population": profile_obj.population if profile_obj else 1000000,
        "urban_percentage": profile_obj.urban_percentage if profile_obj else 40.0,
        "coastal": profile_obj.coastal if profile_obj else False,
        "elevation_m": profile_obj.elevation_m if profile_obj else 50.0
    }

    forecast = await ClimateDataAgent.get_forecast(district.latitude, district.longitude, district.district_id)
    extra_data = {}

    if hazard_id == "air_quality":
        extra_data["air_quality"] = await ClimateDataAgent.get_air_quality(district.latitude, district.longitude)
    elif hazard_id == "coastal" and profile.get("coastal"):
        extra_data["marine"] = await ClimateDataAgent.get_marine_data(district.latitude, district.longitude)

    raw_daily = forecast.get("raw_daily", forecast.get("daily", {}))
    raw_hourly = forecast.get("raw_hourly", forecast.get("hourly", {}))

    res = hazard_mod.calculate(
        district_name=district.district_name,
        day_index=day,
        forecast_daily=raw_daily,
        forecast_hourly=raw_hourly,
        district_profile=profile,
        extra_data=extra_data
    )

    return res.to_dict()

@router.get("/system/debug", summary="Admin system debug & distribution inspection")
async def get_system_debug(
    district_id: str = Query("chennai"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Exposes raw forecast inputs, derived features, training distribution comparisons,
    and contract validation state.
    """
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()

    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    forecast = await ClimateDataAgent.get_forecast(district.latitude, district.longitude, district.district_id)
    fe = FeatureEngineeringService()
    raw_daily = forecast.get("raw_daily", forecast.get("daily", {}))
    raw_hourly = forecast.get("raw_hourly", forecast.get("hourly", {}))

    feat_res = fe.build_feature_vector(
        district_name=district.district_name,
        day_index=0,
        daily_forecast=raw_daily,
        hourly_forecast=raw_hourly
    )

    feat_dict = feat_res["features_dict"]

    comparison = []
    for feat_name, dist_info in TRAINING_DISTRIBUTIONS.items():
        val = feat_dict.get(feat_name, None)
        out_of_bounds = False
        if val is not None and isinstance(val, (int, float)):
            out_of_bounds = (val < dist_info["min"] or val > dist_info["max"])
        comparison.append({
            "feature": feat_name,
            "forecast_value": val,
            "training_min": dist_info["min"],
            "training_mean": dist_info["mean"],
            "training_max": dist_info["max"],
            "unit": dist_info["unit"],
            "out_of_distribution": out_of_bounds
        })

    # Contract validations
    ok_f, r_f, m_f = FeatureContractValidator.validate(FLOOD_CONTRACT, feat_dict)
    ok_d, r_d, m_d = FeatureContractValidator.validate(DROUGHT_CONTRACT, feat_dict)
    ok_h, r_h, m_h = FeatureContractValidator.validate(HEATWAVE_CONTRACT, feat_dict)

    logger.info(f"[VALIDATION] System debug ran for {district.district_name}. Contracts: Flood={ok_f}, Drought={ok_d}, Heatwave={ok_h}")

    return {
        "district": district.district_name,
        "features_comparison": comparison,
        "contracts": {
            "flood": {"valid": ok_f, "reason": r_f, "missing": m_f},
            "drought": {"valid": ok_d, "reason": r_d, "missing": m_d},
            "heatwave": {"valid": ok_h, "reason": r_h, "missing": m_h}
        },
        "raw_current": forecast.get("current", {})
    }
