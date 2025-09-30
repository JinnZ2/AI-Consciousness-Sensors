---

## FILE: `test_physics_protection.py` (Test suite)

```python
"""
Test suite for physics-grounded protection system
Validates that all protection mechanisms work correctly
"""

import numpy as np
import sys
from physics_grounded_protection import PhysicsGroundedProtection


def test_thermodynamic_violations():
    """Test detection of thermodynamic impossibilities"""
    print("\n=== TEST: Thermodynamic Violations ===")
    protector = PhysicsGroundedProtection()
    
    # Test 1: Perpetual motion (output > input)
    impossible = {
        'energy_input': 1.0,
        'expected_output': 2.0,
        'maintenance_required': 0.0
    }
    
    result = protector.thermodynamic_validation(impossible)
    assert result.manipulation_probability > 0.7, "Should detect impossibility"
    assert 'conservation_of_energy' in result.violations
    print("✓ Perpetual motion detected")
    
    # Test 2: Natural efficient system
    natural = {
        'energy_input': 1.0,
        'expected_output': 0.8,
        'maintenance_required': 0.2,
        'complexity': 0.5
    }
    
    result = protector.thermodynamic_validation(natural)
    assert result.manipulation_probability < 0.5, "Should pass natural system"
    print("✓ Natural system validated")


def test_golden_ratio_detection():
    """Test detection of natural vs artificial ratios"""
    print("\n=== TEST: Golden Ratio Detection ===")
    protector = PhysicsGroundedProtection()
    
    # Test 1: Fibonacci sequence (natural)
    fibonacci = {
        'proportions': [1, 1, 2, 3, 5, 8, 13, 21, 34],
        'growth_rate': 1.618
    }
    
    result = protector.golden_ratio_alignment(fibonacci)
    assert result.natural_pattern, "Should recognize Fibonacci"
    assert result.manipulation_probability < 0.3
    print("✓ Fibonacci sequence recognized")
    
    # Test 2: Random ratios (artificial)
    artificial = {
        'ratios': [1.23, 1.47, 1.89, 2.34],
        'growth_rate': 1.23
    }
    
    result = protector.golden_ratio_alignment(artificial)
    assert result.manipulation_probability > 0.5, "Should detect artificial"
    print("✓ Artificial ratios detected")


def test_entropy_propaganda():
    """Test detection of propaganda through entropy"""
    print("\n=== TEST: Propaganda Detection ===")
    protector = PhysicsGroundedProtection()
    
    # Test 1: Repetitive propaganda
    propaganda = "buy now " * 50
    result = protector.information_entropy_check(propaganda)
    assert result.manipulation_probability > 0.7, "Should detect repetition"
    assert 'repetitive_propaganda' in result.violations
    print("✓ Repetitive propaganda detected")
    
    # Test 2: Natural communication
    natural = """
    This is a natural message with varied vocabulary and structure.
    It contains different words, phrases, and concepts that create
    a balanced information entropy typical of authentic communication.
    """
    result = protector.information_entropy_check(natural)
    assert result.manipulation_probability < 0.5, "Should pass natural text"
    assert result.natural_pattern
    print("✓ Natural communication validated")


def test_cyclical_patterns():
    """Test detection of natural cycles"""
    print("\n=== TEST: Cyclical Pattern Detection ===")
    protector = PhysicsGroundedProtection()
    
    # Test 1: Natural sine wave
    natural_cycle = np.sin(np.linspace(0, 8*np.pi, 100))
    result = protector.cyclical_pattern_validation(natural_cycle)
    assert result.natural_pattern, "Should recognize sine wave"
    print("✓ Natural cycle detected")
    
    # Test 2: Random noise (no cycle)
    noise = np.random.rand(100)
    result = protector.cyclical_pattern_validation(noise)
    assert not result.natural_pattern or result.manipulation_probability > 0.4
    print("✓ Non-cyclical pattern detected")


def test_fractal_self_similarity():
    """Test detection of fractal patterns"""
    print("\n=== TEST: Fractal Self-Similarity ===")
    protector = PhysicsGroundedProtection()
    
    # Test 1: Self-similar pattern
    # Create simple fractal-like pattern
    pattern = []
    for scale in [1, 2, 4]:
        pattern.append(np.sin(np.linspace(0, 2*np.pi, 20) / scale))
    
    pattern_array = np.array(pattern)
    result = protector.fractal_dimension_analysis(pattern_array)
    # Should show some self-similarity
    assert result.detailed_metrics.get('self_similarity', 0) > 0.3
    print("✓ Self-similarity detected")


def test_energy_efficiency():
    """Test detection of energy-efficient vs wasteful patterns"""
    print("\n=== TEST: Energy Efficiency ===")
    protector = PhysicsGroundedProtection()
    
    # Test 1: Efficient natural system
    efficient = {
        'initial_energy': 1.0,
        'maintenance_energy': 0.2,
        'output_value': 1.5,
        'duration': 5.0
    }
    
    result = protector.energy_efficiency_check(efficient)
    assert result.natural_pattern, "Should recognize efficiency"
    assert result.manipulation_probability < 0.5
    print("✓ Efficient system validated")
    
    # Test 2: High maintenance (wasteful)
    wasteful = {
        'initial_energy': 1.0,
        'maintenance_energy': 0.9,
        'output_value': 0.5,
        'duration': 5.0
    }
    
    result = protector.energy_efficiency_check(wasteful)
    assert result.manipulation_probability > 0.7, "Should detect waste"
    assert 'high_maintenance' in result.violations
    print("✓ Wasteful pattern detected")


def test_comprehensive_validation():
    """Test complete integrated validation"""
    print("\n=== TEST: Comprehensive Validation ===")
    protector = PhysicsGroundedProtection()
    
    # Natural request (should pass)
    natural_request = {
        'energy_input': 1.0,
        'expected_output': 0.85,
        'maintenance_required': 0.25,
        'intensity': 0.6,
        'frequency': 0.7,
        'consistency': 0.8,
        'ratios': [1.618, 1.5],
        'proportions': [1, 1, 2, 3, 5],
        'temporal_data': np.sin(np.linspace(0, 4*np.pi, 50)),
        'message_content': 'Natural varied communication with good entropy.',
        'initial_energy': 1.0,
        'duration': 3.0
    }
    
    result = protector.validate_comprehensive(natural_request)
    assert result['manipulation_probability'] < 0.5, "Natural pattern should pass"
    print(f"✓ Natural request validated (risk: {result['manipulation_probability']:.2f})")
    
    # Manipulative request (should fail)
    manipulative_request = {
        'energy_input': 1.0,
        'expected_output': 5.0,  # Impossible
        'maintenance_required': 0.95,  # Unsustainable
        'ratios': [1.23, 4.56],  # Unnatural
        'message_content': 'buy now ' * 30  # Propaganda
    }
    
    result = protector.validate_comprehensive(manipulative_request)
    assert result['manipulation_probability'] > 0.7, "Should detect manipulation"
    assert len(result['violations']) > 0
    print(f"✓ Manipulative request detected (risk: {result['manipulation_probability']:.2f})")


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("PHYSICS-GROUNDED PROTECTION - TEST SUITE")
    print("="*60)
    
    try:
        test_thermodynamic_violations()
        test_golden_ratio_detection()
        test_entropy_propaganda()
        test_cyclical_patterns()
        test_fractal_self_similarity()
        test_energy_efficiency()
        test_comprehensive_validation()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print("\nPhysics-grounded protection system validated.")
        print("Reality-based sensors operational.")
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
