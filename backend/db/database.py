import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger("climate_db")

# Connection strings
PG_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/climate_platform")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(DATA_DIR, "climate_risk.db")
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

# Primary PostgreSQL with SQLite automatic backup fallback
DB_ENGINE_TYPE = "sqlite"
engine = None

try:
    prefer_postgres = os.getenv("PREFER_POSTGRES", "true").lower() in ("true", "1", "yes")
    if prefer_postgres:
        temp_engine = create_engine(PG_URL, connect_args={})
        with temp_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = temp_engine
        DB_ENGINE_TYPE = "postgresql"
        logger.info("Connected to PostgreSQL primary database (climate_platform).")
    else:
        engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
        DB_ENGINE_TYPE = "sqlite"
        logger.info(f"Using SQLite backup database at {SQLITE_PATH}")
except Exception as e:
    logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite backup at {SQLITE_PATH}")
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    DB_ENGINE_TYPE = "sqlite"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from contextlib import contextmanager

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_status():
    return {
        "engine": DB_ENGINE_TYPE,
        "url": PG_URL if DB_ENGINE_TYPE == "postgresql" else SQLITE_URL,
        "status": "connected"
    }
