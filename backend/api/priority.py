from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import District, PriorityMethodologyRecord
from backend.services.priority_service import PriorityService

router = APIRouter(prefix="/priority", tags=["Adaptation Priority"])

@router.get("/methodologies")
async def list_priority_methodologies(db: Session = Depends(get_db)):
    methodologies = db.query(PriorityMethodologyRecord).all()
    res = []
    for m in methodologies:
        res.append({
            "methodology_id": m.methodology_id,
            "name": m.name,
            "version": m.version,
            "framework": m.framework,
            "description": m.description,
            "status": m.status
        })
    return res

@router.get("/drivers")
async def list_priority_drivers():
    return {
        "taxonomy_version": "v1.0.0",
        "drivers": [
            { "driver_type": "HIGH_HAZARD_RISK", "description": "Phase E XGBoost hazard risk prediction exceeds threshold." },
            { "driver_type": "HIGH_POPULATION_EXPOSURE", "description": "Resident population in district exceeds 2,000,000." },
            { "driver_type": "HIGH_CRITICAL_ASSET_EXPOSURE", "description": "Critical infrastructure assets present within district hazard area." },
            { "driver_type": "HIGH_SENSITIVITY", "description": "High urban density and impervious surface fraction." },
            { "driver_type": "LOW_ADAPTIVE_CAPACITY", "description": "Limited historical infrastructure or emergency response capacity." },
            { "driver_type": "RESILIENCE_GAP", "description": "Documented gap in sector-specific climate resilience." }
        ]
    }

@router.get("/map")
async def get_priority_map_layer(hazard_id: Optional[str] = Query("flood"), db: Session = Depends(get_db)):
    h_clean = hazard_id.lower().strip()
    districts = db.query(District).all()
    features = []
    for d in districts:
        profile = PriorityService.get_priority_profile(db, d.district_id, h_clean)
        features.append({
            "type": "Feature",
            "geometry": d.geojson_properties.get("geometry") if d.geojson_properties else None,
            "properties": {
                "district_id": d.district_id,
                "district_name": d.district_name,
                "hazard_id": h_clean,
                "priority_status": profile.get("priority_status"),
                "priority_horizon": profile.get("priority_horizon"),
                "drivers_count": len(profile.get("priority_drivers", []))
            }
        })
    return {
        "type": "FeatureCollection",
        "hazard_id": h_clean,
        "crs": "EPSG:4326",
        "features": features
    }

@router.get("")
async def list_district_priorities(hazard_id: Optional[str] = Query("flood"), db: Session = Depends(get_db)):
    h_clean = hazard_id.lower().strip()
    districts = db.query(District).order_by(District.district_name).all()
    results = []
    for d in districts:
        profile = PriorityService.get_priority_profile(db, d.district_id, h_clean)
        results.append(profile)
    return {
        "hazard_id": h_clean,
        "methodology_id": "MTH-PRIORITY-TN-001",
        "total_districts": len(results),
        "district_priorities": results
    }
