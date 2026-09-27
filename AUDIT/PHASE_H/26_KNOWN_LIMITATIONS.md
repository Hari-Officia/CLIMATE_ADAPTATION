# Phase H Audit — 26 Known Limitations

## 1. Documented System Limitations
1. **No Composite Priority Index**: Phase H explicitly avoids calculating a single scalar composite score (`priority_score = NULL`) to prevent unscientific weighting bias.
2. **Deterministic Priority Horizons**: Priority horizons (`IMMEDIATE`, `SHORT_TERM`, `MEDIUM_TERM`, `LONG_TERM`) are categorized based on hazard severity and exposure thresholds, not optimization trade-off surfaces.
3. **No Optimization in Phase H**: Classical optimization (Phase J), QUBO mapping (Phase K), and QAOA quantum execution (Phase L) are strictly reserved for downstream phases.
