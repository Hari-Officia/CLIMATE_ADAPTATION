from typing import Optional

"""
Centralized Risk Thresholds Configuration
Single source of truth for hazard classification across the entire platform.
"""

RISK_THRESHOLDS = {
    "HIGH": 0.70,
    "MEDIUM": 0.40,
    "LOW": 0.00
}

def classify_ml_probability(probability: Optional[float]) -> str:
    """
    Standard ML probability classification:
    - HIGH: >= 0.70
    - MEDIUM: >= 0.40 and < 0.70
    - LOW: < 0.40
    - UNAVAILABLE: probability is None
    """
    if probability is None:
        return "UNAVAILABLE"
    if probability >= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
    if probability >= RISK_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "LOW"

