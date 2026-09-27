# Phase H Documentation — Component Normalization

## 1. Objective & Guidelines
Component values in Phase H are normalized to physical units or categorized ordinal scales rather than arbitrary zero-to-one min-max scales that obscure real-world thresholds.

## 2. Categorical Normalization Rules
- **Hazard Probability**: Normalized to range `[0.0, 1.0]`.
- **Population Exposure**: Retains raw count with categorical brackets (`< 500k`, `500k - 2M`, `> 2M`).
- **Urban Density**: Categorized as `LOW`, `MEDIUM`, or `HIGH` based on built-up area fraction.
- **Data Completeness**: Measured strictly by verified indicator counts without imputing missing values.
