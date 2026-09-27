"""
Constraint Service — Phase J/K Classical Optimization
Builds hard constraint matrices (conflicts x_i + x_j <= 1, dependencies x_A <= x_B, portfolio size sum(x_i) <= K) and validates portfolio feasibility.
"""

import os
import json
from typing import Dict, Any, List, Tuple

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "master")

class ConstraintService:
    def __init__(self):
        self.relationships = self._load_json("strategy_relationships.json")

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        path = os.path.join(CONFIG_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_conflict_pairs(self, candidate_strategy_ids: List[str]) -> List[Tuple[int, int]]:
        """Find index pairs (i, j) of conflicting strategies."""
        cand_set = set(candidate_strategy_ids)
        conflicts = []
        for rel in self.relationships:
            if rel.get("relationship_type") == "CONFLICTING":
                sa = rel["strategy_a"]
                sb = rel["strategy_b"]
                if sa in cand_set and sb in cand_set:
                    i = candidate_strategy_ids.index(sa)
                    j = candidate_strategy_ids.index(sb)
                    conflicts.append((i, j))
        return conflicts

    def get_dependency_pairs(self, candidate_strategy_ids: List[str]) -> List[Tuple[int, int]]:
        """Find index pairs (A, B) where strategy A depends on strategy B (x_A <= x_B)."""
        cand_set = set(candidate_strategy_ids)
        dependencies = []
        for rel in self.relationships:
            if rel.get("relationship_type") == "DEPENDENT":
                sa = rel["strategy_a"] # dependent strategy
                sb = rel["strategy_b"] # prerequisite strategy
                if sa in cand_set and sb in cand_set:
                    idx_a = candidate_strategy_ids.index(sa)
                    idx_b = candidate_strategy_ids.index(sb)
                    dependencies.append((idx_a, idx_b))
        return dependencies

    def validate_portfolio_feasibility(self, selected_strategy_ids: List[str], max_k: int = 5) -> Dict[str, Any]:
        """
        Validate portfolio feasibility against size limits, hard conflicts, and dependencies.
        """
        selected_set = set(selected_strategy_ids)
        violations = []

        # 1. Size constraint
        if len(selected_strategy_ids) > max_k:
            violations.append(f"Portfolio size ({len(selected_strategy_ids)}) exceeds max limit K={max_k}.")

        # 2. Conflict constraints
        for rel in self.relationships:
            if rel.get("relationship_type") == "CONFLICTING":
                sa = rel["strategy_a"]
                sb = rel["strategy_b"]
                if sa in selected_set and sb in selected_set:
                    violations.append(f"Hard conflict violation: Strategy '{sa}' and '{sb}' cannot be co-deployed.")

        # 3. Dependency constraints
        for rel in self.relationships:
            if rel.get("relationship_type") == "DEPENDENT":
                sa = rel["strategy_a"]
                sb = rel["strategy_b"]
                if sa in selected_set and sb not in selected_set:
                    violations.append(f"Dependency violation: Strategy '{sa}' requires prerequisite strategy '{sb}'.")

        feasible = len(violations) == 0
        return {
            "feasible": feasible,
            "violations": violations,
            "selected_count": len(selected_strategy_ids),
            "max_k": max_k
        }
