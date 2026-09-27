# Phase H — Adaptation Priority Profile Contract Specification

**Contract ID**: `CTR-PRIORITY-001`  
**Version**: `v1.0.0`  
**Status**: `ACTIVE`  
**Authoritative Backend Engine**: `PriorityService` / PostgreSQL + PostGIS

## 1. Objective & Boundaries
This contract defines the output structure of the Phase H Adaptation Priority Engine (`AdaptationPriorityProfile`).

### Operational Principles:
1. **Decoupled Principles**: Priority is evaluated based on verified Hazard Risk (Phase E), Exposure (Phase F), Vulnerability/Sensitivity (Phase G), and Resilience Gap (Phase G).
2. **No Arbitrary Composite Formula**: Unverified formula weights or fake single composite scores are prohibited. `priority_score` remains `null`.
3. **Zero Imputation Policy**: Missing metrics remain `null` / status `UNCERTAIN`.
4. **Deterministic Drivers**: Drivers are extracted from empirical thresholds (`HIGH_POPULATION_EXPOSURE`, `HIGH_HAZARD_RISK`, `HIGH_SENSITIVITY`).

## 2. AdaptationPriorityProfile Response Structure

```json
{
  "priority_id": "PRI-CHENNAI-FLOOD-v1.0",
  "district_id": "chennai",
  "district_name": "Chennai",
  "hazard_id": "flood",
  "methodology_id": "MTH-PRIORITY-TN-001",
  "methodology_version": "1.0.0",
  "priority_status": "REQUIRES_PRIORITY_ATTENTION",
  "priority_horizon": "SHORT_TERM",
  "priority_score": null,
  "score_semantics": "Explicitly NULL. Priority status derived from multi-criteria component decomposition.",
  "component_decomposition": {
    "risk_component": { "status": "LOW", "probability": 0.0103 },
    "exposure_component": { "population": 7088403, "assets_count": 2 },
    "vulnerability_component": { "urban_density": "HIGH", "coastal": true },
    "resilience_gap_component": { "preparedness_gap_status": "DOCUMENTED" }
  },
  "priority_drivers": [
    {
      "driver_id": "DRV-CHENNAI-POP",
      "driver_type": "HIGH_POPULATION_EXPOSURE",
      "evidence": "District resident population is 7,088,403 (Census/WorldPop dataset).",
      "source": "DS-POP-TN-001"
    }
  ],
  "priority_barriers": [
    {
      "barrier_type": "TEMPORAL_MISMATCH",
      "description": "Exposure baseline is from 2021, while hazard risk evaluation uses 2026 forecast."
    }
  ],
  "data_governance": {
    "authoritative_runtime_store": "PostgreSQL + PostGIS",
    "zero_imputation_applied": false,
    "rev_001_metric_status": "REQUIRES_REVIEW",
    "lidar_elevation_gap": "KNOWN_DATA_GAP"
  },
  "deterministic_explanation": {
    "summary": "Adaptation priority status for Chennai (flood) is 'REQUIRES_PRIORITY_ATTENTION'.",
    "key_drivers": ["HIGH_POPULATION_EXPOSURE"],
    "primary_recommendation_timing": "SHORT_TERM"
  },
  "generated_at": "2026-09-22T17:55:00Z"
}
```
