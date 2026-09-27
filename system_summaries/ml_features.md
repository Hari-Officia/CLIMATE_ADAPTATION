# Machine Learning 53-Feature Vector Specification Summary

## 📊 Overview
The **Machine Learning Feature Engineering Subsystem** (`backend/services/feature_engineering.py`) constructs a strict, ordered **53-feature vector** used as input for all multi-hazard XGBoost models. It transforms raw 7-day NWP weather forecasts into scaled, anomaly-calibrated indicators combined with district identity encodings.

---

## 📑 Feature Breakdown (53 Columns)

```
Total 53 Features = 15 Core Climate/Hydrological Features + 38 District One-Hot Features
```

### 1. Core Climate & Hydrological Features (Index 0 to 14)

| Index | Feature Column Name | Unit | Range / Format | Description & Formula |
|---|---|---|---|---|
| `0` | `temp_max` | °C | `15.0 - 50.0` | Maximum daily 2m air temperature |
| `1` | `temp_min` | °C | `10.0 - 35.0` | Minimum daily 2m air temperature |
| `2` | `temp_mean` | °C | `12.5 - 42.5` | Mean daily temperature: $(T_{\max} + T_{\min}) / 2$ |
| `3` | `temp_range` | °C | `2.0 - 25.0` | Diurnal temperature range: $T_{\max} - T_{\min}$ |
| `4` | `humidity` | % | `10.0 - 100.0` | Relative humidity at 2m height |
| `5` | `wind_speed` | m/s | `0.0 - 60.0` | Maximum 10m wind speed |
| `6` | `rainfall` | mm | `0.0 - 500.0` | Daily 24-hour total precipitation sum |
| `7` | `soil_wetness` | fraction | `0.0 - 1.0` | Volumetric soil moisture content (0-1cm depth) |
| `8` | `rainfall_3d` | mm | `0.0 - 800.0` | 3-day moving cumulative rainfall accumulation |
| `9` | `rainfall_7d` | mm | `0.0 - 1200.0` | 7-day moving cumulative rainfall accumulation |
| `10` | `rainfall_30d` | mm | `0.0 - 2500.0` | 30-day estimated rainfall accumulation |
| `11` | `temp_anomaly` | °C | `-10.0 - +15.0` | $T_{\max}$ departure from 30-year district baseline |
| `12` | `rainfall_anomaly` | mm | `-50.0 - +300.0` | Daily rainfall departure from district baseline |
| `13` | `SPI_3` | z-score | `-4.0 - +4.0` | 3-Month Standardized Precipitation Index estimate |
| `14` | `SPI_6` | z-score | `-4.0 - +4.0` | 6-Month Standardized Precipitation Index estimate |

---

### 2. District One-Hot Encoded Features (Index 15 to 52)

Alphabetical sequence of 38 binary columns ($0$ or $1$) representing district identity:

`district_Ariyalur`, `district_Chengalpattu`, `district_Chennai`, `district_Coimbatore`, `district_Cuddalore`, `district_Dharmapuri`, `district_Dindigul`, `district_Erode`, `district_Kallakurichi`, `district_Kancheepuram`, `district_Kanniyakumari`, `district_Karur`, `district_Krishnagiri`, `district_Madurai`, `district_Mayiladuthurai`, `district_Nagapattinam`, `district_Namakkal`, `district_Nilgiris`, `district_Perambalur`, `district_Pudukkottai`, `district_Ramanathapuram`, `district_Ranipet`, `district_Salem`, `district_Sivaganga`, `district_Tenkasi`, `district_Thanjavur`, `district_Theni`, `district_Thoothukudi`, `district_Tiruchirappalli`, `district_Tirunelveli`, `district_Tirupathur`, `district_Tiruppur`, `district_Tiruvallur`, `district_Tiruvannamalai`, `district_Tiruvarur`, `district_Vellore`, `district_Viluppuram`, `district_Virudhunagar`.

---

## 💻 Minimal Code Example

```python
# backend/services/feature_engineering.py
class FeatureEngineeringService:
    DISTRICT_LIST = [
        "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
        "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kancheepuram",
        "Kanniyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
        "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
        "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi",
        "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
        "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur",
        "Vellore", "Viluppuram", "Virudhunagar"
    ]

    def build_53_feature_vector(self, district_name: str, daily_data: dict, baseline: dict) -> list:
        t_max = daily_data.get("temp_max", 33.0)
        t_min = daily_data.get("temp_min", 24.0)
        rain = daily_data.get("rainfall", 0.0)
        
        # 15 Climate Core Features
        core = [
            t_max, t_min, (t_max + t_min)/2.0, max(0.0, t_max - t_min),
            daily_data.get("humidity", 68.0), daily_data.get("wind_speed", 3.5),
            rain, daily_data.get("soil_wetness", 0.45),
            daily_data.get("rainfall_3d", rain * 3), daily_data.get("rainfall_7d", rain * 7),
            daily_data.get("rainfall_30d", rain * 30),
            round(t_max - baseline.get("temp_max_mean", 33.0), 2),
            round(rain - baseline.get("rainfall_daily_mean", 3.0), 2),
            0.15, 0.25 # SPI_3, SPI_6 estimates
        ]
        
        # 38 District One-Hot Encodings
        one_hot = [1 if d.lower() == district_name.lower().strip() else 0 for d in self.DISTRICT_LIST]
        
        feature_vector = core + one_hot
        assert len(feature_vector) == 53, f"Expected 53 features, got {len(feature_vector)}"
        return feature_vector
```
