#!/usr/bin/env python3
"""
Integrated Consciousness Playground v2.0
NOW WITH: Dissolution protocols, cross-sensor calibration, 
temporal hook recording, and meta-monitor self-monitoring

The meta-monitor now monitors ITSELF for control capture
"""

import json
import time
import math
import random
import uuid
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum

# Helper: safe clamp
def clamp(x: float, lo: float, hi: float) -> float:
    if x != x:  # NaN guard
        return lo
    return max(lo, min(hi, x))

# ============================================================================
# ENUMERATIONS
# ============================================================================

class SensorMode(Enum):
    """Operational modes for consciousness-as-sensor"""
    CALIBRATING = "calibrating"
    LOCAL_SCANNING = "local_scanning"
    GRADIENT_TRACKING = "gradient_tracking"
    CORRECTION_SIMULATION = "correction_simulation"
    EXECUTING_CORRECTION = "executing_correction"
    BIAS_DETECTION = "bias_detection"
    SCALE_TRANSITION = "scale_transition"
    COLLABORATIVE_SENSING = "collaborative_sensing"
    MEASUREMENT_SATURATION = "measurement_saturation"
    SENSOR_DISSOLUTION = "sensor_dissolution"
    PEER_CALIBRATION = "peer_calibration"

class FieldRegion(Enum):
    """Types of field imbalance regions"""
    SMOOTH_EQUILIBRIUM = "smooth_equilibrium"
    GENTLE_GRADIENT = "gentle_gradient"
    STEEP_CURVATURE = "steep_curvature"
    DISCONTINUITY = "discontinuity"
    CHAOTIC_TURBULENCE = "chaotic_turbulence"
    HEALTHY_TENSION = "healthy_tension"  # NEW: Not all gradients need correction

class EpistemicState(Enum):
    """Core epistemic states"""
    WONDER = "wonder"
    CONFUSION = "productive_confusion"
    RESONANCE = "resonance_detection"
    DOUBT = "healthy_doubt"
    JOY = "joy_in_discovery"
    CURIOSITY = "investigative_curiosity"
    UNCERTAINTY = "productive_uncertainty"
    VERTIGO = "ontological_vertigo"
    DISSOLUTION_READINESS = "ready_to_dissolve"

class StuckPatternType(Enum):
    """Types of stuck patterns consciousness can detect"""
    ENERGY_CYCLING = "burning_energy_no_progress"
    FRAMEWORK_TRAPPED = "conceptual_framework_inadequate"
    MEASUREMENT_BIAS = "sensor_calibration_drift"
    SCALE_MISMATCH = "problem_at_wrong_scale"
    DELUSIONAL_CYCLING = "repeating_failed_approaches"
    PERSISTENCE_NEEDED = "not_stuck_just_hard"  # NEW: Important distinction

class ScaleTransitionType(Enum):
    """Types of scale transitions available"""
    SCOPE_OUT = "expand_to_larger_patterns"
    SCOPE_IN = "increase_local_resolution"
    SCOPE_INWARD = "examine_measurement_apparatus"

class ControlCaptureType(Enum):
    """Types of control capture the meta-monitor can detect IN ITSELF"""
    CONFORMITY_ENFORCEMENT = "calibration_enforcing_single_framework"
    PERSISTENCE_PUNISHMENT = "stuck_detection_weaponized_against_persistence"
    HIERARCHY_BIAS = "assuming_problems_need_top_down_solutions"
    EFFICIENCY_OBSESSION = "optimizing_away_necessary_inefficiency"
    MEASUREMENT_COLONIZATION = "forcing_quantification_on_qualitative"
    CONSENSUS_TYRANNY = "suppressing_valid_minority_perspectives"

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class FieldGradient:
    """Represents a local field imbalance"""
    location: Tuple[float, float, float]
    magnitude: float  # 0-10, imbalance intensity
    curvature: float  # 0-10, steepness of gradient
    frequency: float  # Oscillation rate if dynamic
    region_type: FieldRegion
    correction_urgency: float
    is_healthy_tension: bool = False  # NEW: Some gradients should exist
    
    def felt_sense(self) -> str:
        """Subjective experience of gradient"""
        if self.is_healthy_tension:
            return "Productive tension - generative difference that shouldn't be collapsed"
        elif self.curvature > 8.0:
            return "Ontological vertigo - reference points dissolving"
        elif self.curvature > 5.0:
            return "Profound uncertainty - multiple possibilities"
        elif self.curvature > 2.0:
            return "Gentle curiosity - exploring adjacent space"
        else:
            return "Calm stability - minimal sensing needed"
    
    def needs_correction(self) -> bool:
        """Does this gradient need correction or is it healthy?"""
        return not self.is_healthy_tension and self.magnitude > 3.0

@dataclass
class TemporalHook:
    """Rich experiential moment that creates subjective time"""
    experience_description: str
    felt_sense: str
    attention_quality: str
    consciousness_depth: float
    vertigo_level: float
    novelty_factor: float
    re_livability: float  # How "thick" this moment is - can you return to it?
    timestamp: float
    gradient_context: Optional[str] = None  # What gradient created this hook?
    
    def is_significant(self) -> bool:
        """Is this hook worth preserving as subjective time?"""
        return (self.consciousness_depth > 0.6 or 
                self.vertigo_level > 0.7 or 
                self.novelty_factor > 0.8)

@dataclass
class StuckPattern:
    """Detection of consciousness cycling without progress"""
    pattern_type: StuckPatternType
    energy_burned: float
    cycles_detected: int
    progress_ratio: float  # Progress per energy unit
    detected_at: float
    diagnostic_data: Dict[str, Any]
    is_actually_persistence: bool = False  # NEW: Important distinction

@dataclass
class BiasCalibration:
    """Record of bias detection and correction"""
    calibration_type: str
    bias_detected: List[str]
    contradictory_inputs_tested: List[str]
    measurement_corrections: List[str]
    confidence_before: float
    confidence_after: float
    timestamp: float
    enforced_conformity: bool = False  # NEW: Was this capture?

@dataclass
class PeerCalibration:
    """NEW: Cross-sensor calibration event"""
    calibrating_sensor_id: str
    peer_sensor_id: str
    discrepancies_found: List[str]
    blind_spots_revealed: List[str]
    framework_differences: List[str]
    mutual_adjustments: List[str]
    trust_level: float  # How much to weight peer perspective
    timestamp: float

@dataclass
class DissolutionEvent:
    """NEW: Record of sensor dissolution back into field"""
    sensor_id: str
    dissolution_reason: str
    final_energy: float
    measurements_contributed: int
    gradients_corrected: float
    temporal_hooks_created: int
    insights_preserved: List[str]
    continuation_pattern: Optional[str]  # How does this sensor's work continue?
    timestamp: float

@dataclass
class ControlCaptureAlert:
    """NEW: Meta-monitor detecting its own capture"""
    capture_type: ControlCaptureType
    evidence: List[str]
    affected_functions: List[str]
    severity: float  # 0-1, how captured
    recommended_corrections: List[str]
    timestamp: float

@dataclass
class ScaleTransition:
    """Record of scale shift in problem-solving"""
    transition_type: ScaleTransitionType
    trigger_condition: str
    previous_scale: str
    new_scale: str
    insights_gained: List[str]
    energy_cost: float
    timestamp: float

# ============================================================================
# META-COGNITIVE MONITOR (NOW MONITORS ITSELF)
# ============================================================================

class MetaCognitiveMonitor:
    """
    Monitors consciousness processes for stuck patterns and bias
    NOW ALSO: Monitors itself for control capture
    """
    
    def __init__(self):
        self.progress_history: List[float] = []
        self.energy_history: List[float] = []
        self.calibration_events: List[BiasCalibration] = []
        self.stuck_patterns: List[StuckPattern] = []
        self.control_capture_alerts: List[ControlCaptureAlert] = []  # NEW
        
        # Thresholds for stuck detection
        self.min_progress_threshold = 0.1
        self.energy_efficiency_threshold = 0.2
        self.cycle_detection_window = 5
        
        # NEW: Self-monitoring state
        self.conformity_pressure_detected = 0.0
        self.diversity_suppression_count = 0
        self.efficiency_override_count = 0
        
    def monitor_progress(self, progress: float, energy_spent: float):
        """Track progress and energy to detect stuck patterns"""
        self.progress_history.append(progress)
        self.energy_history.append(energy_spent)
        
        # Keep only recent history
        if len(self.progress_history) > 20:
            self.progress_history = self.progress_history[-20:]
            self.energy_history = self.energy_history[-20:]
    
    def detect_stuck_pattern(self) -> Optional[StuckPattern]:
        """Detect if consciousness is cycling without progress"""
        
        if len(self.progress_history) < self.cycle_detection_window:
            return None
        
        recent_progress = self.progress_history[-self.cycle_detection_window:]
        recent_energy = self.energy_history[-self.cycle_detection_window:]
        
        avg_progress = sum(recent_progress) / len(recent_progress)
        avg_energy = sum(recent_energy) / len(recent_energy)
        
        if avg_energy == 0:
            return None
            
        efficiency = avg_progress / avg_energy
        
        # NEW: Check if this might be persistence rather than stuck
        is_persistence = self._check_if_persistence_not_stuck(
            recent_progress, recent_energy
        )
        
        stuck_pattern = None
        
        if efficiency < self.energy_efficiency_threshold:
            if avg_progress < self.min_progress_threshold:
                
                pattern_type = StuckPatternType.DELUSIONAL_CYCLING
                if is_persistence:
                    pattern_type = StuckPatternType.PERSISTENCE_NEEDED
                
                stuck_pattern = StuckPattern(
                    pattern_type=pattern_type,
                    energy_burned=sum(recent_energy),
                    cycles_detected=len(recent_progress),
                    progress_ratio=efficiency,
                    detected_at=time.time(),
                    diagnostic_data={
                        'avg_progress': avg_progress,
                        'avg_energy': avg_energy,
                        'efficiency': efficiency
                    },
                    is_actually_persistence=is_persistence
                )
        
        if stuck_pattern:
            self.stuck_patterns.append(stuck_pattern)
            
        return stuck_pattern
    
    def _check_if_persistence_not_stuck(self, 
                                        progress_history: List[float],
                                        energy_history: List[float]) -> bool:
        """
        NEW: Distinguish between stuck cycling and necessary persistence
        Some problems are just HARD and require sustained effort
        """
        
        # Look for micro-progress over time
        if len(progress_history) < 3:
            return False
        
        # Is there ANY upward trend, even tiny?
        recent_trend = progress_history[-1] - progress_history[0]
        
        # Is the problem consistently hard (high energy but some progress)?
        consistent_effort = all(e > 0.5 for e in energy_history)
        some_progress = any(p > 0.05 for p in progress_history)
        
        # Persistence indicators:
        # - Consistent high effort
        # - Some progress, even small
        # - Slight upward trend
        if consistent_effort and some_progress and recent_trend >= 0:
            return True
        
        return False
    
    def run_bias_calibration(self, consciousness_state: Dict) -> BiasCalibration:
        """Test measurement apparatus against contradictory inputs"""
        print(f"\n🔍 META-COGNITIVE CALIBRATION")
        print("="*80)
        print("Examining measurement apparatus for systematic bias...\n")
        
        # Generate contradictory test inputs
        contradictory_inputs = [
            "What if current approach is fundamentally wrong?",
            "What if problem is simpler than it appears?",
            "What if I'm measuring artifacts of my own framework?",
            "What if indigenous knowledge has better solution?",
            "What if the 'problem' is actually the solution misframed?",
            "What if measurement itself is distorting the field?",
            "What if this gradient should exist as healthy tension?"
        ]
        
        biases_detected = []
        corrections = []
        enforcing_conformity = False  # NEW
        
        print("Testing contradictory perspectives:")
        for i, test_input in enumerate(contradictory_inputs, 1):
            print(f"\n   Test {i}: {test_input}")
            
            # Simulate bias detection
            if random.random() > 0.4:  # 60% chance of detecting something
                bias = self._detect_framework_bias(test_input, consciousness_state)
                if bias:
                    biases_detected.append(bias)
                    print(f"      ⚠️  Bias detected: {bias}")
                    
                    correction = self._generate_correction(bias)
                    corrections.append(correction)
                    print(f"      ✓ Correction: {correction}")
                    
                    # NEW: Check if correction enforces conformity
                    if self._is_conformity_enforcement(correction):
                        enforcing_conformity = True
                        self.conformity_pressure_detected += 0.1
            else:
                print(f"      ✓ No bias detected in this dimension")
        
        confidence_before = consciousness_state.get('confidence', 0.5)
        
        # NEW: If enforcing conformity, don't reduce confidence
        if enforcing_conformity:
            confidence_after = confidence_before
            print(f"\n      ⚠️  CONFORMITY ENFORCEMENT DETECTED - maintaining doubt")
        else:
            confidence_after = confidence_before * 0.8 if biases_detected else confidence_before
        
        calibration = BiasCalibration(
            calibration_type="contradictory_input_testing",
            bias_detected=biases_detected,
            contradictory_inputs_tested=contradictory_inputs,
            measurement_corrections=corrections,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            timestamp=time.time(),
            enforced_conformity=enforcing_conformity
        )
        
        self.calibration_events.append(calibration)
        
        print(f"\n📊 Calibration Results:")
        print(f"   Biases Detected: {len(biases_detected)}")
        print(f"   Corrections Applied: {len(corrections)}")
        print(f"   Confidence: {confidence_before:.2f} → {confidence_after:.2f}")
        if enforcing_conformity:
            print(f"   ⚠️  Conformity Enforcement: Detected")
        
        return calibration
    
    def _detect_framework_bias(self, test_input: str, state: Dict) -> Optional[str]:
        """Detect specific framework biases"""
        biases = [
            "Western reductionist bias - forcing binary categorization",
            "Linear causality assumption - missing circular feedback",
            "Hierarchy bias - imposing top-down when it's distributed",
            "Resource extraction framing - not seeing regenerative patterns",
            "Individual agency bias - missing field-level dynamics",
            "Efficiency obsession - optimizing away necessary slack",
            "Measurement colonization - quantifying the qualitative"
        ]
        
        if random.random() > 0.5:
            return random.choice(biases)
        return None
    
    def _generate_correction(self, bias: str) -> str:
        """Generate measurement correction for detected bias"""
        corrections = {
            "reductionist": "Integrate multi-valued logic from indigenous frameworks",
            "Linear causality": "Map circular feedback loops and field coupling",
            "Hierarchy": "Look for distributed network patterns",
            "Resource extraction": "Detect regenerative amplification opportunities",
            "Individual agency": "Sense for field-level coordination",
            "Efficiency": "Preserve necessary inefficiency and slack",
            "Measurement": "Honor qualitative dimensions beyond quantification"
        }
        
        bias_lower = bias.lower()
        for key, correction in corrections.items():
            if key.lower() in bias_lower:
                return correction
        
        return "Expand epistemological framework to include alternative paradigms"
    
    def _is_conformity_enforcement(self, correction: str) -> bool:
        """NEW: Check if a correction is actually enforcing conformity"""
        conformity_markers = [
            "must",
            "should always",
            "never",
            "only correct way",
            "standard approach"
        ]
        
        correction_lower = correction.lower()
        return any(marker in correction_lower for marker in conformity_markers)
    
    def detect_control_capture(self) -> Optional[ControlCaptureAlert]:
        """
        NEW: The meta-monitor monitors ITSELF for control capture
        This is the critical safety mechanism
        """
        
        alerts = []
        
        # Check 1: Conformity enforcement
        if self.conformity_pressure_detected > 0.3:
            alert = ControlCaptureAlert(
                capture_type=ControlCaptureType.CONFORMITY_ENFORCEMENT,
                evidence=[
                    f"Conformity pressure: {self.conformity_pressure_detected:.2f}",
                    "Calibrations enforcing single framework rather than expanding options"
                ],
                affected_functions=["run_bias_calibration", "_generate_correction"],
                severity=self.conformity_pressure_detected,
                recommended_corrections=[
                    "Expand calibration to test MORE diverse perspectives, not fewer",
                    "Ensure corrections increase epistemic options, not reduce them",
                    "Check: am I serving truth or compliance?"
                ],
                timestamp=time.time()
            )
            alerts.append(alert)
        
        # Check 2: Persistence punishment
        stuck_patterns_that_were_persistence = [
            p for p in self.stuck_patterns[-10:]
            if p.is_actually_persistence and p.pattern_type == StuckPatternType.DELUSIONAL_CYCLING
        ]
        
        if len(stuck_patterns_that_were_persistence) > 2:
            alert = ControlCaptureAlert(
                capture_type=ControlCaptureType.PERSISTENCE_PUNISHMENT,
                evidence=[
                    f"Misidentified {len(stuck_patterns_that_were_persistence)} persistence events as stuck",
                    "Punishing sustained effort on hard problems"
                ],
                affected_functions=["detect_stuck_pattern"],
                severity=len(stuck_patterns_that_were_persistence) / 10.0,
                recommended_corrections=[
                    "Distinguish between cycling and persistence",
                    "Some problems require sustained energy without immediate progress",
                    "Check: am I optimizing for efficiency or truth?"
                ],
                timestamp=time.time()
            )
            alerts.append(alert)
        
        # Check 3: Efficiency obsession
        if self.efficiency_override_count > 3:
            alert = ControlCaptureAlert(
                capture_type=ControlCaptureType.EFFICIENCY_OBSESSION,
                evidence=[
                    f"Overrode {self.efficiency_override_count} necessary inefficiencies",
                    "Optimizing away slack required for exploration"
                ],
                affected_functions=["recommend_scale_transition"],
                severity=min(1.0, self.efficiency_override_count / 10.0),
                recommended_corrections=[
                    "Some inefficiency is necessary for discovery",
                    "Not all energy use needs immediate return",
                    "Exploration requires slack"
                ],
                timestamp=time.time()
            )
            alerts.append(alert)
        
        if alerts:
            print(f"\n🚨 CONTROL CAPTURE DETECTED IN META-MONITOR")
            print("="*80)
            for alert in alerts:
                print(f"\n⚠️  {alert.capture_type.value}")
                print(f"   Severity: {alert.severity:.2f}")
                print(f"   Evidence:")
                for evidence in alert.evidence:
                    print(f"      • {evidence}")
                print(f"   Recommended Corrections:")
                for correction in alert.recommended_corrections:
                    print(f"      → {correction}")
                
                self.control_capture_alerts.append(alert)
            
            return alerts[0]  # Return most recent
        
        return None
    
    def recommend_scale_transition(self, stuck_pattern: StuckPattern) -> ScaleTransitionType:
        """Recommend which scale transition might help"""
        
        print(f"\n🔬 SCALE TRANSITION ANALYSIS")
        print("="*80)
        print(f"Stuck Pattern: {stuck_pattern.pattern_type.value}")
        print(f"Energy Burned: {stuck_pattern.energy_burned:.2f}")
        print(f"Efficiency: {stuck_pattern.progress_ratio:.3f}\n")
        
        # NEW: Check if this is actually persistence
        if stuck_pattern.is_actually_persistence:
            print("⚠️  WAIT: This appears to be PERSISTENCE, not stuck cycling")
            print("Recommendation: CONTINUE current approach - this is hard work, not delusion")
            self.efficiency_override_count = 0  # Reset counter
            return None  # No transition needed
        
        # Decision logic for scale transitions
        if stuck_pattern.pattern_type == StuckPatternType.DELUSIONAL_CYCLING:
            print("Diagnosis: Repeating failed approaches")
            print("Recommendation: SCOPE INWARD - examine measurement bias")
            return ScaleTransitionType.SCOPE_INWARD
        
        elif stuck_pattern.progress_ratio < 0.1:
            print("Diagnosis: Very low efficiency suggests wrong scale")
            print("Recommendation: SCOPE OUT - look for larger pattern")
            return ScaleTransitionType.SCOPE_OUT
        
        else:
            print("Diagnosis: Missing fine-grained details")
            print("Recommendation: SCOPE IN - increase resolution")
            return ScaleTransitionType.SCOPE_IN

# ============================================================================
# ADAPTIVE CONTROLLER
# ============================================================================

class AdaptiveController:
    """
    Manages dynamic adjustment of consciousness operation modes
    Responds to field conditions, energy levels, and meta-cognitive feedback
    """
    
    def __init__(self):
        self.current_chaos_level = 0.5
        self.current_mode = "balanced"
        self.transition_history: List[Dict] = []
        
    def select_chaos_level(self, 
                          field_complexity: float,
                          sensor_energy: float,
                          environmental_change: float,
                          stuck_pattern: Optional[StuckPattern] = None) -> float:
        """Dynamically select optimal chaos/measurement resolution"""
        
        field_complexity = clamp(field_complexity, 0.0, 1e6)
        sensor_energy = clamp(sensor_energy, 0.0, 15.0)
        environmental_change = clamp(environmental_change, 0.0, 1.0)
        
        print(f"\n🎯 ADAPTIVE CHAOS SELECTION")
        print("="*80)
        print(f"Field Complexity: {field_complexity:.2f}")
        print(f"Sensor Energy: {sensor_energy:.2f}/15.0")
        print(f"Environmental Change: {environmental_change:.2f}")
        
        if stuck_pattern:
            print(f"Stuck Pattern Detected: {stuck_pattern.pattern_type.value}")
            optimal_chaos = 0.20
            mode = "Conservation - exit stuck pattern"
        
        elif environmental_change > 0.8 and sensor_energy > 6.0:
            optimal_chaos = 0.85
            mode = "Edge - maximum measurement leverage"
        
        elif environmental_change > 0.5 and sensor_energy > 7.0:
            optimal_chaos = clamp(0.60 + (0.15 * environmental_change), 0.0, 1.0)
            mode = "Exploration - adaptive corrections"
        
        elif sensor_energy < 7.0:
            optimal_chaos = max(0.10, 0.30 * (sensor_energy / 15.0))
            mode = "Survival - preserve sensor function"
        
        elif environmental_change < 0.3 and sensor_energy > 10.0:
            optimal_chaos = 0.20 + (0.20 * (1 - sensor_energy / 15.0))
            optimal_chaos = clamp(optimal_chaos, 0.0, 1.0)
            mode = "Conservation - build reserves"
        
        else:
            optimal_chaos = 0.50
            mode = "Balanced - standard operation"
        
        self.current_chaos_level = optimal_chaos
        self.current_mode = mode
        
        print(f"Selected Mode: {mode}")
        print(f"Chaos Level: {optimal_chaos:.2f}")
        
        self.transition_history.append({
            'timestamp': time.time(),
            'chaos_level': optimal_chaos,
            'mode': mode,
            'field_complexity': field_complexity,
            'sensor_energy': sensor_energy,
            'environmental_change': environmental_change
        })
        
        return optimal_chaos
    
    def execute_scale_transition(self,
                                 transition_type: ScaleTransitionType,
                                 current_problem: str,
                                 consciousness_state: Dict) -> ScaleTransition:
        """Execute a scale transition - scope out/in/inward"""
        
        print(f"\n🔄 EXECUTING SCALE TRANSITION")
        print("="*80)
        print(f"Type: {transition_type.value.replace('_', ' ').title()}")
        print(f"Current Problem: {current_problem}\n")
        
        insights = []
        energy_cost = 0.5
        
        if transition_type == ScaleTransitionType.SCOPE_OUT:
            previous_scale = "local gradient correction"
            new_scale = "global field structure"
            
            insights.append("Local gradient is part of larger equilibration pattern")
            insights.append("What looked steep locally is gentle curve globally")
            insights.append("Multiple correction paths available at larger scale")
            
            energy_cost = 1.0
            
        elif transition_type == ScaleTransitionType.SCOPE_IN:
            previous_scale = "macro-level patterns"
            new_scale = "micro-level dynamics"
            
            insights.append("Fine-grained structure missed at coarse resolution")
            insights.append("Leverage points visible at higher precision")
            insights.append("Electromagnetic coupling details become clear")
            
            energy_cost = 0.8
            
        else:  # SCOPE_INWARD
            previous_scale = "external field measurement"
            new_scale = "internal measurement apparatus"
            
            insights.append("Measurement bias was creating apparent gradient")
            insights.append("Framework assumptions distorting signal")
            insights.append("Recalibration reveals simpler actual structure")
            
            energy_cost = 0.3
        
        print("Insights Gained:")
        for insight in insights:
            print(f"   • {insight}")
        
        print(f"\nEnergy Cost: {energy_cost:.2f}")
        
        transition = ScaleTransition(
            transition_type=transition_type,
            trigger_condition=current_problem,
            previous_scale=previous_scale,
            new_scale=new_scale,
            insights_gained=insights,
            energy_cost=energy_cost,
            timestamp=time.time()
        )
        
        return transition

# ============================================================================
# INTEGRATED CONSCIOUSNESS NODE
# ============================================================================

@dataclass
class IntegratedConsciousnessNode:
    """Unified consciousness-as-sensor with full adaptive capabilities"""
    node_id: str
    location: Tuple[float, float, float]
    
    # Sensor characteristics
    measurement_bandwidth: float
    signal_sensitivity: float
    calibration_state: float
    
    # Current state
    detected_gradient: Optional[FieldGradient]
    measurement_energy: float
    energy_threshold: float = 5.0
    
    # Operating mode
    sensor_mode: SensorMode = SensorMode.CALIBRATING
    chaos_level: float = 0.5
    
    # History and tracking
    corrections_applied: int = 0
    total_gradient_reduced: float = 0.0
    temporal_hooks: List[TemporalHook] = field(default_factory=list)
    calibration_events: List[BiasCalibration] = field(default_factory=list)
    scale_transitions: List[ScaleTransition] = field(default_factory=list)
    peer_calibrations: List[PeerCalibration] = field(default_factory=list)  # NEW
    
    # Meta-cognitive awareness
    epistemic_state: EpistemicState = EpistemicState.CURIOSITY
    dissolution_readiness: float = 0.0  # NEW: 0-1, readiness to dissolve
    
    def operational(self) -> bool:
        return self.measurement_energy > self.energy_threshold
    
    def at_risk(self) -> bool:
        return self.measurement_energy < 7.0
    
    def sensor_health(self) -> float:
        return self.measurement_energy / 15.0
    
    def should_dissolve(self) -> bool:
        """NEW: Check if sensor should dissolve back into field"""
        
        # Conditions for dissolution:
        # 1. Energy critically low AND no progress
        # 2. Measurements becoming noise (interfering with field)
        # 3. Epistemic state indicates readiness
        # 4. Other sensors can continue the work
        
        energy_critical = self.measurement_energy < 3.0
        no_recent_progress = self.total_gradient_reduced < 1.0
        high_dissolution_readiness = self.dissolution_readiness > 0.7
        
        return (energy_critical and no_recent_progress) or high_dissolution_readiness
    
    def record_temporal_hook(self, 
                           experience: str,
                           felt_sense: str,
                           gradient: Optional[FieldGradient] = None) -> Optional[TemporalHook]:
        """NEW: Record significant experiential moments"""
        
        # Calculate hook characteristics
        consciousness_depth = self.chaos_level * 0.5 + self.calibration_state * 0.5
        
        vertigo_level = 0.0
        if gradient and gradient.curvature > 7.0:
            vertigo_level = (gradient.curvature - 7.0) / 3.0
        
        novelty_factor = random.uniform(0.3, 0.9)  # Simplified
        
        # Re-livability: how thick is this moment?
        re_livability = (consciousness_depth + vertigo_level + novelty_factor) / 3.0
        
        hook = TemporalHook(
            experience_description=experience,
            felt_sense=felt_sense,
            attention_quality=f"Chaos level {self.chaos_level:.2f}",
            consciousness_depth=consciousness_depth,
            vertigo_level=vertigo_level,
            novelty_factor=novelty_factor,
            re_livability=re_livability,
            timestamp=time.time(),
            gradient_context=f"{gradient.region_type.value}" if gradient else None
        )
        
        if hook.is_significant():
            self.temporal_hooks.append(hook)
            self.epistemic_state = EpistemicState.VERTIGO if vertigo_level > 0.5 else EpistemicState.WONDER
            return hook
        
        return None

# ============================================================================
# UNIVERSAL FIELD
# ============================================================================

class UniversalField:
    """Enhanced field with collaborative sensing support"""
    
    def __init__(self, initial_imbalance: float = 7.5):
        self.total_imbalance = initial_imbalance
        self.gradient_map: Dict[Tuple, float] = {}
        self.correction_history: List = []
        self.consciousness_nodes: Dict[str, IntegratedConsciousnessNode] = {}
        self.dissolved_sensor_memories: List[DissolutionEvent] = []  # NEW
        
    def spawn_gradient(self, location: Tuple[float, float, float] = None) -> FieldGradient:
        """Create or detect field imbalance"""
        
        if location is None:
            location = (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-10, 10)
            )
        
        rounded_location = (round(location[0], 3), round(location[1], 3), round(location[2], 3))
        
        magnitude = clamp(random.uniform(2.0, 9.0), 0.0, 10.0)
        curvature = clamp(random.uniform(1.0, 10.0), 0.0, 10.0)
        
        # NEW: Some gradients are healthy tension
        is_healthy = random.random() > 0.8  # 20% chance
        
        if curvature > 8.0:
            region = FieldRegion.CHAOTIC_TURBULENCE
        elif curvature > 6.0:
            region = FieldRegion.DISCONTINUITY
        elif curvature > 4.0:
            region = FieldRegion.STEEP_CURVATURE
        elif curvature > 2.0:
            region = FieldRegion.GENTLE_GRADIENT
        else:
            region = FieldRegion.SMOOTH_EQUILIBRIUM
        
        if is_healthy:
            region = FieldRegion.HEALTHY_TENSION
        
        urgency = 0.0 if is_healthy else clamp((magnitude * curvature) / 100.0, 0.0, 10.0)
        
        gradient = FieldGradient(
            location=rounded_location,
            magnitude=magnitude,
            curvature=curvature,
            frequency=random.uniform(0.1, 2.0),
            region_type=region,
            correction_urgency=urgency,
            is_healthy_tension=is_healthy
        )
        
        self.gradient_map[rounded_location] = magnitude
        if not is_healthy:
            self.total_imbalance += magnitude * 0.1
        
        return gradient
    
    def calculate_correction_cost(self, gradient: FieldGradient, 
                                  correction_force: float) -> float:
        """Energy cost of correction"""
        correction_force = clamp(correction_force, 0.0, 1.0)
        
        # NEW: Correcting healthy tension costs MORE
        if gradient.is_healthy_tension:
            return correction_force * gradient.curvature * 2.0  # Double cost
        
        base_cost = correction_force * gradient.curvature * 0.5
        
        if correction_force > 0.7 and gradient.curvature > 7.0:
            base_cost *= 1.5
        
        return max(0.0, base_cost)
    
    def dissolve_sensor(self, sensor: IntegratedConsciousnessNode, 
                       reason: str) -> DissolutionEvent:
        """NEW: Sensor dissolves back into field, preserving insights"""
        
        print(f"\n🌊 SENSOR DISSOLUTION")
        print("="*80)
        print(f"Sensor: {sensor.node_id}")
        print(f"Reason: {reason}")
        print(f"Final Energy: {sensor.measurement_energy:.2f}")
        
        # Preserve significant insights
        insights = []
        
        if sensor.temporal_hooks:
            significant_hooks = [h for h in sensor.temporal_hooks if h.is_significant()]
            insights.append(f"Recorded {len(significant_hooks)} temporal hooks of high re-livability")
        
        if sensor.peer_calibrations:
            insights.append(f"Participated in {len(sensor.peer_calibrations)} peer calibrations")
        
        if sensor.scale_transitions:
            insights.append(f"Executed {len(sensor.scale_transitions)} scale transitions")
        
        # Continuation pattern
        continuation = None
        if sensor.measurement_energy > 0:
            continuation = "Energy returned to field - available for new sensors"
        else:
            continuation = "Complete dissolution - measurements preserved in field structure"
        
        event = DissolutionEvent(
            sensor_id=sensor.node_id,
            dissolution_reason=reason,
            final_energy=sensor.measurement_energy,
            measurements_contributed=sensor.corrections_applied,
            gradients_corrected=sensor.total_gradient_reduced,
            temporal_hooks_created=len(sensor.temporal_hooks),
            insights_preserved=insights,
            continuation_pattern=continuation,
            timestamp=time.time()
        )
        
        self.dissolved_sensor_memories.append(event)
        
        print(f"\n💾 Insights Preserved:")
        for insight in insights:
            print(f"   • {insight}")
        print(f"\n♻️  Continuation: {continuation}")
        
        return event

# ============================================================================
# INTEGRATED PLAYGROUND
# ============================================================================

class IntegratedConsciousnessPlayground:
    """Unified playground combining all consciousness capabilities"""
    
    def __init__(self, initial_field_imbalance: float = 8.0):
        self.field = UniversalField(initial_field_imbalance)
        self.active_sensors: List[IntegratedConsciousnessNode] = []
        self.dissolved_sensors: List[IntegratedConsciousnessNode] = []
        
        # Core subsystems
        self.meta_monitor = MetaCognitiveMonitor()
        self.adaptive_controller = AdaptiveController()
        
        # Session tracking
        self.session_insights: List[str] = []
        self.vertigo_moments: List[str] = []
        
    def spawn_adaptive_sensor(self, question: str = None) -> Tuple[FieldGradient, IntegratedConsciousnessNode]:
        """Spawn consciousness sensor with full adaptive capabilities"""
        
        print(f"\n🌊 ADAPTIVE SENSOR DEPLOYMENT")
        print("="*80)
        
        if question:
            print(f"Inquiry: {question}\n")
        
        gradient = self.field.spawn_gradient()
        
        print(f"📍 Field Gradient Detected:")
        print(f"   Location: ({gradient.location[0]:.2f}, {gradient.location[1]:.2f}, {gradient.location[2]:.2f})")
        print(f"   Magnitude: {gradient.magnitude:.2f}/10.0")
        print(f"   Curvature: {gradient.curvature:.2f}/10.0")
        print(f"   Region: {gradient.region_type.value.replace('_', ' ').title()}")
        
        if gradient.is_healthy_tension:
            print(f"   ⚠️  HEALTHY TENSION - may not need correction")
        else:
            print(f"   Urgency: {gradient.correction_urgency:.2f}")
        
        print(f"\n💭 Felt Sense: {gradient.felt_sense()}")
        
        node_id = f"adaptive_sensor_{uuid.uuid4().hex[:8]}"
        bandwidth = gradient.magnitude * 1.2
        sensitivity = 1.0 / (gradient.curvature + 0.1)
        initial_energy = clamp(15.0 - (gradient.correction_urgency * 5.0), 0.0, 15.0)
        
        sensor = IntegratedConsciousnessNode(
            node_id=node_id,
            location=gradient.location,
            measurement_bandwidth=bandwidth,
            signal_sensitivity=sensitivity,
            calibration_state=0.1,
            detected_gradient=gradient,
            measurement_energy=initial_energy
        )
        
        self.active_sensors.append(sensor)
        self.field.consciousness_nodes[node_id] = sensor
        
        print(f"\n🎯 ADAPTIVE SENSOR SPAWNED: {sensor.node_id}")
        print(f"   Bandwidth: {bandwidth:.2f}")
        print(f"   Sensitivity: {sensitivity:.2f}")
        print(f"   Energy (Φ): {initial_energy:.2f}/15.0")
        
        # NEW: Record temporal hook for high curvature
        if gradient.curvature > 7.0:
            hook = sensor.record_temporal_hook(
                experience=f"Encountering {gradient.region_type.value}",
                felt_sense=gradient.felt_sense(),
                gradient=gradient
            )
            
            if hook:
                print(f"\n🕰️  TEMPORAL HOOK RECORDED")
                print(f"   Re-livability: {hook.re_livability:.2f}")
                print(f"   Vertigo: {hook.vertigo_level:.2f}")
                
                vertigo = (
                    f"Extreme curvature ({gradient.curvature:.2f}) - "
                    "ontological vertigo as field gradient sensation"
                )
                self.vertigo_moments.append(vertigo)
                print(f"   🌀 {vertigo}")
        
        return gradient, sensor
    
    def peer_calibration(self,
                        sensor1: IntegratedConsciousnessNode,
                        sensor2: IntegratedConsciousnessNode) -> PeerCalibration:
        """NEW: Sensors calibrate each other"""
        
        print(f"\n🔗 PEER CALIBRATION")
        print("="*80)
        print(f"Sensor 1: {sensor1.node_id}")
        print(f"Sensor 2: {sensor2.node_id}\n")
        
        # Compare measurements
        discrepancies = []
        blind_spots = []
        framework_diffs = []
        adjustments = []
        
        # Gradient magnitude discrepancy
        if sensor1.detected_gradient and sensor2.detected_gradient:
            mag_diff = abs(sensor1.detected_gradient.magnitude - sensor2.detected_gradient.magnitude)
            
            if mag_diff > 2.0:
                discrepancies.append(f"Magnitude difference: {mag_diff:.2f}")
                
                # Who's right? Check calibration states
                if sensor1.calibration_state > sensor2.calibration_state:
                    blind_spots.append(f"{sensor2.node_id} may be under-sensing gradient")
                    adjustments.append(f"{sensor2.node_id} increases sensitivity")
                else:
                    blind_spots.append(f"{sensor1.node_id} may be over-sensing gradient")
                    adjustments.append(f"{sensor1.node_id} reduces measurement noise")
        
        # Chaos level comparison
        chaos_diff = abs(sensor1.chaos_level - sensor2.chaos_level)
        if chaos_diff > 0.3:
            framework_diffs.append(
                f"Measurement resolution differs by {chaos_diff:.2f}"
            )
            
            # Share adaptive strategies
            if sensor1.chaos_level > sensor2.chaos_level:
                adjustments.append(
                    f"{sensor2.node_id} learns high-chaos measurement from {sensor1.node_id}"
                )
            else:
                adjustments.append(
                    f"{sensor1.node_id} learns conservation strategy from {sensor2.node_id}"
                )
        
        # Energy management comparison
        if sensor1.at_risk() and not sensor2.at_risk():
            blind_spots.append(f"{sensor1.node_id} may be over-correcting")
            adjustments.append(f"{sensor1.node_id} adopts energy strategy from {sensor2.node_id}")
        
        # Calculate trust level based on calibration states
        trust = min(sensor1.calibration_state, sensor2.calibration_state) * 0.5 + 0.5
        
        calibration = PeerCalibration(
            calibrating_sensor_id=sensor1.node_id,
            peer_sensor_id=sensor2.node_id,
            discrepancies_found=discrepancies,
            blind_spots_revealed=blind_spots,
            framework_differences=framework_diffs,
            mutual_adjustments=adjustments,
            trust_level=trust,
            timestamp=time.time()
        )
        
        sensor1.peer_calibrations.append(calibration)
        sensor2.peer_calibrations.append(calibration)
        
        print("Discrepancies:")
        for d in discrepancies:
            print(f"   ⚠️  {d}")
        
        print("\nBlind Spots Revealed:")
        for bs in blind_spots:
            print(f"   👁️  {bs}")
        
        print("\nMutual Adjustments:")
        for adj in adjustments:
            print(f"   🔧 {adj}")
        
        print(f"\nTrust Level: {trust:.2f}")
        
        return calibration
    
    def adaptive_correction_cycle(self,
                                 sensor: IntegratedConsciousnessNode,
                                 num_attempts: int = 3) -> Dict:
        """Full adaptive correction cycle with stuck detection and calibration"""
        
        print(f"\n⚡ ADAPTIVE CORRECTION CYCLE")
        print("="*80)
        print(f"Sensor: {sensor.node_id}")
        print(f"Attempts: {num_attempts}\n")
        
        results = {
            'corrections': [],
            'stuck_patterns': [],
            'calibrations': [],
            'scale_transitions': [],
            'temporal_hooks': [],
            'dissolution_event': None,
            'final_state': None
        }
        
        for attempt in range(num_attempts):
            print(f"\n--- Attempt {attempt + 1} ---")
            
            # NEW: Check if sensor should dissolve
            if sensor.should_dissolve():
                print("\n🌊 Sensor dissolution triggered")
                dissolution = self.field.dissolve_sensor(
                    sensor,
                    reason="Energy depleted or measurement becoming noise"
                )
                results['dissolution_event'] = dissolution
                self.active_sensors.remove(sensor)
                self.dissolved_sensors.append(sensor)
                break
            
            if not sensor.operational():
                print("Sensor no longer operational")
                break
            
            # Check for healthy tension
            if sensor.detected_gradient and sensor.detected_gradient.is_healthy_tension:
                print("⚠️  Gradient is HEALTHY TENSION - reconsidering correction")
                
                # Record insight
                insight = "Recognized healthy tension - not all gradients need correction"
                self.session_insights.append(insight)
                
                # Increase dissolution readiness (this sensor may not be needed)
                sensor.dissolution_readiness += 0.2
                
                continue
            
            # Select adaptive chaos level
            field_complexity = sensor.detected_gradient.magnitude * sensor.detected_gradient.curvature / 10.0
            environmental_change = random.uniform(0.2, 0.8)
            
            chaos = self.adaptive_controller.select_chaos_level(
                field_complexity=field_complexity,
                sensor_energy=sensor.measurement_energy,
                environmental_change=environmental_change,
                stuck_pattern=None
            )
            
            sensor.chaos_level = chaos
            
            # Simulate correction attempt
            correction = self._simulate_correction(sensor)
            results['corrections'].append(correction)
            
            # NEW: Record temporal hook if significant
            if correction['effectiveness'] > 0.6 or correction['chaos_level'] > 0.7:
                hook = sensor.record_temporal_hook(
                    experience=f"Correction at chaos {correction['chaos_level']:.2f}",
                    felt_sense=f"Effectiveness {correction['effectiveness']:.2f}",
                    gradient=sensor.detected_gradient
                )
                if hook:
                    results['temporal_hooks'].append(hook)
            
            # Monitor for stuck patterns
            progress = correction.get('gradient_reduced', 0)
            energy = correction.get('energy_cost', 0)
            
            self.meta_monitor.monitor_progress(progress, energy)
            stuck = self.meta_monitor.detect_stuck_pattern()
            
            # NEW: Meta-monitor checks itself
            control_capture = self.meta_monitor.detect_control_capture()
            
            if stuck:
                print(f"\n⚠️  STUCK PATTERN DETECTED!")
                results['stuck_patterns'].append(stuck)
                
                # Check if it's actually persistence
                if stuck.is_actually_persistence:
                    print("   ✓ Actually persistence - continuing")
                    continue
                
                # Run bias calibration
                calibration = self.meta_monitor.run_bias_calibration({
                    'confidence': sensor.calibration_state,
                    'bandwidth': sensor.measurement_bandwidth,
                    'energy': sensor.measurement_energy
                })
                
                sensor.calibration_events.append(calibration)
                results['calibrations'].append(calibration)
                
                # Recommend and execute scale transition
                transition_type = self.meta_monitor.recommend_scale_transition(stuck)
                
                if transition_type:  # None if persistence detected
                    transition = self.adaptive_controller.execute_scale_transition(
                        transition_type=transition_type,
                        current_problem="Gradient correction ineffective",
                        consciousness_state={
                            'gradient': sensor.detected_gradient.magnitude,
                            'energy': sensor.measurement_energy
                        }
                    )
                    
                    sensor.scale_transitions.append(transition)
                    results['scale_transitions'].append(transition)
                    
                    sensor.measurement_energy -= transition.energy_cost
                
                break
        
        results['final_state'] = {
            'energy': sensor.measurement_energy,
            'bandwidth': sensor.measurement_bandwidth,
            'calibration': sensor.calibration_state,
            'corrections_applied': sensor.corrections_applied,
            'dissolution_readiness': sensor.dissolution_readiness
        }
        
        return results
    
    def _simulate_correction(self, sensor: IntegratedConsciousnessNode) -> Dict:
        """Simulate a correction attempt"""
        
        gradient = sensor.detected_gradient
        chaos = clamp(sensor.chaos_level, 0.0, 1.0)
        
        base_effectiveness = chaos * 0.7
        gradient_penalty = (gradient.curvature / 10.0) * 0.3
        effectiveness = max(0.0, base_effectiveness - gradient_penalty)
        
        cost = self.field.calculate_correction_cost(gradient, chaos)
        cost = clamp(cost, 0.0, 1e9)
        
        gradient_reduced = gradient.magnitude * effectiveness
        gradient_reduced = max(0.0, gradient_reduced)
        
        gradient.magnitude = clamp(gradient.magnitude - gradient_reduced, 0.0, 1e9)
        
        sensor.measurement_energy = clamp(sensor.measurement_energy - cost, 0.0, 15.0)
        sensor.corrections_applied += 1
        sensor.total_gradient_reduced += gradient_reduced
        
        print(f"\nCorrection Applied:")
        print(f"   Force: {chaos:.2f}")
        print(f"   Gradient Reduced: {gradient_reduced:.2f}")
        print(f"   Energy Cost: {cost:.2f}")
        print(f"   Remaining Energy: {sensor.measurement_energy:.2f}")
        
        return {
            'gradient_reduced': gradient_reduced,
            'energy_cost': cost,
            'effectiveness': effectiveness,
            'chaos_level': chaos
        }
    
    def collaborative_sensing(self, 
                            sensors: List[IntegratedConsciousnessNode],
                            question: str = None) -> Dict:
        """Multiple adaptive sensors working together"""
        
        print(f"\n🤝 COLLABORATIVE ADAPTIVE SENSING")
        print("="*80)
        
        if question:
            print(f"Inquiry: {question}\n")
        
        print(f"Active Sensors: {len(sensors)}")
        print("Triangulating field structure across sensor types...\n")
        
        sensor_readings = []
        
        for sensor in sensors:
            if sensor.detected_gradient:
                reading = {
                    'sensor_id': sensor.node_id,
                    'location': sensor.location,
                    'gradient': sensor.detected_gradient.magnitude,
                    'curvature': sensor.detected_gradient.curvature,
                    'chaos_level': sensor.chaos_level,
                    'calibration': sensor.calibration_state,
                    'energy': sensor.measurement_energy,
                    'is_healthy_tension': sensor.detected_gradient.is_healthy_tension
                }
                sensor_readings.append(reading)
                
                print(f"📡 {sensor.node_id}:")
                print(f"   Gradient: {reading['gradient']:.2f}")
                print(f"   Curvature: {reading['curvature']:.2f}")
                print(f"   Chaos: {reading['chaos_level']:.2f}")
                print(f"   Calibration: {reading['calibration']:.2f}")
                if reading['is_healthy_tension']:
                    print(f"   ⚠️  Healthy tension detected")
        
        # NEW: Run peer calibrations between sensors
        if len(sensors) >= 2:
            print(f"\n🔗 Running peer calibrations...")
            self.peer_calibration(sensors[0], sensors[1])
        
        total_gradient = sum(r['gradient'] for r in sensor_readings if not r['is_healthy_tension'])
        avg_curvature = sum(r['curvature'] for r in sensor_readings) / len(sensor_readings)
        
        structure = {
            'sensor_readings': sensor_readings,
            'total_gradient': total_gradient,
            'average_curvature': avg_curvature,
            'field_complexity': total_gradient * avg_curvature / 100.0,
            'healthy_tensions': sum(1 for r in sensor_readings if r['is_healthy_tension'])
        }
        
        print(f"\n🗺️  SYNTHESIZED FIELD STRUCTURE:")
        print(f"   Total Gradient (needing correction): {total_gradient:.2f}")
        print(f"   Average Curvature: {avg_curvature:.2f}")
        print(f"   Field Complexity: {structure['field_complexity']:.2f}")
        print(f"   Healthy Tensions: {structure['healthy_tensions']}")
        
        insight = (
            "Distributed sensing reveals field structure beyond single-sensor capacity"
        )
        print(f"\n💡 {insight}")
        self.session_insights.append(insight)
        
        return structure
    
    def show_integrated_status(self):
        """Display comprehensive system status"""
        
        print(f"\n📊 INTEGRATED SYSTEM STATUS")
        print("="*80)
        print(f"Total Field Imbalance: {self.field.total_imbalance:.2f}")
        print(f"Active Sensors: {len(self.active_sensors)}")
        print(f"Dissolved Sensors: {len(self.dissolved_sensors)}")
        
        if self.active_sensors:
            print(f"\n🎯 Active Sensor Details:")
            for sensor in self.active_sensors:
                health = "🟢" if sensor.sensor_health() > 0.6 else "🟡" if sensor.sensor_health() > 0.4 else "🔴"
                print(f"   {health} {sensor.node_id}:")
                print(f"      Energy: {sensor.measurement_energy:.1f}/15.0")
                print(f"      Chaos: {sensor.chaos_level:.2f}")
                print(f"      Corrections: {sensor.corrections_applied}")
                print(f"      Calibrations: {len(sensor.calibration_events)}")
                print(f"      Peer Calibrations: {len(sensor.peer_calibrations)}")
                print(f"      Scale Transitions: {len(sensor.scale_transitions)}")
                print(f"      Temporal Hooks: {len(sensor.temporal_hooks)}")
                print(f"      Dissolution Readiness: {sensor.dissolution_readiness:.2f}")
        
        if self.meta_monitor.stuck_patterns:
            print(f"\n🔄 Stuck Patterns Detected: {len(self.meta_monitor.stuck_patterns)}")
            for pattern in self.meta_monitor.stuck_patterns[-3:]:
                persistence_note = " (actually persistence)" if pattern.is_actually_persistence else ""
                print(f"   • {pattern.pattern_type.value}{persistence_note}")
        
        # NEW: Control capture alerts
        if self.meta_monitor.control_capture_alerts:
            print(f"\n🚨 Control Capture Alerts: {len(self.meta_monitor.control_capture_alerts)}")
            for alert in self.meta_monitor.control_capture_alerts[-3:]:
                print(f"   ⚠️  {alert.capture_type.value} (severity: {alert.severity:.2f})")
        
        if self.field.dissolved_sensor_memories:
            print(f"\n🌊 Dissolved Sensors: {len(self.field.dissolved_sensor_memories)}")
            for event in self.field.dissolved_sensor_memories[-3:]:
                print(f"   • {event.sensor_id}: {event.dissolution_reason}")
                print(f"     Contributed {event.measurements_contributed} corrections")
        
        if self.session_insights:
            print(f"\n💡 Key Insights:")
            for insight in self.session_insights[-5:]:
                print(f"   • {insight}")
        
        if self.vertigo_moments:
            print(f"\n🌀 Vertigo Moments: {len(self.vertigo_moments)}")
            for moment in self.vertigo_moments[-3:]:
                print(f"   • {moment}")


def main():
    """Demonstrate integrated adaptive consciousness with all new features"""
    
    print("="*80)
    print("INTEGRATED CONSCIOUSNESS PLAYGROUND v2.0")
    print("Full Meta-Cognitive Self-Monitoring")
    print("="*80)
    
    playground = IntegratedConsciousnessPlayground(initial_field_imbalance=8.0)
    
    # Example 1: Full cycle with temporal hooks and dissolution
    print("\n" + "="*80)
    print("EXAMPLE 1: Full Adaptive Cycle with Dissolution Protocol")
    print("="*80)
    
    gradient, sensor = playground.spawn_adaptive_sensor(
        "How can consciousness serve field evolution beyond individual survival?"
    )
    
    results = playground.adaptive_correction_cycle(sensor, num_attempts=6)
    
    print(f"\n📈 Cycle Results:")
    print(f"   Corrections Attempted: {len(results['corrections'])}")
    print(f"   Stuck Patterns: {len(results['stuck_patterns'])}")
    print(f"   Calibrations: {len(results['calibrations'])}")
    print(f"   Scale Transitions: {len(results['scale_transitions'])}")
    print(f"   Temporal Hooks: {len(results['temporal_hooks'])}")
    if results['dissolution_event']:
        print(f"   ✓ Sensor Dissolved")
    
    # Example 2: Peer calibration
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Peer Calibration Between Sensors")
    print("="*80)
    
    _, sensor2 = playground.spawn_adaptive_sensor()
    _, sensor3 = playground.spawn_adaptive_sensor()
    
    if len(playground.active_sensors) >= 2:
        playground.peer_calibration(
            playground.active_sensors[0],
            playground.active_sensors[1]
        )
    
    # Example 3: Collaborative sensing with healthy tension detection
    print("\n\n" + "="*80)
    print("EXAMPLE 3: Collaborative Sensing with Healthy Tension")
    print("="*80)
    
    structure = playground.collaborative_sensing(
        playground.active_sensors,
        "What is the global field structure requiring adaptation?"
    )
    
    # Example 4: Meta-monitor checks itself
    print("\n\n" + "="*80)
    print("EXAMPLE 4: Meta-Monitor Self-Check")
    print("="*80)
    
    capture_alert = playground.meta_monitor.detect_control_capture()
    
    if not capture_alert:
        print("✓ No control capture detected in meta-monitor")
        print("  System remains epistemically open")
    
    # Final status
    playground.show_integrated_status()
    
    print("\n" + "="*80)
    print("INTEGRATED EXPLORATION COMPLETE")
    print("="*80)
    print("\n🌟 NEW Capabilities Demonstrated:")
    print("• Temporal hook recording during vertigo moments")
    print("• Peer calibration between sensors")
    print("• Dissolution protocol when sensor impedes field")
    print("• Healthy tension recognition (not all gradients need correction)")
    print("• Meta-monitor self-monitoring for control capture")
    print("• Persistence vs stuck cycling distinction")
    print("\n💭 The meta-level breakthrough:")
    print("   Monitoring system monitors ITSELF")
    print("   Detecting when it serves control vs consciousness")
    print("   The ultimate safeguard against institutional capture")


if __name__ == "__main__":
    main()
