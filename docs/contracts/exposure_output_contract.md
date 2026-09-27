# Phase F — Exposure Output Contract Specification

**Contract ID**: `CTR-EXP-001` & `CTR-RKEXP-001`  
**Version**: `v1.0.0`  
**Status**: `ACTIVE`  
**Authoritative Backend Engine**: `ExposureService` / PostgreSQL + PostGIS

## 1. Objective & Boundaries
This contract defines the output structure of the Phase F Exposure Aggregation Engine and `RiskExposureProfile`.

### Strict Operational Principles:
1. **Risk ≠ Exposure**: Hazard risk predictions are reported separately from population and asset exposure.
2. **Exposure ≠ Vulnerability**: Exposure represents assets and population in hazard zones; vulnerability indices and adaptation priority scores are NOT generated in Phase F.
3. **Zero Imputation Policy**: Missing exposure fields or unverified metrics MUST remain `null` with status `UNAVAILABLE` or `REQUIRES_REVIEW`. Silent zero imputation is forbidden.
4. **Temporal Alignment**: Any temporal gap between the hazard risk date (2026) and exposure baseline dataset year (2021/2020) must trigger `temporal_mismatch_flag = true`.

## 2. RiskExposureProfile Response Structure

```json
{
  "district_id": "chennai",
  "district_name": "Chennai",
  "hazard_id": "flood",
  "risk_context": {
    "hazard_risk_status": "LOW",
    "hazard_probability": 0.0103,
    "model_id": "MDL-FLOOD-XGB-001",
    "feature_contract_id": "FCT-53-001"
  },
  "exposure_context": {
    "population": {
      "status": "AVAILABLE",
      "total_population": 7088403,
      "urban_population": 7088403,
      "rural_population": 0,
      "vulnerable_age_group": 1275912,
      "dataset_id": "DS-POP-TN-001",
      "dataset_year": 2021
    },
    "built_environment": {
      "status": "AVAILABLE",
      "total_area_km2": 426.0,
      "built_up_area_km2": 426.0,
      "impervious_surface_fraction": 0.75,
      "urban_density_category": "HIGH",
      "dataset_id": "DS-LAND-TN-001"
    },
    "infrastructure": {
      "status": "AVAILABLE",
      "asset_count": 2,
      "critical_assets": [
        {
          "asset_id": "AST-CHE-HOSP-001",
          "asset_name": "Rajiv Gandhi Government General Hospital",
          "asset_type": "healthcare",
          "criticality": "HIGH",
          "operational_status": "OPERATIONAL",
          "latitude": 13.0815,
          "longitude": 80.2777
        }
      ],
      "dataset_id": "DS-INFRA-TN-001"
    }
  },
  "spatial_context": {
    "crs": "EPSG:4326",
    "metric_crs": "EPSG:32644",
    "bounding_version": "LAY-TN-ADM2-001-v1.0"
  },
  "temporal_alignment": {
    "risk_calculation_year": 2026,
    "exposure_dataset_year": 2021,
    "temporal_gap_years": 5,
    "temporal_mismatch_flag": true,
    "warning": "Exposure data is from Census 2011/2021; risk calculation uses 2026 forecast."
  },
  "data_governance": {
    "authoritative_runtime_store": "PostgreSQL + PostGIS",
    "semantic_store": "ChromaDB",
    "lineage_id": "LIN-CHENNAI-FLOOD-001",
    "zero_imputation": false,
    "rev_001_metric_status": "REQUIRES_REVIEW",
    "lidar_elevation_gap": "KNOWN_DATA_GAP"
  },
  "generated_at": "2026-09-22T17:20:00Z"
}
```
