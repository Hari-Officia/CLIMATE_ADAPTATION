from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class DistrictProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    population: int
    area_km2: float
    population_density: float
    urban_percentage: float
    coastal: bool
    elevation_m: Optional[float] = None
    source: Optional[str] = None
    source_year: Optional[int] = None

class DistrictSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    district_id: str
    district_name: str
    district_code: Optional[str] = None
    latitude: float
    longitude: float

class DistrictDetail(DistrictSummary):
    model_config = ConfigDict(from_attributes=True)

    profile: Optional[DistrictProfileSchema] = None
    geojson_properties: Optional[Dict[str, Any]] = None

