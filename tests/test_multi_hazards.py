import unittest
from backend.hazards.registry import HazardRegistry
from backend.hazards.risk_engine import RiskEngine
from backend.hazards.extreme_rain import ExtremeRainfallHazard
from backend.hazards.extreme_wind import ExtremeWindHazard
from backend.hazards.heat_stress import HeatStressHazard
from backend.hazards.coastal import CoastalHazard
from backend.hazards.air_quality import AirQualityHazard
from backend.hazards.cyclone import CycloneHazard

class TestMultiHazards(unittest.TestCase):

    def setUp(self):
        self.registry = HazardRegistry.get_instance()
        self.engine = RiskEngine.get_instance()

    def test_registry_has_all_10_hazards(self):
        all_h = self.registry.list_all()
        self.assertEqual(len(all_h), 10)
        h_ids = {h["id"] for h in all_h}
        expected = {
            "flood", "drought", "heatwave", "extreme_rainfall",
            "extreme_wind", "heat_stress", "thunderstorm",
            "coastal", "air_quality", "cyclone"
        }
        self.assertEqual(h_ids, expected)

    def test_extreme_rainfall_imd_thresholds(self):
        h = ExtremeRainfallHazard()

        # Case A: Light rain (5 mm) -> LOW
        res_low = h.calculate("Chennai", 0, {"precipitation_sum": [5.0]}, {"precipitation": [0.2] * 24})
        self.assertEqual(res_low.risk_level, "LOW")
        self.assertIsNone(res_low.probability)

        # Case B: Heavy rain (80 mm) -> MEDIUM (IMD Heavy Rain)
        res_med = h.calculate("Chennai", 0, {"precipitation_sum": [80.0]}, {"precipitation": [3.3] * 24})
        self.assertEqual(res_med.risk_level, "MEDIUM")

        # Case C: Very Heavy rain (150 mm) -> HIGH (IMD Very Heavy Rain)
        res_high = h.calculate("Chennai", 0, {"precipitation_sum": [150.0]}, {"precipitation": [6.2] * 24})
        self.assertEqual(res_high.risk_level, "HIGH")

        # Case D: Extremely Heavy rain (250 mm) -> SEVERE
        res_sev = h.calculate("Chennai", 0, {"precipitation_sum": [250.0]}, {"precipitation": [10.4] * 24})
        self.assertEqual(res_sev.risk_level, "SEVERE")

    def test_extreme_wind_thresholds(self):
        h = ExtremeWindHazard()

        # Case A: Normal wind (4 m/s) -> LOW
        res_low = h.calculate("Chennai", 0, {"wind_speed_10m_max": [4.0]}, {})
        self.assertEqual(res_low.risk_level, "LOW")

        # Case B: Strong wind (12 m/s / 43 km/h) -> MEDIUM
        res_med = h.calculate("Chennai", 0, {"wind_speed_10m_max": [12.0]}, {})
        self.assertEqual(res_med.risk_level, "MEDIUM")

        # Case C: Gale (18 m/s / 65 km/h) -> HIGH
        res_high = h.calculate("Chennai", 0, {"wind_speed_10m_max": [18.0]}, {})
        self.assertEqual(res_high.risk_level, "HIGH")

    def test_heat_stress_noaa_heat_index(self):
        h = HeatStressHazard()

        # Case A: High temp + high humidity (38°C + 75% RH) -> Danger (HIGH)
        res_danger = h.calculate("Chennai", 0, {"temperature_2m_max": [38.0]}, {"relative_humidity_2m": [75.0] * 24})
        self.assertIn(res_danger.risk_level, ["HIGH", "SEVERE"])
        self.assertGreater(res_danger.value, 41.0)

        # Case B: Moderate conditions (28°C + 50% RH) -> LOW
        res_low = h.calculate("Chennai", 0, {"temperature_2m_max": [28.0]}, {"relative_humidity_2m": [50.0] * 24})
        self.assertEqual(res_low.risk_level, "LOW")

    def test_coastal_hazard_location_applicability(self):
        h = CoastalHazard()

        # Coastal district (Chennai) -> AVAILABLE
        res_coastal = h.calculate("Chennai", 0, {}, {}, district_profile={"coastal": True}, extra_data={"marine": {"wave_height": 1.5}})
        self.assertEqual(res_coastal.status, "AVAILABLE")
        self.assertEqual(res_coastal.risk_level, "MEDIUM")

        # Inland district (Coimbatore) -> NOT_APPLICABLE
        res_inland = h.calculate("Coimbatore", 0, {}, {}, district_profile={"coastal": False})
        self.assertEqual(res_inland.status, "NOT_APPLICABLE")
        self.assertEqual(res_inland.risk_level, "NOT_APPLICABLE")
        self.assertEqual(res_inland.display_value, "Not applicable")

    def test_air_quality_epa_bands(self):
        h = AirQualityHazard()
        res_mod = h.calculate("Chennai", 0, {}, {}, extra_data={"air_quality": {"us_aqi": 75, "pm2_5": 18.0, "pm10": 35.0}})
        self.assertEqual(res_mod.risk_level, "LOW")
        self.assertIn("Moderate", res_mod.display_value)

        res_unhealthy = h.calculate("Chennai", 0, {}, {}, extra_data={"air_quality": {"us_aqi": 165, "pm2_5": 85.0, "pm10": 150.0}})
        self.assertEqual(res_unhealthy.risk_level, "HIGH")

    def test_risk_engine_failure_isolation(self):
        # Calculate for mock data
        out = self.engine.calculate_all(
            district_name="Chennai",
            day_index=0,
            forecast_daily={"temperature_2m_max": [33.0], "precipitation_sum": [10.0], "wind_speed_10m_max": [4.0]},
            forecast_hourly={"temperature_2m": [30.0]*24, "precipitation": [0.4]*24, "relative_humidity_2m": [70.0]*24},
            district_profile={"coastal": True, "population": 1000000}
        )
        self.assertIn("overall_threat_level", out)
        self.assertIn("hazards", out)
        self.assertEqual(len(out["hazards"]), 10)

if __name__ == "__main__":
    unittest.main()
