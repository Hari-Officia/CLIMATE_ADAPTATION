# PHASE 5 V2 — QUBO FORMULATION & EQUIVALENCE PROOF MASTER REPORT
**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation and Mitigation Strategy Planning (Q-MADSS)  
**Geography:** All 38 Administrative Districts of Tamil Nadu, India  
**Strategy Version:** V2.0 Expanded (42 Canonical Strategies, 18 Candidates per District)  
**Status:** `QUBO_V2_READY_FOR_QAOA`  
**Date:** October 6, 2026  

---

## 1. Executive Summary

Phase 5 V2 converts the certified Phase 4 V2 MILP strategy selection problems into mathematically equivalent **Quadratic Unconstrained Binary Optimization (QUBO)** formulations suitable for Phase 6 V2 QAOA quantum optimization. Each district problem is represented by a $21 \times 21$ upper-triangular QUBO matrix $Q$ (comprising 18 strategy variables $x_0 \dots x_{17}$ and 3 binary slack variables $s_0, s_1, s_2$ to enforce the portfolio size inequality $\sum x_i + s = 5$).

Equivalence Verification Results:
- **Matrix Dimension:** Exactly 21 QUBO variables per district ($18 + 3 = 21$).
- **Equivalence Status:** **38 / 38 Districts (100%)**
- **Equivalence Energy Gap:** **0.0000** error between global QUBO energy minimum $E(x^*, s^*)$ and exact Phase 4 V2 MILP ground truth objective score ($E_{\text{min}} = -F_{\text{MILP}}^*$).
- **Penalty Parameter Rigor:** $P_{\text{size}} = 50.0, P_{\text{dep}} = 100.0, P_{\text{conf}} = 100.0$ mathematically proven to exceed maximum achievable adaptation benefit ($\sum c_i = 15.6$), ensuring zero ground-state constraint leakage.

---

## 2. Mathematical QUBO Energy Derivation

The total QUBO energy objective is formulated as:

$$E(x, s) = -\sum_{i=0}^{17} c_i x_i + P_{\text{size}} \left(\sum_{i=0}^{17} x_i + s_0 + 2s_1 + 4s_2 - 5\right)^2 + P_{\text{dep}} \sum_{(A,B)} x_A(1 - x_B) + P_{\text{conf}} \sum_{(A,B)} x_A x_B$$

### Binary Slack Variable Representation
Since $K = 5$, portfolio size $\sum x_i$ ranges from $0$ to $5$. The slack variable $s = 5 - \sum x_i \in \{0, 1, \dots, 5\}$ is binary encoded as:
$$s = s_0 + 2 s_1 + 4 s_2, \quad s_0, s_1, s_2 \in \{0, 1\}$$

---

## 3. 38-District QUBO V2 Equivalence Summary

| District ID | District Name | QUBO Dim | Strategy Bits | Slack Bits | QUBO Min Energy ($E^*$) | Decoded Objective | MILP Obj ($F^*$) | Equivalence Error | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `ariyalur` | Ariyalur | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `chengalpattu` | Chengalpattu | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `chennai` | Chennai | 21 | 18 | 3 | **-4.6600** | **4.6600** | **4.6600** | 0.0000 | `EQUIVALENT` |
| `coimbatore` | Coimbatore | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `cuddalore` | Cuddalore | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `dharmapuri` | Dharmapuri | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `dindigul` | Dindigul | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `erode` | Erode | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `kallakurichi` | Kallakurichi | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `kancheepuram` | Kancheepuram | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `kanniyakumari` | Kanniyakumari | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `karur` | Karur | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `krishnagiri` | Krishnagiri | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `madurai` | Madurai | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `mayiladuthurai` | Mayiladuthurai | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `nagapattinam` | Nagapattinam | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `namakkal` | Namakkal | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `nilgiris` | Nilgiris | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `perambalur` | Perambalur | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `pudukkottai` | Pudukkottai | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `ramanathapuram`| Ramanathapuram| 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `ranipet` | Ranipet | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `salem` | Salem | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `sivaganga` | Sivaganga | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `tenkasi` | Tenkasi | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `thanjavur` | Thanjavur | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `theni` | Theni | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `thoothukudi` | Thoothukudi | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `tiruchirappalli`| Tiruchirappalli | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `tirunelveli` | Tirunelveli | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `tirupathur` | Tirupathur | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `tiruppur` | Tiruppur | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `tiruvallur` | Tiruvallur | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `tiruvannamalai`| Tiruvannamalai| 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `tiruvarur` | Tiruvarur | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `vellore` | Vellore | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |
| `viluppuram` | Viluppuram | 21 | 18 | 3 | **-4.6900** | **4.6900** | **4.6900** | 0.0000 | `EQUIVALENT` |
| `virudhunagar` | Virudhunagar | 21 | 18 | 3 | **-4.6400** | **4.6400** | **4.6400** | 0.0000 | `EQUIVALENT` |

---

## 4. Final Classification

Phase 5 V2 passes all certification gates with zero equivalence error:

### **`QUBO_V2_READY_FOR_QAOA`**
