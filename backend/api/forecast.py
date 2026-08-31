from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District
from backend.agents.climate_data_agent import ClimateDataAgent
from backend.services.geocoding_service import GeocodingService
from backend.schemas.forecast import ForecastResponse

router = APIRouter(tags=["Climate Data & Forecast"])

@router.get("/coordinates", response_model=ForecastResponse)
async def get_forecast_by_coordinates(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0)
):
    geocoding_service = GeocodingService.get_instance()
    district_info = geocoding_service.find_district_by_coordinates(lat, lon)
    district_id = district_info["district_id"] if district_info else None
    district_name = district_info["district_name"] if district_info else None

    data = await ClimateDataAgent.get_forecast(lat=lat, lon=lon, district_id=district_id)
    return {
        **data,
        "district_id": district_id,
        "district_name": district_name
    }

@router.get("/{district_id}", response_model=ForecastResponse)
async def get_forecast_by_district(
    district_id: str,
    db: Session = Depends(get_db)
):
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()

    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    data = await ClimateDataAgent.get_forecast(
        lat=district.latitude,
        lon=district.longitude,
        district_id=district.district_id
    )

    return {
        **data,
        "district_id": district.district_id,
        "district_name": district.district_name
    }
