import os
from typing import Dict, Any

class QuantumHardwareAdapter:
    """
    Quantum Hardware Provider Adapter:
    - Detects IBM Quantum / AWS Braket credentials safely from environment variables.
    - Zero hardcoded secrets or committed API keys.
    - Operates in SIMULATOR_MODE by default when no hardware provider token is set.
    """

    @staticmethod
    def detect_available_providers() -> Dict[str, Any]:
        """Detect available quantum hardware providers."""
        ibm_token = os.environ.get("IBMQ_API_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")
        braket_token = os.environ.get("AWS_BRAKET_ACCESS_KEY")
        
        has_ibm = bool(ibm_token and len(ibm_token) > 10)
        has_braket = bool(braket_token and len(braket_token) > 10)
        
        return {
            "mode": "HARDWARE" if (has_ibm or has_braket) else "SIMULATOR_ONLY",
            "ibm_quantum_available": has_ibm,
            "aws_braket_available": has_braket,
            "active_backend": "ibm_sherbrooke" if has_ibm else "aer_simulator_statevector",
            "hardware_tested": False
        }
