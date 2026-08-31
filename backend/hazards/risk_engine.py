import time
import logging
from typing import Dict, Any, Optional, List
from backend.hazards.registry import HazardRegistry
from backend.hazards.base import HazardResult

logger = logging.getLogger("risk_engine")

class RiskEngine:
    """
    Central Multi-Hazard Decision Support Risk Engine.
    Executes all registered climate hazards with complete failure isolation.
    """
    _instance: Optional["RiskEngine"] = None

    def __init__(self):
        self.registry = HazardRegistry.get_instance()

    @classmethod
    def get_instance(cls) -> "RiskEngine":
        if cls._instance is None:
            cls._instance = RiskEngine()
        return cls._instance

    def calculate_all(
        self,
        district_name: str,
        day_index: int,
        forecast_daily: Dict[str, Any],
        forecast_hourly: Dict[str, Any],
        district_profile: Optional[Dict[str, Any]] = None,
        historical_baseline: Optional[Dict[str, Any]] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs assessment across all registered hazards with strict failure isolation.
        If any single model or calculation raises an exception, it fails independently
        without interrupting remaining hazard assessments.
        """
        results: Dict[str, Any] = {}
        all_hazards = self.registry._hazards

        for hazard_id, hazard in all_hazards.items():
            try:
                res = hazard.calculate(
                    district_name=district_name,
                    day_index=day_index,
                    forecast_daily=forecast_daily,
                    forecast_hourly=forecast_hourly,
                    district_profile=district_profile,
                    historical_baseline=historical_baseline,
                    extra_data=extra_data
                )
                results[hazard_id] = res.model_dump()
            except Exception as e:
                logger.error(f"Error calculating hazard '{hazard_id}' for {district_name}: {e}", exc_info=True)
                results[hazard_id] = HazardResult(
                    hazard_id=hazard.hazard_id,
                    hazard_name=hazard.hazard_name,
                    engine_type=hazard.engine_type,
                    method=f"Failed execution: {hazard.hazard_name}",
                    status="UNAVAILABLE",
                    risk_level="UNAVAILABLE",
                    display_value="—",
                    source=f"Module {hazard_id}",
                    reason=f"Calculation error: {str(e)}"
                ).model_dump()

        # Determine overall multi-hazard threat tier
        risk_priority = {"SEVERE": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "AVAILABLE": 1, "UNAVAILABLE": 0, "NOT_APPLICABLE": 0}
        highest_tier = "LOW"
        highest_score = 1

        for h in results.values():
            lvl = h.get("risk_level", "LOW")
            score = risk_priority.get(lvl, 0)
            if score > highest_score:
                highest_score = score
                highest_tier = lvl

        return {
            "district_name": district_name,
            "day_index": day_index,
            "timestamp": time.time(),
            "overall_threat_level": highest_tier,
            "hazards": results
        }

    def calculate_single(
        self,
        hazard_id: str,
        district_name: str,
        day_index: int,
        forecast_daily: Dict[str, Any],
        forecast_hourly: Dict[str, Any],
        district_profile: Optional[Dict[str, Any]] = None,
        historical_baseline: Optional[Dict[str, Any]] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        hazard = self.registry.get(hazard_id)
        if not hazard:
            return None

        res = hazard.calculate(
            district_name=district_name,
            day_index=day_index,
            forecast_daily=forecast_daily,
            forecast_hourly=forecast_hourly,
            district_profile=district_profile,
            historical_baseline=historical_baseline,
            extra_data=extra_data
        )
        return res.model_dump()
