import os
import json
import csv

ROOT_DIR = r"c:\Users\haris\OneDrive\Desktop\PROJECT_DATA"

# Load V2 Strategies
with open(os.path.join(ROOT_DIR, "config", "master", "strategies_v2.0_expanded.json"), "r", encoding="utf-8") as f:
    V2_STRATEGIES = json.load(f)
V2_MAP = {s["strategy_id"]: s for s in V2_STRATEGIES}

# Load District Profiles to find coastal flag
with open(os.path.join(ROOT_DIR, "data", "geojson", "tamil_nadu_districts.geojson"), "r", encoding="utf-8") as f:
    GEOJSON = json.load(f)

# Load MILP portfolios
with open(os.path.join(ROOT_DIR, "phase4_v2_selected_portfolios.csv"), "r", encoding="utf-8") as f:
    MILP_PORTFOLIOS = list(csv.DictReader(f))

# Load QAOA portfolios
with open(os.path.join(ROOT_DIR, "phase6_v2_phase7_handoff_contract.json"), "r", encoding="utf-8") as f:
    QAOA_HANDOFF = json.load(f)

print("--- AUDIT 1: STR-EWS-002 & COASTAL STRATEGY DISTRIBUTION ---")

coastal_dids = set()
for feat in GEOJSON["features"]:
    props = feat["properties"]
    if props.get("coastal") is True or props.get("district_id") in ['chennai','chengalpattu','cuddalore','kanniyakumari','mayiladuthurai','nagapattinam','pudukkottai','ramanathapuram','thanjavur','thoothukudi','tirunelveli','tiruvallur','viluppuram']:
        coastal_dids.add(props["district_id"])

print(f"Identified {len(coastal_dids)} coastal districts and {38 - len(coastal_dids)} inland districts.")

cst_dependent_ids = {'STR-CST-001', 'STR-CST-002', 'STR-CST-003', 'STR-CST-004', 'STR-CST-005'}

inland_with_cst_milp = []
inland_with_cst_qaoa = []
inland_with_ews2_milp = []
inland_with_ews2_qaoa = []

for r in MILP_PORTFOLIOS:
    did = r["district_id"]
    sids_milp = set(json.loads(r["selected_strategy_ids"]))
    sids_qaoa = set(QAOA_HANDOFF[did]["qaoa_results"]["best_feasible_portfolio"])

    is_coastal = did in coastal_dids

    cst_milp = cst_dependent_ids & sids_milp
    cst_qaoa = cst_dependent_ids & sids_qaoa

    if not is_coastal and cst_milp:
        inland_with_cst_milp.append((did, list(cst_milp)))
    if not is_coastal and cst_qaoa:
        inland_with_cst_qaoa.append((did, list(cst_qaoa)))

    if not is_coastal and "STR-EWS-002" in sids_milp:
        inland_with_ews2_milp.append(did)
    if not is_coastal and "STR-EWS-002" in sids_qaoa:
        inland_with_ews2_qaoa.append(did)

print(f"\nInland districts with coastal-dependent strategies (STR-CST-001..005) in MILP: {inland_with_cst_milp}")
print(f"Inland districts with coastal-dependent strategies (STR-CST-001..005) in QAOA: {inland_with_cst_qaoa}")

print(f"\nInland districts with STR-EWS-002 in MILP: {len(inland_with_ews2_milp)} districts -> {inland_with_ews2_milp}")
print(f"Inland districts with STR-EWS-002 in QAOA: {len(inland_with_ews2_qaoa)} districts -> {inland_with_ews2_qaoa}")

print("\nSTR-EWS-002 Metadata:")
ews2 = V2_MAP["STR-EWS-002"]
print(f"  ID: {ews2['strategy_id']}")
print(f"  Canonical Name: {ews2['canonical_name']}")
print(f"  Display Name: {ews2['display_name']}")
print(f"  Domain Name: {ews2['domain_name']}")
print(f"  Measure Type: {ews2['measure_type']}")
print(f"  Primary Hazard: {ews2['primary_hazard_id']}")
print(f"  Sectors: {ews2['sector_ids']}")

print("\n--- AUDIT 2: QAOA p VALUE ---")
# Check QAOA circuit builder / solver & certified reports for p value
qaoa_v2_report_path = os.path.join(ROOT_DIR, "PHASE_6_V2_QAOA_RE_CERTIFICATION_REPORT.md")
if os.path.exists(qaoa_v2_report_path):
    with open(qaoa_v2_report_path, "r", encoding="utf-8") as f:
        content = f.read()
        for line in content.splitlines():
            if "p=" in line.lower() or "circuit" in line.lower() or "ansatz" in line.lower() or "depth" in line.lower():
                print("  [Report Line]:", line)

print("\n--- AUDIT 3: STRATEGY REGISTRY COUNT ---")
with open(os.path.join(ROOT_DIR, "config", "master", "strategies_v2.0_expanded.json"), "r", encoding="utf-8") as f:
    master_strats = json.load(f)
print(f"Master V2 Strategies Count: {len(master_strats)}")

v1_strats_path = os.path.join(ROOT_DIR, "config", "master", "strategies_v1.0_certified.json")
if os.path.exists(v1_strats_path):
    with open(v1_strats_path, "r", encoding="utf-8") as f:
        v1_strats = json.load(f)
    print(f"Master V1 Strategies Count: {len(v1_strats)}")

# Check backend strategies endpoint response
import urllib.request
try:
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/strategies")
    api_strats = json.loads(res.read())
    print(f"Backend API /api/v1/strategies Count: {len(api_strats)}")
except Exception as e:
    print(f"Backend API call failed: {e}")
