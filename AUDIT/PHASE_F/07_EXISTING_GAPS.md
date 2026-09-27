# Phase F — 07 Existing Gaps Register

**Timestamp**: 2026-09-22T17:16:20+05:30  
**Scope**: Climate Adaptation Only — Tamil Nadu (38 Districts)

## Identified Gaps & Status

| Gap ID | Description | Severity | Impacted Component | Handling Strategy / Status |
|---|---|---|---|---|
| GAP-LIDAR-001 | High-resolution LiDAR micro-contour terrain elevation data unavailable for Tamil Nadu tertiary drainage channels. | MEDIUM | Spatial Context (F8) | Marked as `KNOWN_DATA_GAP`. No tertiary drain elevation geometry fabricated. SRTM 30m DEM used for broad elevation context. |
| GAP-REV-001 | Cool roof microclimate thermal reduction (2–4°C) quantitative metric remains UNVERIFIED by local field trials. | LOW | Exposure / Strategy | Marked as `REQUIRES_REVIEW`. Quantitative thermal reduction value set to `NULL`. Excluded from ML models & exposure scores. |
| GAP-SUBDIST-POP-001 | Sub-district / Village level census population breakdowns for 2024 pending official census release. | LOW | Population Exposure (F4) | District-level Census 2011 + WorldPop 2020 raster overlay used with explicit `temporal_gap` flag (`TEMPORAL_MISMATCH`). |
| GAP-CRIT-TELECOM-001 | Precise geo-coordinates for private cellular telecom towers classified by telecom authority. | LOW | Infrastructure (F6) | Marked as `UNAVAILABLE`. Only public emergency communication centers included in infrastructure inventory. |
