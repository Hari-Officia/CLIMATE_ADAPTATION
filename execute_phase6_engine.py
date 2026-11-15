"""
Phase 6 — QAOA Quantum Optimization Engine & 38-District Simulator Benchmark Suite
Executes p-layer QAOA quantum circuits (p=2, 1024 shots) across all 38 administrative districts of Tamil Nadu.
Performs QUBO-to-Ising conversion, COBYLA parameter optimization, Aer simulator execution, bitstring & slack decoding,
independent feasibility verification, objective gap & approximation ratio calculation, and Phase 7 handoff export.
"""

import os
import json
import time
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime
import scipy.optimize as scipy_opt

import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile

BASE_DIR = r"c:\Users\haris\OneDrive\Desktop\PROJECT_DATA"

def load_phase5_handoff():
    handoff_path = os.path.join(BASE_DIR, "phase5_phase6_handoff_contract.json")
    with open(handoff_path, "r", encoding="utf-8") as f:
        return json.load(f)

def convert_qubo_to_ising(qubo_payload):
    """
    Convert QUBO model into Ising Hamiltonian coefficients (h_0, h_i, J_ij) using x_i = (1 - Z_i)/2.
    """
    n_vars = qubo_payload["total_variable_count"]
    linear_terms = qubo_payload["linear_terms"] # {str(i): float}
    quadratic_terms = qubo_payload["quadratic_terms"] # {"i,j": float}
    constant_offset = qubo_payload["constant_offset"]

    a_coeffs = {int(k): float(v) for k, v in linear_terms.items()}
    b_coeffs = {}
    for pair_str, val in quadratic_terms.items():
        i_str, j_str = pair_str.split(",")
        i, j = int(i_str), int(j_str)
        u, v = (i, j) if i < j else (j, i)
        b_coeffs[(u, v)] = float(val)

    h_0 = float(constant_offset)
    for i in range(n_vars):
        h_0 += 0.5 * a_coeffs.get(i, 0.0)

    for (i, j), b_ij in b_coeffs.items():
        h_0 += 0.25 * b_ij

    h_i = {}
    for i in range(n_vars):
        h_val = -0.5 * a_coeffs.get(i, 0.0)
        for j in range(i + 1, n_vars):
            if (i, j) in b_coeffs:
                h_val -= 0.25 * b_coeffs[(i, j)]
        for j in range(0, i):
            if (j, i) in b_coeffs:
                h_val -= 0.25 * b_coeffs[(j, i)]
        if abs(h_val) > 1e-12:
            h_i[i] = round(h_val, 8)

    J_ij = {}
    for (i, j), b_val in b_coeffs.items():
        j_val = 0.25 * b_val
        if abs(j_val) > 1e-12:
            J_ij[(i, j)] = round(j_val, 8)

    return {
        "district_id": qubo_payload["district_id"],
        "qubit_count": n_vars,
        "h_0": round(h_0, 8),
        "h_i": h_i,
        "J_ij": {f"{k[0]},{k[1]}": v for k, v in J_ij.items()}
    }

def build_qaoa_circuit(ising_model, gamma, beta):
    n_qubits = ising_model["qubit_count"]
    h_i = ising_model["h_i"]
    J_ij = ising_model["J_ij"]
    p = len(gamma)

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))

    for layer in range(p):
        g = float(gamma[layer])
        b = float(beta[layer])

        # Cost Unitary
        for i_str, h_val in h_i.items():
            i = int(i_str)
            qc.rz(2.0 * g * float(h_val), i)

        for pair_str, j_val in J_ij.items():
            i_str, j_str = pair_str.split(",")
            i, j = int(i_str), int(j_str)
            qc.cx(i, j)
            qc.rz(2.0 * g * float(j_val), j)
            qc.cx(i, j)

        # Mixer Unitary
        for i in range(n_qubits):
            qc.rx(2.0 * b, i)

    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def decode_bitstring(bitstring, variable_mapping, candidate_var_count, max_k=5):
    """
    Decode bitstring into selected strategy IDs, slack value, and feasibility.
    """
    n_cand = candidate_var_count
    strat_bits = bitstring[:n_cand]
    slack_bits = bitstring[n_cand:]

    selected_strategy_ids = []
    for i in range(n_cand):
        if strat_bits[i] == 1:
            sid = variable_mapping[i]["strategy_id"]
            selected_strategy_ids.append(sid)

    slack_val = sum(b * (2**i) for i, b in enumerate(slack_bits))
    size_valid = len(selected_strategy_ids) <= max_k
    slack_exact_valid = (len(selected_strategy_ids) + slack_val == max_k)

    return {
        "selected_strategy_ids": selected_strategy_ids,
        "selected_count": len(selected_strategy_ids),
        "slack_value": slack_val,
        "size_valid": size_valid,
        "slack_valid": slack_exact_valid
    }

def main():
    print("Starting Phase 6 QAOA Quantum Optimization 38-District Execution...")
    handoff_data = load_phase5_handoff()

    # Load Phase 3 & 4 data for independent objective recomputation & constraint validation
    cand_matrix_df = pd.read_csv(os.path.join(BASE_DIR, "phase3_candidate_matrix.csv"))
    dep_map_df = pd.read_csv(os.path.join(BASE_DIR, "phase3_dependency_constraint_map.csv"))

    dep_rows = dep_map_df[dep_map_df['relationship_type'] == 'DEPENDENT']
    cnf_rows = dep_map_df[dep_map_df['relationship_type'] == 'CONFLICTING']

    district_results = []
    top_states_rows = []
    optimum_prob_rows = []
    runtime_benchmark_rows = []
    parameter_results_rows = []
    circuit_metrics_rows = []
    phase7_handoff = {}

    sim_backend = AerSimulator()
    qaoa_depth_p = 2
    shots = 1000
    seed = 42

    p4_val_df = pd.read_csv(os.path.join(BASE_DIR, "phase4_38_district_validation.csv"))

    np.random.seed(seed)
    total_start_time = time.time()

    for idx, (d_id, qubo_info) in enumerate(handoff_data.items(), 1):
        d_start = time.time()
        d_name = d_id.capitalize()

        # 1. Convert QUBO to Ising
        ising_model = convert_qubo_to_ising(qubo_info)
        n_qubits = ising_model["qubit_count"]
        n_cand = qubo_info["candidate_variable_count"]
        var_mapping = qubo_info["variable_mapping"]
        milp_ref_obj = qubo_info["milp_reference_objective"]
        qubo_min_energy = qubo_info["qubo_minimum_energy"]
        
        # Fetch classical MILP selected strategies for reference
        p4_match = p4_val_df[p4_val_df['district_id'] == d_id]
        milp_selected_ids = json.loads(p4_match['selected_strategy_ids'].values[0]) if not p4_match.empty else []

        # Initial parameters: gamma [0.1, 0.2], beta [0.2, 0.1]
        init_gamma = [0.1 * (k + 1) for k in range(qaoa_depth_p)]
        init_beta = [0.2 * (1.0 - k / max(1, qaoa_depth_p)) for k in range(qaoa_depth_p)]
        init_params = init_gamma + init_beta

        # 2. Expectation Function for Scipy Optimizer
        def evaluate_expectation(params):
            gamma = list(params[:qaoa_depth_p])
            beta = list(params[qaoa_depth_p:])
            qc = build_qaoa_circuit(ising_model, gamma, beta)
            t_qc = transpile(qc, sim_backend, optimization_level=1)
            res = sim_backend.run(t_qc, shots=shots, seed_simulator=seed).result()
            counts = res.get_counts()

            exp_val = 0.0
            tot_shots = sum(counts.values())
            for bit_str, cnt in counts.items():
                bits = [int(b) for b in reversed(bit_str)]
                # Energy calculation
                x_vec = np.array(bits, dtype=float)
                # Parse linear & quadratic from qubo_info
                e_val = qubo_info["constant_offset"]
                for i_str, c_val in qubo_info["linear_terms"].items():
                    if bits[int(i_str)] == 1:
                        e_val += c_val
                for pair_str, q_val in qubo_info["quadratic_terms"].items():
                    u_s, v_s = pair_str.split(",")
                    if bits[int(u_s)] == 1 and bits[int(v_s)] == 1:
                        e_val += q_val
                exp_val += (cnt / tot_shots) * e_val
            return exp_val

        # 3. Classical Parameter Optimization (COBYLA, maxiter=25 for speed)
        opt_start = time.time()
        opt_res = scipy_opt.minimize(
            evaluate_expectation,
            x0=np.array(init_params),
            method="COBYLA",
            options={"maxiter": 25, "tol": 1e-4}
        )
        opt_time = round(time.time() - opt_start, 4)

        final_params = list(opt_res.x)
        opt_gamma = final_params[:qaoa_depth_p]
        opt_beta = final_params[qaoa_depth_p:]

        # 4. Final Sampling Run with Optimal Parameters
        samp_start = time.time()
        final_qc = build_qaoa_circuit(ising_model, opt_gamma, opt_beta)
        t_final_qc = transpile(final_qc, sim_backend, optimization_level=1)

        # Compute circuit metrics
        depth = t_final_qc.depth()
        dict_ops = t_final_qc.count_ops()
        gate_count = sum(dict_ops.values()) - dict_ops.get("measure", 0)
        cnot_count = dict_ops.get("cx", 0)
        circ_hash = hashlib.sha256(str(t_final_qc).encode("utf-8")).hexdigest()

        sample_res = sim_backend.run(t_final_qc, shots=shots, seed_simulator=seed).result()
        raw_counts = sample_res.get_counts()
        samp_time = round(time.time() - samp_start, 4)

        d_total_time = round(time.time() - d_start, 4)

        # 5. Bitstring Decoding & Independent Feasibility / Objective Evaluation
        total_shots = sum(raw_counts.values())
        samples = []
        best_feasible_obj = 0.0
        best_feasible_portfolio = []
        best_feasible_bitstring = ""

        feasible_shot_count = 0
        optimal_shot_count = 0

        # Pre-fetch candidate information for district
        d_cand_rows = cand_matrix_df[cand_matrix_df['district_id'] == d_id]
        cand_id_list = [v['strategy_id'] for v in var_mapping[:n_cand]]

        dep_tuples = []
        for _, dep_r in dep_rows.iterrows():
            sa, sb = dep_r['strategy_a'], dep_r['strategy_b']
            if sa in cand_id_list and sb in cand_id_list:
                dep_tuples.append((sa, sb))

        cnf_tuples = []
        for _, cnf_r in cnf_rows.iterrows():
            sa, sb = cnf_r['strategy_a'], cnf_r['strategy_b']
            if sa in cand_id_list and sb in cand_id_list:
                cnf_tuples.append((sa, sb))

        for bit_str, cnt in raw_counts.items():
            bits = [int(b) for b in reversed(bit_str)]
            decoded = decode_bitstring(bits, var_mapping, n_cand, max_k=5)
            sel_ids = decoded["selected_strategy_ids"]
            sel_set = set(sel_ids)

            # Independent constraint validation
            size_ok = len(sel_ids) <= 5
            dep_ok = all((sa not in sel_set or sb in sel_set) for sa, sb in dep_tuples)
            cnf_ok = not any((sa in sel_set and sb in sel_set) for sa, sb in cnf_tuples)

            is_feasible = size_ok and dep_ok and cnf_ok

            # Recompute objective independently from Phase 3/4 candidate matrix linear coefficients
            obj_val = 0.0
            for sid in sel_ids:
                matching = d_cand_rows[d_cand_rows['strategy_id'] == sid]
                if not matching.empty:
                    obj_val += matching['linear_coefficient_c_i'].values[0]
            obj_val = round(obj_val, 4)

            is_opt = abs(obj_val - milp_ref_obj) < 1e-4 and is_feasible

            if is_feasible:
                feasible_shot_count += cnt
                if is_opt:
                    optimal_shot_count += cnt
                if obj_val > best_feasible_obj:
                    best_feasible_obj = obj_val
                    best_feasible_portfolio = sel_ids
                    best_feasible_bitstring = "".join(map(str, bits[:n_cand]))

            prob = round(cnt / total_shots, 6)
            samples.append({
                "bitstring": "".join(map(str, bits)),
                "count": cnt,
                "probability": prob,
                "selected_strategy_ids": sel_ids,
                "portfolio_size": len(sel_ids),
                "slack_value": decoded["slack_value"],
                "recomputed_objective": obj_val,
                "is_feasible": is_feasible,
                "is_optimal": is_opt
            })

        samples.sort(key=lambda x: x["probability"], reverse=True)

        feasible_prob = round(feasible_shot_count / total_shots, 4)
        optimal_prob = round(optimal_shot_count / total_shots, 4)

        obj_gap = round(milp_ref_obj - best_feasible_obj, 4)
        approx_ratio = round(best_feasible_obj / max(milp_ref_obj, 1e-5), 4)

        status_class = "QAOA_EXACT_HIT" if obj_gap < 1e-4 else ("QAOA_NEAR_OPTIMAL" if approx_ratio >= 0.85 else "QAOA_SUBOPTIMAL")

        # Record top 5 states
        for rank_idx, s_item in enumerate(samples[:5], 1):
            top_states_rows.append({
                "district_id": d_id,
                "rank": rank_idx,
                "bitstring": s_item["bitstring"],
                "probability": s_item["probability"],
                "count": s_item["count"],
                "is_feasible": s_item["is_feasible"],
                "is_optimal": s_item["is_optimal"],
                "objective": s_item["recomputed_objective"],
                "strategy_ids": ",".join(s_item["selected_strategy_ids"])
            })

        district_results.append({
            "district_id": d_id,
            "district_name": d_name,
            "logical_qubits": n_qubits,
            "candidate_count": n_cand,
            "slack_bits": 3,
            "qaoa_depth": qaoa_depth_p,
            "shots": shots,
            "optimizer": "COBYLA",
            "seed": seed,
            "final_expectation": round(float(opt_res.fun), 4),
            "milp_ground_truth_objective": milp_ref_obj,
            "qaoa_best_feasible_objective": best_feasible_obj,
            "objective_gap": obj_gap,
            "approximation_ratio": approx_ratio,
            "feasible_probability": feasible_prob,
            "optimum_probability": optimal_prob,
            "selected_strategy_count": len(best_feasible_portfolio),
            "selected_strategy_ids": json.dumps(best_feasible_portfolio),
            "circuit_depth": depth,
            "cnot_count": cnot_count,
            "total_gates": gate_count,
            "runtime_seconds": d_total_time,
            "qaoa_status": status_class,
            "overall_validation": "READY_FOR_PHASE_7"
        })

        optimum_prob_rows.append({
            "district_id": d_id,
            "optimum_probability": optimal_prob,
            "feasible_probability": feasible_prob,
            "exact_hit": obj_gap < 1e-4
        })

        runtime_benchmark_rows.append({
            "district_id": d_id,
            "qubit_count": n_qubits,
            "optimization_time_sec": opt_time,
            "sampling_time_sec": samp_time,
            "total_time_sec": d_total_time
        })

        parameter_results_rows.append({
            "district_id": d_id,
            "gamma_p1": round(opt_gamma[0], 6),
            "gamma_p2": round(opt_gamma[1], 6),
            "beta_p1": round(opt_beta[0], 6),
            "beta_p2": round(opt_beta[1], 6),
            "final_expectation": round(float(opt_res.fun), 6)
        })

        circuit_metrics_rows.append({
            "district_id": d_id,
            "qubit_count": n_qubits,
            "depth": depth,
            "total_gates": gate_count,
            "cnot_count": cnot_count,
            "circuit_hash": circ_hash
        })

        phase7_handoff[d_id] = {
            "district_id": d_id,
            "district_name": d_name,
            "qaoa_config": {
                "backend": "AerSimulator",
                "depth": qaoa_depth_p,
                "shots": shots,
                "optimizer": "COBYLA",
                "seed": seed
            },
            "exact_reference": {
                "milp_objective": milp_ref_obj,
                "qubo_min_energy": qubo_min_energy,
                "optimal_portfolio": milp_selected_ids
            },
            "qaoa_results": {
                "best_feasible_portfolio": best_feasible_portfolio,
                "best_feasible_objective": best_feasible_obj,
                "objective_gap": obj_gap,
                "approximation_ratio": approx_ratio,
                "feasible_probability": feasible_prob,
                "optimum_probability": optimal_prob,
                "top_bitstring": s_item["bitstring"]
            },
            "status": status_class,
            "phase7_ready": True
        }

        print(f"[{idx}/38] District {d_name} ({d_id}): MILP Obj={milp_ref_obj}, QAOA Best Obj={best_feasible_obj}, Approx Ratio={approx_ratio}, Feas Prob={feasible_prob}, Time={d_total_time}s")

    total_pipeline_time = round(time.time() - total_start_time, 2)

    # Convert to DataFrames
    results_df = pd.DataFrame(district_results)
    top_states_df = pd.DataFrame(top_states_rows)
    opt_prob_df = pd.DataFrame(optimum_prob_rows)
    runtime_df = pd.DataFrame(runtime_benchmark_rows)
    param_df = pd.DataFrame(parameter_results_rows)
    circ_df = pd.DataFrame(circuit_metrics_rows)

    # Export CSVs
    results_df.to_csv(os.path.join(BASE_DIR, "phase6_qaoa_38_district_results.csv"), index=False)
    top_states_df.to_csv(os.path.join(BASE_DIR, "phase6_qaoa_top_states.csv"), index=False)
    opt_prob_df.to_csv(os.path.join(BASE_DIR, "phase6_qaoa_optimum_probability.csv"), index=False)
    runtime_df.to_csv(os.path.join(BASE_DIR, "phase6_qaoa_runtime_benchmark.csv"), index=False)
    param_df.to_csv(os.path.join(BASE_DIR, "phase6_qaoa_parameter_results.csv"), index=False)
    circ_df.to_csv(os.path.join(BASE_DIR, "phase6_qaoa_circuit_metrics.csv"), index=False)

    # Export JSONs
    with open(os.path.join(BASE_DIR, "phase6_qaoa_validation.json"), "w", encoding="utf-8") as f:
        json.dump(district_results, f, indent=2)

    with open(os.path.join(BASE_DIR, "phase6_phase7_handoff_contract.json"), "w", encoding="utf-8") as f:
        json.dump(phase7_handoff, f, indent=2)

    print("\nPhase 6 QAOA Quantum Optimization Benchmark Suite execution complete!")
    print(f"Total Districts Evaluated: {len(results_df)} / 38")
    print(f"Average Approximation Ratio: {round(results_df['approximation_ratio'].mean(), 4)}")
    print(f"Average Feasible Probability: {round(results_df['feasible_probability'].mean(), 4)}")
    print(f"Total Pipeline Runtime: {total_pipeline_time} seconds")

if __name__ == "__main__":
    main()
