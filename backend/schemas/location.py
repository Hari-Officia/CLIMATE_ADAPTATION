from pydantic import BaseModel
from typing import Optional

class LocationSearchResult(BaseModel):
    name: str
    latitude: float
    longitude: float
    district_id: str
    district_name: str
    category: str = "location"

class ReverseGeocodeResult(BaseModel):
    latitude: float
    longitude: float
    district_id: Optional[str] = None
    district_name: Optional[str] = None
    is_inside_tamil_nadu: bool = True
