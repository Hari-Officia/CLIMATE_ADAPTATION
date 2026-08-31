from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult

class ExtremeRainfallHazard(BaseHazard):
    """
    Type B: Scientific / Rule-Based Extreme Rainfall Module.
    Uses official India Meteorological Department (IMD) accumulation thresholds.
    Never outputs a pseudo-probability; outputs physical rainfall depth and risk tier.
    """
    def __init__(self):
        super().__init__(
            hazard_id="extreme_rainfall",
            hazard_name="Extreme Rainfall",
            engine_type="rule_based",
            description="Evaluates 24-hour and short-duration precipitation against official IMD meteorological thresholds.",
            temporal_resolution="hourly & daily",
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
        daily_sums = forecast_daily.get("precipitation_sum", [])
        rain_24h = daily_sums[day_index] if day_index < len(daily_sums) else 0.0

        # Extract 24-hour window from hourly forecast if available
        hourly_precip = forecast_hourly.get("precipitation", [])
        start_h = day_index * 24
        end_h = min(start_h + 24, len(hourly_precip))
        day_hourly = hourly_precip[start_h:end_h] if start_h < len(hourly_precip) else []

        max_1h = max(day_hourly) if day_hourly else (rain_24h / 24.0)

        # 3-hour rolling max
        max_3h = 0.0
        if len(day_hourly) >= 3:
            for i in range(len(day_hourly) - 2):
                max_3h = max(max_3h, sum(day_hourly[i:i+3]))
        else:
            max_3h = max_1h * 2.0

        # IMD Threshold Evaluation
        # >= 204.5 mm: Extremely Heavy (Severe / Red)
        # >= 115.6 mm: Very Heavy (High / Orange)
        # >= 64.5 mm: Heavy (Medium / Yellow)
        # Short burst override: 1h >= 30mm or 3h >= 60mm
        if rain_24h >= 204.5 or max_3h >= 100.0:
            level = "SEVERE"
            threshold_note = "IMD Extremely Heavy Rain (≥ 204.5 mm/24h)"
        elif rain_24h >= 115.6 or max_3h >= 60.0 or max_1h >= 35.0:
            level = "HIGH"
            threshold_note = "IMD Very Heavy Rain (≥ 115.6 mm/24h or torrential burst)"
        elif rain_24h >= 64.5 or max_1h >= 20.0:
            level = "MEDIUM"
            threshold_note = "IMD Heavy Rain Advisory (≥ 64.5 mm/24h)"
        else:
            level = "LOW"
            threshold_note = "Light to Moderate Rainfall (< 64.5 mm/24h)"

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="IMD Rainfall Threshold Evaluation (1h, 3h, 24h accumulation)",
            status="AVAILABLE",
            risk_level=level,
            value=round(rain_24h, 1),
            display_value=f"{rain_24h:.1f} mm/24h",
            unit="mm/24h",
            probability=None,  # Rule-based scores must never be labeled as probability
            source="Open-Meteo NWP Precipitation",
            confidence_note=threshold_note,
            explanation=f"24-hour forecast rainfall is {rain_24h:.1f} mm (peak 1h: {max_1h:.1f} mm, peak 3h: {max_3h:.1f} mm). Classified as {level}.",
            details={
                "rain_24h_mm": round(rain_24h, 1),
                "peak_1h_mm": round(max_1h, 1),
                "peak_3h_mm": round(max_3h, 1),
                "threshold_applied": threshold_note
            }
        )
