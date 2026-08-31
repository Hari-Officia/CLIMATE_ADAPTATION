from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class HourlyForecastPoint(BaseModel):
    time: str
    temperature_c: float
    humidity_pct: float
    precipitation_mm: float
    wind_speed_ms: float
    surface_pressure_hpa: Optional[float] = None
    weather_code: Optional[int] = None

class DailyForecastPoint(BaseModel):
    date: str
    temp_max_c: float
    temp_min_c: float
    precipitation_sum_mm: float
    wind_speed_max_ms: Optional[float] = None
    weather_code: Optional[int] = None
    condition: Optional[str] = None

class ForecastResponse(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district_id: Optional[str] = None
    district_name: Optional[str] = None
    timezone: Optional[str] = "Asia/Kolkata"
    current: Optional[Dict[str, Any]] = None
    hourly: Optional[Any] = None
    daily: Optional[Any] = None
    source: Optional[str] = "Open-Meteo NWP"
    data_quality: Optional[Dict[str, Any]] = None
    coordinates: Optional[Dict[str, float]] = None

    class Config:
        extra = "allow"
