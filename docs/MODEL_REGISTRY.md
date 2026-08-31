# Model Registry — Climate Risk Intelligence (Review II)

## Overview
This registry records the trained machine learning models used by the Risk Agent for multi-hazard climate risk assessment across Tamil Nadu. All models were trained using historical daily meteorological data (NASA POWER, 2010–2021) and validated on post-2021 observations.

---

## 1. Model Artifact Inventory

| Hazard | Model Artifact | Framework | Architecture | Input Features | Target Label | Risk Thresholds |
|---|---|---|---|---|---|---|
| **Flood** | `Models/flood_xgboost.pkl` | XGBoost (`XGBClassifier`) | Gradient Boosted Trees (`max_depth=6`, `n_estimators=500`, `scale_pos_weight=145.65`) | 53 | Binary (0: No Flood, 1: Flood) | High: $\ge 0.70$<br>Medium: $0.40 - 0.69$<br>Low: $< 0.40$ |
| **Drought** | `Models/drought_xgboost.pkl` | XGBoost (`XGBClassifier`) | Gradient Boosted Trees (`max_depth=6`, `n_estimators=500`, `scale_pos_weight=1.89`) | 53 | Binary (0: Normal, 1: Drought) | High: $\ge 0.70$<br>Medium: $0.40 - 0.69$<br>Low: $< 0.40$ |
| **Heatwave** | `Models/heatwave_xgboost.pkl` | XGBoost (`XGBClassifier`) | Gradient Boosted Trees (`max_depth=6`, `n_estimators=500`, `scale_pos_weight=198.28`) | 53 | Binary (0: Normal, 1: Heatwave) | High: $\ge 0.70$<br>Medium: $0.40 - 0.69$<br>Low: $< 0.40$ |

---

## 2. Input Feature Specification (Exact 53-Column Schema)

All 3 models expect the exact same 53 input features in this strict sequence. Missing values must be imputed or validated before inference; raw `NaN` inputs will degrade tree traversal.

### Part A: 15 Continuous Meteorological & Derived Features
1. `temp_max` (°C): Maximum 2m air temperature for the day.
2. `temp_min` (°C): Minimum 2m air temperature for the day.
3. `temp_mean` (°C): Daily mean temperature, computed as `(temp_max + temp_min) / 2`.
4. `temp_range` (°C): Daily diurnal temperature range, computed as `temp_max - temp_min`.
5. `humidity` (%): Daily mean relative humidity at 2 meters.
6. `wind_speed` (m/s): Daily mean 10m/2m horizontal wind speed.
7. `rainfall` (mm/day): Total daily precipitation.
8. `soil_wetness` (0–1 fraction): Root-zone soil wetness from land surface model.
9. `rainfall_3d` (mm): Rolling 3-day accumulated precipitation.
10. `rainfall_7d` (mm): Rolling 7-day accumulated precipitation.
11. `rainfall_30d` (mm): Rolling 30-day accumulated precipitation.
12. `temp_anomaly` (°C): Deviation of `temp_max` from district day-of-year/monthly climatological mean.
13. `rainfall_anomaly` (mm): Deviation of daily rainfall from district climatological mean (fill `0.0` if baseline variance is 0).
14. `SPI_3`: Standardized Precipitation Index computed on a 3-month (90-day) aggregation window.
15. `SPI_6`: Standardized Precipitation Index computed on a 6-month (180-day) aggregation window.

### Part B: 38 One-Hot Encoded District Indicators (Alphabetical Order)
`district_Ariyalur`, `district_Chengalpattu`, `district_Chennai`, `district_Coimbatore`, `district_Cuddalore`, `district_Dharmapuri`, `district_Dindigul`, `district_Erode`, `district_Kallakurichi`, `district_Kancheepuram`, `district_Kanniyakumari`, `district_Karur`, `district_Krishnagiri`, `district_Madurai`, `district_Mayiladuthurai`, `district_Nagapattinam`, `district_Namakkal`, `district_Nilgiris`, `district_Perambalur`, `district_Pudukkottai`, `district_Ramanathapuram`, `district_Ranipet`, `district_Salem`, `district_Sivaganga`, `district_Tenkasi`, `district_Thanjavur`, `district_Theni`, `district_Thoothukudi`, `district_Tiruchirappalli`, `district_Tirunelveli`, `district_Tirupathur`, `district_Tiruppur`, `district_Tiruvallur`, `district_Tiruvannamalai`, `district_Tiruvarur`, `district_Vellore`, `district_Viluppuram`, `district_Virudhunagar`.

---

## 3. Spatial & Temporal Resolution
- **Spatial Resolution**: District-level ($38$ administrative districts of Tamil Nadu). Models do not predict street-level or micro-catchment risks.
- **Temporal Resolution**: Daily ($24$-hour aggregated time step). Weather forecasts provide hourly granularity, whereas ML risk predictions operate on daily aggregates.

---

## 4. Model Preprocessing & Encoders
- **Scalers**: None required. XGBoost tree splits are scale-invariant.
- **Categorical Encoding**: One-hot indicator vector of length 38 where exactly one district column is `1` and the remaining 37 are `0`.
- **Inference Pipeline**: Managed by `backend/agents/risk_agent.py`.
