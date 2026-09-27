# Phase F — Temporal Alignment & Versioning

## Temporal Versioning Rules
1. **Historical Snapshots**: Every dataset version stores `dataset_version`, `checksum`, and timestamp.
2. **Temporal Alignment Check**: Calculates `temporal_gap_years = risk_calculation_year - exposure_dataset_year`.
3. **Mismatch Warning**: If gap > 2 years, triggers `temporal_mismatch_flag = true` and logs explicit warning in response payload.
