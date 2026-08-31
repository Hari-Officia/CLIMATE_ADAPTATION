from typing import Dict, List, Optional, Any
import logging
from backend.hazards.base import BaseHazard
from backend.hazards.flood import FloodHazard
from backend.hazards.drought import DroughtHazard
from backend.hazards.heatwave import HeatwaveHazard
from backend.hazards.extreme_rain import ExtremeRainfallHazard
from backend.hazards.extreme_wind import ExtremeWindHazard
from backend.hazards.heat_stress import HeatStressHazard
from backend.hazards.thunderstorm import ThunderstormHazard
from backend.hazards.coastal import CoastalHazard
from backend.hazards.air_quality import AirQualityHazard
from backend.hazards.cyclone import CycloneHazard

logger = logging.getLogger("hazard_registry")

class HazardRegistry:
    """
    Central Extensible Climate Hazard Registry.
    Allows dynamic plug-and-play addition of ML models, rule indices, and external APIs.
    """
    _instance: Optional["HazardRegistry"] = None

    def __init__(self):
        self._hazards: Dict[str, BaseHazard] = {}
        self._load_defaults()

    @classmethod
    def get_instance(cls) -> "HazardRegistry":
        if cls._instance is None:
            cls._instance = HazardRegistry()
        return cls._instance

    def _load_defaults(self):
        """Registers the 10 core climate hazard modules."""
        self.register(FloodHazard())
        self.register(DroughtHazard())
        self.register(HeatwaveHazard())
        self.register(ExtremeRainfallHazard())
        self.register(ExtremeWindHazard())
        self.register(HeatStressHazard())
        self.register(ThunderstormHazard())
        self.register(CoastalHazard())
        self.register(AirQualityHazard())
        self.register(CycloneHazard())
        logger.info(f"HazardRegistry initialized with {len(self._hazards)} hazard modules.")

    def register(self, hazard: BaseHazard):
        self._hazards[hazard.hazard_id] = hazard
        logger.info(f"Registered hazard: {hazard.hazard_id} ({hazard.hazard_name})")

    def get(self, hazard_id: str) -> Optional[BaseHazard]:
        return self._hazards.get(hazard_id)

    def list_all(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": h.hazard_id,
                "name": h.hazard_name,
                "engine_type": h.engine_type,
                "description": h.description,
                "temporal_resolution": h.temporal_resolution,
                "spatial_resolution": h.spatial_resolution
            }
            for h in self._hazards.values()
        ]

    def get_applicable_hazards(self, district_profile: Optional[Dict[str, Any]] = None) -> List[BaseHazard]:
        """Returns all hazards applicable to the given location."""
        applicable = []
        for h in self._hazards.values():
            ok, _ = h.is_applicable(district_profile)
            if ok:
                applicable.append(h)
        return applicable
