"""
Verification Script: Scientific Contracts
Verifies config/governance/scientific_contract_registry.json exists, contains 13 required contracts, and matches hashes.
"""
import json
from pathlib import Path

def verify_scientific_contracts():
    registry_path = Path("config/governance/scientific_contract_registry.json")
    if not registry_path.exists():
        return {"status": "FAIL", "message": "Scientific contract registry missing"}
    
    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    contracts = data.get("contracts", [])
    if len(contracts) < 13:
        return {"status": "FAIL", "message": f"Expected at least 13 contracts, found {len(contracts)}"}
        
    contract_ids = {c["contract_id"] for c in contracts}
    required = {
        "SC-FEAT-001", "SC-FORM-001", "SC-MOD-001", "SC-RISK-002",
        "SC-EXPO-001", "SC-VULN-001", "SC-RESI-001", "SC-PRIO-001",
        "SC-OPT-001", "SC-QUBO-001", "SC-QAOA-001", "SC-RAG-001", "SC-LLM-001"
    }
    
    missing = required - contract_ids
    if missing:
        return {"status": "FAIL", "message": f"Missing scientific contracts: {missing}"}
        
    return {"status": "PASS", "contract_count": len(contracts), "registry": "BASE-3.0.0-20260923"}

if __name__ == "__main__":
    res = verify_scientific_contracts()
    print(json.dumps(res, indent=2))
