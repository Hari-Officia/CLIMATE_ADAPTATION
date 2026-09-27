"""
Verification Script: 38-District Independent Certification
Executes decision workflow reconstruction across all 38 Tamil Nadu districts.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.services.feature_engineering import DISTRICT_LIST
from backend.services.orchestration.workflow_engine import MasterDecisionOrchestrator

def verify_38_districts():
    districts = [d.lower() for d in DISTRICT_LIST]
    if len(districts) != 38:
        return {"status": "FAIL", "message": f"Expected 38 districts, got {len(districts)}"}
        
    orchestrator = MasterDecisionOrchestrator()
    verified_districts = []
    
    for d in districts:
        try:
            res = orchestrator.execute_workflow(district_id=d)
            if res and res.get("validation_status") == "VERIFIED":
                verified_districts.append(d)
        except Exception as e:
            return {"status": "FAIL", "message": f"District {d} failed verification: {str(e)}"}
            
    if len(verified_districts) != 38:
        return {"status": "FAIL", "message": f"Expected 38 verified districts, got {len(verified_districts)}"}
        
    return {
        "status": "PASS",
        "districts_expected": 38,
        "districts_verified": 38,
        "district_list": verified_districts
    }

if __name__ == "__main__":
    import json
    res = verify_38_districts()
    print(json.dumps(res, indent=2))
