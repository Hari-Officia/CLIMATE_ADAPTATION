import os
import sys
import logging
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from backend.db.models import (
    Base, User, District, DistrictProfile, Location,
    ForecastRun, ForecastData, RiskResult, ModelRegistryRecord, SystemLog
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_to_postgres")

def get_sqlite_engine():
    sqlite_path = Path(__file__).resolve().parent.parent / "backend" / "data" / "climate_risk.db"
    if not sqlite_path.exists():
        # Check alternate location
        sqlite_path = Path(__file__).resolve().parent.parent / "data" / "climate_risk.db"
    return create_engine(f"sqlite:///{sqlite_path}")

def get_postgres_engine():
    pg_url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/climate_platform")
    return create_engine(pg_url)

MODELS = [
    User,
    District,
    DistrictProfile,
    Location,
    ForecastRun,
    ForecastData,
    RiskResult,
    ModelRegistryRecord,
    SystemLog
]

def migrate():
    sqlite_engine = get_sqlite_engine()
    pg_engine = get_postgres_engine()

    logger.info("Creating all tables in PostgreSQL ('climate_platform')...")
    Base.metadata.create_all(bind=pg_engine)
    logger.info("PostgreSQL tables created successfully.")

    SqliteSession = sessionmaker(bind=sqlite_engine)
    PgSession = sessionmaker(bind=pg_engine)

    sqlite_db = SqliteSession()
    pg_db = PgSession()

    try:
        for model in MODELS:
            table_name = model.__tablename__
            rows = sqlite_db.query(model).all()
            logger.info(f"Reading {len(rows)} records from SQLite table '{table_name}'...")

            migrated_count = 0
            for row in rows:
                # Check if record already exists in Postgres
                existing = None
                if hasattr(model, "id") and row.id is not None:
                    existing = pg_db.query(model).filter(model.id == row.id).first()
                elif hasattr(model, "district_id") and row.district_id is not None:
                    existing = pg_db.query(model).filter(model.district_id == row.district_id).first()

                if not existing:
                    # Construct a clean dictionary of column values
                    col_data = {
                        c.name: getattr(row, c.name)
                        for c in model.__table__.columns
                    }
                    new_obj = model(**col_data)
                    pg_db.add(new_obj)
                    migrated_count += 1

            pg_db.commit()
            logger.info(f"Migrated {migrated_count} new records into PostgreSQL table '{table_name}'. Total in PG: {pg_db.query(model).count()}")

        # Update primary key sequences in PostgreSQL for tables with integer PKs
        with pg_engine.connect() as conn:
            for model in MODELS:
                table_name = model.__tablename__
                # Check if sequence exists
                seq_query = text(f"SELECT pg_get_serial_sequence('{table_name}', 'id');")
                seq_name = conn.execute(seq_query).scalar()
                if seq_name:
                    max_id_query = text(f"SELECT COALESCE(MAX(id), 0) FROM {table_name};")
                    max_id = conn.execute(max_id_query).scalar()
                    if max_id > 0:
                        conn.execute(text(f"SELECT setval('{seq_name}', {max_id});"))
            conn.commit()

        logger.info("Migration to PostgreSQL completed successfully!")

    except Exception as e:
        pg_db.rollback()
        logger.error(f"Migration error: {e}")
        raise
    finally:
        sqlite_db.close()
        pg_db.close()

if __name__ == "__main__":
    migrate()
