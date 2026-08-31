import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

logger = logging.getLogger("feature_engineering")

CLIMATOLOGY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "feature_mappings", "district_climatology.json")

# The exact 38 Tamil Nadu districts in the exact one-hot alphabetical sequence expected by XGBoost models
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

FEATURE_COLUMNS_53 = [
    "temp_max", "temp_min", "temp_mean", "temp_range",
    "humidity", "wind_speed", "rainfall", "soil_wetness",
    "rainfall_3d", "rainfall_7d", "rainfall_30d",
    "temp_anomaly", "rainfall_anomaly", "SPI_3", "SPI_6"
] + [f"district_{d}" for d in DISTRICT_LIST]

class FeatureEngineeringService:
    _climatology: Dict[str, Any] = {}

    def __init__(self):
        self._load_climatology()

    def _load_climatology(self):
        if os.path.exists(CLIMATOLOGY_PATH):
            try:
                with open(CLIMATOLOGY_PATH, "r", encoding="utf-8") as f:
                    self._climatology = json.load(f)
                logger.info(f"Loaded climatology baselines for {len(self._climatology)} districts.")
            except Exception as e:
                logger.error(f"Failed to load climatology: {e}")
        else:
            logger.warning(f"Climatology file not found at {CLIMATOLOGY_PATH}")

    def get_district_baseline(self, district_name: str, month: int = 8) -> Dict[str, float]:
        name_clean = district_name.strip()
        for k, v in self._climatology.items():
            if k.lower() == name_clean.lower():
                monthly = v.get("monthly", {}).get(str(month), {})
                overall = v.get("overall", {})
                return {
                    "temp_max_mean": monthly.get("temp_max_mean", overall.get("temp_max_mean", 33.5)),
                    "temp_min_mean": monthly.get("temp_min_mean", overall.get("temp_min_mean", 24.0)),
                    "rainfall_daily_mean": monthly.get("rainfall_mean", overall.get("rainfall_daily_mean", 3.0)),
                    "rainfall_daily_std": monthly.get("rainfall_std", overall.get("rainfall_daily_std", 6.0)),
                    "humidity_mean": monthly.get("humidity_mean", overall.get("humidity_mean", 68.0)),
                    "wind_speed_mean": monthly.get("wind_speed_mean", overall.get("wind_speed_mean", 3.5)),
                    "soil_wetness_mean": monthly.get("soil_wetness_mean", overall.get("soil_wetness_mean", 0.45)),
                }

        return {
            "temp_max_mean": 33.5,
            "temp_min_mean": 24.0,
            "rainfall_daily_mean": 3.2,
            "rainfall_daily_std": 6.5,
            "humidity_mean": 68.0,
            "wind_speed_mean": 3.5,
            "soil_wetness_mean": 0.45
        }

    def build_feature_vector(
        self,
        district_name: str,
        day_index: int = 0,
        daily_forecast: Union[Dict[str, Any], List[Dict[str, Any]], None] = None,
        hourly_forecast: Union[Dict[str, Any], List[Dict[str, Any]], None] = None,
        forecast_day_index: Optional[int] = None,
        daily_forecast_list: Optional[List[Dict[str, Any]]] = None,
        hourly_forecast_list: Optional[List[Dict[str, Any]]] = None,
        historical_baseline: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Derives the exact 53-feature vector for a specific day in the forecast.
        Accepts daily and hourly data in both Open-Meteo dictionary and normalized list forms.
        """
        idx = day_index if forecast_day_index is None else forecast_day_index
        daily_input = daily_forecast if daily_forecast is not None else daily_forecast_list
        hourly_input = hourly_forecast if hourly_forecast is not None else hourly_forecast_list

        month = datetime.utcnow().month

        # Parse daily variables
        temp_max = 33.0
        temp_min = 24.0
        rainfall = 0.0
        wind_speed = 3.5
        all_daily_rain = []

        if isinstance(daily_input, dict):
            t_max_arr = daily_input.get("temperature_2m_max", [])
            t_min_arr = daily_input.get("temperature_2m_min", [])
            p_arr = daily_input.get("precipitation_sum", [])
            w_arr = daily_input.get("wind_speed_10m_max", [])

            if idx < len(t_max_arr): temp_max = float(t_max_arr[idx])
            if idx < len(t_min_arr): temp_min = float(t_min_arr[idx])
            if idx < len(p_arr): rainfall = float(p_arr[idx])
            if idx < len(w_arr): wind_speed = float(w_arr[idx])
            all_daily_rain = [float(p) for p in p_arr]
        elif isinstance(daily_input, list) and len(daily_input) > 0:
            day_info = daily_input[min(idx, len(daily_input) - 1)]
            temp_max = float(day_info.get("temp_max_c", 33.0))
            temp_min = float(day_info.get("temp_min_c", 24.0))
            rainfall = float(day_info.get("precipitation_sum_mm", 0.0))
            wind_speed = float(day_info.get("wind_speed_max_ms", 3.5))
            all_daily_rain = [float(d.get("precipitation_sum_mm", 0.0)) for d in daily_input]

        temp_mean = (temp_max + temp_min) / 2.0
        temp_range = max(0.0, temp_max - temp_min)

        # Parse hourly variables
        humidity = 68.0
        soil_wetness = 0.40

        if isinstance(hourly_input, dict):
            hum_arr = hourly_input.get("relative_humidity_2m", [])
            start_h = idx * 24
            end_h = min(start_h + 24, len(hum_arr))
            if start_h < len(hum_arr):
                day_hum = hum_arr[start_h:end_h]
                if day_hum:
                    humidity = sum(day_hum) / len(day_hum)
            soil_arr = hourly_input.get("soil_moisture_0_to_1cm", [])
            if soil_arr:
                soil_wetness = min(1.0, max(0.1, sum(soil_arr[:24]) / min(24, len(soil_arr))))
        elif isinstance(hourly_input, list) and len(hourly_input) > 0:
            h_vals = [h.get("humidity_pct", 68.0) for h in hourly_input]
            if h_vals:
                humidity = sum(h_vals) / len(h_vals)
            s_vals = [h.get("soil_moisture_fraction", 0.40) for h in hourly_input if "soil_moisture_fraction" in h]
            if s_vals:
                soil_wetness = sum(s_vals) / len(s_vals)

        # Multi-day precipitation accumulation
        if not all_daily_rain:
            all_daily_rain = [rainfall] * 7

        safe_idx = min(idx, len(all_daily_rain) - 1)
        start_3d = max(0, safe_idx - 1)
        end_3d = min(len(all_daily_rain), safe_idx + 2)
        rainfall_3d = sum(all_daily_rain[start_3d:end_3d])
        if len(all_daily_rain[start_3d:end_3d]) < 3:
            rainfall_3d += rainfall * (3 - len(all_daily_rain[start_3d:end_3d]))

        rainfall_7d = sum(all_daily_rain[:7])

        # Climatological baseline
        baseline = historical_baseline or self.get_district_baseline(district_name, month=month)
        rainfall_30d = rainfall_7d + (baseline["rainfall_daily_mean"] * 23.0)

        temp_anomaly = round(temp_max - baseline["temp_max_mean"], 2)
        rainfall_anomaly = round(rainfall - baseline["rainfall_daily_mean"], 2)

        # Standardized Precipitation Index estimate
        expected_90d = baseline["rainfall_daily_mean"] * 90.0
        std_90d = baseline["rainfall_daily_std"] * (90.0 ** 0.5)
        est_90d = (rainfall_30d * 3.0)
        spi_3 = round((est_90d - expected_90d) / (std_90d if std_90d > 0.1 else 10.0), 3)

        expected_180d = baseline["rainfall_daily_mean"] * 180.0
        std_180d = baseline["rainfall_daily_std"] * (180.0 ** 0.5)
        est_180d = (rainfall_30d * 6.0)
        spi_6 = round((est_180d - expected_180d) / (std_180d if std_180d > 0.1 else 20.0), 3)

        # District One-Hot Encodings (38 columns)
        district_normalized = district_name.strip()
        one_hot = {}
        for d in DISTRICT_LIST:
            col_name = f"district_{d}"
            one_hot[col_name] = 1 if d.lower() == district_normalized.lower() else 0

        # Construct full 53-feature dictionary
        features_dict = {
            "temp_max": round(temp_max, 2),
            "temp_min": round(temp_min, 2),
            "temp_mean": round(temp_mean, 2),
            "temp_range": round(temp_range, 2),
            "humidity": round(humidity, 2),
            "wind_speed": round(wind_speed, 2),
            "rainfall": round(rainfall, 2),
            "soil_wetness": round(soil_wetness, 3),
            "rainfall_3d": round(rainfall_3d, 2),
            "rainfall_7d": round(rainfall_7d, 2),
            "rainfall_30d": round(rainfall_30d, 2),
            "temp_anomaly": temp_anomaly,
            "rainfall_anomaly": rainfall_anomaly,
            "SPI_3": spi_3,
            "SPI_6": spi_6,
            **one_hot
        }

        # Build strict ordered list of 53 values
        features_vector = [features_dict[col] for col in FEATURE_COLUMNS_53]

        return {
            "features_dict": features_dict,
            "features_vector": features_vector,
            "feature_vector": features_vector,
            "feature_names": FEATURE_COLUMNS_53,
            "baseline": baseline
        }
