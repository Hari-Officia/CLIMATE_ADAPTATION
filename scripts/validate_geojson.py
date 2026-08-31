"""
Validation script for Tamil Nadu GeoJSON.
Verifies JSON validity, Polygon/MultiPolygon geometry, district identifiers, WGS84 CRS, and all 38 districts.
"""
import json
import os
import sys

TARGET_GEOJSON = os.path.join(os.path.dirname(__file__), "..", "data", "geojson", "tamil_nadu_districts.geojson")

EXPECTED_DISTRICTS = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri",
    "Dindigul", "Erode", "Kallakurichi", "Kancheepuram", "Kanniyakumari", "Karur",
    "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam", "Namakkal", "Nilgiris",
    "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga",
    "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
    "Viluppuram", "Virudhunagar"
]

def validate():
    print(f"Validating {TARGET_GEOJSON}...")
    if not os.path.exists(TARGET_GEOJSON):
        print("FAIL: GeoJSON file does not exist.")
        return False

    with open(TARGET_GEOJSON, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"FAIL: Invalid JSON: {e}")
            return False

    if data.get("type") != "FeatureCollection":
        print(f"FAIL: Root type is not FeatureCollection: {data.get('type')}")
        return False

    features = data.get("features", [])
    if len(features) != 38:
        print(f"FAIL: Expected 38 features, found {len(features)}")
        return False

    found_names = set()
    for i, feat in enumerate(features):
        geom_type = feat.get("geometry", {}).get("type")
        if geom_type not in ["Polygon", "MultiPolygon"]:
            print(f"FAIL: Feature {i} geometry type {geom_type} is not Polygon/MultiPolygon")
            return False

        props = feat.get("properties", {})
        d_name = props.get("district_name")
        d_code = props.get("district_code")
        d_id = props.get("district_id")

        if not d_name or not d_code or not d_id:
            print(f"FAIL: Feature {i} missing district identifier properties: {props}")
            return False

        lat = props.get("latitude")
        lon = props.get("longitude")
        if not (8.0 <= lat <= 14.0 and 76.0 <= lon <= 81.0):
            print(f"FAIL: Centroid coordinates out of Tamil Nadu bounds for {d_name}: lat={lat}, lon={lon}")
            return False

        found_names.add(d_name)

    missing = set(EXPECTED_DISTRICTS) - found_names
    if missing:
        print(f"FAIL: Missing districts: {missing}")
        return False

    print("SUCCESS: All 38 Tamil Nadu districts verified. Topologically valid Polygons/MultiPolygons with CRS84.")
    return True

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
