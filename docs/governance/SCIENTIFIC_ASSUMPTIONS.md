# Phase R — Scientific Assumptions Register

## Explicit Scientific & Mathematical Assumptions

| Assumption ID | Component | Mathematical / Domain Assumption | Source / Reference | Risk | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SA-001** | Risk Engine | Composite Hazard Index $R = \sum w_h \cdot H_h$ uses normalized IPCC WGII exposure weighting | IPCC AR6 WGII Report | LOW | VALIDATED |
| **SA-002** | Exposure Engine | District spatial exposure calculated via 1km spatial polygon zonal statistics | PostGIS `ST_ZonalStatistics` | LOW | VALIDATED |
| **SA-003** | Priority Engine | Priority matrix maps Risk Severity $\times$ Vulnerability Index into discrete buckets | Tamil Nadu SAPCC | LOW | VALIDATED |
| **SA-004** | Strategy Intelligence | 14 canonical adaptation strategies cover all 38 districts with cost-benefit bounds | TN Adaptation Strategy Catalog | LOW | VALIDATED |
| **SA-005** | Classical MILP | Strategic budget constraints strictly enforceable via binary decision variables | Operations Research Literature | LOW | VALIDATED |
| **SA-006** | QUBO Matrix | Penalty parameter $P = 10.0$ guarantees budget constraint enforcement in binary matrix | Ising Model Formulations | MEDIUM | VALIDATED |
| **SA-007** | QAOA Engine | QAOA state vector sampling on simulator provides probabilistic sample of Ising ground state | Nielsen & Chuang | MEDIUM | EXPERIMENTAL |
