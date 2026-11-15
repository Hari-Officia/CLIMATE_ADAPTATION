import os
import json
import time
import asyncio
import logging
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District, DistrictProfile
from backend.agents.risk_agent import RiskAgent
from backend.agents.climate_data_agent import ClimateDataAgent

from backend.risk.thresholds import classify_ml_probability

logger = logging.getLogger("gis_api")

router = APIRouter(tags=["GIS & Spatial"])

GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "geojson", "tamil_nadu_districts.geojson")

_overlay_cache = {}
_overlay_cache_ttl = 1800  # 30 mins

@router.get("/districts-geojson")
async def get_districts_geojson(db: Session = Depends(get_db)):
    if not os.path.exists(GEOJSON_PATH):
        raise HTTPException(status_code=500, detail="GeoJSON asset not found")

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    profiles = {p.district_id: p for p in db.query(DistrictProfile).all()}
    for feat in geojson.get("features", []):
        props = feat.get("properties", {})
        d_id = props.get("district_id")
        if d_id and d_id in profiles:
            p = profiles[d_id]
            props["population"] = p.population
            props["population_density"] = p.population_density
            props["urban_percentage"] = p.urban_percentage
            props["coastal"] = p.coastal
            props["elevation_m"] = p.elevation_m

    return geojson

@router.get("/risk-overlay")
async def get_risk_overlay(
    hazard: str = Query("flood", pattern="^(flood|heatwave|drought|overall)$"),
    day: int = Query(0, ge=0, le=6),
    db: Session = Depends(get_db)
):
    """
    Returns GeoJSON FeatureCollection enriched with authoritative ML hazard probabilities
    and risk levels for each district for the specified day and hazard.
    """
    cache_key = f"{hazard}_{day}"
    now = time.time()
    if cache_key in _overlay_cache:
        entry = _overlay_cache[cache_key]
        if now - entry["timestamp"] < _overlay_cache_ttl:
            logger.info(f"[GIS] Serving risk overlay from memory cache for {cache_key}")
            return entry["data"]

    if not os.path.exists(GEOJSON_PATH):
        raise HTTPException(status_code=500, detail="GeoJSON asset not found")

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    districts = {d.district_id: d for d in db.query(District).all()}
    profiles = {p.district_id: p for p in db.query(DistrictProfile).all()}
    risk_agent = RiskAgent.get_instance()

    features = geojson.get("features", [])
    district_objs = [districts.get(feat.get("properties", {}).get("district_id")) for feat in features]

    # Concurrent forecast gathering
    async def fetch_forecast(district_obj, d_id):
        if not district_obj:
            return None
        try:
            return await ClimateDataAgent.get_forecast(
                lat=district_obj.latitude,
                lon=district_obj.longitude,
                district_id=d_id
            )
        except Exception as e:
            logger.warning(f"[GIS] Failed to fetch forecast for {d_id}: {e}")
            return None

    forecast_results = await asyncio.gather(
        *[fetch_forecast(d_obj, feat.get("properties", {}).get("district_id")) for d_obj, feat in zip(district_objs, features)]
    )

    for feat, forecast in zip(features, forecast_results):
        props = feat.get("properties", {})
        d_id = props.get("district_id")
        d_name = props.get("district_name", d_id)

        props["hazard"] = hazard
        props["day_index"] = day

        if d_id in profiles:
            p = profiles[d_id]
            props["population"] = p.population
            props["population_density"] = p.population_density
            props["urban_percentage"] = p.urban_percentage
            props["coastal"] = p.coastal

        if forecast:
            try:
                raw_daily = forecast.get("raw_daily", forecast.get("daily", {}))
                raw_hourly = forecast.get("raw_hourly", forecast.get("hourly", {}))
                assessment = risk_agent.assess_risk(
                    district_name=d_name,
                    forecast_day_index=day,
                    daily_forecast_list=raw_daily,
                    hourly_forecast_list=raw_hourly
                )

                props["overall_risk"] = assessment.get("overall_hazard_level", "LOW")
                props["flood_probability"] = assessment.get("flood", {}).get("probability", None)
                props["flood_risk"] = assessment.get("flood", {}).get("risk_level", "UNAVAILABLE")
                props["heatwave_probability"] = assessment.get("heatwave", {}).get("probability", None)
                props["heatwave_risk"] = assessment.get("heatwave", {}).get("risk_level", "UNAVAILABLE")

                # Drought status
                drought_info = assessment.get("drought", {})
                props["drought_probability"] = drought_info.get("probability", None)
                props["drought_risk"] = drought_info.get("risk_level", "UNAVAILABLE")
                props["drought_status"] = drought_info.get("status", "UNAVAILABLE")

                if hazard == "flood":
                    props["probability"] = props["flood_probability"]
                    props["risk_level"] = props["flood_risk"]
                elif hazard == "heatwave":
                    props["probability"] = props["heatwave_probability"]
                    props["risk_level"] = props["heatwave_risk"]
                elif hazard == "drought":
                    props["probability"] = props["drought_probability"]
                    props["risk_level"] = props["drought_risk"]
                else:  # overall
                    valid_probs = [p for p in [props["flood_probability"], props["heatwave_probability"], props["drought_probability"]] if p is not None]
                    if valid_probs:
                        max_p = max(valid_probs)
                        props["probability"] = max_p
                        props["risk_level"] = classify_ml_probability(max_p)
                        props["overall_risk"] = props["risk_level"]
                    else:
                        props["probability"] = None
                        props["risk_level"] = "UNAVAILABLE"
                        props["overall_risk"] = "UNAVAILABLE"

            except Exception as e:
                logger.error(f"[GIS] Risk evaluation failed for {d_name}: {e}")
                props["probability"] = None
                props["risk_level"] = "UNAVAILABLE"
                props["overall_risk"] = "UNAVAILABLE"
        else:
            props["probability"] = None
            props["risk_level"] = "UNAVAILABLE"
            props["overall_risk"] = "UNAVAILABLE"

    _overlay_cache[cache_key] = {"timestamp": now, "data": geojson}
    logger.info(f"[GIS] Computed & cached risk overlay for hazard='{hazard}', day={day}")
    return geojson

PHASE7_GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "geojson", "phase7_tamil_nadu_adaptation_overlay.geojson")

@router.get("/adaptation-overlay")
async def get_adaptation_overlay():
    """
    Phase 7 — Returns enriched Spatial GeoJSON FeatureCollection containing 
    climate risk, MILP portfolios, QAOA portfolios, and comparative metrics 
    for all 38 Tamil Nadu districts.
    """
    path = PHASE7_GEOJSON_PATH if os.path.exists(PHASE7_GEOJSON_PATH) else GEOJSON_PATH
    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail="Phase 7 Adaptation Overlay GeoJSON not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/districts/{district_id}")
async def get_district_gis_detail(district_id: str):
    """
    Phase 7 — Returns individual district spatial decision intelligence, 
    including hazard risk, MILP portfolio, QAOA portfolio, and comparison.
    """
    d_clean = district_id.lower().strip()
    path = PHASE7_GEOJSON_PATH if os.path.exists(PHASE7_GEOJSON_PATH) else GEOJSON_PATH
    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail="GIS GeoJSON asset not found")
    with open(path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    for feat in geojson.get("features", []):
        props = feat.get("properties", {})
        if props.get("district_id", "").lower() == d_clean:
            return {
                "district_id": props.get("district_id"),
                "district_name": props.get("district_name"),
                "geometry": feat.get("geometry"),
                "properties": props
            }
    raise HTTPException(status_code=404, detail=f"District '{district_id}' not found in spatial decision model")

@router.get("/portfolio/{district_id}")
async def get_district_portfolio(district_id: str):
    """
    Phase 7 — Returns MILP ground truth and QAOA quantum candidate strategy portfolios for a specific district.
    """
    detail = await get_district_gis_detail(district_id)
    props = detail["properties"]
    milp_ids = props.get("milp_strategy_ids", props.get("milp_strategies", []))
    qaoa_ids = props.get("qaoa_strategy_ids", props.get("qaoa_strategies", []))
    return {
        "district_id": props.get("district_id"),
        "district_name": props.get("district_name"),
        "milp": {
            "selected_strategy_ids": milp_ids,
            "selected_strategy_names": props.get("milp_strategy_names", []),
            "selected_count": props.get("milp_selected_count", len(milp_ids)),
            "objective_value": props.get("milp_objective"),
            "domains": props.get("milp_domains", [])
        },
        "qaoa": {
            "selected_strategy_ids": qaoa_ids,
            "selected_strategy_names": props.get("qaoa_strategy_names", []),
            "selected_count": props.get("qaoa_selected_count", len(qaoa_ids)),
            "objective_value": props.get("qaoa_objective"),
            "approximation_ratio": props.get("qaoa_approximation_ratio"),
            "status": props.get("qaoa_status"),
            "domains": props.get("qaoa_domains", [])
        }
    }

@router.get("/comparison/{district_id}")
async def get_district_comparison(district_id: str):
    """
    Phase 7 — Returns comparative metrics between classical MILP ground truth and QAOA quantum approximate solution.
    """
    detail = await get_district_gis_detail(district_id)
    props = detail["properties"]
    milp_sids = props.get("milp_strategy_ids", props.get("milp_strategies", []))
    qaoa_sids = props.get("qaoa_strategy_ids", props.get("qaoa_strategies", []))
    milp_strats = set(milp_sids)
    qaoa_strats = set(qaoa_sids)
    
    common = list(milp_strats.intersection(qaoa_strats))
    milp_only = list(milp_strats - qaoa_strats)
    qaoa_only = list(qaoa_strats - milp_strats)
    
    return {
        "district_id": props.get("district_id"),
        "district_name": props.get("district_name"),
        "metrics": {
            "milp_selected_count": len(milp_strats),
            "qaoa_selected_count": len(qaoa_strats),
            "common_strategies_count": len(common),
            "common_strategies": common,
            "milp_only_strategies": milp_only,
            "qaoa_only_strategies": qaoa_only,
            "portfolio_match_ratio": props.get("portfolio_match_ratio"),
            "milp_objective": props.get("milp_objective"),
            "qaoa_objective": props.get("qaoa_objective"),
            "qaoa_approximation_ratio": props.get("qaoa_approximation_ratio"),
            "qaoa_status": props.get("qaoa_status")
        }
    }

