"""
Observability Tracer Service (Phase O)
Provides structured JSON logging, metrics, and event tracing across all decision workflow stages.
"""

import json
import logging
import time
from typing import Dict, Any, Optional

logger = logging.getLogger("decision_observability")
logger.setLevel(logging.INFO)

class ObservabilityTracer:
    def log_event(
        self,
        event_type: str,
        workflow_id: str,
        stage: str,
        status: str,
        duration_ms: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        event = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "service": "decision_orchestrator",
            "workflow_id": workflow_id,
            "stage": stage,
            "event_type": event_type,
            "status": status,
            "duration_ms": duration_ms,
            "metadata": metadata or {}
        }
        logger.info(json.dumps(event))
        return event
