# Verified Risk ML Model Metrics Audit

> **Forensic Audit Notice**: This table summarizes the verified risk classification metrics extracted directly from project model execution outputs (`ProjectCollab/ClimateRisk.ipynb`), master registries (`config/master/models.json`), and baseline snapshots (`config/models/model_registry.json`).

| Hazard | Algorithm | Split | Accuracy | Precision | Recall | F1 | PR-AUC | ROC-AUC | Positive Prevalence | Leakage Status | Calibration Status | Verification Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| **Flood** | XGBoost (`XGBClassifier`) | Test Set | `0.9867` | `0.1006` | `0.3377` | `0.1550` | `0.0745` | `0.9062` | `0.3626%` | `LEAKAGE-SAFE` | `UNCALIBRATED RISK SCORE` | **VERIFIED** |
| **Flood** | XGBoost (`XGBClassifier`) | Validation Set | `0.9934` | `0.0093` | `0.0132` | `0.0109` | `0.0026` | `0.4050` | `0.2740%` | `LEAKAGE-SAFE (ANOMALY)` | `UNCALIBRATED RISK SCORE` | **VERIFIED** |
| **Flood** | XGBoost (`MOD-FLD-XGB-v1.2`) | Registry Snapshot | `N/A` | `N/A` | `N/A` | `N/A` | `0.8450` | `0.8920` | `0.4234%` | `LEAKAGE-SAFE` | `UNCALIBRATED RISK SCORE` | **HISTORICAL SNAPSHOT** |
| **Drought** | XGBoost (`XGBClassifier`) | Test / Notebook | `N/A` | `N/A` | `N/A` | `N/A` | `0.9993` | `0.9998` | `29.8644%` | `REPORTED RESULT — LEAKAGE-AFFECTED` | `UNCALIBRATED RISK SCORE` | **ABLATION/HISTORICAL ONLY** |
| **Drought** | XGBoost (`MOD-DRO-SPI-v1.0`) | Registry Snapshot | `N/A` | `N/A` | `N/A` | `N/A` | `0.8120` | `0.8650` | `29.8644%` | `REPORTED RESULT — LEAKAGE-AFFECTED` | `UNCALIBRATED RISK SCORE` | **HISTORICAL SNAPSHOT** |
| **Heatwave** | XGBoost (`XGBClassifier`) | Test / Notebook | `N/A` | `N/A` | `N/A` | `N/A` | `0.9964` | `1.0000` | `0.4812%` | `LEAKAGE-SAFE (RULE OVERFIT)` | `UNCALIBRATED RISK SCORE` | **VERIFIED** |
| **Heatwave** | XGBoost (`MOD-HTW-ANO-v1.1`) | Registry Snapshot | `N/A` | `N/A` | `N/A` | `N/A` | `0.8780` | `0.9100` | `0.4812%` | `LEAKAGE-SAFE` | `UNCALIBRATED RISK SCORE` | **HISTORICAL SNAPSHOT** |

---

### Critical Forensic Observations:
1. **Accuracy Paradox in Flood Classifier**: The Flood test set displays an accuracy of **98.67%**, but a PR-AUC of only **0.0745** and F1 of **15.50%**. This occurs due to extreme negative class prevalence (99.64%). High accuracy must NOT be interpreted as successful risk prediction.
2. **Validation Anomalous Degradation**: In the 2018–2019 validation set, Flood ROC-AUC collapsed to **0.4050** and PR-AUC to **0.0026** because the 76 ground-truth flood labels in the dataset occurred during low-rainfall periods (mean 30-day rain = 15.7 mm vs non-flood 74.8 mm).
3. **Drought Target Proxy Leakage**: `SPI_3` and `SPI_6` were included as input features for Drought prediction while simultaneously being the exact mathematical indicators defining the ground-truth drought target. The 0.9998 ROC-AUC result is leakage-affected.
