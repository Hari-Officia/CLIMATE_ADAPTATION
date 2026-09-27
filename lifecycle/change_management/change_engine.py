"""
Change Management Engine
Manages Class 0 through Class 10 change requests and release promotion gates.
"""
import json
from pathlib import Path

REGISTRY_PATH = Path("lifecycle/change_management/change_registry.json")

class ChangeEngine:
    def __init__(self):
        self._load_registry()

    def _load_registry(self):
        if not REGISTRY_PATH.exists():
            self.data = {"change_requests": []}
            return
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def list_changes(self):
        return self.data.get("change_requests", [])

    def requires_scientific_review(self, classification: str) -> bool:
        # Classes 6 through 10 require scientific review
        class_num = int(classification.split(":")[0].replace("CLASS ", "").strip())
        return class_num >= 6
