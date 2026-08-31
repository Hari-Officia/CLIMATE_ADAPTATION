from backend.services.forecast_service import ForecastService
from backend.services.feature_service import FeatureService

# Mock district lookup - will be database in PH 3
DISTRICT_COORDS = {
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Ariyalur": {"lat": 11.1411, "lon": 79.0734},
}

class ClimateAgent:
    @staticmethod
    async def get_forecast_for_district(district: str):
        coords = DISTRICT_COORDS.get(district)
        if not coords:
            return {"error": "District not found"}

        forecast = await ForecastService.get_forecast(coords["lat"], coords["lon"])

        # Derived features
        model_features = FeatureService.derive_features(forecast)

        return {
            "district": district,
            "forecast": forecast,
            "model_features": model_features,
            "data_quality": {"status": "ok"}
        }
