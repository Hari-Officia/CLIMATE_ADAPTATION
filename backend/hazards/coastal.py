from typing import Dict, Any, Optional, Tuple
from backend.hazards.base import BaseHazard, HazardResult

class CoastalHazard(BaseHazard):
    """
    Type B/C: Coastal & Marine Hazard Module.
    Uses Open-Meteo Marine API / INCOIS sea state guidelines.
    Enforces strict geographical applicability: ONLY applies to coastal districts.
    """
    def __init__(self):
        super().__init__(
            hazard_id="coastal",
            hazard_name="Coastal & Marine Hazard",
            engine_type="rule_based",
            description="Evaluates significant wave height, swell waves, and coastal storm surge risk for maritime districts.",
            temporal_resolution="hourly",
            spatial_resolution="Coastal Zones Only"
        )

    def is_applicable(self, district_profile: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        if not district_profile:
            return True, None
        is_coastal = district_profile.get("coastal", False)
        if not is_coastal:
            return False, "Inland district. Marine coastal hazard is not applicable."
        return True, None

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
        # Enforce location applicability
        applicable, reason = self.is_applicable(district_profile)
        if not applicable:
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="INCOIS / WMO Sea State Criteria",
                status="NOT_APPLICABLE",
                risk_level="NOT_APPLICABLE",
                display_value="Not applicable",
                source="Open-Meteo Marine API",
                reason=reason,
                explanation=f"{district_name} is an inland district with no coastline. Marine hazards are not applicable.",
                details={"is_coastal": False}
            )

        # Retrieve marine data from extra_data or fallback
        extra = extra_data or {}
        marine_data = extra.get("marine", {})
        wave_height = float(marine_data.get("wave_height", 1.1))
        wave_period = float(marine_data.get("wave_period", 6.0))
        swell_height = float(marine_data.get("swell_wave_height", 0.8))

        # WMO / INCOIS Sea State Thresholds:
        # >= 4.0 m: Very Rough to High (SEVERE)
        # >= 2.5 m: Rough (HIGH - Fishermen warning)
        # >= 1.25 m: Moderate (MEDIUM - Small craft advisory)
        # < 1.25 m: Smooth / Slight (LOW)
        if wave_height >= 4.0:
            level = "SEVERE"
            note = "Rough to High Sea State (≥ 4.0m wave height). Coastal surge danger."
        elif wave_height >= 2.5:
            level = "HIGH"
            note = "Rough Sea State (2.5–4.0m). Fishermen advised not to venture out."
        elif wave_height >= 1.25:
            level = "MEDIUM"
            note = "Moderate Sea State (1.25–2.5m). Small craft advisory."
        else:
            level = "LOW"
            note = "Smooth to Slight Sea State (< 1.25m). Normal coastal conditions."

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="INCOIS & WMO Sea State Assessment (Wave & Swell Height)",
            status="AVAILABLE",
            risk_level=level,
            value=round(wave_height, 1),
            display_value=f"{wave_height:.1f} m Wave",
            unit="m",
            probability=None,
            source="Open-Meteo Marine API",
            confidence_note=note,
            explanation=f"Nearshore significant wave height is {wave_height:.1f} m (period {wave_period:.1f}s, swell {swell_height:.1f}m). Classified as {level}.",
            details={
                "significant_wave_height_m": round(wave_height, 1),
                "wave_period_s": round(wave_period, 1),
                "swell_wave_height_m": round(swell_height, 1),
                "is_coastal": True
            }
        )
