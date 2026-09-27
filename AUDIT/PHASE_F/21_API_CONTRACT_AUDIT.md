# Phase F — 21 API Contract Audit Report

**Timestamp**: 2026-09-22T17:42:20+05:30  
**Backend Framework**: FastAPI  
**Contract Version**: `v1.0.0` / `/api/v1/`

## API Contract Audit Matrix

| Endpoint | HTTP Method | Response Model / Contract | Schema Validation | Null Handling | Audit Status |
|---|---|---|---|---|---|
| `/districts/{id}/exposure` | GET | `ExposureSchema` | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/districts/{id}/risk-exposure` | GET | `RiskExposureProfileSchema` | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/exposure/hazards/{hazard_id}` | GET | Exposure List | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/exposure/infrastructure` | GET | Asset List | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/exposure/infrastructure/{id}` | GET | Asset Detail | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/exposure/map/layers` | GET | Spatial Layers List | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/exposure/map/exposure` | GET | GeoJSON FeatureCollection | **PASSED** | Explicit `null` / `UNAVAILABLE` | **VALIDATED** |
| `/districts/geocode` | POST | Point-in-Polygon Result | **PASSED** | `OUT_OF_SCOPE` status returned | **VALIDATED** |
