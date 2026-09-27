# Phase F — 20 Exposure Test Matrix

**Timestamp**: 2026-09-22T17:42:00+05:30

## Automated Test Matrix Summary

| Test ID | Test Category | Description | Command / Location | Result |
|---|---|---|---|---|
| T-F-001 | Spatial Integrity | 38/38 canonical TN districts present in DB | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-F-002 | Spatial PIP | Point-in-Polygon lookup for Chennai coordinates | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-F-003 | Spatial Out of Scope | PIP returns OUT_OF_SCOPE for points outside TN | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-F-004 | Lineage Traceability | Dataset to Source provenance & checksum checks | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-F-005 | Population Exposure | District population & built environment profile | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-F-006 | Risk-Exposure Contract | RiskExposureProfile structure & mismatch flag | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-F-007 | Orphan Protection | Zero orphan exposure records in PostGIS DB | `pytest tests/test_phase_f_exposure.py` | **PASSED** |
| T-D-001..6 | Phase D Contracts | Master registry & schema contracts | `pytest tests/test_phase_d_contracts.py` | **PASSED (6/6)** |
| T-E-001..28 | Phase E Suite | Master integration & ML risk pipeline flow | `python scripts/run_all_tests.py` | **PASSED (28/28)** |
