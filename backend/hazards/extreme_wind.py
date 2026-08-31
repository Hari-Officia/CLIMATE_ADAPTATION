from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult

class ExtremeWindHazard(BaseHazard):
    """
    Type B: Scientific / Rule-Based Extreme Wind & Gale Module.
    Evaluates sustained wind speeds and peak gusts against IMD / Beaufort scale thresholds.
    """
    def __init__(self):
        super().__init__(
            hazard_id="extreme_wind",
            hazard_name="Extreme Wind",
            engine_type="rule_based",
            description="Evaluates sustained 10m wind velocity and gusts against IMD and Beaufort gale criteria.",
            temporal_resolution="hourly",
            spatial_resolution="Point / District"
        )

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
        daily_max_winds = forecast_daily.get("wind_speed_10m_max", [])
        daily_max_gusts = forecast_daily.get("wind_gusts_10m_max", [])

        sustained = daily_max_winds[day_index] if day_index < len(daily_max_winds) else 3.0
        gust = daily_max_gusts[day_index] if day_index < len(daily_max_gusts) else (sustained * 1.4)

        sustained_kmh = sustained * 3.6
        gust_kmh = gust * 3.6

        # Beaufort & IMD Thresholds:
        # Sustained >= 24.5 m/s (89 km/h) or Gust >= 30 m/s: Storm Force (SEVERE)
        # Sustained >= 17.2 m/s (62 km/h) or Gust >= 22 m/s: Gale Force (HIGH)
        # Sustained >= 10.8 m/s (39 km/h) or Gust >= 15 m/s: Strong Breeze (MEDIUM)
        if sustained >= 24.5 or gust >= 30.0:
            level = "SEVERE"
            threshold_note = "IMD Storm / Violent Gale Force (≥ 89 km/h)"
        elif sustained >= 17.2 or gust >= 22.0:
            level = "HIGH"
            threshold_note = "IMD Gale Warning (62–88 km/h)"
        elif sustained >= 10.8 or gust >= 15.0:
            level = "MEDIUM"
            threshold_note = "Strong Breeze / High Wind Advisory (39–61 km/h)"
        else:
            level = "LOW"
            threshold_note = "Gentle to Moderate Breeze (< 39 km/h)"

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="IMD & Beaufort Wind Scale (10m sustained velocity + max gusts)",
            status="AVAILABLE",
            risk_level=level,
            value=round(sustained_kmh, 1),
            display_value=f"{sustained_kmh:.0f} km/h (gust {gust_kmh:.0f})",
            unit="km/h",
            probability=None,
            source="Open-Meteo 10m Wind & Gust Forecast",
            confidence_note=threshold_note,
            explanation=f"Peak sustained wind is {sustained_kmh:.0f} km/h ({sustained:.1f} m/s) with gusts up to {gust_kmh:.0f} km/h. Classified as {level}.",
            details={
                "sustained_ms": round(sustained, 1),
                "sustained_kmh": round(sustained_kmh, 1),
                "gust_ms": round(gust, 1),
                "gust_kmh": round(gust_kmh, 1),
                "threshold_applied": threshold_note
            }
        )
