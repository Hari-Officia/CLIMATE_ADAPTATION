from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District, DistrictProfile
from backend.schemas.district import DistrictSummary, DistrictDetail, DistrictProfileSchema

router = APIRouter(tags=["Districts"])

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
