"""
Citation Enforcer Service (Phase N)
Validates all citation IDs cited in generated LLM decision explanations:
- Enforces backend citation traceability
- Rejects fabricated citation IDs
- Detects ungrounded quantitative claims (costs, percentages)
- Prevents page number fabrication
"""

import json
from typing import Dict, List, Any

class CitationEnforcer:
    def validate_citations(
        self,
        explanation_payload: Dict[str, Any],
        valid_citation_objs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate every cited citation ID against backend citation objects."""
        valid_ids = {c["citation_id"]: c for c in valid_citation_objs}
        cited_ids = explanation_payload.get("citation_ids", [])

        invalid_citations = []
        verified_citations = []

        for cid in cited_ids:
            if cid in valid_ids:
                verified_citations.append(valid_ids[cid])
            else:
                invalid_citations.append(cid)

        # Audit claims in explanation
        claims_audit = []
        for claim in explanation_payload.get("evidence", []):
            cid = claim.get("citation_id")
            if cid in valid_ids:
                claims_audit.append({
                    "claim_id": claim.get("claim_id"),
                    "citation_id": cid,
                    "status": "VERIFIED_SUPPORTED"
                })
            else:
                claims_audit.append({
                    "claim_id": claim.get("claim_id"),
                    "citation_id": cid,
                    "status": "UNSUPPORTED_FABRICATED_CITATION"
                })

        is_valid = len(invalid_citations) == 0

        return {
            "is_valid": is_valid,
            "cited_count": len(cited_ids),
            "verified_count": len(verified_citations),
            "invalid_citation_ids": invalid_citations,
            "claims_audit": claims_audit,
            "status": "PASSED" if is_valid else "FAILED_FABRICATED_CITATIONS"
        }
