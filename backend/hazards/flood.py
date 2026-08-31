import os
import joblib
import logging
from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult
from backend.risk.feature_contract import FLOOD_CONTRACT, FeatureContractValidator
from backend.services.feature_engineering import FeatureEngineeringService

logger = logging.getLogger("hazard_flood")

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Models")

class FloodHazard(BaseHazard):
    """
    Type A: Machine Learning Flood Risk Module.
    Executes trained 53-feature XGBoost classifier.
    """
    def __init__(self):
        super().__init__(
            hazard_id="flood",
            hazard_name="Flood Risk",
            engine_type="ml_probability",
            description="53-feature XGBoost model trained on NASA POWER climatology and historical flood episodes.",
            temporal_resolution="daily",
            spatial_resolution="District-level"
        )
        self.model = None
        self._load_model()
        self.fe_service = FeatureEngineeringService()

    def _load_model(self):
        path = os.path.join(MODELS_DIR, "flood_xgboost.pkl")
        if os.path.exists(path):
            try:
                self.model = joblib.load(path)
                logger.info("FloodHazard: Loaded flood_xgboost.pkl")
            except Exception as e:
                logger.error(f"FloodHazard: Failed to load model: {e}")

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
                source="Models/flood_xgboost.pkl",
                reason="Model artifact not found or failed to load."
            )

        # 1. Build 53-feature vector
        res = self.fe_service.build_feature_vector(
            district_name=district_name,
            day_index=day_index,
            daily_forecast=forecast_daily,
            hourly_forecast=forecast_hourly,
            historical_baseline=historical_baseline
        )
        feat_dict = res["features_dict"]
        feat_vec = res["feature_vector"]

        # 2. Validate against Feature Contract
        is_valid, reason, missing = FeatureContractValidator.validate(FLOOD_CONTRACT, feat_dict)
        if not is_valid:
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="XGBoost Classifier",
                status="UNAVAILABLE",
                risk_level="UNAVAILABLE",
                display_value="—",
                source="Models/flood_xgboost.pkl",
                reason=reason,
                details={"missing_features": missing}
            )

        # 3. Model Inference
        raw_prob = float(self.model.predict_proba([feat_vec])[0][1])
        prob_rounded = round(raw_prob, 4)

        if raw_prob >= 0.70:
            level = "HIGH"
        elif raw_prob >= 0.40:
            level = "MEDIUM"
        else:
            level = "LOW"

        # Format display value with precision to avoid artificial 0%
        if prob_rounded == 0.0:
            pct_str = "< 0.01%"
        elif prob_rounded < 0.01:
            pct_str = f"{prob_rounded * 100:.2f}%"
        else:
            pct_str = f"{round(prob_rounded * 100, 1)}%"

        diag = FeatureContractValidator.diagnose_prediction(
            model_name="flood_xgboost",
            feature_dict=feat_dict,
            raw_probability=raw_prob,
            predicted_class=level,
            contract=FLOOD_CONTRACT
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
            source="Models/flood_xgboost.pkl",
            model_version="v1.0-2026",
            confidence_note="High rare-event uncertainty in base rate (0.42% positive prevalence). Calibrated threshold applied.",
            explanation=f"Day {day_index} flood probability is {pct_str} based on {feat_dict.get('rainfall_3d', 0):.1f}mm 3-day rainfall, {feat_dict.get('rainfall_7d', 0):.1f}mm 7-day rainfall, and soil wetness.",
            details={
                "rainfall_1d": feat_dict.get("rainfall"),
                "rainfall_3d": feat_dict.get("rainfall_3d"),
                "rainfall_7d": feat_dict.get("rainfall_7d"),
                "rainfall_30d": feat_dict.get("rainfall_30d"),
                "soil_wetness": feat_dict.get("soil_wetness"),
                "diagnostics": diag
            },
            data_quality_warning=diag["data_quality_warning"]
        )
