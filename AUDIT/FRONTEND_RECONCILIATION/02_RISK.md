# Multi-Hazard Risk Reconciliation

- Hazards Covered: Flood, Drought, Heatwave (plus 7 complementary physical hazard indicators)
- Underlying Machine Learning Model: 53-feature XGBoost Ensemble (ROC-AUC 0.906, 0.999, 1.000)
- Rules: Probabilities are returned strictly by backend XGBoost models. Zero React calculation.
- Display: Risk levels (LOW, MEDIUM, HIGH, SEVERE) rendered with accessible color semantics and explicit source metadata.
