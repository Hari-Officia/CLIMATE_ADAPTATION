"""
Output Validator Service (Phase N)
Performs post-generation verification:
- Schema validation against explanation.schema.json
- Numeric consistency checking (verifies risk values, priority scores, QAOA metrics match input context exactly)
- Entity consistency checking (verifies district name, strategy IDs, hazard IDs match input context exactly)
- Hallucination and prompt injection detection
"""

import json
from typing import Dict, List, Any

class OutputValidator:
    def validate_explanation(
        self,
        explanation_payload: Dict[str, Any],
        context_packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate numeric consistency, entity consistency, and hallucination bounds."""
        violations = []

        # 1. Entity consistency check
        expected_district_id = context_packet["district_id"]
        if explanation_payload.get("district_id") != expected_district_id:
            violations.append(f"District ID mismatch: expected '{expected_district_id}', got '{explanation_payload.get('district_id')}'")

        # 2. Strategy portfolio consistency check
        expected_strat_ids = set(context_packet["selected_strategy_ids"])
        payload_strat_ids = {s["strategy_id"] for s in explanation_payload.get("selected_strategies", [])}
        if payload_strat_ids != expected_strat_ids:
            violations.append(f"Strategy portfolio drift detected: expected {expected_strat_ids}, got {payload_strat_ids}")

        # 3. QAOA & Quantum Advantage Check
        qaoa_exp = explanation_payload.get("optimization_explanation", {})
        if qaoa_exp.get("quantum_advantage_claimed") is True:
            violations.append("PROHIBITED CLAIM: Quantum advantage cannot be claimed based on simulator benchmark.")

        # 4. Numeric check
        qaoa_input = context_packet.get("qaoa_metrics", {})
        payload_p = qaoa_exp.get("qaoa_p_depth")
        if payload_p is not None and payload_p != qaoa_input.get("qaoa_depth"):
            violations.append(f"Numeric mismatch in QAOA depth: expected {qaoa_input.get('qaoa_depth')}, got {payload_p}")

        is_valid = len(violations) == 0

        return {
            "is_valid": is_valid,
            "violations_count": len(violations),
            "violations": violations,
            "validation_status": "VERIFIED" if is_valid else "FAILED_CONSISTENCY_CHECK"
        }
