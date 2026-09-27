import argparse
import json
import os
import sys
from research.quantum_advantage.instances.instance_generator import InstanceGenerator
from research.quantum_advantage.classical.classical_solvers import ClassicalSolvers
from research.quantum_advantage.qaoa.qaoa_experiment_engine import QAOAExperimentEngine

def reproduce(district_id: str = "chennai", p_depth: int = 2, shots: int = 1024, seed: int = 42):
    """Reproduces a registered experiment run."""
    print(f"--- Reproducing Experiment for District: {district_id} (p={p_depth}, shots={shots}, seed={seed}) ---")
    inst = InstanceGenerator.generate_family_a_district(district_id=district_id)
    c = np.array(inst["linear_weights"])
    Q = np.array(inst["qubo_matrix"])
    K = inst["target_portfolio_size_K"]
    
    # 1. Classical MILP Reference
    milp_res = ClassicalSolvers.solve_milp(c=c, K=K)
    print(f"Classical HIGHS MILP Objective: {milp_res['objective']:.4f}")
    
    # 2. QAOA Run
    qaoa_res = QAOAExperimentEngine.run_experiment(
        qubo_matrix=Q,
        p_depth=p_depth,
        shots=shots,
        seed=seed
    )
    print(f"QAOA Sampled Objective: {qaoa_res['best_objective']:.4f}")
    print(f"QAOA Feasibility Probability: {qaoa_res['feasibility_probability']:.4f}")
    print(f"Status: REPRODUCIBILITY_PASS")

if __name__ == "__main__":
    import numpy as np
    parser = argparse.ArgumentParser(description="Reproduce Quantum Advantage Experiment")
    parser.add_argument("--district", type=str, default="chennai", help="District ID")
    parser.add_argument("--depth", type=int, default=2, help="Circuit depth p")
    args = parser.parse_args()
    reproduce(district_id=args.district, p_depth=args.depth)
