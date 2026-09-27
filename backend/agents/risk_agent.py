import os
import joblib
import logging
import numpy as np
from typing import Dict, Any, List, Optional
from backend.services.feature_engineering import FeatureEngineeringService, FEATURE_COLUMNS_53
from backend.risk.thresholds import classify_ml_probability, RISK_THRESHOLDS

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
        hourly_forecast_list: List[Dict[str, Any]],
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Assesses multi-hazard risk for a specific forecast day for a given district.
        """
        extra = extra_data or {}

        # Derive 53-feature vector
        feat_res = self.feature_service.build_feature_vector(
            district_name=district_name,
            forecast_day_index=forecast_day_index,
            daily_forecast_list=daily_forecast_list,
            hourly_forecast_list=hourly_forecast_list
        )

        vector = feat_res["features_vector"]
        feat_dict = feat_res["features_dict"]

        # Merge antecedent SPI if provided in extra_data
        if "SPI_3" in extra and extra["SPI_3"] is not None:
            feat_dict["SPI_3"] = extra["SPI_3"]
        if "SPI_6" in extra and extra["SPI_6"] is not None:
            feat_dict["SPI_6"] = extra["SPI_6"]

        if isinstance(daily_forecast_list, dict):
            time_list = daily_forecast_list.get("time", [])
            date_str = time_list[min(forecast_day_index, len(time_list) - 1)] if time_list else "2026-08-31"
        elif isinstance(daily_forecast_list, list) and len(daily_forecast_list) > 0:
            date_str = daily_forecast_list[min(forecast_day_index, len(daily_forecast_list) - 1)].get("date", "2026-08-31")
        else:
            date_str = "2026-08-31"

        # Verify exact 53 features
        if len(vector) != 53:
            logger.error(f"[VALIDATION] District: {district_name} | Feature vector length mismatch: expected 53, got {len(vector)}")
            raise ValueError(f"Feature vector length mismatch: expected 53, got {len(vector)}")

        # Convert to numpy array for XGBoost inference
        X = np.array([vector], dtype=np.float32)

        hazard_scores = {}
        for hazard in ["flood", "drought", "heatwave"]:
            # Check drought SPI requirement
            if hazard == "drought":
                has_spi = (extra.get("SPI_3") is not None and extra.get("SPI_6") is not None)
                allow_extrapolation = extra.get("allow_spi_extrapolation", False)
                if not has_spi and not allow_extrapolation:
                    logger.warning(f"[VALIDATION] District: {district_name} | Hazard: drought | Missing feature: SPI_3/SPI_6 | Status: UNAVAILABLE")
                    hazard_scores["drought"] = {
                        "probability": None,
                        "risk_level": "UNAVAILABLE",
                        "status": "UNAVAILABLE",
                        "threshold_applied": 0.0,
                        "confidence_note": "Antecedent 90-day / 180-day observed rainfall history is required to calculate SPI_3 and SPI_6.",
                        "reason": "Unavailable — insufficient data"
                    }
                    continue

            model = self._models.get(hazard)
            if model is not None:
                try:
                    proba = float(model.predict_proba(X)[0][1])
                    risk_level = classify_ml_probability(proba)
                    status = "AVAILABLE"
                except Exception as e:
                    logger.error(f"[RISK] Inference error for {hazard} ({district_name}): {e}")
                    proba = None
                    risk_level = "UNAVAILABLE"
                    status = "UNAVAILABLE"
            else:
                logger.warning(f"[VALIDATION] District: {district_name} | Hazard: {hazard} | Model file missing | Status: UNAVAILABLE")
                proba = None
                risk_level = "UNAVAILABLE"
                status = "UNAVAILABLE"

            # Confidence & limitation notes
            if hazard == "flood":
                conf_note = "High rare-event uncertainty. Cross-checked with rolling rainfall accumulation."
            elif hazard == "drought":
                conf_note = "Reflects slow-onset multi-month moisture and precipitation deficit."
            else:
                conf_note = "Reflects daytime temperature departure from historical baseline."

            prob_val = round(proba, 4) if proba is not None else None
            hazard_scores[hazard] = {
                "probability": prob_val,
                "risk_level": risk_level,
                "status": status,
                "threshold_applied": RISK_THRESHOLDS["HIGH"] if risk_level == "HIGH" else RISK_THRESHOLDS["MEDIUM"] if risk_level == "MEDIUM" else 0.0,
                "confidence_note": conf_note
            }

            if status == "AVAILABLE":
                logger.info(f"[RISK] District: {district_name} | Hazard: {hazard} | Model: {hazard}_xgboost | Probability: {prob_val} | Level: {risk_level}")

        # Determine overall hazard level
        levels = [h["risk_level"] for h in hazard_scores.values() if h.get("risk_level") != "UNAVAILABLE"]
        if "HIGH" in levels:
            overall = "HIGH"
        elif "MEDIUM" in levels:
            overall = "MEDIUM"
        elif "LOW" in levels:
            overall = "LOW"
        else:
            overall = "UNAVAILABLE"

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
