"""
Staleness Checker Service (Phase N)
Detects stale context by comparing stored context hashes against fresh context evaluation.
"""

import hashlib
import json
from typing import Dict, Any

class StalenessChecker:
    def check_staleness(self, stored_context_hash: str, fresh_context_packet: Dict[str, Any]) -> Dict[str, Any]:
        """Check if fresh context packet hash matches stored context hash."""
        fresh_hash = fresh_context_packet.get("context_hash")
        is_stale = (stored_context_hash != fresh_hash)

        return {
            "is_stale": is_stale,
            "stored_hash": stored_context_hash,
            "fresh_hash": fresh_hash,
            "status": "STALE_CONTEXT" if is_stale else "UP_TO_DATE"
        }
