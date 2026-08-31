import unittest
from backend.risk.feature_contract import (
    FLOOD_CONTRACT,
    DROUGHT_CONTRACT,
    HEATWAVE_CONTRACT,
    FeatureContractValidator,
    TRAINING_DISTRIBUTIONS
)

class TestFeatureContracts(unittest.TestCase):

    def test_flood_contract_valid(self):
        valid_features = {
            "temp_max": 34.0,
            "temp_min": 25.0,
            "temp_mean": 29.5,
            "temp_range": 9.0,
            "humidity": 65.0,
            "wind_speed": 3.0,
            "rainfall": 0.0,  # Real zero allowed
            "soil_wetness": 0.5,
            "rainfall_3d": 0.0,
            "rainfall_7d": 0.0,
            "rainfall_30d": 50.0,
            "temp_anomaly": 1.2,
            "rainfall_anomaly": -2.0,
            "SPI_3": None,
            "SPI_6": None
        }
        ok, reason, missing = FeatureContractValidator.validate(FLOOD_CONTRACT, valid_features)
        self.assertTrue(ok, f"Expected valid flood features, got: {reason}")
        self.assertEqual(len(missing), 0)

    def test_drought_contract_fails_when_spi_missing(self):
        missing_spi_features = {
            "temp_max": 34.0,
            "soil_wetness": 0.5,
            "rainfall_30d": 50.0,
            "rainfall_anomaly": -2.0,
            "SPI_3": None,  # Required
            "SPI_6": None   # Required
        }
        ok, reason, missing = FeatureContractValidator.validate(DROUGHT_CONTRACT, missing_spi_features)
        self.assertFalse(ok)
        self.assertIn("SPI_3", missing)
        self.assertIn("SPI_6", missing)

    def test_heatwave_contract_fails_when_temp_anomaly_missing(self):
        missing_anomaly = {
            "temp_max": 38.0,
            "temp_mean": 32.0,
            "temp_range": 12.0,
            "humidity": 50.0,
            "temp_anomaly": None  # Required
        }
        ok, reason, missing = FeatureContractValidator.validate(HEATWAVE_CONTRACT, missing_anomaly)
        self.assertFalse(ok)
        self.assertIn("temp_anomaly", missing)

    def test_diagnose_prediction_structure(self):
        sample_dict = {
            "temp_max": 46.0,  # Out of training max (44.89)
            "temp_min": 25.0,
            "temp_mean": 35.5,
            "temp_range": 21.0,
            "humidity": 65.0,
            "wind_speed": 3.0,
            "rainfall": 0.0,
            "soil_wetness": 0.5,
            "rainfall_3d": 0.0,
            "rainfall_7d": 0.0,
            "rainfall_30d": 50.0,
            "temp_anomaly": 6.5,
            "rainfall_anomaly": 0.0,
            "SPI_3": 0.0,
            "SPI_6": 0.0
        }
        diag = FeatureContractValidator.diagnose_prediction(
            model_name="flood_xgboost",
            feature_dict=sample_dict,
            raw_probability=0.05,
            predicted_class="LOW",
            contract=FLOOD_CONTRACT
        )
        self.assertIn("inputs", diag)
        self.assertIn("warnings", diag)
        self.assertTrue(diag["data_quality_warning"])
        # Check temp_max out of bounds warning
        self.assertTrue(any("temp_max" in w for w in diag["warnings"]))

if __name__ == "__main__":
    unittest.main()
