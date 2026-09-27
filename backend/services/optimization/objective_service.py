"""
Objective Service — Phase J/K Classical Optimization
Calculates normalized objective coefficients for candidate strategies based on hazard coverage, adaptation priority alignment, evidence strength, and inter-strategy complementarity.
"""

import os
import json
from typing import Dict, Any, List

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "master")

class ObjectiveService:
    def __init__(self):
        self.strategies = self._load_json("strategies.json")
        self.objectives = self._load_json("optimization_objectives.json")
        self.relationships = self._load_json("strategy_relationships.json")

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        path = os.path.join(CONFIG_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def build_objective_coefficients(self, candidate_strategy_ids: List[str], district_context: Dict[str, Any] = None) -> List[float]:
        """
        Build linear objective coefficients c_i for binary decision variables x_i.
        c_i = w_hazard * HazardCoverage + w_priority * PriorityAlignment + w_evidence * EvidenceStrength
        """
        coefficients = []
        for sid in candidate_strategy_ids:
            strat = next((s for s in self.strategies if s["strategy_id"] == sid), None)
            if not strat:
                coefficients.append(0.0)
                continue

            # 1. Hazard Coverage Component (0.0 to 1.0)
            hazard_score = 1.0 if strat.get("primary_hazard_id") in ["HAZ-FLD", "HAZ-HTW", "HAZ-DRG"] else 0.5
            
            # 2. Priority Alignment Component (0.0 to 1.0)
            horizon = strat.get("planning_horizon", "SHORT_TERM")
            priority_score = 1.0 if horizon == "IMMEDIATE" else (0.8 if horizon == "SHORT_TERM" else 0.5)

            # 3. Evidence Strength Component (0.0 to 1.0)
            ev_strength = strat.get("evidence_strength", "STRONG")
            evidence_score = 1.0 if ev_strength == "VERY_STRONG" else (0.8 if ev_strength == "STRONG" else 0.5)

            # Composite weighted linear coefficient
            c_i = round(0.35 * hazard_score + 0.35 * priority_score + 0.30 * evidence_score, 4)
            coefficients.append(c_i)

        return coefficients

    def evaluate_portfolio_objective(self, selected_strategy_ids: List[str], candidate_strategy_ids: List[str]) -> float:
        """
        Evaluate exact portfolio objective value including complementary pair bonuses.
        F(x) = sum(c_i * x_i) + sum(bonus_ij * x_i * x_j)
        """
        coeffs = self.build_objective_coefficients(candidate_strategy_ids)
        total_val = 0.0

        for sid in selected_strategy_ids:
            if sid in candidate_strategy_ids:
                idx = candidate_strategy_ids.index(sid)
                total_val += coeffs[idx]

        # Add complementary/synergistic relationship bonuses
        selected_set = set(selected_strategy_ids)
        for rel in self.relationships:
            sa = rel["strategy_a"]
            sb = rel["strategy_b"]
            if sa in selected_set and sb in selected_set:
                rel_type = rel.get("relationship_type")
                if rel_type == "COMPLEMENTARY":
                    total_val += 0.15
                elif rel_type == "SYNERGISTIC":
                    total_val += 0.25

        return round(total_val, 4)
