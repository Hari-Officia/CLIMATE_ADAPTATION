"""
QAOA API Router — Phase M Enterprise QAOA
Exposes REST endpoints for QAOA optimization runs, classical-vs-QAOA benchmarks, sample distributions, circuit metrics, and certificates.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from backend.db.database import get_db_context
from backend.db.models import (
    QAOAExperimentRecord, QAOASampleRecord, QAOACircuitRecord,
    QAOACertificateRecord, QAOABenchmarkRecord
)
from backend.services.optimization.qaoa.qaoa_solver import QAOASolver
from backend.services.optimization.qaoa.benchmark_engine import QAOABenchmarkEngine

qaoa_router = APIRouter(tags=["QAOA Quantum Optimization Engine"])

class QAOARunRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "chennai"})
    max_k: int = Field(5, ge=1, le=15, json_schema_extra={"example": 5})
    qaoa_depth_p: int = Field(2, ge=1, le=5, json_schema_extra={"example": 2})
    shots: int = Field(1000, ge=100, le=10000, json_schema_extra={"example": 1000})
    optimizer: str = Field("COBYLA", json_schema_extra={"example": "COBYLA"})
    seed: int = Field(42, json_schema_extra={"example": 42})

class QAOABenchmarkRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "chennai"})
    max_k: int = Field(5, ge=1, le=15, json_schema_extra={"example": 5})
    p_depths: List[int] = Field([1, 2, 3], json_schema_extra={"example": [1, 2, 3]})
    shots: int = Field(1000, ge=100, le=5000, json_schema_extra={"example": 1000})
    seed: int = Field(42, json_schema_extra={"example": 42})


@qaoa_router.post("/run", summary="Run QAOA Optimization Experiment")
def run_qaoa_experiment(payload: QAOARunRequest):
    """Execute QAOA optimization experiment on frozen Phase L QUBO model for a district."""
    solver = QAOASolver()
    try:
        res = solver.run_qaoa(
            district_id=payload.district_id,
            max_k=payload.max_k,
            qaoa_depth_p=payload.qaoa_depth_p,
            shots=payload.shots,
            optimizer=payload.optimizer,
            seed=payload.seed,
            persist=True
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"QAOA experiment failed: {str(e)}")

@qaoa_router.post("/benchmark", summary="Run Multi-Algorithm Benchmark (Exact/MILP/Greedy vs QAOA)")
def run_qaoa_benchmark(payload: QAOABenchmarkRequest):
    """Run multi-algorithm classical-vs-QAOA benchmark across p=1,2,3 depths."""
    engine = QAOABenchmarkEngine()
    try:
        res = engine.run_benchmark(
            district_id=payload.district_id,
            max_k=payload.max_k,
            p_depths=payload.p_depths,
            shots=payload.shots,
            seed=payload.seed,
            persist=True
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"QAOA benchmark failed: {str(e)}")

@qaoa_router.get("/benchmarks", summary="Get QAOA Benchmark History")
def get_benchmarks(district_id: Optional[str] = Query(None)):
    with get_db_context() as db:
        query = db.query(QAOABenchmarkRecord)
        if district_id:
            query = query.filter_by(district_id=district_id.lower())
        records = query.order_by(QAOABenchmarkRecord.created_at.desc()).all()
        return [
            {
                "benchmark_id": r.benchmark_id,
                "district_id": r.district_id,
                "qubo_id": r.qubo_id,
                "qubit_count": r.qubit_count,
                "classical_method": r.classical_method,
                "qaoa_p": r.qaoa_p,
                "shots": r.shots,
                "seed": r.seed,
                "classical_objective": r.classical_objective,
                "qaoa_objective": r.qaoa_objective,
                "objective_gap": r.objective_gap,
                "feasible_probability": r.feasible_probability,
                "optimal_probability": r.optimal_probability,
                "runtime_ms": r.runtime_ms,
                "circuit_depth": r.circuit_depth,
                "two_qubit_gates": r.two_qubit_gates,
                "status": r.status
            } for r in records
        ]

@qaoa_router.get("/statistics", summary="Get Global QAOA Experiment Statistics")
def get_qaoa_statistics():
    try:
        import qiskit
        qv = getattr(qiskit, "__version__", "1.0.0")
    except ImportError:
        qv = "1.0.0"

    with get_db_context() as db:
        total_exp = db.query(QAOAExperimentRecord).count()
        total_bench = db.query(QAOABenchmarkRecord).count()
        verified_certs = db.query(QAOACertificateRecord).filter_by(status="VERIFIED").count()
        return {
            "total_qaoa_experiments": total_exp,
            "total_benchmarks_run": total_bench,
            "verified_certificates": verified_certs,
            "backend": "Qiskit Aer Simulator 0.17.2",
            "qiskit_version": qv
        }


@qaoa_router.get("/{experiment_id}", summary="Get QAOA Experiment Record")
def get_experiment(experiment_id: str = Path(...)):
    with get_db_context() as db:
        exp = db.query(QAOAExperimentRecord).filter_by(experiment_id=experiment_id).first()
        if not exp:
            raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found.")
        
        return {
            "experiment_id": exp.experiment_id,
            "qubo_id": exp.qubo_id,
            "qubo_hash": exp.qubo_hash,
            "classical_model_hash": exp.classical_model_hash,
            "district_id": exp.district_id,
            "candidate_count": exp.candidate_count,
            "slack_count": exp.slack_count,
            "logical_qubit_count": exp.logical_qubit_count,
            "qaoa_depth": exp.qaoa_depth,
            "optimizer": exp.optimizer,
            "seed": exp.seed,
            "shots": exp.shots,
            "backend": exp.backend,
            "final_expectation": exp.final_expectation,
            "best_sample_energy": exp.best_sample_energy,
            "best_sample_objective": exp.best_sample_objective,
            "classical_optimum_objective": exp.classical_optimum_objective,
            "objective_gap": exp.objective_gap,
            "relative_objective_gap": exp.relative_objective_gap,
            "feasible_probability": exp.feasible_probability,
            "optimal_probability": exp.optimal_probability,
            "constraint_violation_rate": exp.constraint_violation_rate,
            "total_time": exp.total_time,
            "status": exp.convergence_status
        }

@qaoa_router.get("/{experiment_id}/samples", summary="Get QAOA Bitstring Sample Distribution")
def get_experiment_samples(experiment_id: str = Path(...)):
    with get_db_context() as db:
        samples = db.query(QAOASampleRecord).filter_by(experiment_id=experiment_id).order_by(QAOASampleRecord.probability.desc()).all()
        return [
            {
                "sample_id": s.sample_id,
                "bitstring": s.bitstring,
                "probability": s.probability,
                "count": s.count,
                "decoded_strategy_ids": s.decoded_strategy_ids,
                "decoded_slack_values": s.decoded_slack_values,
                "qubo_energy": s.qubo_energy,
                "original_objective": s.original_objective,
                "is_feasible": s.is_feasible,
                "is_optimal": s.is_optimal,
                "violations": s.constraint_violations
            } for s in samples
        ]

@qaoa_router.get("/{experiment_id}/circuit", summary="Get QAOA Circuit Metrics")
def get_experiment_circuit(experiment_id: str = Path(...)):
    with get_db_context() as db:
        circ = db.query(QAOACircuitRecord).filter_by(experiment_id=experiment_id).first()
        if not circ:
            raise HTTPException(status_code=404, detail=f"Circuit for experiment '{experiment_id}' not found.")
        
        return {
            "circuit_id": circ.circuit_id,
            "experiment_id": circ.experiment_id,
            "qubit_count": circ.qubit_count,
            "qaoa_depth": circ.qaoa_depth,
            "gate_count": circ.gate_count,
            "two_qubit_gate_count": circ.two_qubit_gate_count,
            "depth": circ.depth,
            "basis_gates": circ.basis_gates,
            "backend": circ.backend,
            "circuit_hash": circ.circuit_hash
        }
