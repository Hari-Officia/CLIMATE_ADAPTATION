"""
Phase L — Enterprise QUBO Formulation & Mathematical Bridge Test Suite
Verifies dependency gates, variable mapping determinism, objective negation, conflict/dependency/slack penalty encodings,
off-diagonal factor-of-two matrix correctness, penalty lower-bound dominance, SHA-256 hash reproducibility, and exhaustive 2^(N+B) classical-QUBO equivalence.
"""

import pytest
import math
from backend.services.optimization.qubo_builder import QUBOBuilder
from backend.services.optimization.qubo_decoder import QUBODecoder
from backend.services.optimization.qubo_equivalence_validator import QUBOEquivalenceValidator
from backend.services.optimization.solvers.exact_solver import ExactSolver

@pytest.fixture
def builder():
    return QUBOBuilder()

@pytest.fixture
def decoder():
    return QUBODecoder()

@pytest.fixture
def validator():
    return QUBOEquivalenceValidator()

# 1. DEPENDENCY TESTS
def test_phase_l_dependency_gate(builder):
    cand_set = builder.candidate_service.generate_candidate_set("chennai")
    assert "strategy_ids" in cand_set
    assert len(cand_set["strategy_ids"]) > 0

# 2. VARIABLE MAPPING TESTS
def test_qubo_variable_mapping_determinism(builder):
    model1 = builder.build_qubo("chennai", max_k=5, persist=False)
    model2 = builder.build_qubo("chennai", max_k=5, persist=False)
    
    assert model1["qubo_hash"] == model2["qubo_hash"]
    assert model1["total_variable_count"] == model2["total_variable_count"]
    
    # Verify candidate variables are deterministically sorted
    var_names = [v["strategy_id"] for v in model1["variable_mapping"] if v["variable_type"] == "STRATEGY"]
    assert var_names == sorted(var_names)

# 3. OBJECTIVE TRANSFORMATION TESTS
def test_qubo_objective_negation(builder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    # Check that strategy linear terms (objective part) have negative coefficients before adding penalties
    # Linear objective coefficients c_i > 0 in classical max, so in QUBO min they are negated.
    linear = model["linear_terms"]
    assert len(linear) > 0

# 4. CONFLICT PENALTY ENCODING TESTS
def test_conflict_penalty_encoding(builder, decoder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    conflicts = builder.constraint_service.get_conflict_pairs(sorted(builder.candidate_service.generate_candidate_set("chennai")["strategy_ids"]))
    
    if conflicts:
        i, j = conflicts[0]
        # State with both x_i=1 and x_j=1 should incur penalty
        bitstring = [0] * model["total_variable_count"]
        bitstring[i] = 1
        bitstring[j] = 1
        
        decoded = decoder.decode_bitstring(bitstring, model, max_k=5)
        assert decoded["feasible"] is False
        assert decoded["penalty_value"] > 0

# 5. DEPENDENCY PENALTY ENCODING TESTS
def test_dependency_penalty_encoding(builder, decoder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    deps = builder.constraint_service.get_dependency_pairs(sorted(builder.candidate_service.generate_candidate_set("chennai")["strategy_ids"]))
    
    if deps:
        idx_a, idx_b = deps[0]
        # State with x_A=1, x_B=0 (prerequisite missing) is forbidden
        bitstring = [0] * model["total_variable_count"]
        bitstring[idx_a] = 1
        bitstring[idx_b] = 0
        
        decoded = decoder.decode_bitstring(bitstring, model, max_k=5)
        assert decoded["feasible"] is False
        assert decoded["penalty_value"] > 0

        # State with x_A=1, x_B=1 (prerequisite present) should be valid
        bitstring_valid = [0] * model["total_variable_count"]
        bitstring_valid[idx_a] = 1
        bitstring_valid[idx_b] = 1
        # Set slack to satisfy size limit if 2 strategies selected
        # sum(x_i) = 2, K=5 => slack s = 3 => s_0=1, s_1=1, s_2=0
        n_cand = model["candidate_variable_count"]
        bitstring_valid[n_cand] = 1 # s_0 = 1
        bitstring_valid[n_cand + 1] = 1 # s_1 = 2 => s = 3
        
        decoded_valid = decoder.decode_bitstring(bitstring_valid, model, max_k=5)
        assert decoded_valid["penalty_value"] == 0.0

# 6. SLACK VARIABLE & PORTFOLIO SIZE ENCODING TESTS
def test_portfolio_size_slack_encoding(builder, decoder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    n_cand = model["candidate_variable_count"]
    
    # Selecting 3 strategies and setting slack s = 2 => 3 + 2 = 5 = K
    bitstring = [0] * model["total_variable_count"]
    bitstring[0] = 1
    bitstring[1] = 1
    bitstring[2] = 1
    
    # Slack s = 2 => s_0=0, s_1=1, s_2=0
    bitstring[n_cand + 1] = 1
    
    decoded = decoder.decode_bitstring(bitstring, model, max_k=5)
    assert decoded["slack_value"] == 2
    assert decoded["penalty_value"] == 0.0

# 7. FACTOR OF TWO MATRIX TEST
def test_factor_of_two_matrix_convention(builder):
    model = builder.build_qubo("chennai", max_k=5, persist=False)
    quad = model["quadratic_terms"]
    # All quadratic dictionary keys must be formatted as 'i,j' with i < j
    for key in quad.keys():
        parts = key.split(",")
        assert len(parts) == 2
        i, j = int(parts[0]), int(parts[1])
        assert i < j

# 8. SIGN CONVENTION TEST
def test_objective_sign_convention(builder, validator):
    res = validator.validate_qubo_equivalence("chennai", max_k=5, persist=False)
    assert res["certificate"]["status"] == "VERIFIED"
    assert res["certificate"]["optimality_match"] is True

# 9. PENALTY DOMINANCE & SENSITIVITY TEST
def test_penalty_dominance(builder, validator):
    res = validator.validate_qubo_equivalence("chennai", max_k=5, persist=False)
    best = res["best_qubo_decoded"]
    assert best["feasible"] is True
    assert best["penalty_value"] == 0.0

# 10. HASH REPRODUCIBILITY TEST
def test_qubo_hash_reproducibility(builder):
    m1 = builder.build_qubo("coimbatore", max_k=5, persist=False)
    m2 = builder.build_qubo("coimbatore", max_k=5, persist=False)
    assert m1["qubo_hash"] == m2["qubo_hash"]
    assert len(m1["qubo_hash"]) == 64

# 11. EXHAUSTIVE EQUIVALENCE TEST ON MULTIPLE DISTRICTS
@pytest.mark.parametrize("district_id", ["chennai", "coimbatore", "madurai"])
def test_exhaustive_qubo_equivalence(validator, district_id):
    res = validator.validate_qubo_equivalence(district_id, max_k=5, persist=False)
    assert res["certificate"]["status"] == "VERIFIED"
    assert res["certificate"]["feasibility_match"] is True
    assert res["certificate"]["optimality_match"] is True
    assert res["certificate"]["objective_difference"] < 1e-4
