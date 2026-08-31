# Climate Hazard Thresholds & Scientific Sources

## 1. Overview
All hazard calculations in the Quantum Multi-Agent Climate Risk Decision Support System adhere strictly to authoritative scientific guidelines and official meteorological standards. No thresholds are arbitrary.

---

## 2. Threshold Specifications by Hazard

### A. Extreme Rainfall (Source: India Meteorological Department — IMD)
The IMD defines rainfall intensity categories for 24-hour accumulated rainfall:

| Category | 24-Hour Rainfall (mm) | Operational Classification |
|---|---|---|
| Light to Moderate | $0.1 - 64.4$ | LOW |
| Heavy Rain | $64.5 - 115.5$ | MEDIUM / ADVISORY |
| Very Heavy Rain | $115.6 - 204.4$ | HIGH / WARNING |
| Extremely Heavy Rain | $\ge 204.5$ | SEVERE / RED ALERT |

Short-Duration Intensity Checks (Flash Flood Potential):
- 1-hour accumulation: $\ge 30.0$ mm (Torrential Burst)
- 3-hour accumulation: $\ge 60.0$ mm (Urban Waterlogging Threat)

### B. Extreme Wind & Gale (Source: IMD & World Meteorological Organization — WMO / Beaufort Scale)

| Classification | Sustained Wind Speed | Wind Gusts | Operational Risk Level |
|---|---|---|---|
| Normal Breeze | $< 10.8$ m/s ($< 39$ km/h) | $< 15.0$ m/s | LOW |
| Strong Wind / High Wind | $10.8 - 17.1$ m/s ($39 - 61$ km/h) | $15.0 - 22.0$ m/s | MEDIUM (Caution for structures/fishermen) |
| Gale / Severe Gale | $17.2 - 24.4$ m/s ($62 - 88$ km/h) | $22.0 - 30.0$ m/s | HIGH (Tree branches break, structural damage) |
| Storm / Violent Storm | $\ge 24.5$ m/s ($\ge 89$ km/h) | $\ge 30.0$ m/s | SEVERE (Widespread destruction) |

### C. Heat Stress & Apparent Temperature (Source: NOAA / National Weather Service — NWS)
Derived using the Rothfusz Heat Index regression and Steadman apparent temperature:

| Heat Index Range | Classification | Health & Physiological Effect |
|---|---|---|
| $< 27.0^\circ\text{C}$ ($< 80^\circ\text{F}$) | Normal | Safe operating conditions |
| $27.0 - 32.7^\circ\text{C}$ ($80 - 90^\circ\text{F}$) | Caution | Fatigue possible with prolonged exposure |
| $32.8 - 41.0^\circ\text{C}$ ($91 - 105^\circ\text{F}$) | Extreme Caution | Sunstroke, muscle cramps, and heat exhaustion possible |
| $41.1 - 54.0^\circ\text{C}$ ($106 - 130^\circ\text{F}$) | Danger | Sunstroke highly likely, heat cramps imminent |
| $\ge 54.1^\circ\text{C}$ ($\ge 130^\circ\text{F}$) | Extreme Danger | Heat stroke / sunstroke imminent |

### D. Coastal & Marine Hazard (Source: INCOIS / WMO Sea State Code)
Applied strictly to coastal districts:

| Significant Wave Height | Sea State Classification | Operational Risk Level |
|---|---|---|
| $< 1.25$ m | Smooth / Slight | LOW (Safe for all craft) |
| $1.25 - 2.50$ m | Moderate | MEDIUM (Small craft advisory) |
| $2.50 - 4.00$ m | Rough | HIGH (Fishermen warned not to venture out) |
| $\ge 4.00$ m | Very Rough to High | SEVERE (Coastal surge threat) |

### E. Air Quality (Source: US Environmental Protection Agency — EPA Air Quality Index)

| AQI Range | Descriptor | Health Advisory |
|---|---|---|
| $0 - 50$ | Good | Air quality is satisfactory |
| $51 - 100$ | Moderate | Acceptable air quality |
| $101 - 150$ | Unhealthy for Sensitive Groups | Sensitive individuals may experience respiratory irritation |
| $151 - 200$ | Unhealthy | Everyone may begin to experience health effects |
| $201 - 300$ | Very Unhealthy | Health alert: serious effects |
| $\ge 301$ | Hazardous | Emergency conditions |

### F. Machine Learning Calibrated Risk Thresholds (Flood, Heatwave, Drought)

| Model | Framework | Low Risk | Medium Risk | High Risk |
|---|---|---|---|---|
| Flood Classifier | XGBoost | $P < 0.40$ | $0.40 \le P < 0.70$ | $P \ge 0.70$ |
| Heatwave Classifier | XGBoost | $P < 0.40$ | $0.40 \le P < 0.70$ | $P \ge 0.70$ |
| Drought Classifier | XGBoost | $P < 0.40$ | $0.40 \le P < 0.70$ | $P \ge 0.70$ |
