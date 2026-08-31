import os
import json
import asyncio
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District, DistrictProfile
from backend.agents.risk_agent import RiskAgent
from backend.agents.climate_data_agent import ClimateDataAgent

router = APIRouter(tags=["GIS & Spatial"])

GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "geojson", "tamil_nadu_districts.geojson")

@router.get("/districts-geojson")
async def get_districts_geojson(db: Session = Depends(get_db)):
    if not os.path.exists(GEOJSON_PATH):
        raise HTTPException(status_code=500, detail="GeoJSON asset not found")

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    # Attach profile data if available
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
    Returns GeoJSON FeatureCollection enriched with ML hazard probabilities
    and risk levels for each district for the specified day and hazard.
    """
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
        except Exception:
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
        props["probability"] = 0.05
        props["risk_level"] = "LOW"
        props["overall_risk"] = "LOW"

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

                props["overall_risk"] = assessment["overall_hazard_level"]
                props["flood_probability"] = assessment["flood"]["probability"]
                props["flood_risk"] = assessment["flood"]["risk_level"]
                props["heatwave_probability"] = assessment["heatwave"]["probability"]
                props["heatwave_risk"] = assessment["heatwave"]["risk_level"]
                props["drought_probability"] = assessment["drought"]["probability"]
                props["drought_risk"] = assessment["drought"]["risk_level"]

                if hazard in ["flood", "heatwave", "drought"]:
                    props["probability"] = assessment[hazard]["probability"]
                    props["risk_level"] = assessment[hazard]["risk_level"]
                else:
                    props["risk_level"] = assessment["overall_hazard_level"]
                    props["probability"] = max(
                        assessment["flood"]["probability"],
                        assessment["heatwave"]["probability"],
                        assessment["drought"]["probability"]
                    )
            except Exception:
                pass

    return geojson

