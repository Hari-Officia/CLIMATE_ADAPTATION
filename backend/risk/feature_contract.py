"""
Feature Contract & Model Pre-Inference Validation System.
Enforces zero-tolerance for silent zero-filling, differentiates real zeros from
missing/unavailable data, and provides comprehensive diagnostic auditing.
"""

from typing import Dict, List, Any, Optional, Tuple

# Exact Training Feature Bounds (Computed across all 38 districts from 2010–2021 historical data)
TRAINING_DISTRIBUTIONS: Dict[str, Dict[str, float]] = {
    "temp_max": {"min": 21.03, "mean": 32.59, "max": 44.89, "std": 3.68},
    "temp_min": {"min": 10.27, "mean": 23.09, "max": 30.65, "std": 3.08},
    "temp_mean": {"min": 18.22, "mean": 27.84, "max": 36.75, "std": 2.84},
    "temp_range": {"min": 0.42, "mean": 9.51, "max": 22.08, "std": 3.71},
    "humidity": {"min": 23.98, "mean": 71.03, "max": 96.49, "std": 11.63},
    "wind_speed": {"min": 0.28, "mean": 2.72, "max": 9.79, "std": 1.15},
    "rainfall": {"min": 0.00, "mean": 2.74, "max": 212.91, "std": 6.35},
    "soil_wetness": {"min": 0.22, "mean": 0.58, "max": 1.00, "std": 0.13},
    "rainfall_3d": {"min": 0.00, "mean": 8.22, "max": 302.21, "std": 15.17},
    "rainfall_7d": {"min": 0.00, "mean": 19.18, "max": 399.46, "std": 28.69},
    "rainfall_30d": {"min": 0.00, "mean": 82.49, "max": 1199.56, "std": 88.34},
    "temp_anomaly": {"min": -7.80, "mean": 0.43, "max": 8.20, "std": 1.85},
    "rainfall_anomaly": {"min": -25.00, "mean": -0.07, "max": 190.00, "std": 7.12},
    "SPI_3": {"min": -3.31, "mean": -0.16, "max": 3.85, "std": 1.02},
    "SPI_6": {"min": -3.50, "mean": -0.31, "max": 4.10, "std": 1.01},
}

# Feature Specification Model Contracts
FLOOD_CONTRACT = {
    "model_id": "flood_xgb_v1",
    "required_features": [
        {"name": "temp_max", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "temp_min", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "temp_mean", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "derived_mean", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "temp_range", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "derived_range", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "humidity", "unit": "%", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "wind_speed", "unit": "m/s", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "rainfall", "unit": "mm", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "REAL_ZERO_ALLOWED"},
        {"name": "soil_wetness", "unit": "fraction", "source": "Open-Meteo NWP / NASA", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "rainfall_3d", "unit": "mm", "source": "Open-Meteo NWP", "derivation": "rolling_sum_3d", "required": True, "missing_policy": "REAL_ZERO_ALLOWED"},
        {"name": "rainfall_7d", "unit": "mm", "source": "Open-Meteo NWP", "derivation": "rolling_sum_7d", "required": True, "missing_policy": "REAL_ZERO_ALLOWED"},
        {"name": "rainfall_30d", "unit": "mm", "source": "Open-Meteo NWP / NASA", "derivation": "rolling_sum_30d", "required": True, "missing_policy": "REAL_ZERO_ALLOWED"},
        {"name": "temp_anomaly", "unit": "°C", "source": "NASA Climatology Baseline", "derivation": "Tmax - baseline", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "rainfall_anomaly", "unit": "mm", "source": "NASA Climatology Baseline", "derivation": "Rain - baseline", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "SPI_3", "unit": "index", "source": "Antecedent Climatology", "derivation": "standardized_90d", "required": False, "missing_policy": "DEFAULT_NEUTRAL"},
        {"name": "SPI_6", "unit": "index", "source": "Antecedent Climatology", "derivation": "standardized_180d", "required": False, "missing_policy": "DEFAULT_NEUTRAL"},
    ]
}

DROUGHT_CONTRACT = {
    "model_id": "drought_xgb_v1",
    "required_features": [
        {"name": "temp_max", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "soil_wetness", "unit": "fraction", "source": "Open-Meteo NWP / NASA", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "rainfall_30d", "unit": "mm", "source": "Open-Meteo NWP / NASA", "derivation": "rolling_sum_30d", "required": True, "missing_policy": "REAL_ZERO_ALLOWED"},
        {"name": "rainfall_anomaly", "unit": "mm", "source": "NASA Climatology Baseline", "derivation": "Rain - baseline", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "SPI_3", "unit": "index", "source": "Antecedent Precipitation History", "derivation": "standardized_90d", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "SPI_6", "unit": "index", "source": "Antecedent Precipitation History", "derivation": "standardized_180d", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
    ]
}

HEATWAVE_CONTRACT = {
    "model_id": "heatwave_xgb_v1",
    "required_features": [
        {"name": "temp_max", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "temp_mean", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "derived_mean", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "temp_range", "unit": "°C", "source": "Open-Meteo NWP", "derivation": "derived_range", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "humidity", "unit": "%", "source": "Open-Meteo NWP", "derivation": "direct", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
        {"name": "temp_anomaly", "unit": "°C", "source": "NASA Climatology Baseline", "derivation": "Tmax - baseline", "required": True, "missing_policy": "FAIL_UNAVAILABLE"},
    ]
}


class FeatureContractValidator:
    """Validates inputs against strict contracts and generates diagnostic reports."""

    @staticmethod
    def validate(contract: Dict[str, Any], features: Dict[str, Any]) -> Tuple[bool, Optional[str], List[str]]:
        """
        Validates feature vector against the specified contract.
        Returns: (is_valid, failure_reason, missing_feature_names)
        """
        missing_required = []
        for feat in contract["required_features"]:
            name = feat["name"]
            is_req = feat.get("required", True)
            policy = feat.get("missing_policy", "FAIL_UNAVAILABLE")

            val = features.get(name)
            # Check if strictly None / null / missing
            if val is None:
                if is_req or policy == "FAIL_UNAVAILABLE":
                    missing_required.append(name)

        if missing_required:
            reason = f"Required feature(s) unavailable for {contract['model_id']}: {', '.join(missing_required)}"
            return False, reason, missing_required

        return True, None, []

    @staticmethod
    def diagnose_prediction(
        model_name: str,
        feature_dict: Dict[str, Any],
        raw_probability: Optional[float],
        predicted_class: Optional[str],
        contract: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive diagnostic structure comparing model input, forecast values,
        training distributions, and contract compliance.
        """
        diagnostic_rows = []
        warnings = []

        for feat in contract["required_features"]:
            name = feat["name"]
            val = feature_dict.get(name)
            dist = TRAINING_DISTRIBUTIONS.get(name, {})

            status = "VALID"
            is_missing = val is None
            out_of_range = False

            if is_missing:
                status = "MISSING / UNAVAILABLE"
                warnings.append(f"Feature '{name}' is missing.")
            elif dist and "min" in dist and "max" in dist:
                if val < dist["min"]:
                    status = "BELOW_TRAINING_MIN"
                    out_of_range = True
                    warnings.append(f"'{name}'={val} is below training min {dist['min']}.")
                elif val > dist["max"]:
                    status = "ABOVE_TRAINING_MAX"
                    out_of_range = True
                    warnings.append(f"'{name}'={val} is above training max {dist['max']}.")

            diagnostic_rows.append({
                "feature_name": name,
                "value": val,
                "dtype": type(val).__name__ if val is not None else "null",
                "unit": feat["unit"],
                "source": feat["source"],
                "derivation": feat["derivation"],
                "missing": is_missing,
                "status": status,
                "training_min": dist.get("min"),
                "training_max": dist.get("max"),
                "training_mean": dist.get("mean"),
                "out_of_training_range": out_of_range
            })

        return {
            "model_name": model_name,
            "contract_model_id": contract["model_id"],
            "raw_probability": raw_probability,
            "predicted_class": predicted_class,
            "inputs": diagnostic_rows,
            "warnings": warnings,
            "data_quality_warning": len(warnings) > 0
        }
