# Phase AC-R Execution Call Trace Audit Report

```text
execute_physical_job()
  |- transpile_physical_circuit() [logical_depth=4p+2, 0 SWAPs]
  |- NoiseSimulator.run_noisy_simulation() [gate_error=0.0075, readout_error=0.012]
  |- IndependentEvaluator.evaluate_bitstring() [original_objective, feasible, gap]
  |- job_id fabricated locally: JOB-PHYSICAL-IBM_SHER-<hash>
```

## Trace Audit Summary
- **Physical Hardware Provider Invoked**: `FALSE`
- **Noise Simulator Proxy Invoked**: `TRUE`
- **Qiskit Runtime Job Created**: `FALSE`
- **Job ID Origin**: Local string formatting (`JOB-PHYSICAL-IBM_SHER-...`)
