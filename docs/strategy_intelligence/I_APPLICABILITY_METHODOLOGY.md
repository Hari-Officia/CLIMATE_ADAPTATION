# Phase I Documentation — Applicability Methodology

## 1. Eligibility States
- `ELIGIBLE`: All mandatory conditions satisfied.
- `INELIGIBLE`: Hard physical or spatial condition contradicts applicability.
- `CONDITIONALLY_ELIGIBLE`: Applicable subject to prerequisite fulfillment.
- `INSUFFICIENT_DATA`: Required context data unavailable.
- `REQUIRES_REVIEW`: Scientific peer-review flag active.
- `NOT_APPLICABLE`: Out of physical scope.

## 2. Spatial Rules
Coastal strategies (`DOM-CST`, `STR-CST-001`) are evaluated against PostGIS district boundary coastal exposure flags. Inland districts default to `INELIGIBLE` for coastal bio-shield restoration.
