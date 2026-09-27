"""
Phase L — 38-District QUBO Validation & Audit Script
Builds QUBO models, performs exhaustive 2^(N+B) equivalence verification against Phase J/K classical ground truth,
persists immutable certificates to database, and outputs AUDIT/PHASE_L/38_DISTRICT_QUBO_VALIDATION.csv and EXACT_QUBO_VALIDATION.csv.
"""

import os
import csv
import json
import time
from backend.db.database import get_db_context
from backend.db.models import District
from backend.services.optimization.qubo_builder import QUBOBuilder
from backend.services.optimization.qubo_equivalence_validator import QUBOEquivalenceValidator

AUDIT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AUDIT", "PHASE_L")
os.makedirs(AUDIT_DIR, exist_ok=True)

def run_38_district_qubo_audit():
    builder = QUBOBuilder()
    validator = QUBOEquivalenceValidator()

    with get_db_context() as db:
        districts = db.query(District).order_by(District.district_id.asc()).all()

    print(f"Processing QUBO formulation & equivalence verification for {len(districts)} districts of Tamil Nadu...")

    csv_38_path = os.path.join(AUDIT_DIR, "38_DISTRICT_QUBO_VALIDATION.csv")
    csv_exact_path = os.path.join(AUDIT_DIR, "EXACT_QUBO_VALIDATION.csv")

    rows_38 = []
    rows_exact = []

    verified_count = 0
    total_states_evaluated = 0

    for idx, dist in enumerate(districts, 1):
        d_id = dist.district_id.lower()
        d_name = dist.district_name

        try:
            val_res = validator.validate_qubo_equivalence(d_id, max_k=5, persist=True)
            cert = val_res["certificate"]
            best = val_res["best_qubo_decoded"]
            qubo_model = builder.build_qubo(d_id, max_k=5, persist=True)

            status = cert["status"]
            if status == "VERIFIED":
                verified_count += 1

            total_states_evaluated += cert["tested_state_count"]

            row_38 = {
                "district_id": d_id,
                "district_name": d_name,
                "candidate_set_id": qubo_model["candidate_set_id"],
                "qubo_id": cert["qubo_id"],
                "candidate_variables": qubo_model["candidate_variable_count"],
                "slack_variables": qubo_model["slack_variable_count"],
                "total_variables": cert["variable_count"],
                "linear_terms": qubo_model["linear_term_count"],
                "quadratic_terms": qubo_model["quadratic_term_count"],
                "qubo_hash": cert["qubo_hash"],
                "classical_model_hash": cert["classical_model_hash"],
                "equivalence_status": cert["status"],
                "status": "VERIFIED" if status == "VERIFIED" else "FAILED"
            }
            rows_38.append(row_38)

            row_exact = {
                "district_id": d_id,
                "district_name": d_name,
                "candidate_count": qubo_model["candidate_variable_count"],
                "slack_count": qubo_model["slack_variable_count"],
                "total_binary_variables": cert["variable_count"],
                "tested_state_count": cert["tested_state_count"],
                "classical_optimum": cert["classical_optimum"],
                "qubo_optimum": cert["qubo_optimum"],
                "decoded_objective": cert["decoded_objective"],
                "objective_difference": cert["objective_difference"],
                "feasibility": cert["feasibility_match"],
                "optimality": cert["optimality_match"],
                "status": cert["status"]
            }
            rows_exact.append(row_exact)

            print(f"[{idx:02d}/38] {d_name} ({d_id}): {cert['variable_count']} vars | {cert['tested_state_count']} states | Classical opt: {cert['classical_optimum']:.4f} | Decoded obj: {cert['decoded_objective']:.4f} | Status: {cert['status']}", flush=True)

        except Exception as e:
            print(f"[{idx:02d}/38] {d_name} ({d_id}): ERROR - {str(e)}", flush=True)

    # Write 38_DISTRICT_QUBO_VALIDATION.csv
    with open(csv_38_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "district_id", "district_name", "candidate_set_id", "qubo_id",
            "candidate_variables", "slack_variables", "total_variables",
            "linear_terms", "quadratic_terms", "qubo_hash", "classical_model_hash",
            "equivalence_status", "status"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_38)

    # Write EXACT_QUBO_VALIDATION.csv
    with open(csv_exact_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "district_id", "district_name", "candidate_count", "slack_count",
            "total_binary_variables", "tested_state_count", "classical_optimum",
            "qubo_optimum", "decoded_objective", "objective_difference",
            "feasibility", "optimality", "status"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_exact)

    print("\n============================================================")
    print(f"38-DISTRICT QUBO VERIFICATION COMPLETE:")
    print(f"Districts Processed: {len(districts)}")
    print(f"Districts VERIFIED: {verified_count}/{len(districts)}")
    print(f"Total Binary States Evaluated: {total_states_evaluated:,}")
    print(f"Audit files generated in: {AUDIT_DIR}")
    print("============================================================\n")

if __name__ == "__main__":
    run_38_district_qubo_audit()
