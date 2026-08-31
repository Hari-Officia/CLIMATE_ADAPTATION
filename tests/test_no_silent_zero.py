import unittest
from backend.hazards.drought import DroughtHazard
from backend.hazards.flood import FloodHazard
from backend.risk.feature_contract import FeatureContractValidator, DROUGHT_CONTRACT

class TestNoSilentZero(unittest.TestCase):

    def test_drought_returns_unavailable_not_zero_when_spi_missing(self):
        drought_h = DroughtHazard()

        # Call calculate with standard 7-day forecast (which lacks 90-day antecedent observed SPI)
        res = drought_h.calculate(
            district_name="Chennai",
            day_index=0,
            forecast_daily={"temperature_2m_max": [34.0], "precipitation_sum": [0.0]},
            forecast_hourly={"temperature_2m": [30.0]*24, "relative_humidity_2m": [60.0]*24, "precipitation": [0.0]*24},
            district_profile={"coastal": True},
            extra_data={}  # No SPI supplied
        )

        self.assertEqual(res.status, "UNAVAILABLE")
        self.assertEqual(res.risk_level, "UNAVAILABLE")
        self.assertEqual(res.display_value, "—")
        self.assertIn("SPI", res.reason)
        # Verify probability is None or not a false 0.0
        self.assertIsNone(res.probability)

    def test_real_zero_rainfall_is_allowed_for_flood(self):
        flood_h = FloodHazard()
        res = flood_h.calculate(
            district_name="Chennai",
            day_index=0,
            forecast_daily={"temperature_2m_max": [34.0], "temperature_2m_min": [25.0], "precipitation_sum": [0.0]},
            forecast_hourly={"temperature_2m": [30.0]*24, "relative_humidity_2m": [60.0]*24, "wind_speed_10m": [3.0]*24, "precipitation": [0.0]*24, "soil_moisture_0_to_1cm": [0.3]*24},
            district_profile={"coastal": True}
        )
        self.assertEqual(res.status, "AVAILABLE")
        self.assertIsNotNone(res.value)
        # Even if probability is small (< 0.01%), display_value shows high precision (< 0.01%) rather than static hardcoded 0%
        self.assertIn("%", res.display_value)

if __name__ == "__main__":
    unittest.main()
