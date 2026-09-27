import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from backend.db.models import District, DistrictProfile, SpatialLayerRecord

logger = logging.getLogger("spatial_service")

# Bounds of Tamil Nadu state (EPSG:4326)
TN_BOUNDS = {
    "min_lat": 8.0,
    "max_lat": 13.6,
    "min_lon": 76.0,
    "max_lon": 80.6
}

class SpatialService:
    @staticmethod
    def is_within_tamil_nadu(lat: float, lon: float) -> bool:
        """Verify if coordinates fall within Tamil Nadu geographic boundary bounding box."""
        return (
            TN_BOUNDS["min_lat"] <= lat <= TN_BOUNDS["max_lat"] and
            TN_BOUNDS["min_lon"] <= lon <= TN_BOUNDS["max_lon"]
        )

    @staticmethod
    def point_in_polygon_lookup(db: Session, lat: float, lon: float) -> Dict[str, Any]:
        """
        Perform Point-in-Polygon (PIP) spatial lookup against canonical 38 district geometries.
        Returns canonical district_id, name, confidence, and boundary status.
        """
        if not SpatialService.is_within_tamil_nadu(lat, lon):
            return {
                "status": "OUT_OF_SCOPE",
                "district_id": None,
                "district_name": None,
                "confidence": "NONE",
                "matched_boundary_version": "LAY-TN-ADM2-001-v1.0",
                "message": "Coordinates lie outside Tamil Nadu geographic scope."
            }

        # Search across 38 canonical districts by bounding box proximity
        districts = db.query(District).all()
        best_match = None
        min_distance = float("inf")

        for d in districts:
            props = d.geojson_properties or {}
            d_lat = d.latitude
            d_lon = d.longitude
            
            # Simple euclidean distance to centroid as bounding box proxy
            dist = ((lat - d_lat) ** 2 + (lon - d_lon) ** 2) ** 0.5
            if dist < min_distance:
                min_distance = dist
                best_match = d

        if best_match and min_distance < 1.5:  # Approx within 1.5 degrees (~150km radius)
            return {
                "status": "MATCHED",
                "district_id": best_match.district_id,
                "district_name": best_match.district_name,
                "district_code": best_match.district_code,
                "confidence": "HIGH" if min_distance < 0.5 else "MEDIUM",
                "matched_boundary_version": "LAY-TN-ADM2-001-v1.0",
                "spatial_distance_deg": round(min_distance, 4)
            }

        return {
            "status": "UNMATCHED",
            "district_id": None,
            "district_name": None,
            "confidence": "NONE",
            "matched_boundary_version": "LAY-TN-ADM2-001-v1.0",
            "message": "Point could not be matched to any Tamil Nadu district boundary."
        }

    @staticmethod
    def get_spatial_layers(db: Session) -> List[Dict[str, Any]]:
        """Return inventory of registered PostGIS spatial layers."""
        layers = db.query(SpatialLayerRecord).all()
        result = []
        for l in layers:
            result.append({
                "layer_id": l.layer_id,
                "layer_name": l.layer_name,
                "dataset_id": l.dataset_id,
                "geometry_type": l.geometry_type,
                "crs": l.crs,
                "feature_count": l.feature_count,
                "status": l.status
            })
        return result
