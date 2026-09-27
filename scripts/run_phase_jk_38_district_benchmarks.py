"""
Script to run Phase J/K classical strategy optimization benchmarks across all 38 districts of Tamil Nadu, generating mandatory CSV and markdown audit matrices under AUDIT/PHASE_JK/
"""

import os
import csv
import json
from datetime import datetime
from backend.services.optimization.optimization_service import OptimizationService

AUDIT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AUDIT", "PHASE_JK")
os.makedirs(AUDIT_DIR, exist_ok=True)

def run_phase_jk_benchmarks():
    opt_service = OptimizationService()

    profiles_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "district_profiles", "tamil_nadu_profiles.json")
    with open(profiles_path, "r", encoding="utf-8") as f:
        district_profiles = json.load(f)

    # 1. Generate CLASSICAL_SOLVER_BENCHMARK.csv
    bm_csv_path = os.path.join(AUDIT_DIR, "CLASSICAL_SOLVER_BENCHMARK.csv")
    with open(bm_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "district_id", "district_name", "candidate_count", "solver_id",
            "objective_value", "runtime_ms", "status", "selected_strategy_count", "timestamp"
        ])

        for dist in district_profiles:
            d_id = dist["district_id"]
            d_name = dist["district_name"]

            comp_res = opt_service.compare_solvers_for_district(d_id, max_k=5)
            cand_cnt = comp_res["candidate_count"]

            for solver_id, sol_res in comp_res["solvers"].items():
                writer.writerow([
                    d_id,
                    d_name,
                    cand_cnt,
                    solver_id,
                    sol_res["objective_value"],
                    sol_res["runtime_ms"],
                    sol_res["status"],
                    len(sol_res["selected_strategy_ids"]),
                    datetime.utcnow().isoformat()
                ])
    print(f"Generated {bm_csv_path}")

    # 2. Generate 38_DISTRICT_OPTIMIZATION_VALIDATION.csv
    val_csv_path = os.path.join(AUDIT_DIR, "38_DISTRICT_OPTIMIZATION_VALIDATION.csv")
    with open(val_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "district_id", "district_name", "coastal", "optimization_run_id",
            "portfolio_id", "selected_strategies", "objective_value", "status"
        ])

        for dist in district_profiles:
            d_id = dist["district_id"]
            d_name = dist["district_name"]
            run_res = opt_service.run_optimization(d_id, solver_id="MILP_HIGHS", max_k=5)
            port = run_res["portfolio"]

            writer.writerow([
                d_id,
                d_name,
                dist.get("coastal", False),
                run_res["optimization_run_id"],
                port["portfolio_id"],
                " | ".join(port["selected_strategy_ids"]),
                port["objective_value"],
                run_res["status"]
            ])
    print(f"Generated {val_csv_path}")

    # 3. Generate RESEARCH_GAPS.csv
    gap_csv_path = os.path.join(AUDIT_DIR, "RESEARCH_GAPS.csv")
    with open(gap_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "gap_id", "category", "description", "impact_on_optimization", "recommended_action", "status"
        ])
        writer.writerow([
            "REV-001", "QUANTITATIVE_EFFICACY", "Cool roof 2-4°C metric requires local field trial verification.",
            "QUALITATIVE_ONLY_BASELINE", "Maintain qualitative review flag without arbitrary numeric efficacy.", "ACTIVE"
        ])
        writer.writerow([
            "GAP-LIDAR-001", "GIS_ELEVATION", "LiDAR micro-elevation data gap for coastal inundation modeling.",
            "SPATIAL_CONSTRAINT_ONLY", "Rely on PostGIS district boundary coastal flags.", "ACTIVE"
        ])
    print(f"Generated {gap_csv_path}")

if __name__ == "__main__":
    run_phase_jk_benchmarks()
