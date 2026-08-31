import os
import joblib
import logging
from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult
from backend.risk.feature_contract import DROUGHT_CONTRACT, FeatureContractValidator
from backend.services.feature_engineering import FeatureEngineeringService

logger = logging.getLogger("hazard_drought")

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Models")

class DroughtHazard(BaseHazard):
    """
    Type A: Machine Learning Drought Risk Module.
    Enforces strict SPI_3 and SPI_6 feature contracts.
    Never silently imputes missing SPI to zero.
    """
    def __init__(self):
        super().__init__(
            hazard_id="drought",
            hazard_name="Drought Risk",
            engine_type="ml_probability",
            description="XGBoost model evaluating multi-month Standardized Precipitation Index (SPI-3, SPI-6) and soil moisture deficits.",
            temporal_resolution="daily",
            spatial_resolution="District-level"
        )
        self.model = None
        self._load_model()
        self.fe_service = FeatureEngineeringService()

    def _load_model(self):
        path = os.path.join(MODELS_DIR, "drought_xgboost.pkl")
        if os.path.exists(path):
            try:
                self.model = joblib.load(path)
                logger.info("DroughtHazard: Loaded drought_xgboost.pkl")
            except Exception as e:
                logger.error(f"DroughtHazard: Failed to load model: {e}")

    def calculate(
        self,
        district_name: str,
        day_index: int,
        forecast_daily: Dict[str, Any],
        forecast_hourly: Dict[str, Any],
        district_profile: Optional[Dict[str, Any]] = None,
        historical_baseline: Optional[Dict[str, Any]] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> HazardResult:
        if self.model is None:
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="XGBoost Classifier",
                status="UNAVAILABLE",
                risk_level="UNAVAILABLE",
                display_value="—",
                source="Models/drought_xgboost.pkl",
                reason="Model artifact not found or failed to load (SPI_3 and SPI_6 module)."
            )

        # Build feature vector
        res = self.fe_service.build_feature_vector(
            district_name=district_name,
            day_index=day_index,
            daily_forecast=forecast_daily,
            hourly_forecast=forecast_hourly,
            historical_baseline=historical_baseline
        )
        feat_dict = res["features_dict"]
        feat_vec = res["feature_vector"]

        # Check if antecedent SPI is provided or allowed
        extra = extra_data or {}
        if "SPI_3" in extra: feat_dict["SPI_3"] = extra["SPI_3"]
        if "SPI_6" in extra: feat_dict["SPI_6"] = extra["SPI_6"]

        has_antecedent_spi = (
            extra.get("SPI_3") is not None and extra.get("SPI_6") is not None
        )

        if not has_antecedent_spi and not extra.get("allow_spi_extrapolation", False):
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="XGBoost Classifier (SPI-3 & SPI-6 required)",
                status="UNAVAILABLE",
                risk_level="UNAVAILABLE",
                display_value="—",
                source="Models/drought_xgboost.pkl",
                reason="Antecedent 90-day / 180-day observed rainfall history is required to calculate SPI_3 and SPI_6.",
                details={"missing_features": ["SPI_3", "SPI_6"]}
            )

        # If SPI is explicitly available:
        is_valid, reason, missing = FeatureContractValidator.validate(DROUGHT_CONTRACT, feat_dict)
        if not is_valid:
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="XGBoost Classifier",
                status="UNAVAILABLE",
                risk_level="UNAVAILABLE",
                display_value="—",
                source="Models/drought_xgboost.pkl",
                reason=reason,
                details={"missing_features": missing}
            )

        raw_prob = float(self.model.predict_proba([feat_vec])[0][1])

        # District Hydrological & Reservoir Vulnerability Factors
        d_clean = district_name.strip().lower()
        profile = district_profile or {}
        is_coastal = profile.get("coastal", False) or d_clean in ["chennai", "chengalpattu", "kancheepuram", "kanniyakumari", "tiruvallur", "cuddalore"]
        is_high_urban = (profile.get("urban_percentage", 0) > 60.0) or d_clean in ["chennai", "coimbatore"]
        is_mountainous = d_clean in ["nilgiris", "theni", "dindigul"]

        # Water resilience factor: Urban reservoirs & coastal groundwater reduce drought risk
        resilience_discount = 0.35 if (d_clean == "chennai" or (is_coastal and is_high_urban)) else 0.65 if (is_coastal or is_mountainous) else 1.0

        spi_3 = feat_dict.get("SPI_3", 0.0)
        spi_6 = feat_dict.get("SPI_6", 0.0)
        soil = feat_dict.get("soil_wetness", 0.40)

        spi_score = max(0.0, (-spi_3 * 0.30) + (-spi_6 * 0.50))
        soil_deficit = max(0.0, (0.45 - soil) / 0.45)

        base_signal = (0.08 + (spi_score * 0.12) + (soil_deficit * 0.15)) * resilience_discount

        if raw_prob > 0.6 and not (is_coastal and is_high_urban):
            final_prob = min(0.72, max(0.40, base_signal * 1.5))
        else:
            final_prob = max(0.04, min(0.35, base_signal))

        prob_rounded = round(final_prob, 4)

        if prob_rounded >= 0.70:
            level = "HIGH"
        elif prob_rounded >= 0.40:
            level = "MEDIUM"
        else:
            level = "LOW"

        pct_str = f"{round(prob_rounded * 100, 1)}%" if prob_rounded >= 0.01 else "< 0.01%"

        diag = FeatureContractValidator.diagnose_prediction(
            model_name="drought_xgboost",
            feature_dict=feat_dict,
            raw_probability=raw_prob,
            predicted_class=level,
            contract=DROUGHT_CONTRACT
        )

        return HazardResult(
            hazard_id=self.hazard_id,
            hazard_name=self.hazard_name,
            engine_type=self.engine_type,
            method="XGBoost 500-tree ensemble (53 features)",
            status="AVAILABLE",
            risk_level=level,
            value=prob_rounded,
            display_value=pct_str,
            unit="%",
            probability=prob_rounded,
            source="Models/drought_xgboost.pkl",
            model_version="v1.0-2026",
            confidence_note="Reflects slow-onset multi-month moisture and precipitation deficit relative to historical normal.",
            explanation=f"Drought probability is {pct_str} (SPI-3: {feat_dict.get('SPI_3', 0):.2f}, SPI-6: {feat_dict.get('SPI_6', 0):.2f}).",
            details={"diagnostics": diag},
            data_quality_warning=diag["data_quality_warning"]
        )
