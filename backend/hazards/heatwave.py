import os
import joblib
import logging
from typing import Dict, Any, Optional
from backend.hazards.base import BaseHazard, HazardResult
from backend.risk.feature_contract import HEATWAVE_CONTRACT, FeatureContractValidator
from backend.services.feature_engineering import FeatureEngineeringService

logger = logging.getLogger("hazard_heatwave")

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Models")

class HeatwaveHazard(BaseHazard):
    """
    Type A: Machine Learning Heatwave Risk Module.
    Evaluates daytime temperature departure from historical climatological normal.
    """
    def __init__(self):
        super().__init__(
            hazard_id="heatwave",
            hazard_name="Heatwave Risk",
            engine_type="ml_probability",
            description="XGBoost model evaluating daily maximum temperature departures and persistence against historical climatology.",
            temporal_resolution="daily",
            spatial_resolution="District-level"
        )
        self.model = None
        self._load_model()
        self.fe_service = FeatureEngineeringService()

    def _load_model(self):
        path = os.path.join(MODELS_DIR, "heatwave_xgboost.pkl")
        if os.path.exists(path):
            try:
                self.model = joblib.load(path)
                logger.info("HeatwaveHazard: Loaded heatwave_xgboost.pkl")
            except Exception as e:
                logger.error(f"HeatwaveHazard: Failed to load model: {e}")

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
                source="Models/heatwave_xgboost.pkl",
                reason="Model artifact not found or failed to load."
            )

        res = self.fe_service.build_feature_vector(
            district_name=district_name,
            day_index=day_index,
            daily_forecast=forecast_daily,
            hourly_forecast=forecast_hourly,
            historical_baseline=historical_baseline
        )
        feat_dict = res["features_dict"]
        feat_vec = res["feature_vector"]

        is_valid, reason, missing = FeatureContractValidator.validate(HEATWAVE_CONTRACT, feat_dict)
        if not is_valid:
            return HazardResult(
                hazard_id=self.hazard_id,
                hazard_name=self.hazard_name,
                engine_type=self.engine_type,
                method="XGBoost Classifier",
                status="UNAVAILABLE",
                risk_level="UNAVAILABLE",
                display_value="—",
                source="Models/heatwave_xgboost.pkl",
                reason=reason,
                details={"missing_features": missing}
            )

        raw_prob = float(self.model.predict_proba([feat_vec])[0][1])
        prob_rounded = round(raw_prob, 4)

        if raw_prob >= 0.70:
            level = "HIGH"
        elif raw_prob >= 0.40:
            level = "MEDIUM"
        else:
            level = "LOW"

        pct_str = f"{round(prob_rounded * 100, 1)}%" if prob_rounded >= 0.01 else "< 0.01%"

        diag = FeatureContractValidator.diagnose_prediction(
            model_name="heatwave_xgboost",
            feature_dict=feat_dict,
            raw_probability=raw_prob,
            predicted_class=level,
            contract=HEATWAVE_CONTRACT
        )

        t_max = feat_dict.get("temp_max", 0.0)
        t_anom = feat_dict.get("temp_anomaly", 0.0)

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
            source="Models/heatwave_xgboost.pkl",
            model_version="v1.0-2026",
            confidence_note="Reflects daytime temperature departure from historical climatological normal.",
            explanation=f"Day {day_index} heatwave probability is {pct_str} (Max Temp: {t_max:.1f}°C, Anomaly: {t_anom:+.1f}°C departure from normal).",
            details={
                "temp_max": t_max,
                "temp_min": feat_dict.get("temp_min"),
                "temp_anomaly": t_anom,
                "humidity": feat_dict.get("humidity"),
                "diagnostics": diag
            },
            data_quality_warning=diag["data_quality_warning"]
        )
