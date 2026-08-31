import pytest
import asyncio
from backend.agents.climate_data_agent import ClimateDataAgent

@pytest.mark.asyncio
async def test_climate_agent_fetching_and_normalization():
    # Chennai centroid
    forecast = await ClimateDataAgent.get_forecast(13.0827, 80.2707, district_id="chennai")
    assert "current" in forecast
    assert "hourly" in forecast
    assert "daily" in forecast
    assert len(forecast["daily"]) >= 7
    assert "temperature_c" in forecast["current"]
    assert "humidity_pct" in forecast["current"]
    assert "data_quality" in forecast
    assert forecast["data_quality"]["status"] in ["VALID", "PARTIAL"]

@pytest.mark.asyncio
async def test_climate_agent_caching():
    # Query twice, second should be served from memory or disk cache
    t1 = await ClimateDataAgent.get_forecast(13.0827, 80.2707, district_id="chennai")
    t2 = await ClimateDataAgent.get_forecast(13.0827, 80.2707, district_id="chennai")
    assert t1["current"]["temperature_c"] == t2["current"]["temperature_c"]
