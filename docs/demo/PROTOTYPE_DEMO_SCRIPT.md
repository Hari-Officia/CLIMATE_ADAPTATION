# Prototype End-to-End Demo Script

## Step-by-Step Prototype Demonstration Flow

1. **Launch Application**: Open browser to `http://localhost:3000`. Login with authorized credentials.
2. **Executive Dashboard**: Review total district coverage (38 districts), atmospheric state, and multi-hazard risk cards for Flood, Drought, Heatwave.
3. **Tamil Nadu GIS Map**: Navigate to `/risk-map`. Inspect state-wide district boundaries, hover over coastal vs inland districts, toggle risk overlays.
4. **District Search**: Search for "Chennai" or select from dropdown quick switcher.
5. **District Overview**: Navigate to `/district/chennai`. Inspect baseline risk score, adaptation priority score, and validated decision ID.
6. **Hazard Risk Profile**: Review XGBoost ensemble risk predictions for coastal flooding, urban heat, and drought.
7. **Exposure Indicators**: Inspect demographic population exposure, urban density percentage, and elevation.
8. **Vulnerability Context**: Review sensitivity indicators and social vulnerability indices.
9. **Resilience & Adaptive Capacity**: Review community adaptive capacity metrics and infrastructure buffer thresholds.
10. **Adaptation Priority Panel**: Review short-term vs long-term priority scoring derived from certified multi-criteria engine.
11. **Strategy Intelligence**: Review 14 Canonical Adaptation Strategies and filtered candidate portfolio.
12. **Classical MILP Solver**: Navigate to Classical MILP tab or `/optimization`. Inspect HIGHS exact solver optimal portfolio with 0.0000 gap.
13. **QUBO Matrix Formulation**: Inspect QUBO penalty formulation ($P=10.0$) and classical parity certificate.
14. **QAOA Quantum Benchmark**: Navigate to QAOA tab or `/qaoa`. Verify explicit `EXPERIMENTAL` status, reference objective gap `0.4700`, and `QUANTUM ADVANTAGE NOT ESTABLISHED` disclaimer.
15. **RAG Evidence Base**: Navigate to Evidence tab or `/evidence`. Search for policy documents, review Tier 1 Tamil Nadu SAPCC 2.0 citations and page references.
16. **LLM Decision Explanation**: Review grounded AI explanation with citations and uncertainty warnings.
17. **Decision Lineage & Provenance**: Review 19-Node decision graph, context SHA256 hashes, and model schema versions.
18. **Research Gaps & Limitations**: Navigate to `/research`. Review RG-001 (QAOA gap), RG-002 (outcome delay), and NC-002 (single-node DB non-HA risk).
19. **System Status & Health**: Navigate to `/system-status`. Verify `3.1.0` release status, `CONDITIONALLY_CERTIFIED` production certification, and PostgreSQL connection health.
