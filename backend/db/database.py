import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("climate_db")

# Default connection settings
PG_URL = os.getenv("DATABASE_URL", "postgresql://climate_user:climate_password@localhost:5432/climate_risk_db")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(DATA_DIR, "climate_risk.db")
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

# Connection selection with automatic fallback
DB_ENGINE_TYPE = "sqlite"
engine = None

try:
    if os.getenv("PREFER_POSTGRES", "false").lower() == "true":
        temp_engine = create_engine(PG_URL, connect_args={"connect_timeout": 2})
        with temp_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = temp_engine
        DB_ENGINE_TYPE = "postgresql"
        logger.info("Connected to PostgreSQL primary database.")
    else:
        # Default zero-friction local SQLite
        engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
        DB_ENGINE_TYPE = "sqlite"
        logger.info(f"Using SQLite database at {SQLITE_PATH}")
except Exception as e:
    logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite at {SQLITE_PATH}")
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

def get_db_status():
    return {
        "engine": DB_ENGINE_TYPE,
        "url": PG_URL if DB_ENGINE_TYPE == "postgresql" else SQLITE_URL,
        "status": "connected"
    }
