import hashlib
import json
import numpy as np
from typing import Dict, Any, List

class CanonicalModelInstance:
    """
    Canonical Model Instance Abstraction (Phase T):
    - Guarantees that every solver (Exact, MILP, Greedy, SA, QUBOBuilder, QAOA)
      receives the EXACT SAME optimization problem instance.
    - Generates a deterministic SHA-256 instance_hash.
    - Prevents internal re-generation or cross-model coefficient mismatches.
    """

    def __init__(self, district_id: str, K: int = 5, P: float = 10.0):
        self.district_id = district_id.lower()
        self.K = K
        self.P = P
        
        # Load authoritative model from backend QUBOBuilder or deterministic generator
        try:
            from backend.services.optimization.qubo_builder import QUBOBuilder
            qb = QUBOBuilder().build_qubo(district_id=self.district_id, max_k=K, persist=False)
            self.is_fallback = False
            self.instance_type = "DATABASE_REAL_CLIMATE"
        except Exception:
            from research.quantum_advantage.instances.instance_generator import InstanceGenerator
            inst_data = InstanceGenerator.generate_family_a_district(district_id=self.district_id, K=K, P=P)
            qb = {
                "sorted_strategy_ids": [f"STR-{str(i).zfill(3)}" for i in range(1, inst_data["n_variables"] + 1)],
                "linear_weights": inst_data["linear_weights"],
                "qubo_matrix": inst_data["qubo_matrix"],
                "qubo_id": f"QUBO-{self.district_id.upper()}",
                "qubo_hash": inst_data["qubo_hash"]
            }
            self.is_fallback = True
            self.instance_type = "DETERMINISTIC_RESEARCH_FIXTURE"
        
        self.strategy_ids = qb.get("sorted_strategy_ids", [f"STR-{str(i).zfill(3)}" for i in range(1, 15)])
        self.N = len(self.strategy_ids)
        self.linear_weights = np.array(qb.get("linear_weights", [0.35]*self.N), dtype=float)
        self.qubo_matrix = np.array(qb.get("qubo_matrix", np.zeros((self.N, self.N))), dtype=float)
        self.qubo_id = qb["qubo_id"]
        self.qubo_hash = qb["qubo_hash"]
        self.objective_direction = "MAXIMIZATION"
        
        # Deterministic Instance Hash
        payload = {
            "district_id": self.district_id,
            "N": self.N,
            "K": self.K,
            "P": self.P,
            "linear_weights": self.linear_weights.tolist(),
            "qubo_hash": self.qubo_hash
        }
        self.instance_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": f"INST-CANONICAL-{self.district_id.upper()}",
            "district_id": self.district_id,
            "instance_hash": self.instance_hash,
            "qubo_hash": self.qubo_hash,
            "N": self.N,
            "K": self.K,
            "P": self.P,
            "linear_weights": self.linear_weights.tolist(),
            "qubo_matrix": self.qubo_matrix.tolist(),
            "objective_direction": self.objective_direction
        }
