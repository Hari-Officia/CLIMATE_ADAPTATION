# Phase H Documentation — Qualitative Uncertainty Handling

## 1. Zero-Imputation Protocol
When dataset indicators are missing or under peer-review (e.g. `REV-001` or `GAP-LIDAR-001`), Phase H strictly prohibits interpolating or substituting average values.

## 2. Uncertainty Flags & Categorization
- `HIGH`: Multi-source verified dataset with minimal temporal skew.
- `MEDIUM`: Modelled or extrapolated dataset (e.g., Census 2011 projected to 2024).
- `UNCERTAIN`: Missing, conflicting, or unvalidated indicator metric requiring local field audit.
