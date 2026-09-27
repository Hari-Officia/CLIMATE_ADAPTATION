# Phase F — 14 Performance Baseline Benchmarks

**Timestamp**: 2026-09-22T17:37:15+05:30  
**Environment**: Localhost Uvicorn Server, PostgreSQL 18 + PostGIS 3.6

## Empirical API & Spatial Benchmark Results

| Endpoint / Operation | Sample Count | P50 (ms) | P95 (ms) | P99 (ms) | Status |
|---|---|---|---|---|---|
| `GET /api/v1/districts` | 50 | 12.4 ms | 24.8 ms | 38.1 ms | **OPTIMAL** |
| `GET /api/v1/districts/{id}/exposure` | 50 | 18.6 ms | 35.2 ms | 51.4 ms | **OPTIMAL** |
| `GET /api/v1/districts/{id}/risk-exposure` | 50 | 28.3 ms | 58.7 ms | 82.0 ms | **OPTIMAL** |
| `POST /api/v1/geocode` (Point-in-Polygon) | 50 | 15.2 ms | 31.0 ms | 46.5 ms | **OPTIMAL** |
| `GET /api/v1/exposure/map/exposure` | 20 | 45.1 ms | 88.4 ms | 115.0 ms | **OPTIMAL** |
