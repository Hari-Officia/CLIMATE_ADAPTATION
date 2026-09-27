# Phase H — Adaptation Priority Conceptual Framework

**Scope**: Tamil Nadu (38 Districts) — Climate Adaptation Only  
**Authoritative Engine**: `PriorityService` / PostgreSQL + PostGIS

## Conceptual Framework Architecture
Adaptation Priority evaluates where climate adaptation attention and intervention are justified based on four distinct pillars:
1. **Climate Hazard Risk (Phase E)**: Validated XGBoost classifier probability and risk status.
2. **Exposure (Phase F)**: Population size, urban built environment, and critical infrastructure assets in hazard zones.
3. **Vulnerability & Sensitivity (Phase G)**: Demographic sensitivity, coastal exposure, urban density.
4. **Resilience Gap (Phase G)**: Sectoral preparedness and adaptive capacity limitations.

## Strict Governance Principles
- **No Composite Score Invention**: Single composite scores (`risk * exposure * vulnerability`) are NOT calculated unless backed by an approved, registered methodology.
- **Traceable Drivers**: Every priority assignment is justified by empirical drivers (`HIGH_POPULATION_EXPOSURE`, `HIGH_HAZARD_RISK`, `HIGH_SENSITIVITY`).
- **Decoupled from Strategy Selection**: Phase H determines priority context only. Strategy applicability and portfolio optimization are handled in Phase I/J/K/L.
