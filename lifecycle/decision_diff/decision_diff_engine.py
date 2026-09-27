"""
Decision Diff Engine
Compares decision workflow runs across baseline and candidate versions, tracking WHAT, WHY, and WHICH input/version/rule changed.
"""
from typing import Dict, Any

class DecisionDiffEngine:
    @staticmethod
    def compute_diff(run1: Dict[str, Any], run2: Dict[str, Any]) -> Dict[str, Any]:
        district_id = run1.get("district_id") or run2.get("district_id")
        hash1 = run1.get("provenance", {}).get("context_hash")
        hash2 = run2.get("provenance", {}).get("context_hash")
        
        is_identical = (hash1 == hash2)
        
        return {
            "district_id": district_id,
            "is_identical": is_identical,
            "hash_baseline": hash1,
            "hash_candidate": hash2,
            "risk_score_delta": (run2.get("risk_score", 0) - run1.get("risk_score", 0)),
            "priority_score_delta": (run2.get("priority_score", 0) - run1.get("priority_score", 0)),
            "strategy_diff": {
                "unchanged": [s for s in run1.get("selected_strategies", []) if s in run2.get("selected_strategies", [])],
                "added": [s for s in run2.get("selected_strategies", []) if s not in run1.get("selected_strategies", [])],
                "removed": [s for s in run1.get("selected_strategies", []) if s not in run2.get("selected_strategies", [])]
            }
        }
