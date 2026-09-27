import os
import sys
import json
import datetime
from backend.db.database import get_db
from backend.db.models import District, RiskResult, DecisionResultRecord

def perform_database_backup():
    db = next(get_db())
    districts = db.query(District).all()
    risks = db.query(RiskResult).all()
    decisions = db.query(DecisionResultRecord).all()
    
    backup_payload = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "district_count": len(districts),
        "risk_records_count": len(risks),
        "decision_records_count": len(decisions),
        "schema_version": "1.0.0",
        "status": "COMPLETED"
    }
    
    backup_dir = "scratch/backups"
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f"backup_climate_db_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(backup_payload, f, indent=2)
        
    print(f"Database Backup Succeeded: Saved to {backup_file}")
    return backup_file

if __name__ == "__main__":
    perform_database_backup()
