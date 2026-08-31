# Project Artifact Inventory

> Generated from Phase 0 inspection of existing project folder

## Model Artifacts

| Artifact | Type | Path | Purpose | Required for Inference | Notes |
|----------|------|------|---------|------------------------|-------|
| flood_xgboost.pkl | XGBClassifier (pickle/joblib) | Models/flood_xgboost.pkl | Binary flood prediction | YES | Known poor PR-AUC; see FLOOD MODEL PROBLEM |
| drought_xgboost.pkl | XGBClassifier (pickle/joblib) | Models/drought_xgboost.pkl | Binary drought prediction | YES | Excellent performance (ROC-AUC 0.9998) |
| heatwave_xgboost.pkl | XGBClassifier (pickle/joblib) | Models/heatwave_xgboost.pkl | Binary heatwave prediction | YES | Excellent performance (ROC-AUC 1.0) |

## No Separate Preprocessor Artifacts

| Artifact | Exists | Reason |
|----------|--------|--------|
| Scaler (.pkl) | NO | XGBoost does not require feature scaling; raw values were used |
| Encoder (.pkl) | NO | District one-hot encoding was done via pd.get_dummies at inference time |
| Imputer (.pkl) | NO | NaN rows were dropped, not imputed |
| Feature list (.json) | NO | Feature list must be extracted from notebook (documented below) |

## Data Files

| Artifact | Type | Path | Purpose | Required for Inference | Notes |
|----------|------|------|---------|------------------------|-------|
| Chennai.csv | CSV | ClimateData/Chennai.csv | Historical NASA POWER data for Chennai | NO (training data) | 38 district files total |
| Ariyalur.csv ... Virudhunagar.csv | CSV | ClimateData/*.csv | Historical NASA POWER data per district | NO (training data) | Used for training feature engineering |
| Tamil_Nadu_Final_Hazard_Features.csv | CSV | NOT in local folder (Google Drive) | Combined feature-engineered dataset | NO (training data) | 228,950 rows × 25 columns |

## GIS Data

| Artifact | Type | Path | Purpose | Required for Inference | Notes |
|----------|------|------|---------|------------------------|-------|
| geoBoundaries-IND-ADM2.geojson | GeoJSON | geoBoundaries-IND-ADM2-all/ | India ADM2 district boundaries | YES (UI) | Must filter for Tamil Nadu; geoBoundaries source |
| geoBoundaries-IND-ADM2_simplified.geojson | GeoJSON | geoBoundaries-IND-ADM2-all/ | Simplified boundaries (smaller file) | YES (UI preferred) | Better for web rendering |

## Notebooks

| Artifact | Type | Path | Purpose | Notes |
|----------|------|------|---------|-------|
| ClimateRisk.ipynb | Jupyter Notebook | ProjectCollab/ | Model training & evaluation | Contains full training pipeline |
| climaterisk.py | Python script | ProjectCollab/ | Auto-exported version of notebook | Same content as .ipynb |

## Model Training Configuration

| Parameter | Flood | Heatwave | Drought |
|-----------|-------|----------|---------|
| n_estimators | 500 | 500 | 500 |
| max_depth | 6 | 6 | 6 |
| learning_rate | 0.05 | 0.05 | 0.05 |
| subsample | 0.8 | 0.8 | 0.8 |
| colsample_bytree | 0.8 | 0.8 | 0.8 |
| objective | binary:logistic | binary:logistic | binary:logistic |
| eval_metric | aucpr | aucpr | aucpr |
| scale_pos_weight | 169.90 (or 145.65 for v2) | 198.28 | 1.89 |
| random_state | 42 | 42 | 42 |

## Feature Schema (53 columns)

### Numerical Features (15)

| # | Feature Name | Source | Unit | Derivation |
|---|-------------|--------|------|------------|
| 1 | temp_max | NASA POWER T2M_MAX | °C | Direct |
| 2 | temp_min | NASA POWER T2M_MIN | °C | Direct |
| 3 | temp_mean | Derived | °C | (temp_max + temp_min) / 2 |
| 4 | temp_range | NASA POWER T2M_RANGE or derived | °C | temp_max - temp_min |
| 5 | humidity | NASA POWER RH2M | % | Direct |
| 6 | wind_speed | NASA POWER WS2M | m/s | Direct |
| 7 | rainfall | NASA POWER PRECTOTCORR | mm/day | Direct |
| 8 | soil_wetness | NASA POWER GWETROOT | unitless (0–1) | Direct |
| 9 | rainfall_3d | Derived | mm | Rolling 3-day sum of rainfall |
| 10 | rainfall_7d | Derived | mm | Rolling 7-day sum of rainfall |
| 11 | rainfall_30d | Derived | mm | Rolling 30-day sum of rainfall |
| 12 | temp_anomaly | Derived | °C | temp_max minus climatological baseline |
| 13 | rainfall_anomaly | Derived | unitless | Rainfall minus climatological baseline (NaN → 0) |
| 14 | SPI_3 | Derived | unitless | 3-month Standardized Precipitation Index |
| 15 | SPI_6 | Derived | unitless | 6-month Standardized Precipitation Index |

### District One-Hot Columns (38)

district_Ariyalur, district_Chengalpattu, district_Chennai, district_Coimbatore,
district_Cuddalore, district_Dharmapuri, district_Dindigul, district_Erode,
district_Kallakurichi, district_Kancheepuram, district_Kanniyakumari, district_Karur,
district_Krishnagiri, district_Madurai, district_Mayiladuthurai, district_Nagapattinam,
district_Namakkal, district_Nilgiris, district_Perambalur, district_Pudukkottai,
district_Ramanathapuram, district_Ranipet, district_Salem, district_Sivaganga,
district_Tenkasi, district_Thanjavur, district_Theni, district_Thoothukudi,
district_Tiruchirappalli, district_Tirunelveli, district_Tirupathur, district_Tiruppur,
district_Tiruvallur, district_Tiruvannamalai, district_Tiruvarur, district_Vellore,
district_Viluppuram, district_Virudhunagar

## Target Labels

| Target | Type | Positive Rate (training) | Positive Rate (overall) |
|--------|------|--------------------------|------------------------|
| flood | Binary (0/1) | 0.585% | 0.423% |
| heatwave | Binary (0/1) | 0.502% | 0.481% |
| drought | Binary (0/1) | 34.625% | 29.864% |

## Model Evaluation Metrics

### Heatwave Model (STRONG)
| Metric | Validation | Test |
|--------|-----------|------|
| ROC-AUC | 1.0000 | 1.0000 |
| PR-AUC | 0.9997 | 0.9964 |

### Drought Model (STRONG)
| Metric | Validation | Test |
|--------|-----------|------|
| ROC-AUC | 0.9999 | 0.9998 |
| PR-AUC | 0.9992 | 0.9993 |

### Flood Model (PROBLEMATIC)
| Metric | Val (original split) | Test (flood-specific split) |
|--------|---------------------|---------------------------|
| ROC-AUC | 0.901 | 0.906 |
| PR-AUC | 0.0013 | 0.074 |
| Precision (@ 0.5) | — | 0.1006 |
| Recall (@ 0.5) | — | 0.3377 |

**Root Causes:**
- Extreme class imbalance (0.42% positive rate)
- Only 945 flood events in 223,212 observations
- Flood events temporally clustered (2015: 311, 2017: 277, 2021: 147)
- Validation period 2022-2023 had only 4 flood events
- Test period 2024-2026 had 0 flood events

## Temporal Split

| Split | Date Range | Rows | Flood Events |
|-------|-----------|------|--------------|
| Train | 2010-06-01 → 2021-12-31 | 160,816 | 941 |
| Validation | 2022-01-01 → 2023-12-31 | 27,740 | 4 |
| Test | 2024-01-01 → 2026-06-30 | 34,656 | 0 |

## Risk Thresholds (from notebook)

```
HIGH:   probability >= 0.70
MEDIUM: probability >= 0.40
LOW:    probability < 0.40
```

## Missing Value Policy (from training)

1. `rainfall_anomaly` NaN → filled with 0 (199 cases, all Feb 27/29 for specific districts)
2. All other NaN rows → dropped (5,738 rows, primarily SPI_6 warmup period)
3. No imputer was fitted or saved
4. **Inference implication**: For forecast inference, we must provide all 15 features with valid values; cannot pass NaN to the model

## NASA POWER Historical Schema

| NASA POWER Parameter | Description | Unit |
|---------------------|-------------|------|
| T2M_RANGE | Temperature range at 2m | °C |
| T2M_MAX | Max temperature at 2m | °C |
| T2M_MIN | Min temperature at 2m | °C |
| RH2M | Relative humidity at 2m | % |
| WS2M | Wind speed at 2m | m/s |
| PS | Surface pressure | kPa |
| ALLSKY_SFC_SW_DWN | Shortwave downward irradiance | MJ/m²/day |
| GWETROOT | Root zone soil wetness | dimensionless (0–1) |
| PRECTOTCORR | Corrected precipitation | mm/day |

**Note:** PS (pressure) and ALLSKY_SFC_SW_DWN (solar radiation) are in the raw data but NOT in the final ML feature set.
