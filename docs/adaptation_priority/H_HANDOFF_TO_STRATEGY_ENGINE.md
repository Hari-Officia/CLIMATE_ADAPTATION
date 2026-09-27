# Phase H — Handoff to Strategy Applicability Engine (Phase I)

## Handoff Contract Overview
Phase H establishes the adaptation priority profile context for every district and hazard in Tamil Nadu.

### Handoff Payload (`AdaptationPriorityContext`):
- `district_id`: Canonical district identifier (e.g., `chennai`).
- `hazard_id`: Climate hazard evaluated (`flood`, `drought`, `heatwave`).
- `priority_status`: Categorical priority level (`REQUIRES_PRIORITY_ATTENTION`, `MODERATE_PRIORITY`, `MONITORING_ONLY`).
- `priority_horizon`: Target intervention timing (`IMMEDIATE`, `SHORT_TERM`, `MEDIUM_TERM`, `LONG_TERM`).
- `priority_drivers`: List of empirical drivers justifying priority attention.
- `priority_barriers`: Temporal gap flags and data gap warnings.

Phase I (Strategy Applicability) consumes this context payload to filter and match candidate adaptation strategies without recalculating priority from raw database tables.
