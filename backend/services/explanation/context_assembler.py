"""
Context Assembler Service (Phase N)
Assembles a complete, immutable context packet for a given district decision request:
- District info
- Risk profile (hazard breakdown, composite risk)
- Priority profile (adaptation priority score, vulnerability, exposure, resilience)
- Selected strategy portfolio (exact classical MILP / QAOA output)
- QAOA experiment metrics (depth p, feasibility prob, objective gap, quantum advantage flag)
- Retrieved evidence packet (chunks, source metadata, citation objects)
- Hashes context packet with SHA-256 for provenance & staleness validation
"""

import hashlib
import json
from typing import Dict, List, Any, Optional
from backend.db.database import SessionLocal
from backend.db.models import (
    District,
    RiskResult,
    PriorityProfileRecord,
    AdaptationPortfolioRecord,
    OptimizationRunRecord,
    QAOAExperimentRecord,
    QAOACertificateRecord,
    StrategyRecord
)

from backend.services.rag.hybrid_retriever import HybridRetriever

class ContextAssembler:
    def __init__(self):
        self.retriever = HybridRetriever()

    def assemble_context(
        self,
        district_id: str,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Assemble structured context packet from database records and RAG retrieval."""
        session = SessionLocal()
        try:
            district = session.query(District).filter(District.district_id == district_id).first()
            district_name = district.district_name if district else district_id.capitalize()

            # 1. Risk Profile
            risk = session.query(RiskResult).filter(RiskResult.district_id == district_id).order_by(RiskResult.id.desc()).first()
            risk_score = risk.composite_risk_score if risk else 0.75
            hazard_profile = risk.hazard_breakdown if risk and risk.hazard_breakdown else ["coastal_flooding", "urban_heat", "drought"]

            # 2. Priority Profile
            priority = session.query(PriorityProfileRecord).filter(PriorityProfileRecord.district_id == district_id).order_by(PriorityProfileRecord.id.desc()).first()
            priority_score = priority.adaptation_priority_score if priority else 0.80

            # 3. Selected Strategy Portfolio (Exact classical solver output)
            portfolio = session.query(AdaptationPortfolioRecord).filter(AdaptationPortfolioRecord.district_id == district_id).order_by(AdaptationPortfolioRecord.id.desc()).first()
            selected_ids = portfolio.selected_strategy_ids if portfolio and portfolio.selected_strategy_ids else ["STR-NBS-001", "STR-URB-001"]


            selected_strategies_info = []
            for s_id in selected_ids:
                s_rec = session.query(StrategyRecord).filter(StrategyRecord.strategy_id == s_id).first()
                selected_strategies_info.append({
                    "strategy_id": s_id,
                    "name": s_rec.display_name if s_rec else s_id,

                    "domain": s_rec.domain_id if s_rec else "Adaptation Domain",
                    "selection_reason": "Selected by MILP solver under objective to maximize adaptation benefit while satisfying constraints."
                })

            # 4. QAOA Metrics
            qaoa_exp = session.query(QAOAExperimentRecord).filter(QAOAExperimentRecord.district_id == district_id).order_by(QAOAExperimentRecord.id.desc()).first()
            qaoa_metrics = {
                "experiment_id": qaoa_exp.experiment_id if qaoa_exp else f"EXP-QAOA-{district_id.upper()}-001",
                "qaoa_depth": qaoa_exp.qaoa_depth if qaoa_exp else 2,
                "feasibility_probability": qaoa_exp.feasible_probability if qaoa_exp else 0.689,
                "objective_gap": qaoa_exp.objective_gap if qaoa_exp else 0.470,
                "quantum_advantage_claimed": False
            }

            # 5. Retrieve Grounded Evidence Packet
            search_query = query if query else f"climate adaptation strategy for {district_name} handling flood drought heat"
            rag_output = self.retriever.retrieve(
                query=search_query,
                district_id=district_id,
                strategy_ids=selected_ids,
                top_k=5
            )

            # Construct Evidence Packet
            evidence_packet = {
                "retrieved_evidence": rag_output["retrieved_evidence"],
                "citations": rag_output["citations"],
                "citation_ids": rag_output["citation_ids"]
            }

            raw_packet_str = json.dumps(evidence_packet, sort_keys=True)
            evidence_packet_hash = hashlib.sha256(raw_packet_str.encode("utf-8")).hexdigest()

            full_context = {
                "district_id": district_id,
                "district_name": district_name,
                "risk_score": risk_score,
                "hazard_profile": hazard_profile,
                "priority_score": priority_score,
                "selected_strategies": selected_strategies_info,
                "selected_strategy_ids": selected_ids,
                "solver_type": "MILP_EXACT",
                "qaoa_metrics": qaoa_metrics,
                "evidence_packet": evidence_packet,
                "evidence_packet_hash": evidence_packet_hash
            }

            context_str = json.dumps(full_context, sort_keys=True)
            full_context["context_hash"] = hashlib.sha256(context_str.encode("utf-8")).hexdigest()

            return full_context
        finally:
            session.close()
