"""
Script to extract and canonicalize the 38 Tamil Nadu districts from
geoBoundaries-IND-ADM2_simplified.geojson and output data/geojson/tamil_nadu_districts.geojson
"""
import json
import os

SOURCE_GEOJSON = os.path.join(os.path.dirname(__file__), "..", "geoBoundaries-IND-ADM2-all", "geoBoundaries-IND-ADM2_simplified.geojson")
TARGET_GEOJSON = os.path.join(os.path.dirname(__file__), "..", "data", "geojson", "tamil_nadu_districts.geojson")

CANONICAL_DISTRICTS = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri",
    "Dindigul", "Erode", "Kallakurichi", "Kancheepuram", "Kanniyakumari", "Karur",
    "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam", "Namakkal", "Nilgiris",
    "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga",
    "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
    "Viluppuram", "Virudhunagar"
]

GEOBOUNDARIES_NAME_MAP = {
    "Chengalputtu": "Chengalpattu",
    "The Nilgiris": "Nilgiris",
    "Thoothukkudi": "Thoothukudi",
    "Thiruvallur": "Tiruvallur",
    "Thiruvarur": "Tiruvarur"
}

DISTRICT_CENTROIDS = {
    "Ariyalur": {"lat": 11.1401, "lon": 79.0786},
    "Chengalpattu": {"lat": 12.6841, "lon": 79.9836},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558},
    "Cuddalore": {"lat": 11.7480, "lon": 79.7714},
    "Dharmapuri": {"lat": 12.1211, "lon": 78.1582},
    "Dindigul": {"lat": 10.3673, "lon": 77.9803},
    "Erode": {"lat": 11.3410, "lon": 77.7172},
    "Kallakurichi": {"lat": 11.7383, "lon": 78.9639},
    "Kancheepuram": {"lat": 12.8342, "lon": 79.7036},
    "Kanniyakumari": {"lat": 8.0883, "lon": 77.5385},
    "Karur": {"lat": 10.9601, "lon": 78.0766},
    "Krishnagiri": {"lat": 12.5186, "lon": 78.2137},
    "Madurai": {"lat": 9.9252, "lon": 78.1198},
    "Mayiladuthurai": {"lat": 11.1075, "lon": 79.6524},
    "Nagapattinam": {"lat": 10.7672, "lon": 79.8424},
    "Namakkal": {"lat": 11.2189, "lon": 78.1674},
    "Nilgiris": {"lat": 11.4916, "lon": 76.7337},
    "Perambalur": {"lat": 11.2342, "lon": 78.8820},
    "Pudukkottai": {"lat": 10.3797, "lon": 78.8208},
    "Ramanathapuram": {"lat": 9.3639, "lon": 78.8395},
    "Ranipet": {"lat": 12.9298, "lon": 79.3326},
    "Salem": {"lat": 11.6643, "lon": 78.1460},
    "Sivaganga": {"lat": 9.8433, "lon": 78.4809},
    "Tenkasi": {"lat": 8.9594, "lon": 77.3161},
    "Thanjavur": {"lat": 10.7870, "lon": 79.1378},
    "Theni": {"lat": 10.0104, "lon": 77.4768},
    "Thoothukudi": {"lat": 8.7642, "lon": 78.1348},
    "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047},
    "Tirunelveli": {"lat": 8.7139, "lon": 77.7567},
    "Tirupathur": {"lat": 12.4958, "lon": 78.5678},
    "Tiruppur": {"lat": 11.1085, "lon": 77.3411},
    "Tiruvallur": {"lat": 13.1432, "lon": 79.9079},
    "Tiruvannamalai": {"lat": 12.2253, "lon": 79.0747},
    "Tiruvarur": {"lat": 10.7725, "lon": 79.6365},
    "Vellore": {"lat": 12.9165, "lon": 79.1325},
    "Viluppuram": {"lat": 11.9401, "lon": 79.4861},
    "Virudhunagar": {"lat": 9.5680, "lon": 77.9624}
}

def generate():
    os.makedirs(os.path.dirname(TARGET_GEOJSON), exist_ok=True)
    with open(SOURCE_GEOJSON, "r", encoding="utf-8") as f:
        src = json.load(f)

    target_features = []
    found_names = set()

    for feat in src["features"]:
        raw_name = feat["properties"].get("shapeName", "").strip()
        canonical_name = GEOBOUNDARIES_NAME_MAP.get(raw_name, raw_name)
        if canonical_name in CANONICAL_DISTRICTS:
            centroid = DISTRICT_CENTROIDS.get(canonical_name, {"lat": 0.0, "lon": 0.0})
            code = canonical_name.upper().replace(" ", "_")
            feat["id"] = canonical_name.lower()
            feat["properties"] = {
                "district_id": canonical_name.lower(),
                "district_code": code,
                "district_name": canonical_name,
                "state": "Tamil Nadu",
                "latitude": centroid["lat"],
                "longitude": centroid["lon"],
                "original_shape_id": feat["properties"].get("shapeID", ""),
                "area_sqkm": feat["properties"].get("shapeArea", 0)
            }
            target_features.append(feat)
            found_names.add(canonical_name)

    print(f"Extracted {len(target_features)} districts out of {len(CANONICAL_DISTRICTS)}.")
    missing = set(CANONICAL_DISTRICTS) - found_names
    if missing:
        print(f"WARNING: Missing districts: {missing}")

    output_geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": sorted(target_features, key=lambda x: x["properties"]["district_name"])
    }

    with open(TARGET_GEOJSON, "w", encoding="utf-8") as f:
        json.dump(output_geojson, f, indent=2)

    print(f"Successfully saved canonical GeoJSON to {TARGET_GEOJSON}")

if __name__ == "__main__":
    generate()
