# Phase P GIS Architecture Specification

**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation and Mitigation Strategy Planning  
**Geography:** Tamil Nadu, India — All 38 Districts  

---

## 1. Spatial Coordinate Reference System (CRS)

- **Backend Storage CRS:** EPSG:4326 (WGS 84 / Geographic) in PostGIS.
- **API Transfer CRS:** GeoJSON EPSG:4326 (longitude, latitude coordinates).
- **Frontend Map Display CRS:** EPSG:3857 (Web Mercator) handled natively by Leaflet with automatically reprojected EPSG:4326 GeoJSON overlay polygons.

---

## 2. Tamil Nadu Spatial Extent & Map Bounds

- **Bounding Box:** 
  - South Latitude: `8.07` (Kanyakumari)
  - North Latitude: `13.50` (Tiruvallur)
  - West Longitude: `76.23` (Nilgiris)
  - East Longitude: `80.35` (Nagapattinam)
- **Initial Zoom Level:** `7` (centered at `[11.1271, 78.6569]`).
- **Max / Min Zoom Limits:** Min Zoom: `6`, Max Zoom: `13` (prevents unnecessary global tiles).

---

## 3. Spatial Layers & Hierarchy

1. **Base Map Layer:** OpenStreetMap / CartoDB Dark Matter tiles with attribution.
2. **Canonical District Boundaries Layer:** 38 District Polygons fetched directly from `/gis/districts` or `/districts/geojson`.
3. **Hazard Overlay Layers:** Dynamic chloropleth polygons colored by backend risk class (`HIGH`, `MEDIUM`, `LOW`, `UNAVAILABLE`).
   - Flood Risk Layer
   - Drought Risk Layer
   - Heatwave Risk Layer
4. **Spatial Feature Interaction:**
   - Hover: Highlight polygon border and show concise popup tooltip (District Name, ID, Risk Level).
   - Click: Select District, zoom to bounds (`fitBounds`), update global URL query state (`/district/TN-XXX`), and trigger decision profile loading.
