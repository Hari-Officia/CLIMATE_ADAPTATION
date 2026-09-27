# Adaptation Strategy Framework Summary

## 🌿 Overview
The **Adaptation Strategy Framework** manages the catalog of resilience interventions and computes localized suitability scores for each district. It filters candidates based on hazard types, sector vulnerabilities (Agriculture, Coastal, Urban, Water), financial constraints, and expected risk reduction.

---

## 🏗️ Strategy Classification Matrix

| Sector | Example Strategies | Targeted Hazards | Typical Cost (Lakhs INR) | Risk Reduction ($\Delta R$) |
|---|---|---|---|---|
| **Coastal** | Mangrove Buffer Restoration, Seawall Construction | Cyclone, Flood, Storm Surge | 150 - 500 | 25% - 40% |
| **Water** | Desalination Micro-Grids, Tank Check-Dam Restoration | Drought | 200 - 800 | 30% - 50% |
| **Agriculture** | Micro-Irrigation Adoption, Heat-Tolerant Crops | Drought, Heatwave | 50 - 180 | 20% - 35% |
| **Urban** | Stormwater Drainage Expansion, Cool Roof Initiatives | Flood, Heatwave | 100 - 450 | 15% - 30% |

---

## 🎯 Candidate Selection Pipeline

1. **Hazard Hazard Trigger**: High risk score ($R > 0.5$) for specific hazards in district $d$.
2. **Geographic Filtering**: Coastal-only strategies are excluded for inland districts.
3. **Applicability Scoring**: Computes $A_{i,d} \in [0, 1]$ based on vulnerability alignment.
4. **Candidate Set Generation**: Selects top candidate set of size $N$ (e.g. 5 to 15 strategies) for QUBO optimization.

---

## 💻 Minimal Code Example

```python
# backend/services/strategy_candidate_service.py
from typing import Dict, Any, List

class StrategyCandidateService:
    def __init__(self):
        # Library of master adaptation strategies
        self.strategies_db = [
            {"id": "STRAT_COAST_01", "name": "Mangrove Bio-Shield", "sector": "Coastal", "coastal_only": True, "cost": 150.0, "risk_reduction": 0.35},
            {"id": "STRAT_WATER_01", "name": "Tank Check-Dam Grid", "sector": "Water", "coastal_only": False, "cost": 250.0, "risk_reduction": 0.40},
            {"id": "STRAT_AGRI_01", "name": "Micro-Irrigation Conversion", "sector": "Agriculture", "coastal_only": False, "cost": 90.0, "risk_reduction": 0.25},
            {"id": "STRAT_URBAN_01", "name": "Stormwater Drain Upgrade", "sector": "Urban", "coastal_only": False, "cost": 300.0, "risk_reduction": 0.30},
        ]

    def generate_candidate_set(self, district_id: str, is_coastal: bool = True) -> Dict[str, Any]:
        """Filters strategies matching district geographic profile."""
        eligible = []
        for strat in self.strategies_db:
            if strat["coastal_only"] and not is_coastal:
                continue
            eligible.append(strat)

        return {
            "district_id": district_id,
            "total_candidates": len(eligible),
            "strategy_ids": [s["id"] for s in eligible],
            "candidates": eligible
        }
```
