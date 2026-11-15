# Actual Risk Model Performance Audit Report

> **Forensic Audit Notice**: All metrics in this report were independently recomputed directly from loading the saved XGBoost binary model artifacts (`Models/*.pkl`) and executing predictions on the exact evaluation datasets (`ClimateData/*.csv`). No registry JSON metrics or unverified summary tables were accepted without direct execution verification.

---

## 1. Saved Models

| Model File | SHA-256 Checksum | Class | n_features | Estimators | Max Depth | Learning Rate | Scale Pos Weight | Verification Status |
|---|---|---|---:|---:|---:|---:|---:|---|
| `Models/flood_xgboost.pkl` | `0f90ee7a848bd9532881c1cf192aeecc5c63f86aa75c263d56245e3055c9668d` | `XGBClassifier` | 53 | 500 | 6 | 0.05 | 145.65 | **VERIFIED** |
| `Models/drought_xgboost.pkl` | `22dc3244f3ef9fce41581540b143abc562510f4451531994f7898cd5cfd965b9` | `XGBClassifier` | 53 | 500 | 6 | 0.05 | 1.89 | **VERIFIED** |
| `Models/heatwave_xgboost.pkl` | `52a3190a239f58551081cb6f0a6e0ba8964d0c142c9d82b9f6197fc08871a551` | `XGBClassifier` | 53 | 500 | 6 | 0.05 | 198.28 | **VERIFIED** |

---

## 2. Exact Dataset Used

- **Primary Source**: NASA POWER Reanalysis Daily Meteorological Dataset spanning 38 Tamil Nadu administrative districts (`ClimateData/*.csv`).
- **Total Records**: `228,950` daily records (38 districts × 6,025 calendar days, 2010-01-01 through 2026-06-30).

---

## 3. Exact Feature Set (53 Features)

1. **15 Continuous Features**: `temp_max`, `temp_min`, `temp_mean`, `temp_range`, `humidity`, `wind_speed`, `rainfall`, `soil_wetness`, `rainfall_3d`, `rainfall_7d`, `rainfall_30d`, `temp_anomaly`, `rainfall_anomaly`, `SPI_3`, `SPI_6`.
2. **38 District Indicators**: One-hot indicator vector (`district_Ariyalur` through `district_Virudhunagar`).

---

## 4. Exact Evaluation Splits

- **Flood Validation Split**: `2018-01-01` to `2019-12-31` (27,740 samples).
- **Flood Test Split**: `2020-01-01` to `2022-12-31` (41,648 samples).
- **Drought Test Split**: `2024-01-01` to `2026-06-30` (34,656 samples).
- **Heatwave Test Split**: `2024-01-01` to `2026-06-30` (34,656 samples).

---

## 5. Recomputed Predictions

Raw prediction files containing `date`, `district`, `y_true`, `y_pred`, and `y_probability` were generated and saved under `verified_predictions/`:
- `verified_predictions/flood_validation_set_predictions.csv`
- `verified_predictions/flood_test_set_predictions.csv`
- `verified_predictions/drought_test_set_predictions.csv`
- `verified_predictions/heatwave_test_set_predictions.csv`

---

## 6. Confusion Matrices (At Threshold = 0.5)

| Hazard | Split | Total N | True Negatives (TN) | False Positives (FP) | False Negatives (FN) | True Positives (TP) | Positive Count | Prevalence |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Flood** | Test Set | 41,648 | 40,990 | 352 | 181 | 125 | 306 | `0.7347%` |
| **Flood** | Validation Set | 27,740 | 27,632 | 53 | 41 | 14 | 55 | `0.1983%` |
| **Drought** | Test Set | 34,656 | 30,386 | 34 | 76 | 4,160 | 4,236 | `12.2230%` |
| **Heatwave** | Test Set | 34,656 | 33,639 | 0 | 861 | 156 | 1,017 | `2.9346%` |

---

## 7. Verified Metrics (Direct Recomputation)

| Hazard | Split | Accuracy | Bal Acc | Precision | Recall | F1 | Specificity | ROC-AUC | PR-AUC | Brier Score | Log Loss | MCC |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Flood** | Test Set | **0.98720** | 0.69999 | 0.26205 | 0.40850 | **0.31928** | 0.99149 | **0.92449** | **0.21294** | 0.01027 | 0.04094 | 0.32103 |
| **Flood** | Validation Set | **0.99661** | 0.62632 | 0.20896 | 0.25455 | **0.22951** | 0.99809 | **0.94048** | **0.11673** | 0.00285 | 0.01301 | 0.22894 |
| **Drought** | Test Set | **0.99683** | 0.99047 | 0.99189 | 0.98206 | **0.98695** | 0.99888 | **0.99992** | **0.99941** | 0.00274 | 0.01217 | 0.98516 |
| **Heatwave** | Test Set | **0.97516** | 0.57670 | 1.00000 | 0.15339 | **0.26598** | 1.00000 | **0.99284** | **0.79802** | 0.02473 | 0.24348 | 0.38674 |

---

## 8. Previous vs Recomputed Metrics

- **Flood Test PR-AUC**: Previous notebook summary reported `0.0745`; direct recomputation on the 2020–2022 test set yields `0.21294` (F1 = `0.31928`).
- **Flood Validation ROC-AUC**: Direct recomputation on the exact 2018–2019 validation set yields `0.94048` (PR-AUC = `0.11673`), resolving prior reported anomaly concerns.
- **Heatwave Test PR-AUC**: Previous registry snapshot reported `0.8780`; direct recomputation on post-2024 test data yields `0.79802` (F1 = `0.26598`, Precision = `100.0%`, Recall = `15.34%`).

---

## 9. Leakage Audit

1. **Drought Model Target Proxy Leakage**: `REPORTED RESULT — LEAKAGE-AFFECTED`. Features `SPI_3` and `SPI_6` directly define ground-truth drought target labels. Near-perfect metrics (`0.99992` ROC-AUC) reflect rule learning rather than physical predictive discovery.
2. **Flood & Heatwave Leakage**: `LEAKAGE-SAFE`. Chronological date splitting enforced; no temporal or target proxy leakage detected.

---

## 10. Calibration

- **Calibration Status**: `UNCALIBRATED RISK SCORE`. Model probabilities are raw logistic sigmoid outputs.
- Brier scores: Flood Test = `0.01027`, Drought Test = `0.00274`, Heatwave Test = `0.02473`.

---

## 11. Final Verified Results Table

| Hazard | Model | Split | Accuracy | Precision | Recall | F1 | PR-AUC | ROC-AUC | Verification |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **Flood** | `Models/flood_xgboost.pkl` | Test Set | 0.9872 | 0.2621 | 0.4085 | 0.3193 | 0.2129 | 0.9245 | **VERIFIED** |
| **Flood** | `Models/flood_xgboost.pkl` | Validation Set | 0.9966 | 0.2090 | 0.2546 | 0.2295 | 0.1167 | 0.9405 | **VERIFIED** |
| **Drought** | `Models/drought_xgboost.pkl` | Test Set | 0.9968 | 0.9919 | 0.9821 | 0.9870 | 0.9994 | 0.9999 | **VERIFIED (LEAKAGE-AFFECTED)** |
| **Heatwave** | `Models/heatwave_xgboost.pkl` | Test Set | 0.9752 | 1.0000 | 0.1534 | 0.2660 | 0.7980 | 0.9928 | **VERIFIED** |
