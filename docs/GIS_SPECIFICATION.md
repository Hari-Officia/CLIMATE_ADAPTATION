# GIS & Spatial Specification — Review II

## 1. Overview
The GIS component provides spatial boundary management, coordinate reference system (CRS) conformance, geocoding resolution, and point-in-polygon containment across Tamil Nadu's 38 administrative districts.

---

## 2. Canonical GeoJSON Asset

- **File Location**: `data/geojson/tamil_nadu_districts.geojson`
- **Coordinate Reference System (CRS)**: WGS 84 / CRS84 (`urn:ogc:def:crs:OGC:1.3:CRS84`)
- **Total Features**: Exactly 38 features (one Polygon or MultiPolygon per district).
- **Geometric Topology**: Validated via `scripts/validate_geojson.py`.
- **Property Schema**:
  - `district_id`: Lowercase identifier (e.g., `chennai`, `tiruvallur`, `nilgiris`).
  - `district_name`: Formal English title case (e.g., `Chennai`, `Tiruvallur`, `Nilgiris`).
  - `district_code`: Standardized administrative code (e.g., `IND-TN-CHE`).
  - `latitude`: Centroid latitude.
  - `longitude`: Centroid longitude.

---

## 3. Point-in-Polygon Engine (Shapely)

The engine (`backend/services/geocoding_service.py`) operates as a singleton in memory:
1. Loads all 38 district geometries into Shapely `Polygon` or `MultiPolygon` objects.
2. Given coordinates $(lat, lon)$, constructs `shapely.geometry.Point(lon, lat)`.
3. Performs `polygon.contains(point)` or `polygon.intersects(point)`.
4. If coordinates lie marginally offshore or on coastal boundary lines (e.g., Marina Beach water edge), applies a buffer distance test ($\le 0.15^\circ \approx 15\text{ km}$) to snap to the closest coastal district.
5. Returns `None` and raises an out-of-bounds error if the coordinates are outside Tamil Nadu.

---

## 4. Landmark Index & Hybrid Search

- **Curated High-Value Landmarks**: Marina Beach, Chennai Central, Coimbatore Airport, Avadi, Tambaram, Meenakshi Temple, Ooty Lake, Kodaikanal, Shore Temple Mahabalipuram, etc.
- **District Centers**: All 38 district headquarters indexed.
- **External Fallback**: Queries Open-Meteo Geocoding API with Tamil Nadu bounding box filter ($8.0^\circ \le lat \le 14.0^\circ$, $76.0^\circ \le lon \le 81.0^\circ$).
