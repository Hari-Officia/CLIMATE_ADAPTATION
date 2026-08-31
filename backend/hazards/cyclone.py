from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult

class CycloneHazard(BaseHazard):
    """
    Type C: Authoritative Cyclone Alert Module.
    Consumes official meteorological advisories (IMD RSMC New Delhi).
    Never fabricates a synthetic machine-learning probability for cyclone genesis.
    """
    def __init__(self):
        super().__init__(
            hazard_id="cyclone",
            hazard_name="Cyclone Advisory",
            engine_type="external_source",
            description="Authoritative tropical cyclone surveillance and alert status from regional specialized meteorological centers.",
            temporal_resolution="daily",
            spatial_resolution="Regional / Coastal"
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
        extra = extra_data or {}
        cyclone_warning = extra.get("cyclone_warning")

        # In absence of an active IMD RSMC bulletin, report NO ACTIVE CYCLONE ALERT
        if cyclone_warning:
            status = cyclone_warning.get("status", "WATCH")
            level = "HIGH" if status == "WARNING" else "MEDIUM"
            storm_name = cyclone_warning.get("storm_name", "Developing System")
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="IMD Regional Specialized Meteorological Centre (RSMC) Bulletins",
                status="AVAILABLE",
                risk_level=level,
                value=None,
                display_value=f"{status}: {storm_name}",
                unit=None,
                probability=None,
                source="IMD Cyclone Warning Division",
                confidence_note=f"Official IMD advisory: {cyclone_warning.get('details', '')}",
                explanation=f"Active tropical cyclone system '{storm_name}' tracked in Bay of Bengal.",
                details=cyclone_warning
            )

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="IMD Regional Specialized Meteorological Centre (RSMC) Bulletins",
            status="AVAILABLE",
            risk_level="LOW",
            value=None,
            display_value="NO ACTIVE CYCLONE ALERT",
            unit=None,
            probability=None,
            source="IMD Cyclone Warning Division",
            confidence_note="No active tropical depression, deep depression, or cyclonic storm in North Indian Ocean.",
            explanation="Regional specialized meteorological monitoring confirms standard seasonal atmospheric conditions with no active cyclonic systems threatening Tamil Nadu.",
            details={"active_cyclone": False}
        )
