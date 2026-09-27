# Qualitative-to-Numeric Scoring Methodology

When numeric values (e.g. feasibility or resource requirement) are required by optimization algorithms (such as QUBO/QAOA), qualitative labels documented in literature are mapped using the following transparent, documented conversion policy:

- **Feasibility**: `HIGH` = 1.0, `MEDIUM` = 0.6, `LOW` = 0.3
- **Resource Requirement (Cost/Complexity)**: `LOW` = 0.3, `MEDIUM` = 0.6, `HIGH` = 1.0
- **Evidence Confidence**: `VERY_HIGH` = 0.95, `HIGH` = 0.85, `MODERATE` = 0.70, `LOW` = 0.50

*Unverified percentage reduction values remain strictly NULL.*
