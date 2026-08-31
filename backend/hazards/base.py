from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

class HazardResult(BaseModel):
    """
    Standardized multi-hazard evaluation result schema.
    Strictly differentiates ML probabilities from rule-based risk levels
    and external monitoring observations.
    """
    hazard_id: str
    hazard_name: str
    engine_type: str = Field(description="ml_probability | rule_based | external_source")
    method: str = Field(description="Description of model or scientific formula used")
    status: str = Field(default="AVAILABLE", description="AVAILABLE | UNAVAILABLE | NOT_APPLICABLE")
    risk_level: str = Field(description="LOW | MEDIUM | HIGH | SEVERE | UNAVAILABLE | NOT_APPLICABLE")
    value: Optional[float] = Field(default=None, description="Quantitative value (probability or metric index)")
    display_value: str = Field(description="Formatted string for user presentation (e.g. '76%', '124.5 mm', 'N/A')")
    unit: Optional[str] = Field(default=None, description="Measurement unit (e.g. '%', 'mm/24h', 'm/s', '°C')")
    probability: Optional[float] = Field(default=None, description="ML probability ONLY if engine_type == ml_probability")
    source: str = Field(description="Primary data or model artifact source")
    model_version: Optional[str] = None
    confidence_note: Optional[str] = None
    reason: Optional[str] = Field(default=None, description="Reason if status == UNAVAILABLE or NOT_APPLICABLE")
    explanation: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    data_quality_warning: bool = False

    model_config = {"protected_namespaces": ()}


class BaseHazard(ABC):
    """Abstract base class for all climate hazard modules."""

    def __init__(
        self,
        hazard_id: str,
        hazard_name: str,
        engine_type: str,
        description: str,
        temporal_resolution: str = "daily",
        spatial_resolution: str = "District-level"
    ):
        self.hazard_id = hazard_id
        self.hazard_name = hazard_name
        self.engine_type = engine_type
        self.description = description
        self.temporal_resolution = temporal_resolution
        self.spatial_resolution = spatial_resolution

    @abstractmethod
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
        """Calculates risk assessment for a specific district and forecast timeframe."""
        pass

    def is_applicable(self, district_profile: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """Returns True if this hazard applies to the given location."""
        return True, None
