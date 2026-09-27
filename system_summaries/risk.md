# Risk Diagnosis Engine Summary

## ⚠️ Overview
The **Risk Diagnosis Engine** implements the **IPCC AR6 Climate Risk Assessment Framework**. It combines predicted hazard probabilities with district-specific exposure metrics and social vulnerability indicators to calculate a standardized Risk Score ($R$) for each district.

---

## 🧮 Mathematical Risk Formulation

The total composite risk $R_d$ for district $d$ across hazards $h \in \{\text{Heatwave, Flood, Drought, Cyclone}\}$ is calculated as:

$$\text{Risk}_d = \sum_{h} w_h \cdot \Big( \text{Hazard}_h(d) \times \text{Exposure}_h(d) \times \text{Vulnerability}(d) \Big)$$

Where:
* **Hazard ($H_h$)**: Calibrated probability $P(h)$ from the XGBoost ML models multiplied by severity index $[0, 1]$.
* **Exposure ($E_h$)**: Quantitative population, agricultural acreage, or infrastructure exposure value normalized to $[0, 1]$.
* **Vulnerability ($V$)**: Social Vulnerability Index (SVI) incorporating economic sensitivity and infrastructure adaptive capacity gap.

---

## 📊 Risk Category Mapping

| Risk Score Range | Classification Level | Action Trigger |
|---|---|---|
| `0.00 - 0.24` | 🟢 **Low** | Standard monitoring & routine maintenance |
| `0.25 - 0.49` | 🟡 **Moderate** | Targeted seasonal advisory & early warning |
| `0.50 - 0.74` | 🟠 **High** | Accelerated adaptation intervention & funding priority |
| `0.75 - 1.00` | 🔴 **Critical** | Emergency portfolio deployment & quantum optimization |

---

## 💻 Minimal Code Example

```python
# backend/risk/risk_engine.py
from typing import Dict, Any

class RiskEngine:
    HAZARD_WEIGHTS = {"flood": 0.35, "drought": 0.25, "heatwave": 0.20, "cyclone": 0.20}

    def compute_district_risk(
        self,
        hazard_probs: Dict[str, float],
        exposure_score: float,
        vulnerability_index: float
    ) -> Dict[str, Any]:
        """Calculates IPCC Risk = Hazard x Exposure x Vulnerability."""
        weighted_hazard_score = sum(
            hazard_probs.get(h, 0.0) * w 
            for h, w in self.HAZARD_WEIGHTS.items()
        )
        
        # Composite risk multiplication
        raw_risk = weighted_hazard_score * exposure_score * vulnerability_index
        normalized_risk = min(1.0, max(0.0, raw_risk * 2.5)) # Scale to [0, 1]
        
        if normalized_risk >= 0.75: category = "CRITICAL"
        elif normalized_risk >= 0.50: category = "HIGH"
        elif normalized_risk >= 0.25: category = "MODERATE"
        else: category = "LOW"
        
        return {
            "composite_risk_score": round(normalized_risk, 4),
            "risk_category": category,
            "weighted_hazard": round(weighted_hazard_score, 4),
            "exposure": exposure_score,
            "vulnerability": vulnerability_index
        }
```
