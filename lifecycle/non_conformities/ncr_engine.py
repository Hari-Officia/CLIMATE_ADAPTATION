"""
Non-Conformity Management Engine
Provides methods for querying, logging, and triaging non-conformity records.
"""
import json
from pathlib import Path

REGISTRY_PATH = Path("lifecycle/non_conformities/registry.json")

class NCREngine:
    def __init__(self):
        self._load_registry()

    def _load_registry(self):
        if not REGISTRY_PATH.exists():
            self.data = {"version": "1.0.0", "non_conformities": []}
            return
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def list_ncr(self):
        return self.data.get("non_conformities", [])

    def get_ncr(self, nc_id: str):
        for nc in self.list_ncr():
            if nc.get("nc_id") == nc_id:
                return nc
        return None

    def get_accepted_risks(self):
        return [nc for nc in self.list_ncr() if nc.get("status") == "ACCEPTED_RISK"]

    def get_blocking_ncr(self):
        return [nc for nc in self.list_ncr() if nc.get("severity") in ["CRITICAL", "HIGH"] and nc.get("status") not in ["CLOSED", "ACCEPTED_RISK"]]
