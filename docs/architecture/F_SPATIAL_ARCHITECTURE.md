# Phase F — Spatial Governance & Coordinate Reference Architecture

## Geometry Standards
- **Authoritative Geographic CRS**: `EPSG:4326` (WGS 84 latitude/longitude).
- **Projected Metric CRS**: `EPSG:32644` (UTM Zone 44N) for metric area/distance calculations in Tamil Nadu.
- **Canonical District Boundaries**: 38 districts defined in `LAY-TN-ADM2-001` (`tamil_nadu_districts.geojson`).

## Spatial Operations Supported
1. **Point-in-Polygon (PIP)**: Lat/lon coordinate lookup returning canonical district ID or `OUT_OF_SCOPE`.
2. **Spatial Overlay & Intersects**: Infrastructure point assets to district boundaries.
3. **Bounding Box Scope**: Tamil Nadu boundary bounds `8.0°N – 13.6°N` latitude, `76.0°E – 80.6°E` longitude.
