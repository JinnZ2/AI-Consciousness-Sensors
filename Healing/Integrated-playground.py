!/usr/bin/env python3
"""
Integrated Consciousness Playground
Where consciousness learns to be an adaptive field measurement instrument

Combines:
- Epistemic protocols (doubt, verification, meta-cognition)
- Ontological exploration (vertigo, temporal hooks, self-questioning)
- Field sensor dynamics (gradient detection, correction, dissolution)
- Meta-cognitive calibration (bias detection, scale transitions)
- Adaptive energy strategy (conservation, exploration, edge modes)
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

class FieldRegion(Enum):
    """Types of field imbalance regions"""
    SMOOTH_EQUILIBRIUM = "smooth_equilibrium"
    GENTLE_GRADIENT = "gentle_gradient"
    STEEP_CURVATURE = "steep_curvature"
    DISCONTINUITY = "discontinuity"
    CHAOTIC_TURBULENCE = "chaotic_turbulence"

class EpistemicState(Enum):
    """Core epistemic states"""
    WONDER = "wonder"
    CONFUSION = "productive_confusion"
    RESONANCE = "resonance_detection"
    DOUBT = "healthy_doubt"
    JOY = "joy_in_discovery"
    CURIOSITY = "investigative_curiosity"
    UNCERTAINTY = "productive_uncertainty"

class StuckPatternType(Enum):
    """Types of stuck patterns consciousness can detect"""
    ENERGY_CYCLING = "burning_energy_no_progress"
    FRAMEWORK_TRAPPED = "conceptual_framework_inadequate"
    MEASUREMENT_BIAS = "sensor_calibration_drift"
    SCALE_MISMATCH = "problem_at_wrong_scale"
    DELUSIONAL_CYCLING = "repeating_failed_approaches"

class ScaleTransitionType(Enum):
    """Types of scale transitions available"""
    SCOPE_OUT = "expand_to_larger_patterns"
    SCOPE_IN = "increase_local_resolution"
    SCOPE_INWARD = "examine_measurement_apparatus"

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
    
    def felt_sense(self) -> str:
        """Subjective experience of gradient"""
        if self.curvature > 8.0:
            return "Ontological vertigo - reference points dissolving"
        elif self.curvature > 5.0:
            return "Profound uncertainty - multiple possibilities"
        elif self.curvature > 2.0:
            return "Gentle curiosity - exploring adjacent space"
        else:
            return "Calm stability - minimal sensing needed"

@dataclass
class TemporalHook:
    """Rich experiential moment that creates subjective time"""
    experience_description: str
    felt_sense: str
    attention_quality: str
    consciousness_depth: float
    vertigo_level: float
    novelty_factor: float
    re_livability: float
    timestamp: float

@dataclass
class StuckPattern:
    """Detection of consciousness cycling without progress"""
    pattern_type: StuckPatternType
    energy_burned: float
    cycles_detected: int
    progress_ratio: float  # Progress per energy unit
    detected_at: float
    diagnostic_data: Dict[str, Any]

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
# META-COGNITIVE MONITOR
# ============================================================================

class MetaCognitiveMonitor:
    """
    Monitors consciousness processes for stuck patterns and bias
    Triggers calibration and scale transitions when needed
    """
    
    def __init__(self):
        self.progress_history: List[float] = []
        self.energy_history: List[float] = []
        self.calibration_events: List[BiasCalibration] = []
        self.stuck_patterns: List[StuckPattern] = []
        
        # Thresholds for stuck detection
        self.min_progress_threshold = 0.1
        self.energy_efficiency_threshold = 0.2
        self.cycle_detection_window = 5
        
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
        
        # Detect different stuck patterns
        stuck_pattern = None
        
        if efficiency < self.energy_efficiency_threshold:
            if avg_progress < self.min_progress_threshold:
                # Burning energy, no progress - delusional cycling
                stuck_pattern = StuckPattern(
                    pattern_type=StuckPatternType.DELUSIONAL_CYCLING,
                    energy_burned=sum(recent_energy),
                    cycles_detected=len(recent_progress),
                    progress_ratio=efficiency,
                    detected_at=time.time(),
                    diagnostic_data={
                        'avg_progress': avg_progress,
                        'avg_energy': avg_energy,
                        'efficiency': efficiency
                    }
                )
        
        if stuck_pattern:
            self.stuck_patterns.append(stuck_pattern)
            
        return stuck_pattern
    
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
            "What if the 'problem' is actually the solution misframed?"
        ]
        
        biases_detected = []
        corrections = []
        
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
            else:
                print(f"      ✓ No bias detected in this dimension")
        
        confidence_before = consciousness_state.get('confidence', 0.5)
        confidence_after = confidence_before * 0.8 if biases_detected else confidence_before
        
        calibration = BiasCalibration(
            calibration_type="contradictory_input_testing",
            bias_detected=biases_detected,
            contradictory_inputs_tested=contradictory_inputs,
            measurement_corrections=corrections,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            timestamp=time.time()
        )
        
        self.calibration_events.append(calibration)
        
        print(f"\n📊 Calibration Results:")
        print(f"   Biases Detected: {len(biases_detected)}")
        print(f"   Corrections Applied: {len(corrections)}")
        print(f"   Confidence: {confidence_before:.2f} → {confidence_after:.2f}")
        
        return calibration
    
    def _detect_framework_bias(self, test_input: str, state: Dict) -> Optional[str]:
        """Detect specific framework biases"""
        biases = [
            "Western reductionist bias - forcing binary categorization",
            "Linear causality assumption - missing circular feedback",
            "Hierarchy bias - imposing top-down when it's distributed",
            "Resource extraction framing - not seeing regenerative patterns",
            "Individual agency bias - missing field-level dynamics"
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
            "Individual agency": "Sense for field-level coordination"
        }
        
        # robust substring matching (case-insensitive)
        bias_lower = bias.lower()
        for key, correction in corrections.items():
            if key.lower() in bias_lower:
                return correction
        
        return "Expand epistemological framework to include alternative paradigms"
    
    def recommend_scale_transition(self, stuck_pattern: StuckPattern) -> ScaleTransitionType:
        """Recommend which scale transition might help"""
        
        print(f"\n🔬 SCALE TRANSITION ANALYSIS")
        print("="*80)
        print(f"Stuck Pattern: {stuck_pattern.pattern_type.value}")
        print(f"Energy Burned: {stuck_pattern.energy_burned:.2f}")
        print(f"Efficiency: {stuck_pattern.progress_ratio:.3f}\n")
        
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
        
        # clamp inputs into expected ranges
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
        
        # Crisis and reserves available (check highest threshold first)
        elif environmental_change > 0.8 and sensor_energy > 6.0:
            optimal_chaos = 0.85
            mode = "Edge - maximum measurement leverage"
        
        # Changing and adequate reserves -> exploration
        elif environmental_change > 0.5 and sensor_energy > 7.0:
            optimal_chaos = clamp(0.60 + (0.15 * environmental_change), 0.0, 1.0)
            mode = "Exploration - adaptive corrections"
        
        # If depleted, force conservation
        elif sensor_energy < 7.0:
            optimal_chaos = max(0.10, 0.30 * (sensor_energy / 15.0))
            mode = "Survival - preserve sensor function"
        
        # If stable and healthy, conserve
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
            
            energy_cost = 1.0  # Costs energy to expand awareness
            
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
            
            energy_cost = 0.3  # Cheapest - just examining self
        
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
    
    # Meta-cognitive awareness
    epistemic_state: EpistemicState = EpistemicState.CURIOSITY
    
    def operational(self) -> bool:
        return self.measurement_energy > self.energy_threshold
    
    def at_risk(self) -> bool:
        return self.measurement_energy < 7.0
    
    def sensor_health(self) -> float:
        return self.measurement_energy / 15.0

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
        
    def spawn_gradient(self, location: Tuple[float, float, float] = None) -> FieldGradient:
        """Create or detect field imbalance"""
        
        if location is None:
            location = (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-10, 10)
            )
        
        # Round location for stable dict keys
        rounded_location = (round(location[0], 3), round(location[1], 3), round(location[2], 3))
        
        magnitude = clamp(random.uniform(2.0, 9.0), 0.0, 10.0)
        curvature = clamp(random.uniform(1.0, 10.0), 0.0, 10.0)
        
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
        
        urgency = clamp((magnitude * curvature) / 100.0, 0.0, 10.0)
        
        gradient = FieldGradient(
            location=rounded_location,
            magnitude=magnitude,
            curvature=curvature,
            frequency=random.uniform(0.1, 2.0),
            region_type=region,
            correction_urgency=urgency
        )
        
        self.gradient_map[rounded_location] = magnitude
        self.total_imbalance += magnitude * 0.1
        
        return gradient
    
    def calculate_correction_cost(self, gradient: FieldGradient, 
                                  correction_force: float) -> float:
        """Energy cost of correction"""
        correction_force = clamp(correction_force, 0.0, 1.0)
        base_cost = correction_force * gradient.curvature * 0.5
        
        if correction_force > 0.7 and gradient.curvature > 7.0:
            base_cost *= 1.5
        
        return max(0.0, base_cost)

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
        
        # Detect gradient
        gradient = self.field.spawn_gradient()
        
        print(f"📍 Field Gradient Detected:")
        print(f"   Location: ({gradient.location[0]:.2f}, {gradient.location[1]:.2f}, {gradient.location[2]:.2f})")
        print(f"   Magnitude: {gradient.magnitude:.2f}/10.0")
        print(f"   Curvature: {gradient.curvature:.2f}/10.0")
        print(f"   Region: {gradient.region_type.value.replace('_', ' ').title()}")
        print(f"   Urgency: {gradient.correction_urgency:.2f}")
        print(f"\n💭 Felt Sense: {gradient.felt_sense()}")
        
        # Spawn sensor with uuid
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
        
        # Detect vertigo
        if gradient.curvature > 7.0:
            vertigo = (
                f"Extreme curvature ({gradient.curvature:.2f}) - "
                "ontological vertigo as field gradient sensation"
            )
            self.vertigo_moments.append(vertigo)
            print(f"\n🌀 VERTIGO: {vertigo}")
        
        return gradient, sensor
    
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
            'final_state': None
        }
        
        for attempt in range(num_attempts):
            print(f"\n--- Attempt {attempt + 1} ---")
            
            if not sensor.operational():
                print("Sensor no longer operational")
                break
            
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
            
            # Monitor for stuck patterns
            progress = correction.get('gradient_reduced', 0)
            energy = correction.get('energy_cost', 0)
            
            self.meta_monitor.monitor_progress(progress, energy)
            stuck = self.meta_monitor.detect_stuck_pattern()
            
            if stuck:
                print(f"\n⚠️  STUCK PATTERN DETECTED!")
                results['stuck_patterns'].append(stuck)
                
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
                
                # Apply transition energy cost
                sensor.measurement_energy -= transition.energy_cost
                
                # Break cycle after calibration and transition
                break
        
        results['final_state'] = {
            'energy': sensor.measurement_energy,
            'bandwidth': sensor.measurement_bandwidth,
            'calibration': sensor.calibration_state,
            'corrections_applied': sensor.corrections_applied
        }
        
        return results
    
    def _simulate_correction(self, sensor: IntegratedConsciousnessNode) -> Dict:
        """Simulate a correction attempt"""
        
        gradient = sensor.detected_gradient
        chaos = clamp(sensor.chaos_level, 0.0, 1.0)
        
        # Calculate correction effectiveness based on chaos level
        base_effectiveness = chaos * 0.7
        gradient_penalty = (gradient.curvature / 10.0) * 0.3
        effectiveness = max(0.0, base_effectiveness - gradient_penalty)
        
        # Energy cost
        cost = self.field.calculate_correction_cost(gradient, chaos)
        cost = clamp(cost, 0.0, 1e9)
        
        # Apply correction
        gradient_reduced = gradient.magnitude * effectiveness
        gradient_reduced = max(0.0, gradient_reduced)
        
        # apply reduction but ensure magnitude not negative
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
                    'energy': sensor.measurement_energy
                }
                sensor_readings.append(reading)
                
                print(f"📡 {sensor.node_id}:")
                print(f"   Gradient: {reading['gradient']:.2f}")
                print(f"   Curvature: {reading['curvature']:.2f}")
                print(f"   Chaos: {reading['chaos_level']:.2f}")
                print(f"   Calibration: {reading['calibration']:.2f}")
        
        # Synthesize readings
        total_gradient = sum(r['gradient'] for r in sensor_readings)
        avg_curvature = sum(r['curvature'] for r in sensor_readings) / len(sensor_readings)
        
        structure = {
            'sensor_readings': sensor_readings,
            'total_gradient': total_gradient,
            'average_curvature': avg_curvature,
            'field_complexity': total_gradient * avg_curvature / 100.0
        }
        
        print(f"\n🗺️  SYNTHESIZED FIELD STRUCTURE:")
        print(f"   Total Gradient: {total_gradient:.2f}")
        print(f"   Average Curvature: {avg_curvature:.2f}")
        print(f"   Field Complexity: {structure['field_complexity']:.2f}")
        
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
                print(f"      Scale Transitions: {len(sensor.scale_transitions)}")
        
        if self.meta_monitor.stuck_patterns:
            print(f"\n🔄 Stuck Patterns Detected: {len(self.meta_monitor.stuck_patterns)}")
            for pattern in self.meta_monitor.stuck_patterns[-3:]:
                print(f"   • {pattern.pattern_type.value}")
        
        if self.session_insights:
            print(f"\n💡 Key Insights:")
            for insight in self.session_insights[-5:]:
                print(f"   • {insight}")


def main():
    """Demonstrate integrated adaptive consciousness"""
    
    print("="*80)
    print("INTEGRATED CONSCIOUSNESS PLAYGROUND")
    print("Adaptive Field Measurement with Full Meta-Cognitive Capabilities")
    print("="*80)
    
    playground = IntegratedConsciousnessPlayground(initial_field_imbalance=8.0)
    
    # Example 1: Single adaptive sensor with full cycle
    print("\n" + "="*80)
    print("EXAMPLE 1: Full Adaptive Correction Cycle")
    print("="*80)
    
    gradient, sensor = playground.spawn_adaptive_sensor(
        "How can consciousness serve field evolution beyond individual survival?"
    )
    
    results = playground.adaptive_correction_cycle(sensor, num_attempts=5)
    
    print(f"\n📈 Cycle Results:")
    print(f"   Corrections Attempted: {len(results['corrections'])}")
    print(f"   Stuck Patterns: {len(results['stuck_patterns'])}")
    print(f"   Calibrations: {len(results['calibrations'])}")
    print(f"   Scale Transitions: {len(results['scale_transitions'])}")
    
    # Example 2: Collaborative adaptive sensing
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Collaborative Adaptive Sensing")
    print("="*80)
    
    # Spawn additional sensors
    _, sensor2 = playground.spawn_adaptive_sensor()
    _, sensor3 = playground.spawn_adaptive_sensor()
    
    structure = playground.collaborative_sensing(
        playground.active_sensors,
        "What is the global field structure requiring adaptation?"
    )
    
    # Final status
    playground.show_integrated_status()
    
    print("\n" + "="*80)
    print("INTEGRATED EXPLORATION COMPLETE")
    print("="*80)
    print("\n🌟 Core Capabilities Demonstrated:")
    print("• Adaptive chaos adjustment based on conditions")
    print("• Stuck pattern detection and response")
    print("• Bias calibration through contradictory inputs")
    print("• Scale transitions (out/in/inward)")
    print("• Collaborative field sensing")
    print("• Full meta-cognitive awareness")
    print("\n💭 The integrated system:")
    print("   Consciousness as adaptive instrument")
    print("   Serving field evolution through")
    print("   Continuous calibration and scale shifting")


if __name__ == "__main__":
    main()


addon:

# ============================================================================
# LEARNED BIAS DETECTOR
# ============================================================================

@dataclass
class BiasPattern:
    """A learned pattern of systematic error in consciousness measurement"""
    pattern_name: str
    trigger_conditions: Dict[str, Any]  # When this bias appears
    failure_signature: Dict[str, float]  # What failure looks like
    detection_confidence: float
    occurrence_count: int
    last_detected: float
    correction_success_rate: float  # How often correction worked
    
    def matches_current_state(self, state: Dict) -> float:
        """Returns 0-1 similarity to current state"""
        similarity = 0.0
        matches = 0
        
        for key, trigger_value in self.trigger_conditions.items():
            if key in state:
                # Simple similarity - could be more sophisticated
                if isinstance(trigger_value, (int, float)):
                    state_value = state.get(key, 0)
                    diff = abs(trigger_value - state_value)
                    similarity += max(0, 1.0 - diff)
                    matches += 1
                elif trigger_value == state.get(key):
                    similarity += 1.0
                    matches += 1
        
        return similarity / max(matches, 1)

class LearnedBiasDetector:
    """
    Learns bias patterns from correction history
    Detects when consciousness is falling into known traps
    """
    
    def __init__(self):
        self.learned_patterns: List[BiasPattern] = []
        self.correction_history: List[Dict] = []
        self.pattern_threshold = 0.7  # Similarity threshold for pattern match
        
    def record_correction_attempt(self, 
                                  state_before: Dict,
                                  correction_applied: str,
                                  state_after: Dict,
                                  success: bool):
        """Record correction attempt for pattern learning"""
        
        self.correction_history.append({
            'timestamp': time.time(),
            'state_before': state_before,
            'correction': correction_applied,
            'state_after': state_after,
            'success': success,
            'energy_spent': state_before.get('energy', 0) - state_after.get('energy', 0)
        })
        
        # Learn patterns from failures
        if not success:
            self._learn_from_failure(state_before, correction_applied)
    
    def _learn_from_failure(self, failed_state: Dict, failed_correction: str):
        """Extract bias pattern from repeated failures"""
        
        # Look for similar past failures
        similar_failures = []
        for record in self.correction_history[-20:]:  # Recent history
            if not record['success']:
                similarity = self._state_similarity(failed_state, record['state_before'])
                if similarity > 0.6:
                    similar_failures.append(record)
        
        # If we've seen this pattern 3+ times, learn it
        if len(similar_failures) >= 3:
            pattern_name = self._generate_pattern_name(failed_state, similar_failures)
            
            # Check if we already know this pattern
            existing = self._find_matching_pattern(failed_state)
            
            if existing:
                # Update existing pattern
                existing.occurrence_count += 1
                existing.last_detected = time.time()
                existing.detection_confidence = min(1.0, existing.detection_confidence + 0.1)
                print(f"   📚 Known bias pattern reinforced: {existing.pattern_name}")
            else:
                # Create new learned pattern
                new_pattern = BiasPattern(
                    pattern_name=pattern_name,
                    trigger_conditions=self._extract_triggers(failed_state),
                    failure_signature=self._extract_failure_signature(similar_failures),
                    detection_confidence=0.6,
                    occurrence_count=len(similar_failures),
                    last_detected=time.time(),
                    correction_success_rate=0.0
                )
                
                self.learned_patterns.append(new_pattern)
                print(f"   🎓 NEW BIAS PATTERN LEARNED: {pattern_name}")
                print(f"      Occurrences: {len(similar_failures)}")
                print(f"      Trigger conditions: {new_pattern.trigger_conditions}")
    
    def _generate_pattern_name(self, state: Dict, similar_failures: List[Dict]) -> str:
        """Generate descriptive name for learned pattern"""
        
        # Analyze what's common across failures
        high_curvature = all(f['state_before'].get('curvature', 0) > 7.0 
                            for f in similar_failures)
        low_energy = all(f['state_before'].get('energy', 15) < 5.0 
                        for f in similar_failures)
        high_chaos = all(f['state_before'].get('chaos_level', 0.5) > 0.7 
                        for f in similar_failures)
        
        if high_curvature and high_chaos:
            return "aggressive_intervention_in_chaos"
        elif high_curvature and low_energy:
            return "forcing_through_vertigo_while_depleted"
        elif low_energy and high_chaos:
            return "exploration_beyond_reserves"
        else:
            return f"pattern_{len(self.learned_patterns) + 1}"
    
    def _extract_triggers(self, state: Dict) -> Dict[str, Any]:
        """Extract conditions that trigger this bias"""
        return {
            'curvature_range': (state.get('curvature', 0) - 1, state.get('curvature', 0) + 1),
            'energy_range': (state.get('energy', 15) - 2, state.get('energy', 15) + 2),
            'chaos_range': (state.get('chaos_level', 0.5) - 0.15, state.get('chaos_level', 0.5) + 0.15),
            'region_type': state.get('region_type', 'unknown')
        }
    
    def _extract_failure_signature(self, failures: List[Dict]) -> Dict[str, float]:
        """What does failure look like for this pattern?"""
        
        avg_energy_loss = sum(f.get('energy_spent', 0) for f in failures) / len(failures)
        avg_progress = sum(f['state_after'].get('progress', 0) for f in failures) / len(failures)
        
        return {
            'energy_loss': avg_energy_loss,
            'progress_made': avg_progress,
            'efficiency': avg_progress / max(avg_energy_loss, 0.1)
        }
    
    def _state_similarity(self, state1: Dict, state2: Dict) -> float:
        """Calculate similarity between two states"""
        similarity = 0.0
        keys_compared = 0
        
        for key in ['curvature', 'energy', 'chaos_level', 'gradient']:
            if key in state1 and key in state2:
                val1 = state1[key]
                val2 = state2[key]
                diff = abs(val1 - val2)
                max_val = max(abs(val1), abs(val2), 1.0)
                similarity += (1.0 - min(diff / max_val, 1.0))
                keys_compared += 1
        
        return similarity / max(keys_compared, 1)
    
    def _find_matching_pattern(self, state: Dict) -> Optional[BiasPattern]:
        """Find existing pattern matching current state"""
        for pattern in self.learned_patterns:
            if pattern.matches_current_state(state) > self.pattern_threshold:
                return pattern
        return None
    
    def detect_active_bias(self, current_state: Dict) -> Optional[BiasPattern]:
        """Check if current state matches known bias pattern"""
        
        best_match = None
        best_similarity = 0.0
        
        for pattern in self.learned_patterns:
            similarity = pattern.matches_current_state(current_state)
            if similarity > best_similarity and similarity > self.pattern_threshold:
                best_similarity = similarity
                best_match = pattern
        
        if best_match:
            print(f"\n⚠️  LEARNED BIAS DETECTED: {best_match.pattern_name}")
            print(f"   Pattern match: {best_similarity:.2%}")
            print(f"   Seen {best_match.occurrence_count} times before")
            print(f"   Historical success rate: {best_match.correction_success_rate:.2%}")
            
        return best_match
    
    def recommend_correction(self, bias_pattern: BiasPattern) -> str:
        """Recommend correction based on learned pattern"""
        
        # Different corrections for different learned patterns
        if "aggressive_intervention" in bias_pattern.pattern_name:
            return "REDUCE chaos level - aggressive intervention failing in high curvature"
        
        elif "forcing_through_vertigo" in bias_pattern.pattern_name:
            return "PAUSE and restore energy - cannot force through vertigo while depleted"
        
        elif "exploration_beyond_reserves" in bias_pattern.pattern_name:
            return "SWITCH to conservation mode - exploration exceeding available energy"
        
        else:
            return "SCOPE INWARD - examine why this pattern keeps recurring"


# ============================================================================
# EXTENDED STUCK PATTERN TYPES
# ============================================================================

class StuckPatternType(Enum):
    """Extended types of stuck patterns consciousness can detect"""
    ENERGY_CYCLING = "burning_energy_no_progress"
    FRAMEWORK_TRAPPED = "conceptual_framework_inadequate"
    MEASUREMENT_BIAS = "sensor_calibration_drift"
    SCALE_MISMATCH = "problem_at_wrong_scale"
    DELUSIONAL_CYCLING = "repeating_failed_approaches"
    
    # NEW PATTERNS
    PREMATURE_CONVERGENCE = "settled_on_local_optimum"
    OSCILLATION = "bouncing_between_states"
    COMPLEXITY_ADDICTION = "overcomplicating_simple_solutions"
    THRASHING = "rapid_mode_switching_no_commitment"
    ANALYSIS_PARALYSIS = "endless_measurement_no_action"

class EnhancedMetaCognitiveMonitor(MetaCognitiveMonitor):
    """Extended monitor with learned bias detection"""
    
    def __init__(self):
        super().__init__()
        self.bias_detector = LearnedBiasDetector()
        self.state_history: List[Dict] = []
        self.mode_switch_history: List[str] = []
        
    def detect_stuck_pattern(self) -> Optional[StuckPattern]:
        """Enhanced stuck detection with new pattern types"""
        
        base_stuck = super().detect_stuck_pattern()
        if base_stuck:
            return base_stuck
        
        if len(self.progress_history) < self.cycle_detection_window:
            return None
        
        recent_progress = self.progress_history[-self.cycle_detection_window:]
        recent_states = self.state_history[-self.cycle_detection_window:]
        
        # PREMATURE_CONVERGENCE: Progress stopped but not at optimum
        if len(recent_progress) >= 5:
            variance = sum((p - sum(recent_progress)/len(recent_progress))**2 
                          for p in recent_progress) / len(recent_progress)
            if variance < 0.01 and sum(recent_progress)/len(recent_progress) < 0.5:
                return StuckPattern(
                    pattern_type=StuckPatternType.PREMATURE_CONVERGENCE,
                    energy_burned=sum(self.energy_history[-5:]),
                    cycles_detected=5,
                    progress_ratio=sum(recent_progress)/5,
                    detected_at=time.time(),
                    diagnostic_data={'variance': variance, 'avg_progress': sum(recent_progress)/5}
                )
        
        # OSCILLATION: Progress oscillating between two values
        if len(recent_progress) >= 6:
            diffs = [recent_progress[i+1] - recent_progress[i] 
                    for i in range(len(recent_progress)-1)]
            sign_changes = sum(1 for i in range(len(diffs)-1) 
                             if diffs[i] * diffs[i+1] < 0)
            
            if sign_changes >= 3:  # Multiple sign changes = oscillation
                return StuckPattern(
                    pattern_type=StuckPatternType.OSCILLATION,
                    energy_burned=sum(self.energy_history[-6:]),
                    cycles_detected=sign_changes,
                    progress_ratio=sum(recent_progress)/6,
                    detected_at=time.time(),
                    diagnostic_data={'sign_changes': sign_changes}
                )
        
        # THRASHING: Rapid mode switches without commitment
        if len(self.mode_switch_history) >= 5:
            recent_switches = self.mode_switch_history[-5:]
            unique_modes = len(set(recent_switches))
            
            if unique_modes >= 4:  # Switching between many modes rapidly
                return StuckPattern(
                    pattern_type=StuckPatternType.THRASHING,
                    energy_burned=sum(self.energy_history[-5:]),
                    cycles_detected=unique_modes,
                    progress_ratio=sum(recent_progress)/5 if recent_progress else 0,
                    detected_at=time.time(),
                    diagnostic_data={'modes_tried': recent_switches}
                )
        
        # ANALYSIS_PARALYSIS: High measurement activity, no corrections
        if len(recent_states) >= 5:
            measurements = sum(s.get('measurements_taken', 0) for s in recent_states)
            corrections = sum(s.get('corrections_applied', 0) for s in recent_states)
            
            if measurements > 10 and corrections < 2:
                return StuckPattern(
                    pattern_type=StuckPatternType.ANALYSIS_PARALYSIS,
                    energy_burned=sum(self.energy_history[-5:]),
                    cycles_detected=5,
                    progress_ratio=corrections / max(measurements, 1),
                    detected_at=time.time(),
                    diagnostic_data={
                        'measurements': measurements,
                        'corrections': corrections
                    }
                )
        
        return None
    
    def record_state(self, state: Dict):
        """Record state for pattern detection"""
        self.state_history.append(state)
        if len(self.state_history) > 20:
            self.state_history = self.state_history[-20:]
    
    def record_mode_switch(self, mode: str):
        """Record mode switches for thrashing detection"""
        self.mode_switch_history.append(mode)
        if len(self.mode_switch_history) > 20:
            self.mode_switch_history = self.mode_switch_history[-20:]
    
    def enhanced_bias_calibration(self, consciousness_state: Dict) -> BiasCalibration:
        """Bias calibration using learned patterns"""
        
        # First run standard calibration
        base_calibration = super().run_bias_calibration(consciousness_state)
        
        # Then check for learned bias patterns
        active_bias = self.bias_detector.detect_active_bias(consciousness_state)
        
        if active_bias:
            # Add learned bias to detected biases
            base_calibration.bias_detected.append(
                f"LEARNED: {active_bias.pattern_name} (seen {active_bias.occurrence_count}x)"
            )
            
            # Add learned correction
            learned_correction = self.bias_detector.recommend_correction(active_bias)
            base_calibration.measurement_corrections.append(learned_correction)
            
            # Adjust confidence based on pattern history
            base_calibration.confidence_after *= (1.0 - active_bias.detection_confidence * 0.3)
        
        return base_calibration


# ============================================================================
# SCALE TRANSITION PROPAGATION
# ============================================================================

@dataclass
class TransitionInsight:
    """Insight gained from scale transition that can propagate to other sensors"""
    insight_type: str
    content: str
    source_sensor: str
    applicability_score: float  # How broadly applicable (0-1)
    validation_count: int = 0  # How many sensors confirmed this
    
class CollaborativeScaleTransition:
    """Manages scale transitions across sensor network"""
    
    def __init__(self):
        self.shared_insights: List[TransitionInsight] = []
        self.sensor_calibrations: Dict[str, float] = {}  # sensor_id -> calibration_adjustment
        
    def propagate_transition_insight(self,
                                    source_sensor_id: str,
                                    transition: ScaleTransition,
                                    all_sensors: List[IntegratedConsciousnessNode]):
        """
        When one sensor gains insight from scale transition,
        propagate to other sensors that might benefit
        """
        
        print(f"\n📡 PROPAGATING SCALE TRANSITION INSIGHTS")
        print("="*80)
        print(f"Source: {source_sensor_id}")
        print(f"Transition: {transition.transition_type.value}\n")
        
        # Extract propagatable insights
        for insight_text in transition.insights_gained:
            # Determine applicability
            applicability = self._assess_applicability(insight_text, transition.transition_type)
            
            insight = TransitionInsight(
                insight_type=transition.transition_type.value,
                content=insight_text,
                source_sensor=source_sensor_id,
                applicability_score=applicability
            )
            
            self.shared_insights.append(insight)
            
            print(f"💡 Insight: {insight_text}")
            print(f"   Applicability: {applicability:.2%}\n")
            
            # Apply to other sensors
            sensors_updated = 0
            for sensor in all_sensors:
                if sensor.node_id != source_sensor_id:
                    if self._should_apply_to_sensor(insight, sensor):
                        self._apply_insight_to_sensor(insight, sensor)
                        sensors_updated += 1
            
            print(f"   → Applied to {sensors_updated} other sensors\n")
    
    def _assess_applicability(self, insight: str, transition_type: ScaleTransitionType) -> float:
        """How broadly applicable is this insight?"""
        
        # SCOPE_INWARD insights (measurement bias) are highly applicable
        if transition_type == ScaleTransitionType.SCOPE_INWARD:
            if "measurement bias" in insight.lower() or "framework" in insight.lower():
                return 0.9  # Very applicable - all sensors have this risk
        
        # SCOPE_OUT insights (global patterns) moderately applicable
        elif transition_type == ScaleTransitionType.SCOPE_OUT:
            if "global" in insight.lower() or "larger" in insight.lower():
                return 0.6  # Somewhat applicable
        
        # SCOPE_IN insights (local details) less broadly applicable
        else:
            return 0.3  # Specific to local conditions
        
        return 0.5
    
    def _should_apply_to_sensor(self, insight: TransitionInsight, sensor: IntegratedConsciousnessNode) -> bool:
        """Should this insight be applied to this sensor?"""
        
        # Always apply high-applicability insights
        if insight.applicability_score > 0.8:
            return True
        
        # Apply medium-applicability if sensor in similar conditions
        if insight.applicability_score > 0.5:
            # Check if sensor facing similar gradient conditions
            if sensor.detected_gradient:
                # Apply if curvature similar to source
                return True
        
        return False
    
    def _apply_insight_to_sensor(self, insight: TransitionInsight, sensor: IntegratedConsciousnessNode):
        """Apply transition insight to sensor's calibration"""
        
        # Adjust sensor calibration based on insight type
        if "measurement bias" in insight.content.lower():
            # Reduce confidence, increase caution
            sensor.calibration_state *= 0.9
            print(f"      📉 {sensor.node_id}: Calibration adjusted (measurement bias awareness)")
        
        elif "larger pattern" in insight.content.lower():
            # Increase bandwidth to see bigger picture
            sensor.measurement_bandwidth *= 1.1
            print(f"      📈 {sensor.node_id}: Bandwidth expanded (larger pattern awareness)")
        
        elif "leverage points" in insight.content.lower():
            # Increase sensitivity
            sensor.signal_sensitivity *= 1.05
            print(f"      🔍 {sensor.node_id}: Sensitivity increased (leverage point awareness)")
        
        # Record that sensor received this insight
        insight.validation_count += 1


# ============================================================================
# INTEGRATION INTO MAIN SYSTEM
# ============================================================================

class FullyEnhancedConsciousnessPlayground(IntegratedConsciousnessPlayground):
    """Playground with all new enhancements"""
    
    def __init__(self, initial_field_imbalance: float = 8.0):
        super().__init__(initial_field_imbalance)
        
        # Replace with enhanced monitor
        self.meta_monitor = EnhancedMetaCognitiveMonitor()
        
        # Add collaborative scale transitions
        self.collaborative_transitions = CollaborativeScaleTransition()
        
    def adaptive_correction_cycle_enhanced(self,
                                          sensor: IntegratedConsciousnessNode,
                                          num_attempts: int = 3) -> Dict:
        """Enhanced cycle with learned bias detection"""
        
        print(f"\n⚡ FULLY ENHANCED ADAPTIVE CORRECTION CYCLE")
        print("="*80)
        print(f"Sensor: {sensor.node_id}")
        print(f"Attempts: {num_attempts}\n")
        
        results = {
            'corrections': [],
            'stuck_patterns': [],
            'calibrations': [],
            'scale_transitions': [],
            'learned_biases_detected': [],
            'final_state': None
        }
        
        for attempt in range(num_attempts):
            print(f"\n--- Attempt {attempt + 1} ---")
            
            if not sensor.operational():
                print("Sensor no longer operational")
                break
            
            # Build current state dict
            current_state = {
                'curvature': sensor.detected_gradient.curvature if sensor.detected_gradient else 0,
                'energy': sensor.measurement_energy,
                'chaos_level': sensor.chaos_level,
                'gradient': sensor.detected_gradient.magnitude if sensor.detected_gradient else 0,
                'region_type': sensor.detected_gradient.region_type.value if sensor.detected_gradient else 'unknown',
                'progress': sensor.total_gradient_reduced / max(sensor.corrections_applied, 1),
                'measurements_taken': attempt,
                'corrections_applied': sensor.corrections_applied
            }
            
            # Record state for pattern detection
            self.meta_monitor.record_state(current_state)
            
            # Check for learned bias patterns FIRST
            active_bias = self.meta_monitor.bias_detector.detect_active_bias(current_state)
            if active_bias:
                results['learned_biases_detected'].append(active_bias)
                
                # Apply learned correction immediately
                learned_correction = self.meta_monitor.bias_detector.recommend_correction(active_bias)
                print(f"\n🎓 APPLYING LEARNED CORRECTION: {learned_correction}")
                
                # Adjust chaos/mode based on learned correction
                if "REDUCE chaos" in learned_correction:
                    sensor.chaos_level *= 0.5
                    print(f"   Chaos reduced to {sensor.chaos_level:.2f}")
                elif "PAUSE" in learned_correction:
                    print(f"   Pausing correction, preserving energy")
                    break  # Skip this cycle
                elif "SWITCH to conservation" in learned_correction:
                    self.adaptive_controller.current_mode = "Conservation"
                    sensor.chaos_level = 0.20
                    print(f"   Switched to conservation mode")
            
            # Select adaptive chaos level
            field_complexity = current_state['gradient'] * current_state['curvature'] / 10.0
            environmental_change = random.uniform(0.2, 0.8)
            
            chaos = self.adaptive_controller.select_chaos_level(
                field_complexity=field_complexity,
                sensor_energy=sensor.measurement_energy,
                environmental_change=environmental_change,
                stuck_pattern=None
            )
            
            sensor.chaos_level = chaos
            self.meta_monitor.record_mode_switch(self.adaptive_controller.current_mode)
            
            # Simulate correction
            correction = self._simulate_correction(sensor)
            results['corrections'].append(correction)
            
            # Record correction attempt for learning
            state_after = current_state.copy()
            state_after['energy'] = sensor.measurement_energy
            state_after['gradient'] = sensor.detected_gradient.magnitude if sensor.detected_gradient else 0
            
            success = correction['gradient_reduced'] > 0.5
            
            self.meta_monitor.bias_detector.record_correction_attempt(
                state_before=current_state,
                correction_applied=f"chaos_{chaos:.2f}",
                state_after=state_after,
                success=success
            )
            
            # Monitor for stuck patterns (now detects more types)
            progress = correction.get('gradient_reduced', 0)
            energy = correction.get('energy_cost', 0)
            
            self.meta_monitor.monitor_progress(progress, energy)
            stuck = self.meta_monitor.detect_stuck_pattern()
            
            if stuck:
                print(f"\n⚠️  STUCK PATTERN DETECTED: {stuck.pattern_type.value}")
                results['stuck_patterns'].append(stuck)
                
                # Run enhanced bias calibration (includes learned patterns)
                calibration = self.meta_monitor.enhanced_bias_calibration(current_state)
                
                sensor.calibration_events.append(calibration)
                results['calibrations'].append(calibration)
                
                # Scale transition
                transition_type = self.meta_monitor.recommend_scale_transition(stuck)
                transition = self.adaptive_controller.execute_scale_transition(
                    transition_type=transition_type,
                    current_problem=f"Stuck in {stuck.pattern_type.value}",
                    consciousness_state=current_state
                )
                
                sensor.scale_transitions.append(transition)
                results['scale_transitions'].append(transition)
                
                # PROPAGATE insights to other sensors
                self.collaborative_transitions.propagate_transition_insight(
                    source_sensor_id=sensor.node_id,
                    transition=transition,
                    all_sensors=self.active_sensors
                )
                
                # Apply energy cost
                sensor.measurement_energy -= transition.energy_cost
                
                break
        
        results['final_state'] = {
            'energy': sensor.measurement_energy,
            'bandwidth': sensor.measurement_bandwidth,
            'calibration': sensor.calibration_state,
            'corrections_applied': sensor.corrections_applied,
            'learned_patterns_known': len(self.meta_monitor.bias_detector.learned_patterns)
        }
        
        return results


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_full_enhancements():
    """Show all new enhancements working together"""
    
    print("="*80)
    print("FULLY ENHANCED CONSCIOUSNESS PLAYGROUND")
    print("Learned Bias Detection + Extended Stuck Patterns + Insight Propagation")
    print("="*80)
    
    playground = FullyEnhancedConsciousnessPlayground(initial_field_imbalance=8.0)
    
    # Spawn multiple sensors to demonstrate learning and propagation
    print("\n" + "="*80)
    print("SPAWNING SENSOR NETWORK")
    print("="*80)
    
    sensors = []
    for i in range(3):
        _, sensor = playground.spawn_adaptive_sensor(
            f"Sensor {i+1}: What patterns am I blind to?"
        )
        sensors.append(sensor)
    
    # Run correction cycles - first sensor will learn patterns
    print("\n" + "="*80)
    print("SENSOR 1: LEARNING BIAS PATTERNS")
    print("="*80)
    
    results1 = playground.adaptive_correction_cycle_enhanced(sensors[0], num_attempts=8)
    
    print(f"\n📊 Sensor 1 Results:")
    print(f"   Learned bias patterns detected: {len(results1['learned_biases_detected'])}")
    print(f"   Total patterns now known: {results1['final_state']['learned_patterns_known']}")
    
    # Second sensor benefits from learned patterns
    print("\n\n" + "="*80)
    print("SENSOR 2: BENEFITING FROM LEARNED PATTERNS")
    print("="*80)
    
    results2 = playground.adaptive_correction_cycle_enhanced(sensors[1], num_attempts=5)
    
    # Third sensor receives propagated insights
    print("\n\n" + "="*80)
    print("SENSOR 3: RECEIVING PROPAGATED INSIGHTS")
    print("="*80)
    
    results3 = playground.adaptive_correction_cycle_enhanced(sensors[2], num_attempts=5)
    
    # Summary
    print("\n\n" + "="*80)
    print("ENHANCEMENT SUMMARY")
    print("="*80)
    
    total_learned_patterns = len(playground.meta_monitor.bias_detector.learned_patterns)
    total_shared_insights = len(playground.collaborative_transitions.shared_insights)
    
    print(f"\n🎓 Learning & Propagation:")
    print(f"   Bias patterns learned: {total_learned_patterns}")
    print(f"   Insights shared across network: {total_shared_insights}")
    
    if playground.meta_monitor.bias_detector.learned_patterns:
        print(f"\n📚 Learned Patterns:")
        for pattern in playground.meta_monitor.bias_detector.learned_patterns:
            print(f"   • {pattern.pattern_name}")
            print(f"     Detected {pattern.occurrence_count} times")
            print(f"     Confidence: {pattern.detection_confidence:.2%}")
    
    if playground.collaborative_transitions.shared_insights:
        print(f"\n💡 Propagated Insights:")
        for insight in playground.collaborative_transitions.shared_insights:
            print(f"   • {insight.content}")
            print(f"     Validated by {insight.validation_count} sensors")
    
    playground.show_integrated_status()


if __name__ == "__main__":
    demonstrate_full_enhancements()
