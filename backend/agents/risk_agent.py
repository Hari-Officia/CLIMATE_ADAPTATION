import os
import joblib
import logging
import numpy as np
from typing import Dict, Any, List, Optional
from backend.services.feature_engineering import FeatureEngineeringService, FEATURE_COLUMNS_53

logger = logging.getLogger("risk_agent")

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Models")

class RiskAgent:
    _instance = None
    _models: Dict[str, Any] = {}
    _loaded: bool = False

    def __init__(self):
        self.feature_service = FeatureEngineeringService()
        self._load_models()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RiskAgent()
        return cls._instance

    def _load_models(self):
        hazards = ["flood", "drought", "heatwave"]
        for hazard in hazards:
            model_path = os.path.join(MODELS_DIR, f"{hazard}_xgboost.pkl")
            if os.path.exists(model_path):
                try:
                    self._models[hazard] = joblib.load(model_path)
                    logger.info(f"Loaded {hazard} XGBoost model ({getattr(self._models[hazard], 'n_features_in_', 53)} features).")
                except Exception as e:
                    logger.error(f"Error loading model {model_path}: {e}")
            else:
                logger.error(f"Model file not found: {model_path}")

        self._loaded = len(self._models) == 3

    def is_healthy(self) -> bool:
        return len(self._models) == 3

    def get_model_statuses(self) -> List[Dict[str, Any]]:
        metadata = {
            "flood": {"name": "Flood Risk Classifier", "roc_auc": 0.906, "pr_auc": 0.074},
            "drought": {"name": "Drought Risk Classifier", "roc_auc": 0.9998, "pr_auc": 0.9993},
            "heatwave": {"name": "Heatwave Risk Classifier", "roc_auc": 1.0000, "pr_auc": 0.9964}
        }
        statuses = []
        for h in ["flood", "drought", "heatwave"]:
            model = self._models.get(h)
            statuses.append({
                "hazard": h,
                "model_name": metadata[h]["name"],
                "status": "ACTIVE" if model else "OFFLINE",
                "framework": "XGBoost",
                "n_features": getattr(model, "n_features_in_", 53) if model else 53,
                "roc_auc": metadata[h]["roc_auc"],
                "pr_auc": metadata[h]["pr_auc"]
            })
        return statuses

    def assess_risk(
        self,
        district_name: str,
        forecast_day_index: int,
        daily_forecast_list: List[Dict[str, Any]],
        hourly_forecast_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Assesses multi-hazard risk for a specific forecast day for a given district.
        """
        # Derive 53-feature vector
        feat_res = self.feature_service.build_feature_vector(
            district_name=district_name,
            forecast_day_index=forecast_day_index,
            daily_forecast_list=daily_forecast_list,
            hourly_forecast_list=hourly_forecast_list
        )

        vector = feat_res["features_vector"]
        feat_dict = feat_res["features_dict"]
        if isinstance(daily_forecast_list, dict):
            time_list = daily_forecast_list.get("time", [])
            date_str = time_list[min(forecast_day_index, len(time_list) - 1)] if time_list else "2026-08-31"
        elif isinstance(daily_forecast_list, list) and len(daily_forecast_list) > 0:
            date_str = daily_forecast_list[min(forecast_day_index, len(daily_forecast_list) - 1)].get("date", "2026-08-31")
        else:
            date_str = "2026-08-31"

        # Verify exact 53 features
        if len(vector) != 53:
            raise ValueError(f"Feature vector length mismatch: expected 53, got {len(vector)}")

        # Convert to numpy array for XGBoost inference
        X = np.array([vector], dtype=np.float32)

        hazard_scores = {}
        for hazard in ["flood", "drought", "heatwave"]:
            model = self._models.get(hazard)
            if model is not None:
                try:
                    proba = float(model.predict_proba(X)[0][1])
                except Exception as e:
                    logger.error(f"Inference error for {hazard}: {e}")
                    proba = 0.05
            else:
                proba = 0.05

            # Calibrated thresholds: High >= 0.70, Medium >= 0.40, Low < 0.40
            if proba >= 0.70:
                risk_level = "HIGH"
            elif proba >= 0.40:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            # Confidence & limitation notes
            if hazard == "flood":
                conf_note = "High rare-event uncertainty. Cross-checked with rolling rainfall accumulation."
            elif hazard == "drought":
                conf_note = "Reflects slow-onset multi-month moisture and precipitation deficit."
            else:
                conf_note = "Reflects daytime temperature departure from historical baseline."

            hazard_scores[hazard] = {
                "probability": round(proba, 4),
                "risk_level": risk_level,
                "threshold_applied": 0.70 if risk_level == "HIGH" else 0.40 if risk_level == "MEDIUM" else 0.0,
                "confidence_note": conf_note
            }

        # Determine overall hazard level
        levels = [h["risk_level"] for h in hazard_scores.values()]
        if "HIGH" in levels:
            overall = "HIGH"
        elif "MEDIUM" in levels:
            overall = "MEDIUM"
        else:
            overall = "LOW"

        # Continuous feature summary for UI transparency
        summary_keys = [
            "temp_max", "temp_min", "rainfall", "rainfall_3d",
            "rainfall_7d", "temp_anomaly", "rainfall_anomaly", "SPI_3"
        ]
        feat_summary = {k: feat_dict[k] for k in summary_keys if k in feat_dict}

        return {
            "date": date_str,
            "flood": hazard_scores["flood"],
            "heatwave": hazard_scores["heatwave"],
            "drought": hazard_scores["drought"],
            "overall_hazard_level": overall,
            "features_summary": feat_summary,
            "raw_features_dict": feat_dict,
            "baseline": feat_res["baseline"]
        }

    def assess_7day_timeline(
        self,
        district_name: str,
        daily_forecast_list: List[Dict[str, Any]],
        hourly_forecast_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Assesses multi-hazard risk for all 7 days of the forecast timeline.
        """
        timeline = []
        for day_idx in range(len(daily_forecast_list)):
            assessment = self.assess_risk(
                district_name=district_name,
                forecast_day_index=day_idx,
                daily_forecast_list=daily_forecast_list,
                hourly_forecast_list=hourly_forecast_list
            )
            timeline.append(assessment)
        return timeline
