"""
Quarterly Review Scope Definitions
Defines the 48 review domains evaluated during periodic quarterly reviews.
"""
REVIEW_DOMAINS = [
    "01_operational_health", "02_scientific_assumptions", "03_data_freshness",
    "04_data_quality", "05_source_provenance", "06_feature_contract",
    "07_label_integrity", "08_leakage_risk", "09_temporal_validation",
    "10_spatial_validation", "11_model_stability", "12_model_drift",
    "13_calibration", "14_threshold_stability", "15_gis_integrity",
    "16_district_coverage", "17_exposure", "18_vulnerability",
    "19_resilience", "20_adaptation_priority", "21_strategy_registry",
    "22_applicability_rules", "23_evidence_registry", "24_knowledge_base",
    "25_rag", "26_llm", "27_classical_optimization", "28_milp",
    "29_exact_solver", "30_qubo", "31_qaoa", "32_provenance",
    "33_reproducibility", "34_security", "35_dependency_vulnerabilities",
    "36_api_contract", "37_frontend_integrity", "38_performance",
    "39_backup", "40_disaster_recovery", "41_observability",
    "42_governance", "43_documentation", "44_scientific_claims",
    "45_research_gaps", "46_non_conformities", "47_corrective_actions",
    "48_rollback_readiness"
]

def get_review_scope():
    return {
        "domain_count": len(REVIEW_DOMAINS),
        "domains": REVIEW_DOMAINS,
        "baseline": "BASE-3.0.0-20260923",
        "release": "3.0.0-certified"
    }
