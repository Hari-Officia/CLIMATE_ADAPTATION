import sys
import os
import asyncio
import traceback
import importlib.util
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

def load_test_module(name: str):
    file_path = os.path.join(ROOT_DIR, "tests", f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_tests():
    passed = 0
    failed = 0

    print("=" * 65)
    print("STARTING TEST SUITE: Climate Risk System (Review II)")
    print("=" * 65)

    # 1. Geocoding & Point-in-Polygon
    print("\n--- 1. Testing Geocoding & Point-in-Polygon ---")
    try:
        t_geo = load_test_module("test_geocoding_pip")
        t_geo.test_marina_beach_point_in_polygon()
        print("  [PASS] test_marina_beach_point_in_polygon")
        t_geo.test_coimbatore_point_in_polygon()
        print("  [PASS] test_coimbatore_point_in_polygon")
        t_geo.test_avadi_point_in_polygon()
        print("  [PASS] test_avadi_point_in_polygon")
        t_geo.test_outside_tamil_nadu_boundary()
        print("  [PASS] test_outside_tamil_nadu_boundary")
        t_geo.test_reverse_geocoding()
        print("  [PASS] test_reverse_geocoding")
        passed += 5
    except Exception as e:
        print(f"  [FAIL] Geocoding tests: {e}")
        traceback.print_exc()
        failed += 1

    # 2. Feature Engineering 53 features
    print("\n--- 2. Testing Feature Engineering & Schema Alignment ---")
    try:
        t_feat = load_test_module("test_feature_engineering")
        t_feat.test_feature_engineering_exact_53_columns()
        print("  [PASS] test_feature_engineering_exact_53_columns")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Feature Engineering test: {e}")
        traceback.print_exc()
        failed += 1

    # 3. Risk Agent & XGBoost Inference
    print("\n--- 3. Testing Risk Agent & XGBoost Inference ---")
    try:
        t_risk = load_test_module("test_risk_agent")
        t_risk.test_risk_agent_model_loading_and_inference()
        print("  [PASS] test_risk_agent_model_loading_and_inference")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Risk Agent test: {e}")
        traceback.print_exc()
        failed += 1

    # 4. Auth & RBAC
    print("\n--- 4. Testing Auth & Role-Based Access Control ---")
    try:
        t_auth = load_test_module("test_auth")
        t_auth.test_login_success_harish()
        print("  [PASS] test_login_success_harish")
        t_auth.test_login_success_admin()
        print("  [PASS] test_login_success_admin")
        t_auth.test_login_invalid_password()
        print("  [PASS] test_login_invalid_password")
        t_auth.test_get_me_with_token()
        print("  [PASS] test_get_me_with_token")
        t_auth.test_admin_route_forbidden_for_regular_user()
        print("  [PASS] test_admin_route_forbidden_for_regular_user")
        passed += 5
    except Exception as e:
        print(f"  [FAIL] Auth tests: {e}")
        traceback.print_exc()
        failed += 1

    # 5. Climate Data Agent
    print("\n--- 5. Testing Climate Data Acquisition Agent ---")
    try:
        t_clim = load_test_module("test_climate_agent")
        asyncio.run(t_clim.test_climate_agent_fetching_and_normalization())
        print("  [PASS] test_climate_agent_fetching_and_normalization")
        asyncio.run(t_clim.test_climate_agent_caching())
        print("  [PASS] test_climate_agent_caching")
        passed += 2
    except Exception as e:
        print(f"  [FAIL] Climate Agent tests: {e}")
        traceback.print_exc()
        failed += 1

    # 6. Feature Contracts & Diagnostics
    print("\n--- 6. Testing Feature Contracts & Distribution Diagnostics ---")
    try:
        t_fc = load_test_module("test_feature_contracts")
        suite = unittest.TestLoader().loadTestsFromTestCase(t_fc.TestFeatureContracts)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        if res.wasSuccessful():
            print(f"  [PASS] All {res.testsRun} Feature Contract tests passed")
            passed += res.testsRun
        else:
            print(f"  [FAIL] Feature Contract tests failed: {res.failures}")
            failed += len(res.failures) + len(res.errors)
    except Exception as e:
        print(f"  [FAIL] Feature Contract tests: {e}")
        traceback.print_exc()
        failed += 1

    # 7. Multi-Hazard Architecture & Scientific Indices
    print("\n--- 7. Testing Extensible Multi-Hazard Registry & Physical Indices ---")
    try:
        t_mh = load_test_module("test_multi_hazards")
        suite = unittest.TestLoader().loadTestsFromTestCase(t_mh.TestMultiHazards)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        if res.wasSuccessful():
            print(f"  [PASS] All {res.testsRun} Multi-Hazard Engine tests passed")
            passed += res.testsRun
        else:
            print(f"  [FAIL] Multi-Hazard tests failed: {res.failures}")
            failed += len(res.failures) + len(res.errors)
    except Exception as e:
        print(f"  [FAIL] Multi-Hazard tests: {e}")
        traceback.print_exc()
        failed += 1

    # 8. No Silent Zero Imputation Rule
    print("\n--- 8. Testing Zero-Tolerance Policy for Silent Zero Imputation ---")
    try:
        t_nz = load_test_module("test_no_silent_zero")
        suite = unittest.TestLoader().loadTestsFromTestCase(t_nz.TestNoSilentZero)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        if res.wasSuccessful():
            print(f"  [PASS] All {res.testsRun} Zero-Tolerance tests passed")
            passed += res.testsRun
        else:
            print(f"  [FAIL] Zero-Tolerance tests failed: {res.failures}")
            failed += len(res.failures) + len(res.errors)
    except Exception as e:
        print(f"  [FAIL] Zero-Tolerance tests: {e}")
        traceback.print_exc()
        failed += 1

    # 9. End-to-End Integration
    print("\n--- 9. Testing End-to-End Integration Flow ---")
    try:
        t_integ = load_test_module("test_integration")
        t_integ.test_full_pipeline_flow()
        print("  [PASS] test_full_pipeline_flow")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Integration test: {e}")
        traceback.print_exc()
        failed += 1

    print("\n" + "=" * 65)
    print(f"TEST RUN SUMMARY: {passed} PASSED, {failed} FAILED")
    print("=" * 65)

    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
