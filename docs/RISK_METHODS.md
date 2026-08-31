# Scientific Risk Calculation Methods

## 1. Overview
The platform strictly segregates its analytical computations into three distinct architectural categories:
- **Type A: Machine Learning Classifiers** (Probabilistic inference with calibrated thresholds)
- **Type B: Deterministic Meteorological Rules & Physical Indices** (Direct physical threshold evaluation)
- **Type C: External Observational Monitoring & Warning Bulletins** (Direct sensor/agency reporting)

---

## 2. Detailed Method Formulations

### A. Type A: Machine Learning (XGBoost Ensemble)
- **Framework**: XGBoost 500-tree gradient boosted decision trees (`max_depth=6`, `subsample=0.8`, `colsample_bytree=0.8`).
- **Feature Schema**: Strict 53-dimensional vector (15 continuous climatological features + 38 alphabetical district one-hot columns).
- **Calibrated Probability Decision Boundary**:
  $$\text{Risk Level} = \begin{cases} \text{HIGH} & \text{if } P \ge 0.70 \\ \text{MEDIUM} & \text{if } 0.40 \le P < 0.70 \\ \text{LOW} & \text{if } P < 0.40 \end{cases}$$
- **Pre-condition Contract**: Validated through `FeatureContractValidator`. If required historical antecedent features (e.g. $\text{SPI}_3$, $\text{SPI}_6$) are unavailable, execution is stopped and flagged as `UNAVAILABLE`.

---

### B. Type B: Physical Rules & Meteorological Indices

#### 1. Extreme Rainfall (IMD Criteria)
- **Accumulation Windows**: 24-hour total, peak 1-hour burst, peak 3-hour sum.
- **Formulation**:
  $$\text{Risk Level} = \begin{cases} \text{SEVERE} & \text{if } R_{24\text{h}} \ge 204.5\text{ mm or } R_{3\text{h}} \ge 100\text{ mm} \\ \text{HIGH} & \text{if } R_{24\text{h}} \ge 115.6\text{ mm or } R_{3\text{h}} \ge 60\text{ mm or } R_{1\text{h}} \ge 35\text{ mm} \\ \text{MEDIUM} & \text{if } R_{24\text{h}} \ge 64.5\text{ mm or } R_{1\text{h}} \ge 20\text{ mm} \\ \text{LOW} & \text{otherwise} \end{cases}$$

#### 2. Extreme Wind (Beaufort / IMD Gale Criteria)
- **Variables**: Sustained 10m wind velocity ($V_{\text{sust}}$ in m/s) and peak wind gusts ($V_{\text{gust}}$ in m/s).
- **Formulation**:
  $$\text{Risk Level} = \begin{cases} \text{SEVERE} & \text{if } V_{\text{sust}} \ge 24.5\text{ m/s (89 km/h) or } V_{\text{gust}} \ge 30.0\text{ m/s} \\ \text{HIGH} & \text{if } V_{\text{sust}} \ge 17.2\text{ m/s (62 km/h) or } V_{\text{gust}} \ge 22.0\text{ m/s} \\ \text{MEDIUM} & \text{if } V_{\text{sust}} \ge 10.8\text{ m/s (39 km/h) or } V_{\text{gust}} \ge 15.0\text{ m/s} \\ \text{LOW} & \text{otherwise} \end{cases}$$

#### 3. Heat Stress (NOAA / NWS Heat Index)
- **Formulation**: Rothfusz multi-variate regression combining ambient temperature $T$ (°F) and relative humidity $RH$ (%):
  $$\text{HI} = -42.379 + 2.04901523 T + 10.14333127 RH - 0.22475541 T \cdot RH - 0.00683783 T^2 - 0.05481717 RH^2 + 0.00122874 T^2 RH + 0.00085282 T RH^2 - 0.00000199 T^2 RH^2$$
- **Health Risk Boundary**:
  - $\text{HI} \ge 54.0^\circ\text{C}$ ($130^\circ\text{F}$): SEVERE (Extreme Danger)
  - $\text{HI} \ge 41.0^\circ\text{C}$ ($106^\circ\text{F}$): HIGH (Danger)
  - $\text{HI} \ge 32.8^\circ\text{C}$ ($91^\circ\text{F}$): MEDIUM (Extreme Caution)
  - $\text{HI} < 32.8^\circ\text{C}$: LOW (Caution / Normal)

#### 4. Coastal Hazard (INCOIS / WMO Sea State Criteria)
- **Applicability Rule**: Strictly enabled for coastal administrative districts (`coastal = True`); returns `NOT_APPLICABLE` for inland districts.
- **Formulation**:
  $$\text{Risk Level} = \begin{cases} \text{SEVERE} & \text{if } H_s \ge 4.0\text{ m (Rough to High)} \\ \text{HIGH} & \text{if } H_s \ge 2.5\text{ m (Rough - Fishermen Warning)} \\ \text{MEDIUM} & \text{if } H_s \ge 1.25\text{ m (Moderate - Small Craft Advisory)} \\ \text{LOW} & \text{if } H_s < 1.25\text{ m (Smooth / Slight)} \end{cases}$$

---

### C. Type C: External Monitoring & Warning Bulletins

#### 1. Air Quality Status
- **Standard**: US Environmental Protection Agency (EPA) AQI scale using real-time pollutant observations ($\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$).
- **Output**: Categorized environmental index (`Good`, `Moderate`, `Unhealthy for Sensitive Groups`, `Unhealthy`, `Very Unhealthy`, `Hazardous`).

#### 2. Tropical Cyclone Advisory
- **Protocol**: Direct ingestion of IMD Regional Specialized Meteorological Centre (RSMC) tropical cyclone advisories.
- **Output**: Official alert stage (`NO ACTIVE CYCLONE ALERT`, `WATCH`, `WARNING`).
