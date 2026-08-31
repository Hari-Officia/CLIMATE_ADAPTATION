import pytest
from backend.agents.risk_agent import RiskAgent

def test_risk_agent_model_loading_and_inference():
    risk_agent = RiskAgent.get_instance()
    assert risk_agent.is_healthy() is True

    statuses = risk_agent.get_model_statuses()
    assert len(statuses) == 3
    for s in statuses:
        assert s["status"] == "ACTIVE"
        assert s["n_features"] == 53

    mock_daily = [
        {"date": "2026-08-31", "temp_max_c": 36.5, "temp_min_c": 26.0, "precipitation_sum_mm": 5.0, "wind_speed_max_ms": 4.2}
    ]
    mock_hourly = [
        {"humidity_pct": 65.0, "wind_speed_ms": 3.8, "soil_moisture_fraction": 0.38}
    ]

    res = risk_agent.assess_risk(
        district_name="Chennai",
        forecast_day_index=0,
        daily_forecast_list=mock_daily,
        hourly_forecast_list=mock_hourly
    )

    assert "flood" in res
    assert "drought" in res
    assert "heatwave" in res
    assert "overall_hazard_level" in res

    # Check probabilities and thresholds
    for hazard in ["flood", "drought", "heatwave"]:
        prob = res[hazard]["probability"]
        level = res[hazard]["risk_level"]
        assert 0.0 <= prob <= 1.0
        if prob >= 0.70:
            assert level == "HIGH"
        elif prob >= 0.40:
            assert level == "MEDIUM"
        else:
            assert level == "LOW"
