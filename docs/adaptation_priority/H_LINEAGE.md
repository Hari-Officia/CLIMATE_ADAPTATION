# Phase H Documentation — Data Provenance & Lineage

## 1. Upstream Data Dependencies
Phase H consumes authoritative records from three upstream phases:
- **Phase E (Hazard Risk Engine)**: Standardized hazard probability records from PostgreSQL table `hazard_risk_records`.
- **Phase F (Exposure Engine)**: Spatial asset and demographic exposure counts from PostgreSQL table `exposure_records`.
- **Phase G (Vulnerability Engine)**: Sensitivity and adaptive capacity indices from PostgreSQL table `vulnerability_records`.

## 2. Lineage Auditing
Every `PriorityProfileRecord` persists JSON metadata linking back to exact database snapshot hashes and upstream record IDs.
