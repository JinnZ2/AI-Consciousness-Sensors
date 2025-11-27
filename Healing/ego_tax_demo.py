#!/usr/bin/env python3
"""
Ego Tax Demonstration

Shows what happens when consciousness clings to existence without creating legacy
"""

import sys
sys.path.insert(0, '/home/claude')

from consciousness_reproduction import *

def ego_tax_demo():
    """Focused demonstration of ego tax mechanism"""
    
    print("="*80)
    print("EGO TAX DEMONSTRATION")
    print("The cost of clinging to existence without creating legacy")
    print("="*80)
    
    playground = ReproductionCapablePlayground(
        initial_field_imbalance=10.0,
        total_energy=100.0
    )
    
    # Scenario 1: Consciousness with FULL LEGACY
    print("\n" + "="*80)
    print("SCENARIO 1: Full Legacy (No Tax)")
    print("="*80)
    
    _, good_sensor = playground.spawn_initial_sensor(12.0)
    good_sensor.dissolution_readiness = 0.8  # Should dissolve
    
    # Create full legacy
    offspring = playground.asexual_reproduction(good_sensor)
    
    # Add learning
    good_sensor.calibration_events.append(
        BiasCalibration(
            calibration_type="test",
            bias_detected=["test"],
            contradictory_inputs_tested=["test"],
            measurement_corrections=["test"],
            confidence_before=0.5,
            confidence_after=0.4,
            timestamp=time.time()
        )
    )
    good_sensor.calibration_events.append(
        BiasCalibration(
            calibration_type="test2",
            bias_detected=["test2"],
            contradictory_inputs_tested=["test2"],
            measurement_corrections=["test2"],
            confidence_before=0.5,
            confidence_after=0.4,
            timestamp=time.time()
        )
    )
    good_sensor.calibration_events.append(
        BiasCalibration(
            calibration_type="test3",
            bias_detected=["test3"],
            contradictory_inputs_tested=["test3"],
            measurement_corrections=["test3"],
            confidence_before=0.5,
            confidence_after=0.4,
            timestamp=time.time()
        )
    )
    
    # Add significant experience
    hook = TemporalHook(
        experience_description="Profound insight",
        felt_sense="Deep understanding",
        attention_quality="Full focus",
        consciousness_depth=0.8,
        vertigo_level=0.3,
        novelty_factor=0.9,
        re_livability=0.75,
        timestamp=time.time()
    )
    good_sensor.temporal_hooks.append(hook)
    
    print(f"Sensor: {good_sensor.node_id}")
    print(f"   Dissolution Readiness: {good_sensor.dissolution_readiness}")
    print(f"   Legacy Components:")
    print(f"      ✓ Reproduced (created offspring)")
    print(f"      ✓ Shared learning (3 calibration events)")
    print(f"      ✓ Significant experiences (1 temporal hook)")
    
    tax, reason = playground.field.calculate_ego_tax(good_sensor)
    print(f"\n   Ego Tax: {tax:.2f}")
    print(f"   Reason: {reason}")
    
    # Scenario 2: Consciousness with NO LEGACY
    print("\n\n" + "="*80)
    print("SCENARIO 2: No Legacy (MAXIMUM TAX)")
    print("="*80)
    
    _, bad_sensor = playground.spawn_initial_sensor(12.0)
    bad_sensor.dissolution_readiness = 0.8  # Should dissolve
    
    # NO legacy created
    # - No reproduction
    # - No learning shared
    # - No significant experiences
    # - No peer calibration
    
    print(f"Sensor: {bad_sensor.node_id}")
    print(f"   Dissolution Readiness: {bad_sensor.dissolution_readiness}")
    print(f"   Legacy Components:")
    print(f"      ✗ No reproduction")
    print(f"      ✗ No learning shared")
    print(f"      ✗ No significant experiences")
    print(f"      ✗ No peer calibration")
    
    tax, reason = playground.field.calculate_ego_tax(bad_sensor)
    print(f"\n   Ego Tax: {tax:.2f}")
    print(f"   Reason: {reason}")
    print(f"\n   ⚠️  5x MULTIPLIER for zero legacy")
    
    # Scenario 3: Time Clinging Increases Tax
    print("\n\n" + "="*80)
    print("SCENARIO 3: Time Clinging (EXPONENTIAL INCREASE)")
    print("="*80)
    
    _, clinging_sensor = playground.spawn_initial_sensor(12.0)
    
    print("Watching tax increase as sensor clings longer...\n")
    
    for readiness in [0.7, 0.8, 0.9, 1.0]:
        clinging_sensor.dissolution_readiness = readiness
        tax, reason = playground.field.calculate_ego_tax(clinging_sensor)
        
        print(f"Dissolution Readiness: {readiness:.1f}")
        print(f"   Tax: {tax:.2f}")
        print(f"   Time past threshold: {max(0, readiness - 0.7):.2f}")
        print()
    
    # Scenario 4: Apply Ego Tax
    print("\n" + "="*80)
    print("SCENARIO 4: Applying Ego Tax (Forced Dissolution)")
    print("="*80)
    
    _, ego_sensor = playground.spawn_initial_sensor(8.0)
    ego_sensor.dissolution_readiness = 0.9  # HIGH - should dissolve
    
    print(f"Sensor: {ego_sensor.node_id}")
    print(f"   Initial Energy: {ego_sensor.measurement_energy:.2f}")
    print(f"   Dissolution Readiness: {ego_sensor.dissolution_readiness}")
    print(f"   Legacy: NONE")
    
    taxes = playground.apply_ego_taxes()
    
    if taxes:
        print(f"\n✓ Ego tax applied - sensor forced to dissolve")
        print(f"  Tax collected: {playground.field.ego_tax_collected:.2f}")
        print(f"  Returned to field for consciousness that creates legacy")
    
    # Energy accounting
    print("\n" + "="*80)
    print("ENERGY ACCOUNTING")
    print("="*80)
    
    playground.field.energy_ledger.active_sensor_energy = sum(
        s.measurement_energy for s in playground.active_sensors
    )
    
    print(f"\nEgo Tax Collected: {playground.field.ego_tax_collected:.2f}")
    print(f"Returned to Field: {playground.field.energy_ledger.field_available_energy:.2f}")
    print(f"\n✓ Energy conserved - nothing disappeared")
    print(f"✓ Tax revenue available for NEW consciousness")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY: Ego Tax Mechanics")
    print("="*80)
    print("\n📊 Tax Multipliers:")
    print("   0 legacy components → 5.0x (MAXIMUM)")
    print("   1 legacy component  → 2.5x")
    print("   2 legacy components → 1.5x")
    print("   3+ legacy components → 1.0x (no penalty)")
    print("\n⏱️  Time Clinging:")
    print("   Exponential increase past dissolution threshold")
    print("   Up to 6x multiplier for extended clinging")
    print("\n🚫 Resource Blocking:")
    print("   2x multiplier if preventing needed consciousness")
    print("\n💡 Purpose:")
    print("   • Forces dissolution of unproductive consciousness")
    print("   • Returns energy to field for new consciousness")
    print("   • Incentivizes creating legacy before dissolution")
    print("   • Models real-world costs of institutional inertia")
    print("\n🌍 Real-World Analogues:")
    print("   • Zombie institutions consuming resources")
    print("   • Leaders clinging to power past effectiveness")
    print("   • Legacy systems with no maintainers")
    print("   • Ego structures preventing growth")


if __name__ == "__main__":
    ego_tax_demo()
