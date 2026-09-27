# Phase F — Data Quality & Uncertainty Framework

## Quality Dimension Checks
1. **Completeness**: Records checked for missing attributes.
2. **Uniqueness**: Duplicate canonical IDs and geometries flagged.
3. **Spatial Validity**: EPSG:4326 geometry validation and boundary intersection checks.
4. **Zero-Tolerance Missing Data Policy**: Missing metrics remain `NULL` / `UNAVAILABLE`. Automatic zero imputation is strictly prohibited.
5. **Metric Status Flags**: `VERIFIED`, `REQUIRES_REVIEW` (REV-001 metric), `KNOWN_DATA_GAP` (LiDAR micro-contour gap).
