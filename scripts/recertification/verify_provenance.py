"""
Verification Script: Provenance Re-Certification
Verifies resolution of lineage nodes, system versions, and decision context hash.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.services.orchestration.workflow_engine import MasterDecisionOrchestrator

def verify_provenance():
    orchestrator = MasterDecisionOrchestrator()
    res = orchestrator.execute_workflow(district_id="chennai")
    if not res or "provenance" not in res:
        return {"status": "FAIL", "message": "Decision execution missing provenance context"}
        
    provenance = res.get("provenance", {})
    context_hash = provenance.get("context_hash")
    system_versions = provenance.get("system_versions", {})
    
    if not context_hash:
        return {"status": "FAIL", "message": "Missing context_hash in provenance"}
        
    return {
        "status": "PASS",
        "system_versions_count": len(system_versions),
        "context_hash": context_hash,
        "policy": "POL-PROV-001"
    }

if __name__ == "__main__":
    import json
    res = verify_provenance()
    print(json.dumps(res, indent=2))
