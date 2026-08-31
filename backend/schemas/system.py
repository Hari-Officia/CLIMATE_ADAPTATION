from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ModelStatus(BaseModel):
    model_config = {"protected_namespaces": ()}
    hazard: str
    model_name: str
    status: str
    framework: str
    n_features: int
    roc_auc: Optional[float] = None
    pr_auc: Optional[float] = None

class SystemStatusResponse(BaseModel):
    system: str = "Quantum Multi-Agent Climate Risk Decision Support System"
    review_phase: str = "Review II (Core Operational Foundation)"
    status: str
    timestamp: str
    database: Dict[str, Any]
    geojson_loaded: bool
    districts_count: int
    models: List[ModelStatus]
    agents: Dict[str, str]
    feature_schema_features: int = 53
