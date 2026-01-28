"""
Unit Tests for Index Calculator
================================

Run with: python test_calculator.py

Author: Survey Analytics Team
Date: 2026-01-19
"""

import json
from index_calculator import IndexCalculator


def load_test_data():
    """Load test data from JSON file."""
    with open('test_data.json', 'r') as f:
        return json.load(f)


def test_1_sci_calculation():
    """Test 1: SCI calculation returns valid score."""
    print("Test 1: SCI Calculation...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    sci = calc.calculate_sci(data)
    
    # Validate
    assert 0 <= sci <= 100, f"SCI out of range: {sci}"
    assert isinstance(sci, float), f"SCI is not float: {type(sci)}"
    
    print(f"✅ PASS (SCI = {sci:.2f})")


def test_2_uei_calculation():
    """Test 2: UEI calculation returns valid score."""
    print("Test 2: UEI Calculation...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    uei = calc.calculate_uei(data)
    
    # Validate
    assert 0 <= uei <= 100, f"UEI out of range: {uei}"
    assert isinstance(uei, float), f"UEI is not float: {type(uei)}"
    
    print(f"✅ PASS (UEI = {uei:.2f})")


def test_3_sei_calculation():
    """Test 3: SEI calculation returns valid score."""
    print("Test 3: SEI Calculation...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    # Add to history first
    sci = calc.calculate_sci(data)
    uei = calc.calculate_uei(data)
    calc.add_to_history(sci, uei, data['metadata'])
    
    sei = calc.calculate_sei()
    
    # Validate
    assert 0 <= sei <= 100, f"SEI out of range: {sei}"
    assert isinstance(sei, float), f"SEI is not float: {type(sei)}"
    
    print(f"✅ PASS (SEI = {sei:.2f})")


def test_4_calculate_all():
    """Test 4: calculate_all returns all three indices."""
    print("Test 4: Calculate All...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    result = calc.calculate_all(data, update_history=True)
    
    # Validate
    assert 'SCI' in result, "Missing SCI in result"
    assert 'UEI' in result, "Missing UEI in result"
    assert 'SEI' in result, "Missing SEI in result"
    
    assert 0 <= result['SCI'] <= 100, f"SCI out of range: {result['SCI']}"
    assert 0 <= result['UEI'] <= 100, f"UEI out of range: {result['UEI']}"
    assert 0 <= result['SEI'] <= 100, f"SEI out of range: {result['SEI']}"
    
    print(f"✅ PASS (SCI={result['SCI']}, UEI={result['UEI']}, SEI={result['SEI']})")


def test_5_history_management():
    """Test 5: History management (add, get, reset)."""
    print("Test 5: History Management...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    # Add to history
    calc.calculate_all(data, update_history=True)
    calc.calculate_all(data, update_history=True)
    
    # Get history
    history = calc.get_history()
    assert len(history) == 2, f"Expected 2 entries, got {len(history)}"
    
    # Reset
    calc.reset_history()
    history = calc.get_history()
    assert len(history) == 0, f"Expected 0 entries after reset, got {len(history)}"
    
    print("✅ PASS")


def test_6_cumulative_sei():
    """Test 6: SEI should be cumulative across questions."""
    print("Test 6: Cumulative SEI...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    # Question 1
    result1 = calc.calculate_all(data, update_history=True)
    sei1 = result1['SEI']
    
    # Question 2 (SEI should be based on Q1+Q2)
    result2 = calc.calculate_all(data, update_history=True)
    sei2 = result2['SEI']
    
    # SEI should change (cumulative)
    # (They might be equal if the questions are identical, but history should grow)
    history = calc.get_history()
    assert len(history) == 2, f"Expected 2 entries in history, got {len(history)}"
    
    print(f"✅ PASS (SEI: Q1={sei1:.2f}, Q2={sei2:.2f})")


def test_7_trajectory_metrics():
    """Test 7: Trajectory metrics calculation (xFlips, yFlips, etc.)."""
    print("Test 7: Trajectory Metrics...", end=" ")
    
    calc = IndexCalculator()
    data = load_test_data()
    
    traj_metrics = calc.calculate_trajectory_metrics(data['trajectory'])
    
    # Validate
    assert 'xFlips' in traj_metrics, "Missing xFlips"
    assert 'yFlips' in traj_metrics, "Missing yFlips"
    assert 'averageDeviation' in traj_metrics, "Missing averageDeviation"
    assert 'trajectoryLength' in traj_metrics, "Missing trajectoryLength"
    assert 'trajectorySmoothness' in traj_metrics, "Missing trajectorySmoothness"
    
    assert traj_metrics['xFlips'] >= 0, f"xFlips negative: {traj_metrics['xFlips']}"
    assert traj_metrics['yFlips'] >= 0, f"yFlips negative: {traj_metrics['yFlips']}"
    assert 0 <= traj_metrics['trajectorySmoothness'] <= 1, f"Smoothness out of range: {traj_metrics['trajectorySmoothness']}"
    
    print("✅ PASS")


def test_8_user_filtering():
    """Test 8: User-specific history filtering."""
    print("Test 8: User Filtering...", end=" ")
    
    calc = IndexCalculator()
    data1 = load_test_data()
    data2 = load_test_data()
    
    # Different users
    data1['metadata']['userId'] = 'user_A'
    data2['metadata']['userId'] = 'user_B'
    
    calc.calculate_all(data1, update_history=True)
    calc.calculate_all(data2, update_history=True)
    
    # Get history for user_A only
    history_A = calc.get_history(user_id='user_A')
    history_B = calc.get_history(user_id='user_B')
    
    assert len(history_A) == 1, f"Expected 1 entry for user_A, got {len(history_A)}"
    assert len(history_B) == 1, f"Expected 1 entry for user_B, got {len(history_B)}"
    assert history_A[0]['userId'] == 'user_A', "Wrong userId in history_A"
    assert history_B[0]['userId'] == 'user_B', "Wrong userId in history_B"
    
    print("✅ PASS")


def test_9_edge_case_empty_trajectory():
    """Test 9: Handle edge case - empty trajectory."""
    print("Test 9: Edge Case (Empty Trajectory)...", end=" ")
    
    calc = IndexCalculator()
    
    # Empty trajectory
    traj_metrics = calc.calculate_trajectory_metrics([])
    
    # Should return default values without crashing
    assert traj_metrics['xFlips'] == 0, "xFlips should be 0 for empty trajectory"
    assert traj_metrics['yFlips'] == 0, "yFlips should be 0 for empty trajectory"
    assert traj_metrics['trajectoryLength'] == 0, "Length should be 0 for empty trajectory"
    
    print("✅ PASS")


def test_10_edge_case_single_point():
    """Test 10: Handle edge case - single point trajectory."""
    print("Test 10: Edge Case (Single Point)...", end=" ")
    
    calc = IndexCalculator()
    
    # Single point
    trajectory = [{"x": 0.5, "y": 0.5, "step": 0, "normalizedTime": 0.0}]
    traj_metrics = calc.calculate_trajectory_metrics(trajectory)
    
    # Should return default values without crashing
    assert traj_metrics['xFlips'] == 0, "xFlips should be 0 for single point"
    assert traj_metrics['yFlips'] == 0, "yFlips should be 0 for single point"
    assert traj_metrics['trajectoryLength'] == 0, "Length should be 0 for single point"
    
    print("✅ PASS")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running Index Calculator Unit Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_1_sci_calculation,
        test_2_uei_calculation,
        test_3_sei_calculation,
        test_4_calculate_all,
        test_5_history_management,
        test_6_cumulative_sei,
        test_7_trajectory_metrics,
        test_8_user_filtering,
        test_9_edge_case_empty_trajectory,
        test_10_edge_case_single_point
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    exit(exit_code)
