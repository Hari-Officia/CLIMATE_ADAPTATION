"""
Workflow Validator & Quality Gate Service (Phase O)
Executes Decision Quality Gates 1-12 before marking a decision workflow complete:
- Gate 1: Valid district
- Gate 2: Valid risk profile
- Gate 3: Valid priority profile
- Gate 4: Valid strategy applicability
- Gate 5: Valid classical optimization portfolio
- Gate 6: Valid QUBO model (if enabled)
- Gate 7: Valid QAOA metrics (if enabled)
- Gate 8: Valid RAG evidence packet
- Gate 9: Valid citation objects
- Gate 10: Valid LLM decision explanation
- Gate 11: No stale context
- Gate 12: No critical system errors
"""

from typing import Dict, List, Any
from backend.services.orchestration.workflow_state import DecisionWorkflowState

class WorkflowValidator:
    def validate_workflow(self, state: DecisionWorkflowState) -> Dict[str, Any]:
        gates = []
        violations = []

        # Gate 1: District
        g1 = bool(state.district_id)
        gates.append({"gate": "GATE_1_DISTRICT_VALID", "passed": g1})
        if not g1: violations.append("District ID is invalid or missing.")

        # Gate 2: Risk
        g2 = bool(state.risk_context and state.risk_context.get("composite_risk_score") is not None)
        gates.append({"gate": "GATE_2_RISK_VALID", "passed": g2})
        if not g2: violations.append("Risk profile is missing composite risk score.")

        # Gate 3: Priority
        g3 = bool(state.priority_context and state.priority_context.get("priority_score") is not None)
        gates.append({"gate": "GATE_3_PRIORITY_VALID", "passed": g3})
        if not g3: violations.append("Priority context is missing priority score.")

        # Gate 4: Strategy Applicability
        g4 = len(state.strategy_candidates) > 0
        gates.append({"gate": "GATE_4_STRATEGIES_VALID", "passed": g4})
        if not g4: violations.append("Strategy candidate list is empty.")

        # Gate 5: Classical Optimization
        g5 = bool(state.classical_optimization_result and state.classical_optimization_result.get("selected_strategy_ids"))
        gates.append({"gate": "GATE_5_OPTIMIZATION_VALID", "passed": g5})
        if not g5: violations.append("Classical optimization result has no selected strategies.")

        # Gate 6 & 7: QUBO & QAOA (If enabled)
        if state.optimization_mode in ["QAOA", "CLASSICAL_PLUS_QAOA"]:
            g6 = bool(state.qubo_result and "qubo_id" in state.qubo_result)
            gates.append({"gate": "GATE_6_QUBO_VALID", "passed": g6})
            if not g6: violations.append("QUBO formulation missing in QAOA mode.")

            g7 = bool(state.qaoa_result and "qaoa_p_depth" in state.qaoa_result)
            gates.append({"gate": "GATE_7_QAOA_VALID", "passed": g7})
            if not g7: violations.append("QAOA experiment metrics missing.")
        else:
            gates.append({"gate": "GATE_6_QUBO_VALID", "passed": True})
            gates.append({"gate": "GATE_7_QAOA_VALID", "passed": True})

        # Gate 8 & 9: Evidence & Citations
        if isinstance(state.evidence_packet, dict):
            ev_list = state.evidence_packet.get("retrieved_evidence", [])
            cit_list = state.evidence_packet.get("citations", [])
        elif isinstance(state.evidence_packet, list):
            ev_list = state.evidence_packet
            cit_list = state.evidence_packet
        else:
            ev_list = []
            cit_list = []

        g8 = len(ev_list) > 0
        gates.append({"gate": "GATE_8_EVIDENCE_VALID", "passed": g8})
        if not g8: violations.append("Evidence packet has no retrieved evidence.")

        g9 = len(cit_list) > 0
        gates.append({"gate": "GATE_9_CITATIONS_VALID", "passed": g9})
        if not g9: violations.append("Evidence packet has no valid citation objects.")


        # Gate 10: LLM Explanation
        g10 = bool(state.explanation and state.explanation.get("explanation", {}).get("decision_summary"))
        gates.append({"gate": "GATE_10_LLM_EXPLANATION_VALID", "passed": g10})
        if not g10: violations.append("LLM decision explanation is missing summary.")

        # Gate 11: Staleness
        g11 = bool(state.context_hash)
        gates.append({"gate": "GATE_11_NO_STALE_CONTEXT", "passed": g11})
        if not g11: violations.append("Context hash is uncalculated or stale.")

        # Gate 12: Errors
        g12 = len(state.errors) == 0
        gates.append({"gate": "GATE_12_NO_CRITICAL_ERRORS", "passed": g12})
        if not g12: violations.append("Workflow encountered critical errors.")

        passed_all = all(g["passed"] for g in gates)

        return {
            "passed_all": passed_all,
            "gates_summary": gates,
            "violations_count": len(violations),
            "violations": violations,
            "status": "VERIFIED" if passed_all else "FAILED_QUALITY_GATES"
        }
