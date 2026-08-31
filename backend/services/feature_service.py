class FeatureService:
    @staticmethod
    def derive_features(forecast_data: dict):
        """
        Derives model features from Open-Meteo forecast data.

        Forecast API response structure (Open-Meteo):
        hourly: temperature_2m, relative_humidity_2m, precipitation, surface_pressure,
                wind_speed_10m, soil_moisture_0_to_1cm, soil_moisture_1_to_3cm
        daily: temperature_2m_max, temperature_2m_min
        """
        hourly = forecast_data.get("hourly", {})
        daily = forecast_data.get("daily", {})

        # 1. Temperature max/min/mean/range
        # Note: Open-Meteo provides daily max/min directly.
        # Mean/Range need to be derived from these.

        t_max = daily.get("temperature_2m_max", [0.0])[0]
        t_min = daily.get("temperature_2m_min", [0.0])[0]
        t_mean = (t_max + t_min) / 2
        t_range = t_max - t_min

        # 2. Daily precipitation sum
        precipitation = sum(hourly.get("precipitation", [0.0]))

        # 3. Aggregates and other features
        # NOTE: Without historical baseline (SPI_3/6, anomalies),
        # these will be placeholders for now to keep the pipeline functional.

        return {
            "temp_max": float(t_max),
            "temp_min": float(t_min),
            "temp_mean": float(t_mean),
            "temp_range": float(t_range),
            "humidity": float(hourly.get("relative_humidity_2m", [0.0])[0]),
            "wind_speed": float(hourly.get("wind_speed_10m", [0.0])[0]),
            "rainfall": float(precipitation),
            "soil_wetness": float(hourly.get("soil_moisture_0_to_1cm", [0.0])[0]),
            "rainfall_3d": 0.0, # Placeholder
            "rainfall_7d": 0.0, # Placeholder
            "rainfall_30d": 0.0, # Placeholder
            "temp_anomaly": 0.0, # Placeholder
            "rainfall_anomaly": 0.0, # Placeholder
            "SPI_3": 0.0, # Placeholder
            "SPI_6": 0.0  # Placeholder
        }
