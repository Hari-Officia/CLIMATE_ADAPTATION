# Phase F — 15 Lineage Verification Report

**Timestamp**: 2026-09-22T17:37:40+05:30  
**Scope**: Climate Adaptation Only

## End-to-End Lineage Verification
1. **Source Registry**: All 5 registered sources (`SRC-IMD-001`, `SRC-TNDMA-001`, `SRC-CENSUS-2011`, `SRC-WORLDPOP-2020`, `SRC-OSM-2024`) verified with official URLs and authority levels.
2. **Dataset Catalog**: All 4 active datasets (`DS-GEOJSON-TN-ADM2-001`, `DS-POP-TN-001`, `DS-INFRA-TN-001`, `DS-LAND-TN-001`) have valid SHA-256 checksums and source foreign keys.
3. **Derived Exposure Records**: Every record in `population_exposure`, `built_environment_exposure`, and `assets` links back to a registered dataset and source ID.
4. **API Lineage Traceability**: `RiskExposureProfile` payload embeds dataset IDs, lineage IDs, and temporal alignment metadata.
- **Lineage Status**: **100% VERIFIED**.
