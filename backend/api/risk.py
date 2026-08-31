from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District, DistrictProfile
from backend.agents.climate_data_agent import ClimateDataAgent
from backend.agents.risk_agent import RiskAgent
from backend.services.geocoding_service import GeocodingService
from backend.schemas.risk import DistrictRiskResponse, TimelineRiskResponse, DailyRiskAssessment

router = APIRouter(tags=["Multi-Hazard Risk Assessment"])

@router.get("/district/{district_id}", response_model=DistrictRiskResponse)
async def get_district_risk(
    district_id: str,
    day: int = Query(0, ge=0, le=6, description="Forecast day index (0=Today, 6=Day 7)"),
    db: Session = Depends(get_db)
):
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()

    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    profile = db.query(DistrictProfile).filter(DistrictProfile.district_id == district.district_id).first()

    # 1. Fetch climate forecast
    forecast = await ClimateDataAgent.get_forecast(
        lat=district.latitude,
        lon=district.longitude,
        district_id=district.district_id
    )

    # 2. Risk Agent ML assessment
    risk_agent = RiskAgent.get_instance()
    assessment_data = risk_agent.assess_risk(
        district_name=district.district_name,
        forecast_day_index=day,
        daily_forecast_list=forecast["daily"],
        hourly_forecast_list=forecast["hourly"]
    )

    demographic_data = {
        "population": profile.population if profile else None,
        "population_density": profile.population_density if profile else None,
        "urban_percentage": profile.urban_percentage if profile else None,
        "coastal": profile.coastal if profile else False,
        "elevation_m": profile.elevation_m if profile else None
    }

    return {
        "district_id": district.district_id,
        "district_name": district.district_name,
        "date": assessment_data["date"],
        "spatial_resolution": "District-level (Administrative ADM2)",
        "model_status": "Verified XGBoost Ensemble (53 features)",
        "assessment": assessment_data,
        "climatological_context": assessment_data.get("baseline"),
        "demographic_exposure": demographic_data,
        "data_quality": forecast.get("data_quality")
    }

@router.get("/timeline/{district_id}", response_model=TimelineRiskResponse)
async def get_district_timeline(
    district_id: str,
    db: Session = Depends(get_db)
):
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()

    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    forecast = await ClimateDataAgent.get_forecast(
        lat=district.latitude,
        lon=district.longitude,
        district_id=district.district_id
    )

    risk_agent = RiskAgent.get_instance()
    timeline_data = risk_agent.assess_7day_timeline(
        district_name=district.district_name,
        daily_forecast_list=forecast["daily"],
        hourly_forecast_list=forecast["hourly"]
    )

    return {
        "district_id": district.district_id,
        "district_name": district.district_name,
        "spatial_resolution": "District-level",
        "timeline": timeline_data
    }

@router.get("/coordinates", response_model=DistrictRiskResponse)
async def get_risk_by_coordinates(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    day: int = Query(0, ge=0, le=6),
    db: Session = Depends(get_db)
):
    geocoding_service = GeocodingService.get_instance()
    d_info = geocoding_service.find_district_by_coordinates(lat, lon)
    if not d_info:
        # Outside Tamil Nadu
        raise HTTPException(
            status_code=400,
            detail=f"Coordinates ({lat}, {lon}) are outside the Tamil Nadu model domain."
        )

    return await get_district_risk(district_id=d_info["district_id"], day=day, db=db)
