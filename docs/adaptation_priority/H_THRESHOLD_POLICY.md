# Phase H Documentation — Priority Horizon Threshold Policy

## 1. Decision Cutoffs & Priority Horizons
Priority horizons categorize the urgency of adaptation intervention required for a district.

| Priority Horizon | Condition Criteria |
|:---|:---|
| `IMMEDIATE` | Hazard Probability > 0.5 **AND** (Exposed Population > 2M **OR** Critical Assets >= 1) |
| `SHORT_TERM` | Hazard Probability > 0.4 **OR** Urban Density = `HIGH` |
| `MEDIUM_TERM` | Hazard Probability > 0.2 **OR** Exposed Population > 1M |
| `LONG_TERM` | Default baseline for low hazard probability and moderate exposure |

## 2. Deterministic Driver Extraction Rules
- **`HIGH_HAZARD_RISK`**: Triggered when primary hazard probability > 0.5 or hazard status = `HIGH`.
- **`HIGH_POPULATION_EXPOSURE`**: Triggered when total district population > 2,000,000.
- **`HIGH_CRITICAL_ASSET_EXPOSURE`**: Triggered when at least 1 critical facility or coastal asset is exposed.
- **`HIGH_SENSITIVITY`**: Triggered when urban density = `HIGH` or impervious land fraction >= 0.5.
