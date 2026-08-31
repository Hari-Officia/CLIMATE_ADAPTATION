# Model Feature Mapping & Derivation Specification

## 1. Ordered 53-Feature Vector Specification

The 3 XGBoost models (`flood_xgboost.pkl`, `drought_xgboost.pkl`, `heatwave_xgboost.pkl`) strictly require the following 53 features in exact sequence:

| Index | Feature Name | Unit | Source | Derivation Method |
|---|---|---|---|---|
| 0 | `temp_max` | °C | Open-Meteo Daily | Direct daily maximum 2m air temperature |
| 1 | `temp_min` | °C | Open-Meteo Daily | Direct daily minimum 2m air temperature |
| 2 | `temp_mean` | °C | Derived | $(T_{\max} + T_{\min}) / 2.0$ |
| 3 | `temp_range` | °C | Derived | $T_{\max} - T_{\min}$ |
| 4 | `humidity` | % | Open-Meteo Hourly | Mean relative humidity across 24 hours |
| 5 | `wind_speed` | m/s | Open-Meteo Hourly | Mean 10m wind velocity across 24 hours |
| 6 | `rainfall` | mm | Open-Meteo Daily | Daily precipitation sum |
| 7 | `soil_wetness` | 0–1 fraction | Open-Meteo Hourly | 0–1cm / root-zone soil moisture |
| 8 | `rainfall_3d` | mm | Derived | 3-day rolling precipitation sum |
| 9 | `rainfall_7d` | mm | Derived | 7-day rolling precipitation sum |
| 10 | `rainfall_30d` | mm | Derived | 30-day cumulative precipitation |
| 11 | `temp_anomaly` | °C | Climatology Baseline | $T_{\max} - \overline{T_{\max,\text{month}}}$ (NASA 16-year normal) |
| 12 | `rainfall_anomaly` | mm | Climatology Baseline | $R_{\text{day}} - \overline{R_{\text{daily,month}}}$ |
| 13 | `SPI_3` | Index | Antecedent Climatology | Standardized 90-day precipitation index |
| 14 | `SPI_6` | Index | Antecedent Climatology | Standardized 180-day precipitation index |
| 15–52 | `district_Ariyalur` to `district_Virudhunagar` | Binary (0/1) | Geographic Metadata | Alphabetical one-hot encoding for the 38 Tamil Nadu districts |

---

## 2. Policy on Missing Features and Zeros

1. **Real Zero vs. Missing**: A rainfall value of `0.0 mm` is a valid physical observation. A missing `SPI_3` is an unknown antecedent state. The system strictly distinguishes between physical zeros and missing data.
2. **Pre-Inference Validation**: `FeatureContractValidator` tests every vector before execution. If a required feature is missing, the model returns `UNAVAILABLE` rather than predicting with zero-imputed values.
