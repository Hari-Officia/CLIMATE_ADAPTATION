import os
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db, get_db_status
from backend.db.models import District, SystemLog
from backend.agents.risk_agent import RiskAgent
from backend.agents.climate_data_agent import ClimateDataAgent, CACHE_DIR
from backend.api.auth import require_admin, get_current_user
from backend.schemas.system import SystemStatusResponse

router = APIRouter(tags=["System Status & Administration"])

GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "geojson", "tamil_nadu_districts.geojson")

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status(db: Session = Depends(get_db)):
    risk_agent = RiskAgent.get_instance()
    db_info = get_db_status()

    districts_count = db.query(District).count()
    geojson_exists = os.path.exists(GEOJSON_PATH)

    models_status = risk_agent.get_model_statuses()
    all_models_active = all(m["status"] == "ACTIVE" for m in models_status)

    overall_status = "HEALTHY" if (all_models_active and geojson_exists and districts_count == 38) else "DEGRADED"

    return {
        "system": "Quantum Multi-Agent Climate Risk Decision Support System",
        "review_phase": "Review II (Core Operational Foundation)",
        "status": overall_status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "database": db_info,
        "geojson_loaded": geojson_exists,
        "districts_count": districts_count,
        "models": models_status,
        "agents": {
            "ClimateDataAgent": "ONLINE (Open-Meteo + Cached fallback)",
            "RiskAgent": "ONLINE (53-feature XGBoost Ensemble)",
            "FeatureEngineeringService": "ONLINE (Climatology 2010-2026)",
            "GeocodingEngine": "ONLINE (Shapely Point-in-Polygon)"
        },
        "feature_schema_features": 53
    }

@router.get("/models")
async def get_models_detail():
    risk_agent = RiskAgent.get_instance()
    return {
        "schema_length": 53,
        "models": risk_agent.get_model_statuses()
    }

@router.post("/admin/refresh-forecast")
async def refresh_forecast(
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Clear cache files
    cleared_count = 0
    if os.path.exists(CACHE_DIR):
        for f in os.listdir(CACHE_DIR):
            if f.endswith(".json"):
                try:
                    os.remove(os.path.join(CACHE_DIR, f))
                    cleared_count += 1
                except Exception:
                    pass

    ClimateDataAgent._memory_cache.clear()

    log_entry = SystemLog(
        level="INFO",
        component="Admin",
        message=f"Cache cleared by admin user '{current_user.username}'. {cleared_count} files removed."
    )
    db.add(log_entry)
    db.commit()

    return {
        "status": "SUCCESS",
        "message": f"Cleared {cleared_count} cached forecast files and reset memory cache.",
        "cleared_by": current_user.username
    }
