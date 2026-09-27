# Phase H Documentation — Priority Component Formula & Non-Composite Policy

## 1. Non-Composite Priority Policy
Phase H explicitly refrains from computing a single scalar composite priority score (`priority_score = NULL`). Combining disparate physical risk metrics (e.g. flood inundation depth in meters, heat stress days above 40°C, and population density) into an arbitrary linear sum introduces subjective bias and masks critical driver signals.

## 2. Component Decomposition
Instead of a composite index, district priority profiles maintain independent component vectors across four distinct pillars:

1. **Hazard Pillar ($H$)**: Probabilities and return periods for drought, flood, heatwave, and coastal surge.
2. **Exposure Pillar ($E$)**: Exposed human population count, agricultural land area, and critical infrastructure assets.
3. **Vulnerability Pillar ($V$)**: Socio-economic sensitivity, urban density, and infrastructure vulnerability flags.
4. **Adaptive Capacity Pillar ($AC$)**: Historical resilience investments, healthcare access, and disaster preparedness infrastructure.

## 3. Priority Profile Structure
Each component is represented as an independent structured object containing metric values, status flags, and data provenance references.
