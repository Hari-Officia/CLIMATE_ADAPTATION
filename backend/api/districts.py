from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District, DistrictProfile
from backend.schemas.district import DistrictSummary, DistrictDetail, DistrictProfileSchema

from backend.services.exposure_service import ExposureService
from backend.services.spatial_service import SpatialService
from backend.services.priority_service import PriorityService
from pydantic import BaseModel

router = APIRouter(tags=["Districts"])

class GeocodeRequest(BaseModel):
    latitude: float
    longitude: float

@router.get("", response_model=List[DistrictSummary])
async def list_districts(db: Session = Depends(get_db)):
    districts = db.query(District).order_by(District.district_name).all()
    return districts

@router.get("/{district_id}", response_model=DistrictDetail)
async def get_district(district_id: str, db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    district = db.query(District).filter(
        (District.district_id == d_clean) | (District.district_name.ilike(d_clean))
    ).first()
    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")
    return district

@router.get("/{district_id}/profile", response_model=DistrictProfileSchema)
async def get_district_profile(district_id: str, db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    profile = db.query(DistrictProfile).filter(
        (DistrictProfile.district_id == d_clean) | (DistrictProfile.district_name.ilike(d_clean))
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile for district '{district_id}' not found")
    return profile

@router.get("/{district_id}/exposure")
async def get_district_exposure(district_id: str, db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    res = ExposureService.get_district_exposure(db, d_clean)
    if res.get("status") == "DISTRICT_NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")
    return res

@router.get("/{district_id}/risk-exposure")
async def get_district_risk_exposure(district_id: str, hazard_id: str = "flood", db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    res = ExposureService.get_risk_exposure_profile(db, d_clean, hazard_id)
    if res.get("status") == "DISTRICT_NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")
    return res

@router.get("/{district_id}/priority")
async def get_district_priority_overview(district_id: str, hazard_id: str = "flood", db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    res = PriorityService.get_priority_profile(db, d_clean, hazard_id)
    if res.get("status") == "DISTRICT_NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")
    return res

@router.get("/{district_id}/priority/{hazard_id}")
async def get_district_hazard_priority(district_id: str, hazard_id: str, db: Session = Depends(get_db)):
    d_clean = district_id.lower().strip()
    h_clean = hazard_id.lower().strip()
    res = PriorityService.get_priority_profile(db, d_clean, h_clean)
    if res.get("status") == "DISTRICT_NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")
    return res

@router.post("/geocode")
async def geocode_point(req: GeocodeRequest, db: Session = Depends(get_db)):
    res = SpatialService.point_in_polygon_lookup(db, req.latitude, req.longitude)
    return res


