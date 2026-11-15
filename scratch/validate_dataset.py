import csv
import json
import os
import sys

base_dir = r"c:\Users\haris\OneDrive\Desktop\PROJECT_DATA"

files_to_check = [
    "data/adaptation_strategies.csv",
    "data/strategy_hazards.csv",
    "data/strategy_conditions.csv",
    "data/strategy_district.csv",
    "data/strategy_interactions.csv",
    "data/strategy_optimization.csv",
    "data/sources.csv",
    "data/evidence_claims.csv",
    "database/schema.sql",
    "database/seed_data.sql",
    "config/strategy_schema.json",
    "config/hazard_taxonomy.json",
    "config/applicability_schema.json",
    "config/adaptation_strategy.schema.json",
    "docs/ADAPTATION_DATA_DICTIONARY.md",
    "docs/STRATEGY_RULES.md",
    "docs/SOURCE_PROVENANCE.md",
    "docs/DATASET_QA_REPORT.md"
]

print("=== DATASET INTEGRITY VALIDATION ===")
all_ok = True

for rel_path in files_to_check:
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"[FAIL] Missing file: {rel_path}")
        all_ok = False
    else:
        size = os.path.getsize(full_path)
        print(f"[OK] {rel_path} ({size} bytes)")

# Validate JSON files
json_files = [
    "config/strategy_schema.json",
    "config/hazard_taxonomy.json",
    "config/applicability_schema.json",
    "config/adaptation_strategy.schema.json"
]

for rel_path in json_files:
    full_path = os.path.join(base_dir, rel_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"[JSON OK] {rel_path}")
    except Exception as e:
        print(f"[JSON FAIL] {rel_path}: {e}")
        all_ok = False

# Validate CSV files
csv_files = [
    ("data/adaptation_strategies.csv", "strategy_id"),
    ("data/strategy_hazards.csv", "strategy_id"),
    ("data/strategy_conditions.csv", "condition_id"),
    ("data/strategy_district.csv", "strategy_id"),
    ("data/strategy_interactions.csv", "strategy_a"),
    ("data/strategy_optimization.csv", "strategy_id"),
    ("data/sources.csv", "source_id"),
    ("data/evidence_claims.csv", "claim_id")
]

for rel_path, first_col in csv_files:
    full_path = os.path.join(base_dir, rel_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"[CSV OK] {rel_path}: {len(rows)} rows, columns: {reader.fieldnames[:3]}...")
    except Exception as e:
        print(f"[CSV FAIL] {rel_path}: {e}")
        all_ok = False

if all_ok:
    print("\n>>> ALL DATASET IMPLEMENTATION FILES VERIFIED SUCCESSFULLY <<<")
else:
    print("\n>>> DATASET VERIFICATION FAILED <<<")
