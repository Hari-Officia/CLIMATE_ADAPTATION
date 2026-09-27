# Phase H — 07 Weighting Audit Report

**Timestamp**: 2026-09-22T18:02:35+05:30

## Weighting Governance Policy
- **Policy**: Zero undocumented weights.
- **Verification**: No hard-coded weighting multipliers (e.g. `0.4 * risk + 0.3 * exposure`) exist in backend code.
- **Component Contribution**: Components (Risk, Exposure, Vulnerability, Resilience Gap) are evaluated individually and reported transparently in `component_decomposition`.
