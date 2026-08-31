import pytest
from backend.services.feature_engineering import FeatureEngineeringService, FEATURE_COLUMNS_53

def test_feature_engineering_exact_53_columns():
    service = FeatureEngineeringService()
    
    mock_daily = [
        {"date": "2026-08-31", "temp_max_c": 35.0, "temp_min_c": 25.0, "precipitation_sum_mm": 12.5, "wind_speed_max_ms": 4.0},
        {"date": "2026-09-01", "temp_max_c": 34.0, "temp_min_c": 24.5, "precipitation_sum_mm": 8.0, "wind_speed_max_ms": 3.8},
        {"date": "2026-09-02", "temp_max_c": 33.5, "temp_min_c": 24.0, "precipitation_sum_mm": 0.0, "wind_speed_max_ms": 3.5},
    ]
    mock_hourly = [
        {"humidity_pct": 72.0, "wind_speed_ms": 3.5, "soil_moisture_fraction": 0.42}
    ]

    res = service.build_feature_vector(
        district_name="Chennai",
        forecast_day_index=0,
        daily_forecast_list=mock_daily,
        hourly_forecast_list=mock_hourly
    )

    vector = res["features_vector"]
    feat_dict = res["features_dict"]

    # Verify vector length is strictly 53
    assert len(vector) == 53
    assert len(FEATURE_COLUMNS_53) == 53

    # Check key derivations
    assert feat_dict["temp_max"] == 35.0
    assert feat_dict["temp_min"] == 25.0
    assert feat_dict["temp_mean"] == 30.0
    assert feat_dict["temp_range"] == 10.0
    assert feat_dict["rainfall"] == 12.5
    assert feat_dict["rainfall_3d"] >= 12.5
    assert "temp_anomaly" in feat_dict
    assert "rainfall_anomaly" in feat_dict
    assert "SPI_3" in feat_dict
    assert "SPI_6" in feat_dict

    # Check district one-hot encoding
    assert feat_dict["district_Chennai"] == 1
    assert feat_dict["district_Coimbatore"] == 0
    assert feat_dict["district_Madurai"] == 0
