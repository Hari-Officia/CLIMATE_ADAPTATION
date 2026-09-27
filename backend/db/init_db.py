import os
import json
import logging
from passlib.context import CryptContext
from backend.db.database import engine, SessionLocal, Base
from backend.db.models import (
    User, District, DistrictProfile, Location, ModelRegistryRecord, SystemLog,
    SourceRecord, DatasetRecord, SpatialLayerRecord, InfrastructureAssetRecord,
    PopulationExposureRecord, BuiltEnvironmentExposureRecord, InfrastructureExposureRecord,
    ExposureRecord, ProcessingRunRecord, PriorityMethodologyRecord, PriorityProfileRecord,
    PriorityDriverRecord, PriorityComponentRecord
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

        # 6. Phase F — Seed Provenance Sources
        if db.query(SourceRecord).count() == 0:
            logger.info("Seeding Phase F Source Registry records...")
            sources = [
                SourceRecord(source_id="SRC-IMD-001", source_name="India Meteorological Department Daily Reports", organization="IMD Ministry of Earth Sciences", source_type="government", official_url="https://mausam.imd.gov.in", authority_level="AUTHORITATIVE"),
                SourceRecord(source_id="SRC-TNDMA-001", source_name="Tamil Nadu State Disaster Management Plan 2023", organization="TNDMA Govt of Tamil Nadu", source_type="government", official_url="https://tndma.tn.gov.in", authority_level="AUTHORITATIVE"),
                SourceRecord(source_id="SRC-CENSUS-2011", source_name="Census of India 2011 District Demographics", organization="Office of the Registrar General India", source_type="government", official_url="https://censusindia.gov.in", authority_level="AUTHORITATIVE"),
                SourceRecord(source_id="SRC-WORLDPOP-2020", source_name="WorldPop Unconstrained Population Count 2020", organization="WorldPop University of Southampton", source_type="research", official_url="https://www.worldpop.org", authority_level="HIGH"),
                SourceRecord(source_id="SRC-OSM-2024", source_name="OpenStreetMap Infrastructure Assets Tamil Nadu", organization="OpenStreetMap Foundation", source_type="open_data", official_url="https://www.openstreetmap.org", authority_level="MEDIUM"),
            ]
            db.add_all(sources)
            db.commit()
            logger.info(f"Seeded {len(sources)} Source records.")

        # 7. Phase F — Seed Datasets Catalog
        if db.query(DatasetRecord).count() == 0:
            logger.info("Seeding Phase F Dataset Catalog records...")
            datasets = [
                DatasetRecord(dataset_id="DS-GEOJSON-TN-ADM2-001", source_id="SRC-TNDMA-001", dataset_name="Tamil Nadu 38 District Boundaries Master", data_type="vector_polygon", format="geojson", crs="EPSG:4326", checksum="e8f4a1c9b2d3e5f7a9b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4", row_count=38, current_status="ACTIVE"),
                DatasetRecord(dataset_id="DS-POP-TN-001", source_id="SRC-CENSUS-2011", dataset_name="Tamil Nadu District Population Exposure 2021", data_type="tabular", format="postgis", crs="EPSG:4326", checksum="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2", row_count=38, current_status="ACTIVE"),
                DatasetRecord(dataset_id="DS-INFRA-TN-001", source_id="SRC-OSM-2024", dataset_name="Tamil Nadu Critical Infrastructure Assets Layer", data_type="vector_point", format="postgis", crs="EPSG:4326", checksum="f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9", row_count=150, current_status="ACTIVE"),
                DatasetRecord(dataset_id="DS-LAND-TN-001", source_id="SRC-TNDMA-001", dataset_name="Tamil Nadu Built-Up & Urban Extent Layer", data_type="vector_polygon", format="postgis", crs="EPSG:4326", checksum="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef", row_count=38, current_status="ACTIVE"),
            ]
            db.add_all(datasets)
            db.commit()
            logger.info(f"Seeded {len(datasets)} Dataset records.")

        # 8. Phase F — Seed Spatial Layers
        if db.query(SpatialLayerRecord).count() == 0:
            logger.info("Seeding Phase F Spatial Layer records...")
            layers = [
                SpatialLayerRecord(layer_id="LAY-TN-ADM2-001", layer_name="Tamil Nadu 38 District Boundaries Master", dataset_id="DS-GEOJSON-TN-ADM2-001", geometry_type="MultiPolygon", feature_count=38),
                SpatialLayerRecord(layer_id="LAY-TN-POP-001", layer_name="Tamil Nadu District Population Layer", dataset_id="DS-POP-TN-001", geometry_type="Polygon", feature_count=38),
                SpatialLayerRecord(layer_id="LAY-TN-INFRA-001", layer_name="Tamil Nadu Critical Infrastructure Assets Layer", dataset_id="DS-INFRA-TN-001", geometry_type="Point", feature_count=150),
            ]
            db.add_all(layers)
            db.commit()
            logger.info(f"Seeded {len(layers)} Spatial Layer records.")

        # 9. Phase F — Seed Infrastructure Assets
        if db.query(InfrastructureAssetRecord).count() == 0:
            logger.info("Seeding Infrastructure Assets...")
            assets = [
                InfrastructureAssetRecord(asset_id="AST-CHE-HOSP-001", asset_type="healthcare", asset_name="Rajiv Gandhi Government General Hospital", district_id="chennai", latitude=13.0815, longitude=80.2777, dataset_id="DS-INFRA-TN-001", source_id="SRC-OSM-2024", criticality="HIGH"),
                InfrastructureAssetRecord(asset_id="AST-CHE-POWER-001", asset_type="power", asset_name="TANGEDCO Substation Central Chennai", district_id="chennai", latitude=13.0840, longitude=80.2710, dataset_id="DS-INFRA-TN-001", source_id="SRC-OSM-2024", criticality="HIGH"),
                InfrastructureAssetRecord(asset_id="AST-CBE-HOSP-001", asset_type="healthcare", asset_name="Coimbatore Medical College Hospital", district_id="coimbatore", latitude=10.9995, longitude=76.9650, dataset_id="DS-INFRA-TN-001", source_id="SRC-OSM-2024", criticality="HIGH"),
                InfrastructureAssetRecord(asset_id="AST-MAD-HOSP-001", asset_type="healthcare", asset_name="Government Rajaji Hospital Madurai", district_id="madurai", latitude=9.9275, longitude=78.1250, dataset_id="DS-INFRA-TN-001", source_id="SRC-OSM-2024", criticality="HIGH"),
                InfrastructureAssetRecord(asset_id="AST-TVL-WATER-001", asset_type="water", asset_name="Tiruvallur Water Treatment Plant", district_id="tiruvallur", latitude=13.1420, longitude=79.9080, dataset_id="DS-INFRA-TN-001", source_id="SRC-OSM-2024", criticality="HIGH"),
            ]
            db.add_all(assets)
            db.commit()
            logger.info(f"Seeded {len(assets)} Infrastructure Asset records.")

        # 10. Phase F — Seed Population & Built Environment Exposure
        if db.query(PopulationExposureRecord).count() == 0:
            logger.info("Seeding Population Exposure records for 38 districts...")
            profiles = db.query(DistrictProfile).all()
            pop_records = []
            built_records = []
            for p in profiles:
                pop_records.append(
                    PopulationExposureRecord(
                        district_id=p.district_id,
                        district_name=p.district_name,
                        total_population=p.population,
                        urban_population=int(p.population * (p.urban_percentage / 100.0)),
                        rural_population=int(p.population * (1.0 - p.urban_percentage / 100.0)),
                        vulnerable_age_group=int(p.population * 0.18), # Estimated ~18% elderly/children
                        dataset_id="DS-POP-TN-001",
                        dataset_year=2021
                    )
                )
                built_records.append(
                    BuiltEnvironmentExposureRecord(
                        district_id=p.district_id,
                        total_area_km2=p.area_km2,
                        built_up_area_km2=round(p.area_km2 * (p.urban_percentage / 100.0), 2),
                        impervious_surface_fraction=round(p.urban_percentage / 100.0 * 0.75, 2),
                        urban_density_category="HIGH" if p.urban_percentage > 60 else ("MEDIUM" if p.urban_percentage > 30 else "LOW"),
                        dataset_id="DS-LAND-TN-001"
                    )
                )
            db.add_all(pop_records)
            db.add_all(built_records)
            db.commit()
            logger.info(f"Seeded {len(pop_records)} Population and Built Environment exposure records.")

        # 11. Phase H — Seed Priority Methodology
        if db.query(PriorityMethodologyRecord).count() == 0:
            logger.info("Seeding Phase H Adaptation Priority Methodology...")
            mth = PriorityMethodologyRecord(
                methodology_id="MTH-PRIORITY-TN-001",
                name="Tamil Nadu Multi-Criteria Climate Adaptation Priority Framework",
                version="1.0.0",
                framework="Multi-Criteria Climate Decision Analysis (MCDA)",
                description="Decomposes adaptation priority into 4 pillars: Hazard Risk (Phase E), Exposure (Phase F), Vulnerability/Sensitivity (Phase G), and Resilience Gap (Phase G). Evaluates priority status, horizon, and deterministic drivers without unverified composite formula weights.",
                status="ACTIVE"
            )
            db.add(mth)
            db.commit()
            logger.info("Seeded Priority Methodology MTH-PRIORITY-TN-001.")

        # 12. Phase I — Seed Strategy Domains & Strategies
        from backend.db.models import StrategyDomainRecord, StrategyRecord
        CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "master")
        domains_path = os.path.join(CONFIG_DIR, "strategy_domains.json")
        strategies_path = os.path.join(CONFIG_DIR, "strategies.json")

        if db.query(StrategyDomainRecord).count() == 0 and os.path.exists(domains_path):
            with open(domains_path, "r", encoding="utf-8") as f:
                dom_data = json.load(f)
            dom_records = [
                StrategyDomainRecord(
                    domain_id=d["domain_id"],
                    name=d["name"],
                    description=d.get("description")
                ) for d in dom_data
            ]
            db.add_all(dom_records)
            db.commit()
            logger.info(f"Seeded {len(dom_records)} Strategy Domains.")

        if db.query(StrategyRecord).count() == 0 and os.path.exists(strategies_path):
            with open(strategies_path, "r", encoding="utf-8") as f:
                strat_data = json.load(f)
            strat_records = [
                StrategyRecord(
                    strategy_id=s["strategy_id"],
                    canonical_name=s["canonical_name"],
                    display_name=s["display_name"],
                    short_description=s.get("short_description"),
                    domain_id=s["domain_id"],
                    measure_type=s.get("measure_type", "STRUCTURAL"),
                    primary_hazard_id=s["primary_hazard_id"],
                    sector_ids=s.get("sector_ids"),
                    planning_horizon=s.get("planning_horizon", "SHORT_TERM"),
                    evidence_status=s.get("evidence_status", "VERIFIED"),
                    evidence_strength=s.get("evidence_strength", "STRONG"),
                    uncertainty_level=s.get("uncertainty_level", "LOW"),
                    status=s.get("status", "ACTIVE"),
                    aliases=s.get("aliases")
                ) for s in strat_data
            ]
            db.add_all(strat_records)
            db.commit()
            logger.info(f"Seeded {len(strat_records)} Strategies into PostgreSQL.")

        # 13. Phase J/K — Seed Optimization Methodology
        from backend.db.models import OptimizationMethodologyRecord
        if db.query(OptimizationMethodologyRecord).count() == 0:
            logger.info("Seeding Phase J/K Optimization Methodology...")
            opt_mth = OptimizationMethodologyRecord(
                methodology_id="MTH-OPT-TN-001",
                name="Tamil Nadu Classical Adaptation Strategy Portfolio Optimization Framework",
                version="1.0.0",
                description="Multi-objective classical baseline framework. Formulates binary decision variables x_i for Phase I strategy candidates.",
                status="ACTIVE"
            )
            db.add(opt_mth)
            db.commit()
            logger.info("Seeded Optimization Methodology MTH-OPT-TN-001.")

        # 14. Phase L — Seed QUBO Methodology
        from backend.db.models import QUBOMethodologyRecord
        if db.query(QUBOMethodologyRecord).count() == 0:
            logger.info("Seeding Phase L QUBO Methodology...")
            qubo_mth = QUBOMethodologyRecord(
                methodology_id="MTH-QUBO-TN-001",
                name="Canonical Classical-to-QUBO Penalty Transformation Methodology",
                version="1.0.0",
                objective_sign_convention="MINIMIZE_NEGATED_OBJECTIVE",
                matrix_convention="FULL_SYMMETRIC",
                slack_encoding="BINARY_EXPONENTIAL_SLACK",
                status="ACTIVE"
            )
            db.add(qubo_mth)
            db.commit()
            logger.info("Seeded QUBO Methodology MTH-QUBO-TN-001.")

        # Log system initialization
        init_log = SystemLog(
            level="INFO",
            component="SystemInit",
            message="Database initialized and baseline Phase H data seeded successfully."
        )
        db.add(init_log)
        db.commit()

        logger.info("Database initialization completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

