# ML Model Retraining & Calibration Policy

## 1. Scope & Objective
Governs the retraining, calibration, and candidate evaluation pipeline for XGBoost and SPI risk models.

## 2. Trigger Criteria
Retraining may ONLY be initiated by:
- Feature drift exceeding PSI threshold ($PSI > 0.10$).
- Ground-truth outcome label arrival post 1-3 year empirical delay.
- Scientific correction or documented climatology profile update.

## 3. Mandatory Retraining Workflow
1. Data Snapshot & Quality Gate
2. Feature Pipeline Verification (53-feature contract preserved)
3. Model Training & Temporal Splitting ($Train < Validation < Test$)
4. Calibration Review & Metric Comparison (ROC-AUC, PR-AUC, F1)
5. Scientific Board Review
6. Canary Staging Deployment
7. Model Registry Update & Baseline Snapshot
