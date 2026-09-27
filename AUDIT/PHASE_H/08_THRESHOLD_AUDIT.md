# Phase H — 08 Threshold Audit Report

**Timestamp**: 2026-09-22T18:03:00+05:30

## Empirical Driver Threshold Policy
- `HIGH_HAZARD_RISK`: Hazard risk probability > 0.5 or status = `HIGH`.
- `HIGH_POPULATION_EXPOSURE`: District population > 2,000,000 resident population.
- `HIGH_CRITICAL_ASSET_EXPOSURE`: Critical asset count >= 1 within hazard area.
- `HIGH_SENSITIVITY`: Urban density category = `HIGH` (impervious surface fraction >= 0.5).

All driver thresholds are documented in `config/master/priority_drivers.json` and enforced deterministically.
