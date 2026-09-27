"""
Verification Script: Feature Contract
Verifies the 53-feature vector specification (15 continuous + 38 district indicators).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.services.feature_engineering import FEATURE_COLUMNS_53

def verify_feature_contract():
    features = FEATURE_COLUMNS_53
    if len(features) != 53:
        return {"status": "FAIL", "message": f"Expected 53 features, found {len(features)}"}
        
    continuous = [f for f in features if not f.startswith("district_")]
    district_indicators = [f for f in features if f.startswith("district_")]
    
    if len(continuous) != 15:
        return {"status": "FAIL", "message": f"Expected 15 continuous features, found {len(continuous)}"}
        
    if len(district_indicators) != 38:
        return {"status": "FAIL", "message": f"Expected 38 district indicator features, found {len(district_indicators)}"}
        
    return {
        "status": "PASS",
        "total_features": 53,
        "continuous_features": 15,
        "district_features": 38,
        "contract": "SC-FEAT-001"
    }

if __name__ == "__main__":
    import json
    res = verify_feature_contract()
    print(json.dumps(res, indent=2))
