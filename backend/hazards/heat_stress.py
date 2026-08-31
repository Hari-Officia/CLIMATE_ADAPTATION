from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult

class HeatStressHazard(BaseHazard):
    """
    Type B: Scientific / Index-Based Heat Stress Module.
    Calculates physiological Heat Index and Apparent Temperature using NOAA / NWS formulation.
    Separate from multi-day heatwave climatological departure.
    """
    def __init__(self):
        super().__init__(
            hazard_id="heat_stress",
            hazard_name="Heat Stress",
            engine_type="rule_based",
            description="Evaluates human thermal stress using NOAA / NWS Heat Index combining ambient temperature and relative humidity.",
            temporal_resolution="hourly & daily",
            spatial_resolution="Point / District"
        )

    def _calculate_heat_index(self, temp_c: float, humidity_pct: float) -> float:
        """Calculates NOAA Heat Index in Celsius via the Rothfusz regression equation."""
        t_f = (temp_c * 9.0 / 5.0) + 32.0
        rh = max(0.0, min(100.0, humidity_pct))

        # Simple formula for cooler conditions
        hi_simple = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh * 0.094))
        if hi_simple < 80.0:
            hi_f = hi_simple
        else:
            # Rothfusz multi-term regression equation
            hi_f = (
                -42.379
                + 2.04901523 * t_f
                + 10.14333127 * rh
                - 0.22475541 * t_f * rh
                - 0.00683783 * (t_f ** 2)
                - 0.05481717 * (rh ** 2)
                + 0.00122874 * (t_f ** 2) * rh
                + 0.00085282 * t_f * (rh ** 2)
                - 0.00000199 * (t_f ** 2) * (rh ** 2)
            )

        hi_c = (hi_f - 32.0) * 5.0 / 9.0
        return max(temp_c, round(hi_c, 1))

    def calculate(
        self,
        district_name: str,
        day_index: int,
        forecast_daily: Dict[str, Any],
        forecast_hourly: Dict[str, Any],
        district_profile: Optional[Dict[str, Any]] = None,
        historical_baseline: Optional[Dict[str, Any]] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> HazardResult:
        daily_highs = forecast_daily.get("temperature_2m_max", [])
        temp_max = daily_highs[day_index] if day_index < len(daily_highs) else 32.0

        # Peak afternoon humidity approximation
        hourly_hum = forecast_hourly.get("relative_humidity_2m", [])
        start_h = day_index * 24
        end_h = min(start_h + 24, len(hourly_hum))
        day_hum = hourly_hum[start_h:end_h] if start_h < len(hourly_hum) else [60.0]
        # Afternoon relative humidity typically at minimum
        avg_hum = sum(day_hum) / len(day_hum) if day_hum else 60.0
        peak_hi = self._calculate_heat_index(temp_max, avg_hum * 0.85)

        # NOAA Heat Index Risk Tiers:
        # >= 54.0°C (130°F): Extreme Danger (SEVERE)
        # >= 41.0°C (106°F): Danger (HIGH)
        # >= 32.8°C (91°F): Extreme Caution (MEDIUM)
        # Else: LOW / Caution
        if peak_hi >= 54.0:
            level = "SEVERE"
            threshold_note = "NOAA Extreme Danger (Heat stroke imminent)"
        elif peak_hi >= 41.0:
            level = "HIGH"
            threshold_note = "NOAA Danger (Heat cramps or heat exhaustion likely)"
        elif peak_hi >= 32.8:
            level = "MEDIUM"
            threshold_note = "NOAA Extreme Caution (Sunstroke or muscle cramps possible)"
        else:
            level = "LOW"
            threshold_note = "Normal physiological comfort range"

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="NOAA / NWS Rothfusz Heat Index Regression",
            status="AVAILABLE",
            risk_level=level,
            value=round(peak_hi, 1),
            display_value=f"{peak_hi:.1f}°C Heat Index",
            unit="°C",
            probability=None,
            source="Open-Meteo Temperature & Relative Humidity",
            confidence_note=threshold_note,
            explanation=f"Ambient maximum temperature of {temp_max:.1f}°C feels like {peak_hi:.1f}°C under {int(avg_hum)}% humidity. Classified as {level}.",
            details={
                "ambient_temp_c": round(temp_max, 1),
                "relative_humidity_pct": int(round(avg_hum)),
                "heat_index_c": round(peak_hi, 1),
                "threshold_applied": threshold_note
            }
        )
