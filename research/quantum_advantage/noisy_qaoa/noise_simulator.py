import hashlib
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

class NoiseSimulator:
    """
    Phase Z Noise Simulator for QAOA Quantum Advantage Research:
    
    Supports noise model families:
    - Family Z-A: Ideal Control (Statevector / Shot-based)
    - Family Z-B: Depolarizing Gate Noise (gate_error_rate in [0.0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.02])
    - Family Z-C: Readout Noise (readout_error_rate in [0.0, 0.001, 0.005, 0.01, 0.02, 0.05])
    - Family Z-D: Combined Gate + Readout Noise
    - Family Z-E: Hardware-Derived Noise Model (Calibrated backend noise parameters if available; NOT_AVAILABLE if absent)
    
    All noise channels preserve strict raw shot count conservation: sum(raw_counts) == shots.
    """

    @staticmethod
    def compute_noise_model_hash(
        noise_family: str,
        gate_error_rate: float,
        readout_error_rate: float,
        calibration_source: Optional[str] = None
    ) -> str:
        """Computes a deterministic hash for a noise configuration."""
        raw_str = f"{noise_family}|p_gate={gate_error_rate:.6f}|p_readout={readout_error_rate:.6f}|src={calibration_source or 'NONE'}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def apply_depolarizing_channel(
        ideal_probs: Dict[str, float],
        gate_error_rate: float,
        two_qubit_gate_count: int,
        single_qubit_gate_count: int,
        n_qubits: int
    ) -> Dict[str, float]:
        """
        Applies depolarizing channel over quantum circuit execution.
        Depolarizing parameter decay: epsilon = 1 - exp(- (p_2q * G_2q + p_1q * G_1q))
        The distribution decays towards uniform distribution 1 / 2^N.
        """
        if gate_error_rate <= 0.0:
            return ideal_probs.copy()
            
        p_2q = gate_error_rate
        p_1q = gate_error_rate * 0.1
        decay_exponent = (p_2q * two_qubit_gate_count) + (p_1q * single_qubit_gate_count)
        epsilon = 1.0 - np.exp(-decay_exponent)
        epsilon = min(1.0, max(0.0, epsilon))

        n_dim = 2 ** n_qubits
        uniform_p = 1.0 / n_dim
        
        noisy_probs: Dict[str, float] = {}
        for b_str, p_val in ideal_probs.items():
            noisy_probs[b_str] = (1.0 - epsilon) * p_val + epsilon * uniform_p
            
        # Normalize sum to 1.0
        total_p = sum(noisy_probs.values())
        if total_p > 0:
            noisy_probs = {k: v / total_p for k, v in noisy_probs.items()}
            
        return noisy_probs

    @staticmethod
    def apply_readout_channel(
        probs: Dict[str, float],
        readout_error_rate: float,
        n_qubits: int
    ) -> Dict[str, float]:
        """
        Applies symmetric bitflip readout noise channel to measured bitstrings.
        P(y|x) = eta^d_H(x,y) * (1 - eta)^(N - d_H(x,y))
        """
        if readout_error_rate <= 0.0:
            return probs.copy()

        eta = min(0.5, max(0.0, readout_error_rate))
        noisy_probs: Dict[str, float] = {}

        for orig_str, p_val in probs.items():
            if p_val <= 1e-12:
                continue
            orig_bits = [int(c) for c in orig_str]
            actual_n = len(orig_bits)
            noisy_probs[orig_str] = noisy_probs.get(orig_str, 0.0) + p_val * ((1.0 - eta) ** actual_n)
            
            # Single-bit flip transitions
            for i in range(actual_n):
                flipped = list(orig_bits)
                flipped[i] = 1 - flipped[i]
                flip_str = "".join(str(b) for b in flipped)
                transition_p = p_val * eta * ((1.0 - eta) ** max(0, actual_n - 1))
                noisy_probs[flip_str] = noisy_probs.get(flip_str, 0.0) + transition_p

        total_p = sum(noisy_probs.values())
        if total_p > 0:
            noisy_probs = {k: v / total_p for k, v in noisy_probs.items()}

        return noisy_probs

    @staticmethod
    def sample_raw_counts(
        probs: Dict[str, float],
        shots: int,
        seed: int
    ) -> Dict[str, int]:
        """
        Samples raw shot counts from a probability distribution.
        Guarantees sum(raw_counts) == shots.
        """
        rng = np.random.default_rng(seed)
        bitstrings = list(probs.keys())
        p_vals = np.array([probs[b] for b in bitstrings], dtype=np.float64)
        p_vals /= p_vals.sum()

        counts_arr = rng.multinomial(shots, p_vals)
        raw_counts = {bitstrings[i]: int(counts_arr[i]) for i in range(len(bitstrings)) if counts_arr[i] > 0}
        
        # Verify shot sum
        assert sum(raw_counts.values()) == shots, f"Shot count sum mismatch: {sum(raw_counts.values())} vs {shots}"
        return raw_counts

    @classmethod
    def run_noisy_simulation(
        cls,
        ideal_probs: Dict[str, float],
        noise_family: str = "Family Z-A",
        gate_error_rate: float = 0.0,
        readout_error_rate: float = 0.0,
        two_qubit_gate_count: int = 20,
        single_qubit_gate_count: int = 10,
        n_qubits: int = 14,
        shots: int = 1024,
        seed: int = 42,
        calibration_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a complete noisy simulation for a QAOA trial.
        """
        if noise_family == "Family Z-E":
            if not calibration_source:
                return {
                    "status": "NOT_AVAILABLE",
                    "failure_reason": "No valid backend calibration source available in environment for Family Z-E",
                    "noise_family": "Family Z-E"
                }

        n_hash = cls.compute_noise_model_hash(
            noise_family, gate_error_rate, readout_error_rate, calibration_source
        )

        current_probs = ideal_probs.copy()

        if noise_family in ["Family Z-B", "Family Z-D", "Family Z-E"]:
            current_probs = cls.apply_depolarizing_channel(
                current_probs,
                gate_error_rate=gate_error_rate,
                two_qubit_gate_count=two_qubit_gate_count,
                single_qubit_gate_count=single_qubit_gate_count,
                n_qubits=n_qubits
            )

        if noise_family in ["Family Z-C", "Family Z-D", "Family Z-E"]:
            current_probs = cls.apply_readout_channel(
                current_probs,
                readout_error_rate=readout_error_rate,
                n_qubits=n_qubits
            )

        raw_counts = cls.sample_raw_counts(current_probs, shots=shots, seed=seed)

        sorted_samples = sorted(raw_counts.items(), key=lambda x: x[1], reverse=True)
        best_bitstring = sorted_samples[0][0] if sorted_samples else "0" * n_qubits
        best_count = sorted_samples[0][1] if sorted_samples else 0

        return {
            "status": "VALID",
            "noise_family": noise_family,
            "gate_error_rate": gate_error_rate,
            "readout_error_rate": readout_error_rate,
            "noise_model_hash": n_hash,
            "raw_counts": raw_counts,
            "best_bitstring": best_bitstring,
            "best_sample_count": best_count,
            "shots": shots,
            "seed": seed,
            "calibration_source": calibration_source or "SIMULATED_GRID"
        }
