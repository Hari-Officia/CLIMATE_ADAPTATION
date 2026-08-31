# Feature Engineering Specification — Review II

## 1. Overview
The Multi-Hazard Machine Learning models (`flood_xgboost.pkl`, `drought_xgboost.pkl`, `heatwave_xgboost.pkl`) strictly require an ordered input vector of exactly **53 features**. The Feature Engineering Service (`backend/services/feature_engineering.py`) transforms forecast variables and historical baselines into this schema.

---

## 2. Feature Definitions & Formulations

### Continuous Meteorological Variables (15)

1. `temp_max` (°C): Daily maximum 2m air temperature.
2. `temp_min` (°C): Daily minimum 2m air temperature.
3. `temp_mean` (°C): Arithmetic mean:
   $$\text{temp\_mean} = \frac{\text{temp\_max} + \text{temp\_min}}{2}$$
4. `temp_range` (°C): Diurnal temperature range:
   $$\text{temp\_range} = \text{temp\_max} - \text{temp\_min}$$
5. `humidity` (%): Mean relative humidity at 2 meters over the 24-hour daily cycle.
6. `wind_speed` (m/s): Mean horizontal wind speed at 10 meters.
7. `rainfall` (mm/day): Total accumulated daily precipitation.
8. `soil_wetness` (fraction): Root-zone soil wetness fraction ($0.0 \le \text{soil\_wetness} \le 1.0$).
9. `rainfall_3d` (mm): Rolling 3-day accumulated precipitation:
   $$\text{rainfall\_3d} = \sum_{t=-1}^{+1} \text{rainfall}_t$$
10. `rainfall_7d` (mm): Rolling 7-day accumulated precipitation:
    $$\text{rainfall\_7d} = \sum_{t=0}^{6} \text{rainfall}_t$$
11. `rainfall_30d` (mm): Rolling 30-day accumulated precipitation (7-day forecast accumulation + 23-day historical monthly normal).
12. `temp_anomaly` (°C): Departure from historical monthly climatological average:
    $$\text{temp\_anomaly} = \text{temp\_max} - \overline{\text{temp\_max}}_{\text{district, month}}$$
13. `rainfall_anomaly` (mm): Departure from historical daily climatological average:
    $$\text{rainfall\_anomaly} = \text{rainfall} - \overline{\text{rainfall}}_{\text{district, month}}$$
14. `SPI_3`: Standardized Precipitation Index for 3-month window:
    $$\text{SPI\_3} = \frac{\text{rainfall\_90d} - \mu_{90d}}{\sigma_{90d}}$$
15. `SPI_6`: Standardized Precipitation Index for 6-month window:
    $$\text{SPI\_6} = \frac{\text{rainfall\_180d} - \mu_{180d}}{\sigma_{180d}}$$

### Categorical District One-Hot Encodings (38)

Strictly alphabetical sequence from `district_Ariyalur` to `district_Virudhunagar`:
$$\text{district\_}d = \begin{cases} 1 & \text{if } \text{district} = d \\ 0 & \text{otherwise} \end{cases}$$

---

## 3. Order Invariance Guarantee

The feature vector is generated deterministically through `FEATURE_COLUMNS_53`, eliminating any potential risk of column permutation during inference.
