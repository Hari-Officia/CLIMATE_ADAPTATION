# Model Limitations & Uncertainty Documentation — Review II

## 1. Executive Summary
This document delineates the operational boundaries, scientific constraints, and known performance limitations of the trained machine learning models integrated into the Climate Risk Intelligence System. Transparent presentation of model limitations is mandatory to prevent misinterpretation during decision-making.

---

## 2. Hazard-Specific Model Limitations

### A. Flood Risk Model (`flood_xgboost.pkl`)
- **Severe Class Imbalance**: In the historical training dataset of 223,212 daily district records, only 945 were classified as flood events (a positive rate of only 0.42%).
- **Temporal & Spatial Clustering**: Historical flood events are heavily clustered around specific historic cyclonic episodes (e.g., November–December 2015, December 2017 Cyclone Ockhi, November 2021). Consequently, in post-2021 validation splits, flood events were scarce (only 4 events in 2022–2023, and 0 in 2024–2026 test sets).
- **Metric Profile**:
  - ROC-AUC: $\sim 0.906$ (reflects reasonable ranking capacity across all observations).
  - PR-AUC: $0.074$ (reflects low precision on rare events due to class imbalance).
  - Precision at $\ge 0.50$: $10.06\%$ (high false positive rate under uncalibrated default threshold).
  - Recall at $\ge 0.50$: $33.77\%$.
- **Mitigation & UI Handling**:
  - The UI explicitly renders an uncertainty warning: *"High uncertainty: Flood prediction reflects rare-event sensitivity and historical district propensity."*
  - The model output probability is presented alongside hydrological context (3-day and 7-day rolling rainfall accumulation).

### B. Drought Risk Model (`drought_xgboost.pkl`)
- **Metric Profile**: ROC-AUC: $0.9998$, PR-AUC: $0.9993$.
- **Temporal Lag Dependency**: Drought is a creeping slow-onset phenomenon requiring multi-month precipitation deficits (SPI_3 and SPI_6). 
- **Short-Range Forecast Limitation**: A single 24-hour rainfall event will not resolve a multi-month hydrological drought, nor will a dry 3-day window trigger an acute drought if multi-month storage is adequate. The model reflects chronic hydrological deficit rather than day-to-day dryness.

### C. Heatwave Risk Model (`heatwave_xgboost.pkl`)
- **Metric Profile**: ROC-AUC: $1.0000$, PR-AUC: $0.9964$.
- **Climatological Baseline Sensitivity**: Predictions depend on the temperature anomaly relative to district climatology. In transitional seasons (e.g., February to March), abrupt temperature transitions may trigger elevated probabilities if daytime highs exceed historic seasonal averages.

---

## 3. Spatial Resolution Constraints
- **District-Level Aggregation**: All models were trained on district-level centroid / MERRA-2 gridded weather series ($0.5^\circ \times 0.625^\circ$).
- **No Street-Level Claim**: When a user queries a specific landmark or coordinates (e.g., "Marina Beach" or "Coimbatore Airport"), the point-in-polygon engine identifies the containing district ("Chennai" or "Coimbatore"). The system displays:
  - **Weather**: Localized to the search coordinates from Open-Meteo.
  - **Risk**: Clearly labeled as *"District-level climate hazard model"*.
  - The system will **never** claim micro-scale street-level flood or heatwave predictions from a district-scale model.

---

## 4. Temporal Resolution Constraints
- **Weather Horizon**: Hourly resolution for 72 hours, daily summaries for 7 days.
- **Risk Prediction Horizon**: Daily resolution for Days 1 to 7. 
- The system will **never** display hourly ML risk predictions, as the ML models operate strictly on 24-hour daily aggregates.

---

## 5. Exposure vs. Hazard Separation
- **Context Only**: District population, population density, and urbanization percentage represent exposure and vulnerability context.
- **No Arbitrary Multiplication**: The ML model probabilities are generated strictly from meteorological and geographical inputs. Exposure metrics are displayed in separate context cards and never silently multiplied into ML hazard probabilities without empirical re-training.
