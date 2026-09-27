from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import InfrastructureAssetRecord, District
from backend.services.exposure_service import ExposureService
from backend.services.spatial_service import SpatialService

router = APIRouter(prefix="/exposure", tags=["Exposure & Infrastructure"])

@router.get("/hazards/{hazard_id}")
async def get_hazard_exposure(hazard_id: str, db: Session = Depends(get_db)):
    h_clean = hazard_id.lower().strip()
    if h_clean not in ["flood", "drought", "heatwave"]:
        raise HTTPException(status_code=400, detail=f"Invalid hazard_id '{hazard_id}'. Allowed: flood, drought, heatwave")
    
    districts = db.query(District).order_by(District.district_name).all()
    results = []
    for d in districts:
        profile = ExposureService.get_risk_exposure_profile(db, d.district_id, h_clean)
        results.append(profile)
    
    return {
        "hazard_id": h_clean,
        "total_districts": len(results),
        "districts_exposure": results
    }

@router.get("/infrastructure")
async def list_infrastructure_assets(
    district_id: Optional[str] = Query(None),
    asset_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(InfrastructureAssetRecord)
    if district_id:
        query = query.filter(InfrastructureAssetRecord.district_id == district_id.lower().strip())
    if asset_type:
        query = query.filter(InfrastructureAssetRecord.asset_type == asset_type.lower().strip())
    
    assets = query.order_by(InfrastructureAssetRecord.asset_name).all()
    res = []
    for a in assets:
        res.append({
            "asset_id": a.asset_id,
            "asset_type": a.asset_type,
            "asset_name": a.asset_name,
            "district_id": a.district_id,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "criticality": a.criticality,
            "operational_status": a.operational_status,
            "dataset_id": a.dataset_id,
            "source_id": a.source_id
        })
    return res

@router.get("/infrastructure/{asset_id}")
async def get_infrastructure_asset(asset_id: str, db: Session = Depends(get_db)):
    a_clean = asset_id.upper().strip()
    asset = db.query(InfrastructureAssetRecord).filter(
        (InfrastructureAssetRecord.asset_id == a_clean) | (InfrastructureAssetRecord.asset_id == asset_id)
    ).first()
    if not asset:
        raise HTTPException(status_code=404, detail=f"Infrastructure asset '{asset_id}' not found")
    
    return {
        "asset_id": asset.asset_id,
        "asset_type": asset.asset_type,
        "asset_name": asset.asset_name,
        "district_id": asset.district_id,
        "latitude": asset.latitude,
        "longitude": asset.longitude,
        "criticality": asset.criticality,
        "operational_status": asset.operational_status,
        "dataset_id": asset.dataset_id,
        "source_id": asset.source_id,
        "hazard_exposure_status": "EXPOSED"
    }

@router.get("/map/layers")
async def get_map_layers(db: Session = Depends(get_db)):
    layers = SpatialService.get_spatial_layers(db)
    return {
        "total_layers": len(layers),
        "layers": layers
    }

@router.get("/map/exposure")
async def get_map_exposure_layers(layer_id: Optional[str] = Query("LAY-TN-POP-001"), db: Session = Depends(get_db)):
    districts = db.query(District).all()
    features = []
    for d in districts:
        exp = ExposureService.get_district_exposure(db, d.district_id)
        features.append({
            "type": "Feature",
            "geometry": d.geojson_properties.get("geometry") if d.geojson_properties else None,
            "properties": {
                "district_id": d.district_id,
                "district_name": d.district_name,
                "population": exp["population_exposure"].get("total_population"),
                "urban_density": exp["built_environment_exposure"].get("urban_density_category"),
                "critical_assets": exp["infrastructure_exposure"].get("asset_count")
            }
        })
    
    return {
        "type": "FeatureCollection",
        "layer_id": layer_id,
        "crs": "EPSG:4326",
        "features": features
    }
