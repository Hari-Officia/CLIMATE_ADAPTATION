import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
import geoalchemy2  # noqa: F401
import chromadb

# Load environment variables from root .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "knowledge_base/chroma")

def get_db_engine():
    """Create and return a SQLAlchemy engine configured for PostgreSQL/PostGIS."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables.")
    return create_engine(DATABASE_URL)

def get_chroma_client():
    """Create and return a local ChromaDB PersistentClient."""
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
