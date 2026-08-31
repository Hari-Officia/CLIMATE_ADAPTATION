import os
import json
import logging
import httpx
from typing import List, Dict, Any, Optional, Tuple
from shapely.geometry import shape, Point

logger = logging.getLogger("geocoding")

GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "geojson", "tamil_nadu_districts.geojson")

# Curated Tamil Nadu Landmarks with exact coordinates
TAMIL_NADU_LANDMARKS = [
    {"name": "Marina Beach", "lat": 13.0500, "lon": 80.2824, "district_id": "chennai", "category": "landmark"},
    {"name": "Chennai Central (Puratchi Thalaivar Dr. M.G. Ramachandran Central)", "lat": 13.0827, "lon": 80.2755, "district_id": "chennai", "category": "station"},
    {"name": "Chennai Airport (MAA)", "lat": 12.9941, "lon": 80.1709, "district_id": "chengalpattu", "category": "airport"},
    {"name": "Avadi", "lat": 13.1147, "lon": 80.1018, "district_id": "tiruvallur", "category": "town"},
    {"name": "Tambaram", "lat": 12.9249, "lon": 80.1000, "district_id": "chengalpattu", "category": "town"},
    {"name": "Velachery", "lat": 12.9759, "lon": 80.2212, "district_id": "chennai", "category": "neighborhood"},
    {"name": "T. Nagar (Thyagaraya Nagar)", "lat": 13.0418, "lon": 80.2341, "district_id": "chennai", "category": "neighborhood"},
    {"name": "Coimbatore International Airport", "lat": 11.0299, "lon": 77.0434, "district_id": "coimbatore", "category": "airport"},
    {"name": "Gandhipuram, Coimbatore", "lat": 11.0168, "lon": 76.9680, "district_id": "coimbatore", "category": "town"},
    {"name": "Meenakshi Amman Temple", "lat": 9.9195, "lon": 78.1193, "district_id": "madurai", "category": "landmark"},
    {"name": "Ooty Lake & Botanical Garden", "lat": 11.4064, "lon": 76.6896, "district_id": "nilgiris", "category": "landmark"},
    {"name": "Kodaikanal Lake", "lat": 10.2381, "lon": 77.4892, "district_id": "dindigul", "category": "landmark"},
    {"name": "Brihadisvara Temple, Thanjavur", "lat": 10.7828, "lon": 79.1318, "district_id": "thanjavur", "category": "landmark"},
    {"name": "Kanyakumari Pier / Sunset Point", "lat": 8.0780, "lon": 77.5550, "district_id": "kanniyakumari", "category": "landmark"},
    {"name": "Rameswaram Temple", "lat": 9.2881, "lon": 79.3174, "district_id": "ramanathapuram", "category": "landmark"},
    {"name": "Mahabalipuram Shore Temple", "lat": 12.6164, "lon": 80.1983, "district_id": "chengalpattu", "category": "landmark"},
    {"name": "Hogenakkal Falls", "lat": 12.1186, "lon": 77.7770, "district_id": "dharmapuri", "category": "landmark"},
    {"name": "Yercaud Lake", "lat": 11.7753, "lon": 78.2093, "district_id": "salem", "category": "landmark"},
    {"name": "Chidambaram Nataraja Temple", "lat": 11.3992, "lon": 79.6934, "district_id": "cuddalore", "category": "landmark"},
    {"name": "Thiruchendur Murugan Temple", "lat": 8.4975, "lon": 78.1292, "district_id": "thoothukudi", "category": "landmark"},
    {"name": "Courtallam Falls", "lat": 8.9304, "lon": 77.2694, "district_id": "tenkasi", "category": "landmark"}
]

class GeocodingService:
    _instance = None
    _district_polygons: List[Dict[str, Any]] = []
    _search_cache: Dict[str, Any] = {}

    def __init__(self):
        self._load_district_polygons()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = GeocodingService()
        return cls._instance

    def _load_district_polygons(self):
        if not os.path.exists(GEOJSON_PATH):
            logger.error(f"GeoJSON file not found at {GEOJSON_PATH}")
            return

        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        self._district_polygons = []
        for feat in geojson_data.get("features", []):
            geom = shape(feat["geometry"])
            props = feat.get("properties", {})
            self._district_polygons.append({
                "geometry": geom,
                "district_id": props.get("district_id"),
                "district_name": props.get("district_name"),
                "district_code": props.get("district_code"),
                "centroid_lat": props.get("latitude"),
                "centroid_lon": props.get("longitude")
            })

        logger.info(f"Loaded {len(self._district_polygons)} district polygons into Shapely engine.")

    def find_district_by_coordinates(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Point-in-polygon test: given (lat, lon), return containing district.
        Coordinates are (lon, lat) in GeoJSON / Shapely.
        """
        pt = Point(lon, lat)
        for d in self._district_polygons:
            if d["geometry"].contains(pt) or d["geometry"].intersects(pt):
                return {
                    "district_id": d["district_id"],
                    "district_name": d["district_name"],
                    "district_code": d["district_code"],
                    "centroid_lat": d["centroid_lat"],
                    "centroid_lon": d["centroid_lon"],
                    "is_exact_match": True
                }

        # If slightly outside (e.g. coastal waters or exact border edge within ~5km), find closest district
        closest_district = None
        min_dist = float("inf")
        for d in self._district_polygons:
            dist = d["geometry"].distance(pt)
            if dist < min_dist:
                min_dist = dist
                closest_district = d

        # Degree distance: 0.15 deg is approx 15km buffer
        if closest_district and min_dist <= 0.15:
            return {
                "district_id": closest_district["district_id"],
                "district_name": closest_district["district_name"],
                "district_code": closest_district["district_code"],
                "centroid_lat": closest_district["centroid_lat"],
                "centroid_lon": closest_district["centroid_lon"],
                "is_exact_match": False,
                "distance_deg": min_dist
            }

        return None

    async def search_locations(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return []

        if q in self._search_cache:
            return self._search_cache[q][:limit]

        results = []
        seen_names = set()

        # 1. Check curated landmarks
        for lm in TAMIL_NADU_LANDMARKS:
            if q in lm["name"].lower():
                d_info = self.find_district_by_coordinates(lm["lat"], lm["lon"])
                district_name = d_info["district_name"] if d_info else lm["district_id"].title()
                results.append({
                    "name": lm["name"],
                    "latitude": lm["lat"],
                    "longitude": lm["lon"],
                    "district_id": lm["district_id"],
                    "district_name": district_name,
                    "category": lm["category"]
                })
                seen_names.add(lm["name"].lower())

        # 2. Check district centers
        for d in self._district_polygons:
            if q in d["district_name"].lower():
                name = f"{d['district_name']} (District Headquarters)"
                if name.lower() not in seen_names:
                    results.append({
                        "name": name,
                        "latitude": d["centroid_lat"],
                        "longitude": d["centroid_lon"],
                        "district_id": d["district_id"],
                        "district_name": d["district_name"],
                        "category": "district_headquarters"
                    })
                    seen_names.add(name.lower())

        # 3. If fewer than 3 results, query Open-Meteo Geocoding API with bounding box filter
        if len(results) < 3:
            try:
                async with httpx.AsyncClient(timeout=4.0) as client:
                    resp = await client.get(
                        "https://geocoding-api.open-meteo.com/v1/search",
                        params={"name": query, "count": 5, "language": "en", "format": "json"}
                    )
                    if resp.status_code == 200:
                        geo_json = resp.json()
                        for item in geo_json.get("results", []):
                            lat = item.get("latitude")
                            lon = item.get("longitude")
                            name = item.get("name")
                            # Check if in South India / Tamil Nadu bounds
                            if 8.0 <= lat <= 14.0 and 76.0 <= lon <= 81.0:
                                d_info = self.find_district_by_coordinates(lat, lon)
                                if d_info and name.lower() not in seen_names:
                                    results.append({
                                        "name": f"{name}, {d_info['district_name']}",
                                        "latitude": lat,
                                        "longitude": lon,
                                        "district_id": d_info["district_id"],
                                        "district_name": d_info["district_name"],
                                        "category": "geocoded"
                                    })
                                    seen_names.add(name.lower())
            except Exception as e:
                logger.warning(f"External geocoding query failed ({e}), using internal index.")

        self._search_cache[q] = results
        return results[:limit]

    def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        d_info = self.find_district_by_coordinates(lat, lon)
        if d_info:
            return {
                "latitude": lat,
                "longitude": lon,
                "district_id": d_info["district_id"],
                "district_name": d_info["district_name"],
                "district_code": d_info["district_code"],
                "is_inside_tamil_nadu": True,
                "is_exact_match": d_info.get("is_exact_match", True)
            }
        else:
            return {
                "latitude": lat,
                "longitude": lon,
                "district_id": None,
                "district_name": None,
                "district_code": None,
                "is_inside_tamil_nadu": False,
                "is_exact_match": False
            }
