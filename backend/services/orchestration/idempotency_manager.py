"""
Idempotency Manager Service (Phase O)
Hashes decision request payloads to detect duplicate requests and return existing completed decision results.
"""

import hashlib
import json
from typing import Dict, Any, Optional

class IdempotencyManager:
    def __init__(self):
        self._cache = {}

    def compute_idempotency_key(self, request_payload: Dict[str, Any]) -> str:
        """Compute SHA-256 hash over deterministic fields in request."""
        clean_req = {
            "district_id": request_payload.get("district_id"),
            "hazard_ids": sorted(request_payload.get("hazard_ids") or []),
            "optimization_mode": request_payload.get("optimization_mode", "CLASSICAL"),
            "qaoa_p_depth": request_payload.get("qaoa_p_depth", 2)
        }
        raw_str = json.dumps(clean_req, sort_keys=True)
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    def get_cached_result(self, key: str) -> Optional[Dict[str, Any]]:
        return self._cache.get(key)

    def cache_result(self, key: str, decision_result: Dict[str, Any]):
        self._cache[key] = decision_result
