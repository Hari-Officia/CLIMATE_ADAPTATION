from pydantic import BaseModel
from typing import Optional, Dict, Any

class DistrictProfileSchema(BaseModel):
    population: int
    area_km2: float
    population_density: float
    urban_percentage: float
    coastal: bool
    elevation_m: Optional[float] = None
    source: Optional[str] = None
    source_year: Optional[int] = None

    class Config:
        from_attributes = True

class DistrictSummary(BaseModel):
    id: int
    district_id: str
    district_name: str
    district_code: Optional[str] = None
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class DistrictDetail(DistrictSummary):
    profile: Optional[DistrictProfileSchema] = None
    geojson_properties: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
