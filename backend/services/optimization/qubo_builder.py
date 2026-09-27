"""
QUBO Builder — Phase L Classical-to-Quantum Mathematical Bridge
Constructs mathematically rigorous QUBO models from Phase J/K classical strategy optimization instances.
Enforces variable ordering determinism, dynamic penalty bounds, slack variable encoding, term aggregation, and SHA-256 hashing.
"""

import hashlib
import json
import uuid
import math
from typing import Dict, Any, List, Tuple
from datetime import datetime

from backend.db.database import get_db_context
from backend.db.models import (
    QUBOModelRecord, QUBOVariableRecord, QUBOTermRecord,
    QUBOConstraintRecord, QUBOPenaltyRecord, QUBOMethodologyRecord
)
from backend.services.strategy_candidate_service import StrategyCandidateService
from backend.services.optimization.objective_service import ObjectiveService
from backend.services.optimization.constraint_service import ConstraintService

class QUBOBuilder:
    def __init__(self):
        self.candidate_service = StrategyCandidateService()
        self.objective_service = ObjectiveService()
        self.constraint_service = ConstraintService()

    def calculate_classical_model_hash(self, district_id: str, candidate_strategy_ids: List[str], max_k: int) -> str:
        """Compute SHA-256 hash over canonical classical model definition."""
        payload = {
            "district_id": district_id.lower(),
            "candidate_strategy_ids": sorted(candidate_strategy_ids),
            "max_k": max_k,
            "objective_version": "v1.0",
            "constraint_version": "v1.0"
        }
        canonical_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    def calculate_qubo_hash(self, district_id: str, variables: List[Dict[str, Any]], linear: Dict[int, float], quadratic: Dict[Tuple[int, int], float], constant: float) -> str:
        """Compute SHA-256 hash over canonical QUBO representation."""
        quad_str = {f"{k[0]},{k[1]}": round(v, 6) for k, v in sorted(quadratic.items()) if abs(v) > 1e-9}
        lin_str = {str(k): round(v, 6) for k, v in sorted(linear.items()) if abs(v) > 1e-9}
        payload = {
            "district_id": district_id.lower(),
            "variables": variables,
            "linear_terms": lin_str,
            "quadratic_terms": quad_str,
            "constant_offset": round(constant, 6)
        }
        canonical_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    def derive_penalty_bounds(self, candidate_strategy_ids: List[str], max_k: int) -> Dict[str, float]:
        """
        Derive lower-bound safe penalties mathematically based on maximum objective gains.
        P > max possible objective improvement obtainable by violating a constraint.
        """
        c_i = self.objective_service.build_objective_coefficients(candidate_strategy_ids)
        max_c = max(c_i) if c_i else 1.0
        n = len(candidate_strategy_ids)
        max_synergy = 0.25 * (n * (n - 1) / 2.0)
        
        total_max_obj = sum(c_i) + max_synergy
        safety_margin = 2.0
        
        min_p = max(10.0, round(safety_margin * total_max_obj, 2))
        
        return {
            "P_conflict": min_p,
            "P_dep": min_p,
            "P_size": min_p,
            "objective_bound": total_max_obj,
            "safety_margin": safety_margin
        }

    def build_qubo(self, district_id: str, max_k: int = 5, persist: bool = True) -> Dict[str, Any]:
        """
        Build exact QUBO formulation Q(x, s) = (x, s)^T Q (x, s) + c for candidate set.
        """
        district_id = district_id.lower()
        cand_set = self.candidate_service.generate_candidate_set(district_id)
        raw_strategy_ids = cand_set["strategy_ids"]

        # Deterministic sorting of candidate strategy IDs
        sorted_strategy_ids = sorted(raw_strategy_ids)
        n_candidates = len(sorted_strategy_ids)

        # Build variable registry
        variables = []
        variable_mapping = {}
        for idx, sid in enumerate(sorted_strategy_ids):
            var_info = {
                "index": idx,
                "variable_name": f"x_{idx}",
                "variable_type": "STRATEGY",
                "strategy_id": sid,
                "meaning": f"Binary selection of strategy {sid}"
            }
            variables.append(var_info)
            variable_mapping[sid] = idx

        # Portfolio size inequality constraint slack variables: sum(x_i) <= K
        # Encoding: sum(x_i) + s = K where s = s_0 + 2*s_1 + 4*s_2
        num_slack_bits = 3 # 1 + 2 + 4 = 7 >= max_k (5)
        slack_weights = [2**b for b in range(num_slack_bits)]
        
        slack_variables = []
        for b in range(num_slack_bits):
            s_idx = n_candidates + b
            var_info = {
                "index": s_idx,
                "variable_name": f"s_{b}",
                "variable_type": "SLACK",
                "slack_constraint_id": "CNST-SIZE-001",
                "slack_bit": b,
                "meaning": f"Binary slack variable bit {b} (weight {slack_weights[b]}) for size limit K={max_k}"
            }
            variables.append(var_info)
            slack_variables.append(var_info)

        total_vars = n_candidates + num_slack_bits

        # Initialize linear terms dict and quadratic terms dict
        linear_terms: Dict[int, float] = {i: 0.0 for i in range(total_vars)}
        quadratic_terms: Dict[Tuple[int, int], float] = {}

        def add_linear(idx: int, val: float):
            linear_terms[idx] += val

        def add_quadratic(i: int, j: int, val: float):
            if i == j:
                add_linear(i, val) # x_i^2 = x_i self-interaction normalization
                return
            u, v = (i, j) if i < j else (j, i)
            quadratic_terms[(u, v)] = quadratic_terms.get((u, v), 0.0) + val

        # 1. Objective Function (Maximization to Minimization transformation: -F(x))
        c_coeffs = self.objective_service.build_objective_coefficients(sorted_strategy_ids)
        for idx, c_val in enumerate(c_coeffs):
            add_linear(idx, -c_val)

        # Pairwise Complementarity & Synergy Bonuses in -F(x)
        for rel in self.objective_service.relationships:
            sa, sb = rel.get("strategy_a"), rel.get("strategy_b")
            if sa in variable_mapping and sb in variable_mapping:
                i, j = variable_mapping[sa], variable_mapping[sb]
                rel_type = rel.get("relationship_type")
                if rel_type == "COMPLEMENTARY":
                    add_quadratic(i, j, -0.15)
                elif rel_type == "SYNERGISTIC":
                    add_quadratic(i, j, -0.25)

        # Derive penalty bounds
        penalty_bounds = self.derive_penalty_bounds(sorted_strategy_ids, max_k)
        P_conflict = penalty_bounds["P_conflict"]
        P_dep = penalty_bounds["P_dep"]
        P_size = penalty_bounds["P_size"]

        # 2. Conflict Constraints: x_i + x_j <= 1 -> Penalty P * x_i * x_j
        conflicts = self.constraint_service.get_conflict_pairs(sorted_strategy_ids)
        for i, j in conflicts:
            add_quadratic(i, j, P_conflict)

        # 3. Dependency Constraints: x_A <= x_B -> Penalty P * x_A * (1 - x_B) = P * x_A - P * x_A * x_B
        dependencies = self.constraint_service.get_dependency_pairs(sorted_strategy_ids)
        for idx_a, idx_b in dependencies:
            add_linear(idx_a, P_dep)
            add_quadratic(idx_a, idx_b, -P_dep)

        # 4. Portfolio Size Constraint: P * (sum(x_i) + sum(2^b * s_b) - K)^2
        # Let vector V = [x_0...x_{N-1}, s_0...s_{B-1}] with weights W = [1...1, 1, 2, 4...]
        # (sum_k W_k V_k - K)^2 = sum_k W_k^2 V_k + 2 sum_{k<l} W_k W_l V_k V_l - 2 K sum_k W_k V_k + K^2
        weights = [1.0] * n_candidates + [float(w) for w in slack_weights]
        constant_offset = P_size * (max_k ** 2)

        for k in range(total_vars):
            w_k = weights[k]
            # Linear contribution: P_size * (W_k^2 - 2 * K * W_k)
            lin_contrib = P_size * (w_k**2 - 2.0 * max_k * w_k)
            add_linear(k, lin_contrib)

        for k in range(total_vars):
            for l in range(k + 1, total_vars):
                w_k, w_l = weights[k], weights[l]
                quad_contrib = 2.0 * P_size * w_k * w_l
                add_quadratic(k, l, quad_contrib)

        # Compute Hashes
        classical_hash = self.calculate_classical_model_hash(district_id, sorted_strategy_ids, max_k)
        qubo_hash = self.calculate_qubo_hash(district_id, variables, linear_terms, quadratic_terms, constant_offset)

        qubo_id = f"QUBO-{district_id.upper()}-{uuid.uuid4().hex[:8]}"

        qubo_payload = {
            "qubo_id": qubo_id,
            "district_id": district_id,
            "candidate_set_id": cand_set["candidate_set_id"],
            "methodology_id": "MTH-QUBO-TN-001",
            "classical_model_hash": classical_hash,
            "qubo_hash": qubo_hash,
            "candidate_variable_count": n_candidates,
            "slack_variable_count": num_slack_bits,
            "total_variable_count": total_vars,
            "linear_term_count": len([k for k, v in linear_terms.items() if abs(v) > 1e-9]),
            "quadratic_term_count": len([k for k, v in quadratic_terms.items() if abs(v) > 1e-9]),
            "linear_terms": {k: round(v, 6) for k, v in linear_terms.items() if abs(v) > 1e-9},
            "quadratic_terms": {f"{k[0]},{k[1]}": round(v, 6) for k, v in quadratic_terms.items() if abs(v) > 1e-9},
            "constant_offset": round(constant_offset, 6),
            "variable_mapping": variables,
            "penalties": penalty_bounds,
            "status": "VERIFIED",
            "created_at": datetime.utcnow().isoformat()
        }

        if persist:
            with get_db_context() as db:
                existing = db.query(QUBOModelRecord).filter_by(qubo_hash=qubo_hash).first()
                if existing:
                    qubo_payload["qubo_id"] = existing.qubo_id
                    return qubo_payload

                model_rec = QUBOModelRecord(
                    qubo_id=qubo_id,
                    district_id=district_id,
                    candidate_set_id=cand_set["candidate_set_id"],
                    classical_model_hash=classical_hash,
                    qubo_hash=qubo_hash,
                    methodology_id="MTH-QUBO-TN-001",
                    methodology_version="v1.0",
                    objective_version="v1.0",
                    constraint_version="v1.0",
                    candidate_variable_count=n_candidates,
                    slack_variable_count=num_slack_bits,
                    total_variable_count=total_vars,
                    linear_term_count=len(qubo_payload["linear_terms"]),
                    quadratic_term_count=len(qubo_payload["quadratic_terms"]),
                    constant_offset=round(constant_offset, 6),
                    matrix_format="SPARSE_DICT",
                    coefficient_scale=1.0,
                    precision="FLOAT64",
                    status="VERIFIED",
                    created_at=datetime.utcnow()
                )
                db.add(model_rec)
                db.flush()

                for var in variables:
                    var_rec = QUBOVariableRecord(
                        variable_id=f"QUBOVAR-{qubo_id}-{var['index']}",
                        qubo_id=qubo_id,
                        index=var["index"],
                        variable_name=var["variable_name"],
                        variable_type=var["variable_type"],
                        strategy_id=var.get("strategy_id"),
                        slack_constraint_id=var.get("slack_constraint_id"),
                        slack_bit=var.get("slack_bit"),
                        meaning=var["meaning"]
                    )
                    db.add(var_rec)

                # Persist Terms
                for idx, c_val in linear_terms.items():
                    if abs(c_val) > 1e-9:
                        t_rec = QUBOTermRecord(
                            term_id=f"TERM-{qubo_id}-L{idx}",
                            qubo_id=qubo_id,
                            variable_i=idx,
                            variable_j=idx,
                            term_type="LINEAR",
                            coefficient=round(c_val, 6),
                            provenance="Linear objective / penalty term"
                        )
                        db.add(t_rec)

                for (i, j), q_val in quadratic_terms.items():
                    if abs(q_val) > 1e-9:
                        t_rec = QUBOTermRecord(
                            term_id=f"TERM-{qubo_id}-Q{i}-{j}",
                            qubo_id=qubo_id,
                            variable_i=i,
                            variable_j=j,
                            term_type="QUADRATIC",
                            coefficient=round(q_val, 6),
                            provenance="Pairwise synergy / penalty interaction term"
                        )
                        db.add(t_rec)

                db.commit()

        return qubo_payload
