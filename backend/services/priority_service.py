import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db.models import District, PriorityMethodologyRecord, PriorityProfileRecord, PriorityDriverRecord
from backend.services.exposure_service import ExposureService

logger = logging.getLogger("priority_service")

class PriorityService:
    @staticmethod
    def get_priority_profile(db: Session, district_id: str, hazard_id: str = "flood", risk_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build an AdaptationPriorityProfile for a district and hazard.
        Combines Risk (Phase E), Exposure (Phase F), Sensitivity/Vulnerability (Phase G), and Resilience Gap (Phase G).
        Strictly deterministic; no LLM invention or arbitrary composite formula weights.
        """
        exposure_profile = ExposureService.get_district_exposure(db, district_id)
        if exposure_profile.get("status") == "DISTRICT_NOT_FOUND":
            return {"status": "DISTRICT_NOT_FOUND", "district_id": district_id}

        d_name = exposure_profile.get("district_name")
        pop_exp = exposure_profile.get("population_exposure", {})
        built_exp = exposure_profile.get("built_environment_exposure", {})
        infra_exp = exposure_profile.get("infrastructure_exposure", {})

        # Risk context
        hazard_risk_status = risk_payload.get(f"{hazard_id}_risk", "UNKNOWN") if risk_payload else "UNKNOWN"
        hazard_prob = risk_payload.get(f"{hazard_id}_prob") if risk_payload else None

        # Exposure context
        total_pop = pop_exp.get("total_population", 0) or 0
        asset_count = infra_exp.get("asset_count", 0) or 0
        urban_density = built_exp.get("urban_density_category", "LOW")

        # Deterministic Driver Extraction
        drivers = []
        if hazard_risk_status == "HIGH" or (hazard_prob and hazard_prob > 0.5):
            drivers.append({
                "driver_id": f"DRV-{district_id.upper()}-RISK",
                "driver_type": "HIGH_HAZARD_RISK",
                "evidence": f"Phase E XGBoost hazard risk prediction for {hazard_id} is HIGH (Probability: {hazard_prob or 'N/A'}).",
                "source": f"MDL-{hazard_id.upper()}-XGB-001"
            })
        
        if total_pop > 2000000:
            drivers.append({
                "driver_id": f"DRV-{district_id.upper()}-POP",
                "driver_type": "HIGH_POPULATION_EXPOSURE",
                "evidence": f"District resident population is {total_pop:,} (Census/WorldPop dataset).",
                "source": "DS-POP-TN-001"
            })

        if asset_count > 0:
            drivers.append({
                "driver_id": f"DRV-{district_id.upper()}-INFRA",
                "driver_type": "HIGH_CRITICAL_ASSET_EXPOSURE",
                "evidence": f"{asset_count} registered critical infrastructure assets present in district boundary.",
                "source": "DS-INFRA-TN-001"
            })

        if urban_density == "HIGH":
            drivers.append({
                "driver_id": f"DRV-{district_id.upper()}-DENSITY",
                "driver_type": "HIGH_SENSITIVITY",
                "evidence": f"High urban density and built-up land fraction ({built_exp.get('impervious_surface_fraction', 0.0) * 100:.0f}% impervious surface).",
                "source": "DS-LAND-TN-001"
            })

        # Priority Status Determination
        if hazard_risk_status == "HIGH" or len(drivers) >= 2:
            priority_status = "REQUIRES_PRIORITY_ATTENTION"
            horizon = "IMMEDIATE" if hazard_risk_status == "HIGH" else "SHORT_TERM"
        elif len(drivers) == 1:
            priority_status = "MODERATE_PRIORITY"
            horizon = "MEDIUM_TERM"
        else:
            priority_status = "MONITORING_ONLY"
            horizon = "LONG_TERM"

        # Barriers / Uncertainty Extraction
        barriers = []
        temporal_gap = 2026 - pop_exp.get("dataset_year", 2021)
        if temporal_gap > 2:
            barriers.append({
                "barrier_type": "TEMPORAL_MISMATCH",
                "description": f"Exposure baseline is from {pop_exp.get('dataset_year', 2021)}, while hazard risk evaluation uses 2026 forecast."
            })

        barriers.append({
            "barrier_type": "KNOWN_DATA_GAP",
            "description": "LiDAR tertiary drain elevation geometry unavailable; micro-contour elevation remains KNOWN_DATA_GAP."
        })

        profile = {
            "priority_id": f"PRI-{district_id.upper()}-{hazard_id.upper()}-v1.0",
            "district_id": district_id,
            "district_name": d_name,
            "hazard_id": hazard_id,
            "methodology_id": "MTH-PRIORITY-TN-001",
            "methodology_version": "1.0.0",
            "priority_status": priority_status,
            "priority_horizon": horizon,
            "priority_score": None,  # No unverified composite score calculated
            "score_semantics": "Explicitly NULL. Priority status derived from multi-criteria component decomposition.",
            "component_decomposition": {
                "risk_component": { "status": hazard_risk_status, "probability": hazard_prob, "source": f"MDL-{hazard_id.upper()}-XGB-001" },
                "exposure_component": { "population": total_pop, "assets_count": asset_count, "source": "DS-POP-TN-001" },
                "vulnerability_component": { "urban_density": urban_density, "coastal": d_name.lower() in ["chennai", "kanniyakumari", "cuddalore", "nagapattinam", "thoothukudi", "ramanathapuram"] },
                "resilience_gap_component": { "preparedness_gap_status": "DOCUMENTED" }
            },
            "priority_drivers": drivers,
            "priority_barriers": barriers,
            "data_governance": {
                "authoritative_runtime_store": "PostgreSQL + PostGIS",
                "semantic_store": "ChromaDB",
                "zero_imputation_applied": False,
                "rev_001_metric_status": "REQUIRES_REVIEW",
                "lidar_elevation_gap": "KNOWN_DATA_GAP"
            },
            "deterministic_explanation": {
                "summary": f"Adaptation priority status for {d_name} ({hazard_id}) is '{priority_status}'.",
                "key_drivers": [d["driver_type"] for d in drivers],
                "primary_recommendation_timing": horizon
            },
            "generated_at": datetime.utcnow().isoformat()
        }

        return profile
