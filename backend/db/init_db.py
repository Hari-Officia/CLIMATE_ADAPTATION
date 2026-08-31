import os
import json
import logging
from passlib.context import CryptContext
from backend.db.database import engine, SessionLocal, Base
from backend.db.models import (
    User, District, DistrictProfile, Location, ModelRegistryRecord, SystemLog
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

GEOJSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "geojson", "tamil_nadu_districts.geojson")
PROFILES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "district_profiles", "tamil_nadu_profiles.json")

def seed_database():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Seed Users
        if db.query(User).count() == 0:
            logger.info("Seeding default users...")
            admin_user = User(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                role="ADMIN",
                full_name="System Administrator",
                email="admin@climaterisk.tn.gov.in"
            )
            harish_user = User(
                username="harish",
                password_hash=pwd_context.hash("user123"),
                role="USER",
                full_name="Harish Kumar",
                email="harish@climaterisk.tn.gov.in"
            )
            db.add_all([admin_user, harish_user])
            db.commit()
            logger.info("Users seeded: admin (ADMIN), harish (USER).")

        # 2. Seed Districts from GeoJSON
        if db.query(District).count() == 0:
            logger.info(f"Loading districts from {GEOJSON_PATH}...")
            if os.path.exists(GEOJSON_PATH):
                with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
                    geojson_data = json.load(f)

                districts_to_add = []
                for feat in geojson_data.get("features", []):
                    props = feat.get("properties", {})
                    d_id = props.get("district_id")
                    d_name = props.get("district_name")
                    d_code = props.get("district_code")
                    lat = props.get("latitude")
                    lon = props.get("longitude")

                    if d_id and d_name:
                        district = District(
                            district_id=d_id,
                            district_name=d_name,
                            district_code=d_code,
                            latitude=lat,
                            longitude=lon,
                            geojson_properties=props
                        )
                        districts_to_add.append(district)

                db.add_all(districts_to_add)
                db.commit()
                logger.info(f"Seeded {len(districts_to_add)} districts.")

        # 3. Seed District Profiles
        if db.query(DistrictProfile).count() == 0:
            logger.info(f"Loading district profiles from {PROFILES_PATH}...")
            if os.path.exists(PROFILES_PATH):
                with open(PROFILES_PATH, "r", encoding="utf-8") as f:
                    profiles_data = json.load(f)

                profiles_to_add = []
                for p in profiles_data:
                    profile = DistrictProfile(
                        district_id=p["district_id"],
                        district_name=p["district_name"],
                        population=p["population"],
                        area_km2=p["area_km2"],
                        population_density=p["population_density"],
                        urban_percentage=p["urban_percentage"],
                        coastal=p["coastal"],
                        elevation_m=p["elevation_m"],
                        source=p.get("source", "Census of India"),
                        source_year=p.get("source_year", 2021)
                    )
                    profiles_to_add.append(profile)

                db.add_all(profiles_to_add)
                db.commit()
                logger.info(f"Seeded {len(profiles_to_add)} district demographic profiles.")

        # 4. Seed Notable Landmarks / Locations
        if db.query(Location).count() == 0:
            logger.info("Seeding landmark locations...")
            landmarks = [
                Location(name="Marina Beach", latitude=13.0500, longitude=80.2824, district_id="chennai", category="landmark"),
                Location(name="Chennai Central Railway Station", latitude=13.0827, longitude=80.2755, district_id="chennai", category="station"),
                Location(name="Coimbatore International Airport", latitude=11.0299, longitude=77.0434, district_id="coimbatore", category="station"),
                Location(name="Avadi", latitude=13.1147, longitude=80.1018, district_id="tiruvallur", category="town"),
                Location(name="Meenakshi Amman Temple", latitude=9.9195, longitude=78.1193, district_id="madurai", category="landmark"),
                Location(name="Ooty Lake", latitude=11.4064, longitude=76.6896, district_id="nilgiris", category="landmark"),
                Location(name="Kanyakumari Pier / Sunset Point", latitude=8.0780, longitude=77.5550, district_id="kanniyakumari", category="landmark"),
                Location(name="Brihadisvara Temple, Thanjavur", latitude=10.7828, longitude=79.1318, district_id="thanjavur", category="landmark")
            ]
            db.add_all(landmarks)
            db.commit()
            logger.info(f"Seeded {len(landmarks)} landmark locations.")

        # 5. Seed Model Registry Records
        if db.query(ModelRegistryRecord).count() == 0:
            logger.info("Seeding Model Registry metadata...")
            models = [
                ModelRegistryRecord(
                    hazard="flood",
                    model_name="Flood Risk XGBoost Classifier",
                    model_path="Models/flood_xgboost.pkl",
                    framework="XGBoost 1.7+",
                    n_features=53,
                    roc_auc=0.906,
                    pr_auc=0.074,
                    status="ACTIVE"
                ),
                ModelRegistryRecord(
                    hazard="drought",
                    model_name="Drought Risk XGBoost Classifier",
                    model_path="Models/drought_xgboost.pkl",
                    framework="XGBoost 1.7+",
                    n_features=53,
                    roc_auc=0.9998,
                    pr_auc=0.9993,
                    status="ACTIVE"
                ),
                ModelRegistryRecord(
                    hazard="heatwave",
                    model_name="Heatwave Risk XGBoost Classifier",
                    model_path="Models/heatwave_xgboost.pkl",
                    framework="XGBoost 1.7+",
                    n_features=53,
                    roc_auc=1.0000,
                    pr_auc=0.9964,
                    status="ACTIVE"
                ),
            ]
            db.add_all(models)
            db.commit()
            logger.info("Seeded 3 ML Model Registry records.")

        # Log system initialization
        init_log = SystemLog(
            level="INFO",
            component="SystemInit",
            message="Database initialized and baseline data seeded successfully."
        )
        db.add(init_log)
        db.commit()

        logger.info("Database initialization completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
