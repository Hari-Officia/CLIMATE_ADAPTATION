# Enterprise Claim-to-Evidence Matrix

This document provides a systematic audit of all claims associated with the **Quantum Multi-Agent Decision Support System for Climate Adaptation** (Tamil Nadu — 38 Districts).

---

## Claim Classification Legend

- `VALIDATED`: Supported by empirical test execution, mathematical proof, or statutory evidence.
- `CONDITIONALLY_VALIDATED`: Supported under explicitly documented staging or environment constraints.
- `PROHIBITED`: Explicitly disallowed to prevent scientific exaggeration or false representation.
- `NOT_ESTABLISHED`: Under active experimental evaluation but currently unproven.

---

## Claims Audit Matrix

| Claim ID | Claim Statement | Claim Type | Target Scope | Audit Status | Supporting Evidence / Source Test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLM-001** | Multi-hazard risk prediction across Flood, Drought, and Heatwave | System Scope | 38 TN Districts | `VALIDATED` | `tests/test_multi_hazards.py`, XGBoost models |
| **CLM-002** | 100% deterministic decision reproducibility | Reproducibility | 38 TN Districts | `VALIDATED` | `scripts/verify_decision_reproducibility.py` |
| **CLM-003** | Complete 19-node version graph decision context hashing | Provenance | System Architecture | `VALIDATED` | `POL-PROV-001`, `backend/services/orchestration/` |
| **CLM-004** | MILP and QUBO mathematical parity ($P=10.0$) | Mathematical Parity | Optimization | `VALIDATED` | `tests/test_phase_l_qubo.py` |
| **CLM-005** | Quantum Advantage established | Quantum Advantage | Optimization | `PROHIBITED` | Experimental QAOA Gap = 0.4700 (`NOT_ESTABLISHED`) |
| **CLM-006** | Quantum Superiority over classical solvers | Quantum Advantage | Optimization | `PROHIBITED` | MILP solver remains classical benchmark |
| **CLM-007** | Zero Hallucination guarantee | LLM Explanation | RAG / LLM | `PROHIBITED` | Grounded context filtering reduces but cannot guarantee 0% LLM failure |
| **CLM-008** | High Availability / Multi-Node Fault Tolerance | Infrastructure | Database / API | `PROHIBITED` | Staging runs on single-node PostgreSQL (`CONDITIONALLY_CERTIFIED`) |
| **CLM-009** | 0 Hardcoded Secrets | Security | Repository | `VALIDATED` | `scripts/scan_secrets.py`, `POL-SEC-001` |
| **CLM-010** | RPO < 24h & RTO < 1h compliance | Disaster Recovery | Database | `VALIDATED` | `scripts/backup_db.py`, `scripts/restore_db.py` |
| **CLM-011** | Presentation-only Frontend with Python Scientific Authority | Architecture | UI / Backend | `VALIDATED` | `tests/test_phase_p_ui.py` |
| **CLM-012** | Coastal surge downscaling accuracy within $\pm 12\%$ | Scientific Uncertainty | 13 Coastal Districts | `VALIDATED` | Hydrodynamic downscaling validation study |
| **CLM-013** | Ground-truth climate outcome labels available immediately | Model Retraining | Retraining Policy | `PROHIBITED` | Outcome labels delayed 1–3 years |
| **CLM-014** | Zero Silent Defaults for missing spatial data | Data Quality | 38 TN Districts | `VALIDATED` | `tests/test_no_silent_zero.py`, `POL-DATA-001` |

---

## Prohibited Claims Verification Log

The repository scanner (`scripts/recertification/verify_claims.py`) enforces strict exclusion of prohibited claims across all documentation, API responses, and LLM explanations:

- `quantum advantage` $\rightarrow$ **FLAGGED / PROHIBITED**
- `quantum superiority` $\rightarrow$ **FLAGGED / PROHIBITED**
- `zero hallucination` $\rightarrow$ **FLAGGED / PROHIBITED**
- `high availability` $\rightarrow$ **FLAGGED / PROHIBITED**
- `fault tolerant` $\rightarrow$ **FLAGGED / PROHIBITED**
- `100% accurate` $\rightarrow$ **FLAGGED / PROHIBITED**
- `fully autonomous` $\rightarrow$ **FLAGGED / PROHIBITED**
