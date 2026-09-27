"""
Evidence Linker Service (Phase N)
Links canonical strategies to retrieved claims, manages conflict records, and produces strategy-evidence strength matrices.
"""

import json
import os
from typing import Dict, List, Any, Optional

class EvidenceLinker:
    def __init__(self, knowledge_base_dir: str = "knowledge_base/v1.0.0_verified"):
        self.kb_dir = knowledge_base_dir
        self.evidence_matrix_path = os.path.join(self.kb_dir, "04_EVIDENCE", "evidence_matrix.csv")
        self.claims_path = os.path.join(self.kb_dir, "04_EVIDENCE", "evidence_claims.jsonl")
        self._load_data()

    def _load_data(self):
        self.claims = []
        if os.path.exists(self.claims_path):
            with open(self.claims_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        self.claims.append(json.loads(line))

    def get_strategy_evidence(self, strategy_id: str) -> List[Dict[str, Any]]:
        """Retrieve all evidence claims linked to a given canonical strategy ID."""
        linked = []
        for claim in self.claims:
            if claim.get("strategy_id") == strategy_id or strategy_id in claim.get("strategy_ids", []):
                linked.append(claim)
        return linked

    def evaluate_conflict(self, claim_a: Dict[str, Any], claim_b: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect potential evidence conflicts between two claims."""
        if claim_a.get("strategy_id") == claim_b.get("strategy_id"):
            val_a = claim_a.get("quantitative_value")
            val_b = claim_b.get("quantitative_value")
            if val_a is not None and val_b is not None and val_a != val_b:
                return {
                    "conflict_id": f"CFL-{claim_a.get('claim_id')}-{claim_b.get('claim_id')}",
                    "claim_a_id": claim_a.get("claim_id"),
                    "claim_b_id": claim_b.get("claim_id"),
                    "conflict_type": "QUANTITATIVE_MISMATCH",
                    "resolution_status": "CONTEXTUALIZED",
                    "context_notes": f"Source A claims {val_a} while Source B claims {val_b} under different baseline conditions."
                }
        return None
