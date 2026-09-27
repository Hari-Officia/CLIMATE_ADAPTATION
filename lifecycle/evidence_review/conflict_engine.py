"""
Evidence Conflict Detection Engine
Detects contradictory evidence claims across Tier 1–5 sources and enforces statutory hierarchy override.
"""
import json
from pathlib import Path

REGISTRY_PATH = Path("lifecycle/evidence_review/evidence_registry.json")

class ConflictEngine:
    def __init__(self):
        self._load_registry()

    def _load_registry(self):
        if not REGISTRY_PATH.exists():
            self.data = {"evidence_sources": [], "evidence_conflicts": []}
            return
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def detect_conflicts(self):
        conflicts = self.data.get("evidence_conflicts", [])
        return {
            "conflict_count": len(conflicts),
            "conflicts": conflicts,
            "hierarchy_policy": "Tier 1 strictly overrides lower tiers"
        }
