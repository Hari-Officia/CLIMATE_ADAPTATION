import sys
from pathlib import Path
from sqlalchemy import text

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.db.config import get_db_engine, get_chroma_client, CHROMA_PERSIST_DIR

def verify_postgresql():
    engine = get_db_engine()
    with engine.connect() as conn:
        db_name = conn.execute(text("SELECT current_database();")).scalar()
        postgis_ver = conn.execute(text("SELECT PostGIS_Version();")).scalar()
        return db_name, postgis_ver

def verify_chromadb():
    client = get_chroma_client()
    # Ping or heartbeat check to ensure client is operational
    heartbeat = client.heartbeat()
    return CHROMA_PERSIST_DIR, heartbeat

if __name__ == "__main__":
    db_name, postgis_ver = verify_postgresql()
    chroma_path, heartbeat = verify_chromadb()
    
    print("--- INFRASTRUCTURE VERIFICATION RESULTS ---")
    print("PostgreSQL:")
    print("CONNECTED")
    print(f"Database: {db_name}")
    print(f"PostGIS: detected ({postgis_ver})")
    print()
    print("ChromaDB:")
    print("INITIALIZED")
    print(f"Persistent path: {chroma_path}")
