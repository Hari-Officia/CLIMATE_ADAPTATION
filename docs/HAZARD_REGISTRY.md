# Extensible Climate Hazard Registry

## 1. Overview
The Climate Risk Intelligence Platform employs an open, modular Hazard Architecture. Every hazard implements the common `Hazard` base class and is managed by the `HazardRegistry`.

---

## 2. Master Registry of Hazards

| ID | Hazard Name | Engine Type | Method | Key Variables | Spatial Scope |
|---|---|---|---|---|---|
| `flood` | Flood Risk | Type A | Trained ML (XGBoost) | 53-Feature Vector (Precipitation windows, anomalies, soil wetness) | All Districts |
| `heatwave` | Heatwave Risk | Type A | Trained ML (XGBoost) | 53-Feature Vector ($T_{\max}$, temperature departure) | All Districts |
| `drought` | Drought Risk | Type A | Trained ML (XGBoost) | 53-Feature Vector ($\text{SPI}_3$, $\text{SPI}_6$, rainfall anomaly) | All Districts |
| `extreme_rain` | Extreme Rainfall | Type B | Scientific Rule / IMD Thresholds | Hourly/Daily Precipitation Sums (1h, 3h, 6h, 24h) | All Districts |
| `extreme_wind` | Extreme Wind | Type B | Scientific Rule / Beaufort Scale | 10m Wind Speed, Wind Gusts | All Districts |
| `heat_stress` | Heat Stress | Type B | Scientific Index / NOAA Heat Index | $T_{\text{air}}$, Relative Humidity, Dew Point, Apparent Temp | All Districts |
| `thunderstorm` | Thunderstorm Risk | Type B | Convective Rules & WMO Codes | Weather Codes, Wind Gusts, Convective Indicators | All Districts |
| `coastal` | Coastal & Marine Hazard | Type B/C | Marine API + INCOIS Sea State | Significant Wave Height, Swell Height, Wave Period | **Coastal Districts Only** |
| `air_quality` | Air Quality Status | Type C | External Observation (Open-Meteo AQI) | $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, US-AQI | All Districts |
| `cyclone` | Cyclone Advisory | Type C | Authoritative Meteorological Warning | Distance to Track, Central Pressure, IMD Advisories | All Districts |

---

## 3. Engine Type Classification & UI Presentation

1. **Type A: Trained ML Model (`ml_probability`)**:
   - Output: Calibrated Probability (e.g. `0.76` $\rightarrow$ `76%`).
   - UI Badge: `ML Model`.
   - Contract Enforced: Validates against model feature contract before prediction. If required features are unavailable, returns `risk_status = "UNAVAILABLE"`.

2. **Type B: Scientific / Rule-Based Index (`rule_based`)**:
   - Output: Physical Value + Metric Unit (e.g. `124.5 mm/24h` or `42.5°C Heat Index`) + Risk Category (`LOW`, `MEDIUM`, `HIGH`, `SEVERE`).
   - UI Badge: `Rule-based` or `Scientific Index`.
   - **Crucial Rule**: NEVER labeled or displayed as a "probability".

3. **Type C: External Data / Advisory (`external_source`)**:
   - Output: Current measured state or official agency alert status (e.g. `AQI 65 (Moderate)` or `NO ACTIVE CYCLONE ALERT`).
   - UI Badge: `External API` or `Official Advisory`.
