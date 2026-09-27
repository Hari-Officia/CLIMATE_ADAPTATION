# BUGGED BENCHMARK RUN ARCHIVEMANIFEST (2026-09-23)

- **Archive Status**: BENCHMARK_REPORTING_ISSUE
- **Archived Date**: 2026-09-23
- **Reason**: Faulty QAOA objective key lookup (`best_sample_objective` vs `best_qaoa_objective`), fallback objective substitution (`4.20`), asymmetric gap clamping (`np.maximum(0.0, ...)`), and hardcoded `optimal_probability = 0.0`.
- **Invalidated Metrics**:
  - `BEST_OBSERVED_GAP = 0.0000` (INVALIDATED)
  - `BEST_OPTIMAL_PROBABILITY = 0.0000` (INVALIDATED)
- **Production Baseline Status**: UNTOUCHED & 100% IMMUTABLE.
