# Machine Learning Models Summary

## 🤖 Overview
The **ML Models Subsystem** powers multi-hazard probability prediction across all 38 districts of Tamil Nadu. It hosts specialized **XGBoost Classifiers** trained to identify four distinct climate hazard risks: **Heatwave**, **Flood**, **Drought**, and **Cyclone**.

---

## 🎯 Model Architecture & Hazard Registry

| Hazard Type | Model Artifact | Features Input | Target Variable | Objective Function |
|---|---|---|---|---|
| **Heatwave** | `heatwave_model.json` | 53-Feature Vector | Binary Event ($T_{\max} \ge 40^\circ\text{C}$ & anomaly $\ge 4.5^\circ\text{C}$) | `binary:logistic` |
| **Flood** | `flood_model.json` | 53-Feature Vector | Heavy Rainfall / Flooding Event ($R_{\text{daily}} \ge 115.5\text{mm}$) | `binary:logistic` |
| **Drought** | `drought_model.json` | 53-Feature Vector | SPI_3 / SPI_6 Deficit ($\le -1.5$) | `binary:logistic` |
| **Cyclone** | `cyclone_model.json` | 53-Feature Vector | Extreme Wind & Pressure Drop ($W \ge 25\text{ m/s}$) | `binary:logistic` |

---

## ⚙️ Model Execution Pipeline

```
Raw Forecast Data + Climatology
               │
               ▼
+-----------------------------------+
|    FeatureEngineeringService      | --> Constructs 53-element Feature Vector
+-----------------------------------+
               │
               ▼
+-----------------------------------+
|      Hazard Model Registry        | --> Loads XGBoost binary classifiers
+-----------------------------------+
               │
               ▼
+-----------------------------------+
|   Predict Probabilities P(Hazard) | --> Output: [P_heat, P_flood, P_drought, P_cyclone]
+-----------------------------------+
```

---

## 💻 Minimal Code Example

```python
# backend/services/model_service.py
import xgboost as xgb
import numpy as np
from typing import Dict, Any, List

class HazardModelService:
    def __init__(self, model_dir: str = "backend/hazards"):
        self.models = {
            "heatwave": xgb.Booster(),
            "flood": xgb.Booster(),
            "drought": xgb.Booster(),
            "cyclone": xgb.Booster()
        }
        for hazard, model in self.models.items():
            model.load_model(f"{model_dir}/{hazard}_model.json")

    def predict_hazard_probabilities(self, feature_vector: List[float]) -> Dict[str, float]:
        """Runs vectorized XGBoost inference on the 53-feature vector."""
        dmatrix = xgb.DMatrix(np.array([feature_vector]))
        
        predictions = {}
        for hazard_name, model in self.models.items():
            prob = float(model.predict(dmatrix)[0])
            predictions[hazard_name] = round(prob, 4)
            
        return predictions
```
