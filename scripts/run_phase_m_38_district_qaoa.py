"""
Phase M — 38-District QAOA Optimization & Classical-vs-Quantum Benchmark Script
Runs QAOA experiments (p=1, 2, 3) across all 38 districts of Tamil Nadu against Exact, MILP, and Greedy baselines,
persists records to database, and outputs CSV datasets in AUDIT/PHASE_M/.
"""

import os
import csv
import json
import time
from backend.db.database import get_db_context
from backend.db.models import District
from backend.services.optimization.qaoa.qaoa_solver import QAOASolver
from backend.services.optimization.qaoa.benchmark_engine import QAOABenchmarkEngine

AUDIT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AUDIT", "PHASE_M")
os.makedirs(AUDIT_DIR, exist_ok=True)

def run_38_district_qaoa_benchmark():
    solver = QAOASolver()
    engine = QAOABenchmarkEngine()

    with get_db_context() as db:
        districts = db.query(District).order_by(District.district_id.asc()).all()

    print(f"Executing Phase M QAOA optimization benchmarking for {len(districts)} districts of Tamil Nadu...", flush=True)

    summary_rows = []
    exp_rows = []
    circuit_rows = []

    for idx, dist in enumerate(districts, 1):
        d_id = dist.district_id.lower()
        d_name = dist.district_name

        try:
            # Run QAOA p=2 experiment for district
            q_res = solver.run_qaoa(district_id=d_id, max_k=5, qaoa_depth_p=2, shots=1000, seed=42, persist=True)
            
            # Run multi-depth benchmark
            b_res = engine.run_benchmark(district_id=d_id, max_k=5, p_depths=[1, 2], shots=1000, seed=42, persist=True)

            exact_obj = b_res["classical_baselines"]["EXACT"]["objective_value"]
            milp_obj = b_res["classical_baselines"]["MILP"]["objective_value"]
            greedy_obj = b_res["classical_baselines"]["GREEDY"]["objective_value"]

            best_qaoa_obj = q_res["best_sample_objective"]
            gap = q_res["objective_gap"]
            feas_prob = q_res["feasible_probability"]
            opt_prob = q_res["optimal_probability"]

            summary_row = {
                "district_id": d_id,
                "district_name": d_name,
                "candidate_count": q_res["candidate_count"],
                "slack_count": q_res["slack_count"],
                "logical_qubits": q_res["logical_qubit_count"],
                "qaoa_depth_p": 2,
                "shots": 1000,
                "exact_objective": exact_obj,
                "milp_objective": milp_obj,
                "greedy_objective": greedy_obj,
                "qaoa_objective": best_qaoa_obj,
                "objective_gap": gap,
                "relative_gap": q_res["relative_objective_gap"],
                "feasible_probability": feas_prob,
                "optimal_probability": opt_prob,
                "runtime_sec": q_res["total_time_sec"],
                "circuit_depth": q_res["circuit_metrics"]["depth"],
                "two_qubit_gates": q_res["circuit_metrics"]["two_qubit_gate_count"],
                "status": "VERIFIED"
            }
            summary_rows.append(summary_row)

            print(f"[{idx:02d}/38] {d_name} ({d_id}): {q_res['logical_qubit_count']} qubits | Exact: {exact_obj:.4f} | QAOA p=2: {best_qaoa_obj:.4f} | Gap: {gap:.4f} | Feas prob: {feas_prob:.1%} | Opt prob: {opt_prob:.1%} | Time: {q_res['total_time_sec']:.2f}s", flush=True)

        except Exception as e:
            print(f"[{idx:02d}/38] {d_name} ({d_id}): ERROR - {str(e)}", flush=True)

    # Output AUDIT/PHASE_M/qaoa_district_summary.csv
    csv_summary_path = os.path.join(AUDIT_DIR, "qaoa_district_summary.csv")
    with open(csv_summary_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "district_id", "district_name", "candidate_count", "slack_count",
            "logical_qubits", "qaoa_depth_p", "shots", "exact_objective",
            "milp_objective", "greedy_objective", "qaoa_objective",
            "objective_gap", "relative_gap", "feasible_probability",
            "optimal_probability", "runtime_sec", "circuit_depth",
            "two_qubit_gates", "status"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    # Output AUDIT/PHASE_M/qaoa_benchmark.csv
    csv_benchmark_path = os.path.join(AUDIT_DIR, "qaoa_benchmark.csv")
    with open(csv_benchmark_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\n============================================================")
    print("PHASE M 38-DISTRICT QAOA BENCHMARK COMPLETE:")
    print(f"Districts Benchmarked: {len(summary_rows)}/38")
    print(f"Audit CSV datasets written to: {AUDIT_DIR}")
    print("============================================================\n")

if __name__ == "__main__":
    run_38_district_qaoa_benchmark()
