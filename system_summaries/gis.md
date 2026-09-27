# GIS & Spatial Engine Summary

## 🗺️ Overview
The **GIS & Spatial Engine** handles all geospatial operations, boundary resolution, spatial indexing, and point-in-polygon queries for the 38 districts of Tamil Nadu. It utilizes official **geoBoundaries (IND-ADM2)** GeoJSON shapefiles to enable precise geographic alignment across climate forecasts, risk visualization, and strategy allocation.

---

## 📐 Core GIS Capabilities

1. **Point-in-Polygon (PIP) Lookup**: Fast reverse geocoding from GPS coordinates $(\text{lat}, \text{lon})$ to target district boundary using `shapely`.
2. **GeoJSON Boundary Resolution**: Serves simplified vector polygon coordinates for rendering interactive district maps on the React frontend.
3. **Centroid & Distance Calculation**: Computes geographical centroids and Haversine spatial distances between district capitals for multi-district strategy dependencies.

---

## 🌐 Spatial API Endpoints

| Endpoint | Method | Output Format | Description |
|---|---|---|---|
| `/api/v1/gis/districts` | `GET` | GeoJSON FeatureCollection | Returns polygon geometries for all 38 districts |
| `/api/v1/gis/districts/{id}` | `GET` | GeoJSON Feature | Returns boundary polygon for a single district |
| `/api/v1/gis/lookup` | `GET` | JSON | Reverse geocodes $(\text{lat}, \text{lon}) \rightarrow \text{district\_id}$ |

---

## 💻 Minimal Code Example

```python
# backend/services/geocoding_service.py
from shapely.geometry import Point, shape
import json
import os

class GeocodingService:
    def __init__(self, geojson_path: str = "geoBoundaries-IND-ADM2-all/geoBoundaries-IND-ADM2.geojson"):
        with open(geojson_path, "r", encoding="utf-8") as f:
            self.geojson_data = json.load(f)
            
        self.polygons = []
        for feature in self.geojson_data["features"]:
            dist_name = feature["properties"].get("shapeName")
            polygon = shape(feature["geometry"])
            self.polygons.append((dist_name, polygon))

    def find_district_by_coordinates(self, lat: float, lon: float) -> dict:
        """Point-in-polygon check using Shapely."""
        point = Point(lon, lat) # Lon, Lat order in GeoJSON
        
        for name, polygon in self.polygons:
            if polygon.contains(point):
                return {
                    "district_id": name.lower().replace(" ", "_"),
                    "district_name": name
                }
        return None
```
