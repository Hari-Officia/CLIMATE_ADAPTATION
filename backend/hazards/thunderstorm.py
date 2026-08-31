from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult

class ThunderstormHazard(BaseHazard):
    """
    Type B: Convective Storm & Lightning Risk Module.
    Uses WMO weather interpretation codes and peak convective gusts.
    """
    def __init__(self):
        super().__init__(
            hazard_id="thunderstorm",
            hazard_name="Thunderstorm Risk",
            engine_type="rule_based",
            description="Evaluates atmospheric instability and convective storm activity from WMO weather codes and gust velocities.",
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
        daily_codes = forecast_daily.get("weather_code", [])
        day_code = daily_codes[day_index] if day_index < len(daily_codes) else 0

        hourly_codes = forecast_hourly.get("weather_code", [])
        start_h = day_index * 24
        end_h = min(start_h + 24, len(hourly_codes))
        day_hourly_codes = set(hourly_codes[start_h:end_h]) if start_h < len(hourly_codes) else {day_code}

        daily_gusts = forecast_daily.get("wind_gusts_10m_max", [])
        max_gust = daily_gusts[day_index] if day_index < len(daily_gusts) else 6.0

        # WMO Thunderstorm Codes: 95 = Thunderstorm, 96 = with slight hail, 99 = with heavy hail
        has_severe_thunder = 99 in day_hourly_codes or (hasattr(day_code, '__eq__') and day_code == 99)
        has_thunder = any(c in day_hourly_codes for c in [95, 96, 99]) or day_code in [95, 96, 99]

        if has_severe_thunder or (has_thunder and max_gust >= 22.0):
            level = "HIGH"
            display = "High Convective Risk"
            note = "Active Thunderstorm with Severe Gusts / Hail threat"
        elif has_thunder or max_gust >= 18.0:
            level = "MEDIUM"
            display = "Moderate Convective Risk"
            note = "Scattered Convective Storms / Squalls possible"
        else:
            level = "LOW"
            display = "Low Convective Risk"
            note = "Stable atmospheric boundary layer"

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="WMO Convective Code & Boundary Layer Instability Assessment",
            status="AVAILABLE",
            risk_level=level,
            value=None,
            display_value=display,
            unit=None,
            probability=None,
            source="Open-Meteo Weather Codes & Gusts",
            confidence_note=note,
            explanation=f"Forecast indicates {note.lower()} (peak gust {max_gust * 3.6:.0f} km/h).",
            details={
                "wmo_code": day_code,
                "peak_gust_ms": max_gust,
                "thunder_detected": has_thunder
            }
        )
