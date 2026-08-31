import httpx
from fastapi import HTTPException

# Open-Meteo API
API_URL = "https://api.open-meteo.com/v1/forecast"

class ForecastService:
    @staticmethod
    async def get_forecast(lat: float, lon: float):
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(API_URL, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=500, detail=f"Open-Meteo API error: {str(e)}")
