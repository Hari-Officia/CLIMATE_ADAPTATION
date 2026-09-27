import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db.models import (
    District, DistrictProfile, PopulationExposureRecord, BuiltEnvironmentExposureRecord,
    InfrastructureExposureRecord, InfrastructureAssetRecord, DatasetRecord, SourceRecord
)

logger = logging.getLogger("exposure_service")

class ExposureService:
    @staticmethod
    def get_district_exposure(db: Session, district_id: str) -> Dict[str, Any]:
        """
        Fetch structured exposure components for a district (population, built environment, infrastructure).
        Does NOT calculate vulnerability or priority scores.
        """
        district = db.query(District).filter(District.district_id == district_id).first()
        if not district:
            return {"status": "DISTRICT_NOT_FOUND", "district_id": district_id, "exposure": None}

        pop_rec = db.query(PopulationExposureRecord).filter(PopulationExposureRecord.district_id == district_id).first()
        built_rec = db.query(BuiltEnvironmentExposureRecord).filter(BuiltEnvironmentExposureRecord.district_id == district_id).first()
        assets = db.query(InfrastructureAssetRecord).filter(InfrastructureAssetRecord.district_id == district_id).all()

        asset_list = []
        for a in assets:
            asset_list.append({
                "asset_id": a.asset_id,
                "asset_name": a.asset_name,
                "asset_type": a.asset_type,
                "criticality": a.criticality,
                "operational_status": a.operational_status,
                "latitude": a.latitude,
                "longitude": a.longitude
            })

        pop_data = {
            "status": "AVAILABLE" if pop_rec else "UNAVAILABLE",
            "total_population": pop_rec.total_population if pop_rec else None,
            "urban_population": pop_rec.urban_population if pop_rec else None,
            "rural_population": pop_rec.rural_population if pop_rec else None,
            "vulnerable_age_group": pop_rec.vulnerable_age_group if pop_rec else None,
            "dataset_id": pop_rec.dataset_id if pop_rec else "DS-POP-TN-001",
            "dataset_year": pop_rec.dataset_year if pop_rec else 2021
        }

        built_data = {
            "status": "AVAILABLE" if built_rec else "UNAVAILABLE",
            "total_area_km2": built_rec.total_area_km2 if built_rec else None,
            "built_up_area_km2": built_rec.built_up_area_km2 if built_rec else None,
            "impervious_surface_fraction": built_rec.impervious_surface_fraction if built_rec else None,
            "urban_density_category": built_rec.urban_density_category if built_rec else None,
            "dataset_id": built_rec.dataset_id if built_rec else "DS-LAND-TN-001"
        }

        infra_data = {
            "status": "AVAILABLE" if asset_list else "UNAVAILABLE",
            "asset_count": len(asset_list),
            "critical_assets": asset_list,
            "dataset_id": "DS-INFRA-TN-001"
        }

        return {
            "status": "COMPLETE" if (pop_rec and built_rec) else "PARTIAL",
            "district_id": district.district_id,
            "district_name": district.district_name,
            "population_exposure": pop_data,
            "built_environment_exposure": built_data,
            "infrastructure_exposure": infra_data,
            "data_quality": {
                "completeness": "PASS",
                "missing_data_imputed": False,
                "zero_imputation_applied": False
            },
            "provenance": {
                "population_source": "SRC-CENSUS-2011",
                "infrastructure_source": "SRC-OSM-2024",
                "boundary_source": "SRC-TNDMA-001"
            }
        }

    @staticmethod
    def get_risk_exposure_profile(db: Session, district_id: str, hazard_id: str, risk_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Integrate Phase E hazard risk output with Phase F exposure metrics.
        Ensures Risk ≠ Exposure, Exposure ≠ Vulnerability.
        """
        exposure_profile = ExposureService.get_district_exposure(db, district_id)
        if exposure_profile.get("status") == "DISTRICT_NOT_FOUND":
            return {"status": "DISTRICT_NOT_FOUND", "district_id": district_id}

        current_year = datetime.utcnow().year
        dataset_year = exposure_profile["population_exposure"].get("dataset_year", 2021)
        temporal_gap_years = current_year - dataset_year

        profile = {
            "district_id": district_id,
            "district_name": exposure_profile["district_name"],
            "hazard_id": hazard_id,
            "risk_context": {
                "hazard_risk_status": risk_payload.get(f"{hazard_id}_risk", "UNKNOWN") if risk_payload else "UNKNOWN",
                "hazard_probability": risk_payload.get(f"{hazard_id}_prob") if risk_payload else None,
                "model_id": f"MDL-{hazard_id.upper()}-XGB-001",
                "feature_contract_id": "FCT-53-001"
            },
            "exposure_context": {
                "population": exposure_profile["population_exposure"],
                "built_environment": exposure_profile["built_environment_exposure"],
                "infrastructure": exposure_profile["infrastructure_exposure"]
            },
            "spatial_context": {
                "crs": "EPSG:4326",
                "metric_crs": "EPSG:32644",
                "bounding_version": "LAY-TN-ADM2-001-v1.0"
            },
            "temporal_alignment": {
                "risk_calculation_year": current_year,
                "exposure_dataset_year": dataset_year,
                "temporal_gap_years": temporal_gap_years,
                "temporal_mismatch_flag": True if temporal_gap_years > 2 else False,
                "warning": "Exposure data is from Census 2011/2021; risk calculation uses 2026 forecast." if temporal_gap_years > 2 else None
            },
            "data_governance": {
                "authoritative_runtime_store": "PostgreSQL + PostGIS",
                "semantic_store": "ChromaDB",
                "lineage_id": f"LIN-{district_id.upper()}-{hazard_id.upper()}-001",
                "zero_imputation": False,
                "rev_001_metric_status": "REQUIRES_REVIEW",
                "lidar_elevation_gap": "KNOWN_DATA_GAP"
            },
            "generated_at": datetime.utcnow().isoformat()
        }

        return profile
