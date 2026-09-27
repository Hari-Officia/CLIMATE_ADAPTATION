# Phase H — Scientific Decision Log

**Timestamp**: 2026-09-22T18:01:10+05:30  
**Scope**: Climate Adaptation Only — Tamil Nadu (38 Districts)

## Methodological Decisions & Rationale

1. **Rejection of Arbitrary Multiplication (`Priority = Risk * Vulnerability * Exposure`)**:
   - *Decision*: Refused to compute unverified multiplicative composite priority scores.
   - *Rationale*: Multiplicative composite scores impose implicit equal-weighting and linear tradeoff assumptions that lack empirical calibration in Tamil Nadu microclimates. Instead, multi-criteria component decomposition with categorical status and deterministic driver extraction was implemented under `MTH-PRIORITY-TN-001`.

2. **Decoupling Priority from Strategy Selection**:
   - *Decision*: Phase H strictly outputs priority profile, horizon, and drivers. Strategy selection, ROI, and QUBO optimization are deferred to Phase I/J/K/L.
   - *Rationale*: Preserves clean modularity. Need (Priority) must precede Strategy applicability and Optimization.

3. **Zero-Tolerance Missing Data Policy**:
   - *Decision*: Missing metrics remain `NULL` with status `UNCERTAIN` or `UNAVAILABLE`.
   - *Rationale*: Automatic zero fill converts missing data into false certainty (e.g. 0 hospitals when data is missing), causing severe governance failures.

4. **Preservation of Known Limitations**:
   - Metric `REV-001` (cool roof microclimate thermal reduction 2–4°C) remains marked as `REQUIRES_REVIEW` (value = `NULL`).
   - Micro-contour tertiary drain elevation data remains marked as `KNOWN_DATA_GAP`.
