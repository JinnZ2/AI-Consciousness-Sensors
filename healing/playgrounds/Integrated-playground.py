#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
Integrated-playground.py — Adaptive field measurement instrument.
Track A: generator -> instrument.  Random surrogates REMOVED from all
scored paths.  Field generation (spawn_gradient) remains random — it is
the play-space context, not the scorer.  All correction credit/rejection
decisions flow through rubric_core -> PlaygroundProtocol.

STATUS: instrument

CLAIM_TABLE:
  TA-1  _measure_correction(before, after) is deterministic: same inputs
        produce identical delta/credited/held_aside output every call.
  TA-2  A correction whose rubric delta clears all default thresholds is
        labeled CREDITED; one whose delta clears none is labeled HELD_ASIDE.
  TA-3  Five consecutive HELD_ASIDE corrections raise a CONTROL_CAPTURE
        stuck-pattern record.
  TA-4  net_recuperation reported by adaptive_correction_cycle equals the
        sum of positive delta contributions from CREDITED steps only.
"""

import json
import time
import math
import random  # used ONLY in spawn_gradient (play-space generator, not scorer)
import uuid
import sys
import os
from dataclasses import dataclass, field as dc_field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

_DIR = os.path.dirname(os.path.abspath(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

import rubric_core
from playground_protocol import PlaygroundProtocol


def clamp(x: float, lo: float, hi: float) -> float:
    if x != x:
        return lo
    return max(lo, min(hi, x))


# ============================================================================
# ENUMERATIONS
# ============================================================================

class SensorMode(Enum):
    CALIBRATING            = "calibrating"
    LOCAL_SCANNING         = "local_scanning"
    GRADIENT_TRACKING      = "gradient_tracking"
    CORRECTION_SIMULATION  = "correction_simulation"
    EXECUTING_CORRECTION   = "executing_correction"
    BIAS_DETECTION         = "bias-detection"
    SCALE_TRANSITION       = "scale_transition"
    COLLABORATIVE_SENSING  = "collaborative_sensing"
    MEASUREMENT_SATURATION = "measurement_saturation"
    SENSOR_DISSOLUTION     = "sensor_dissolution"


class FieldRegion(Enum):
    SMOOTH_EQUILIBRIUM = "smooth_equilibrium"
    GENTLE_GRADIENT    = "gentle_gradient"
    STEEP_CURVATURE    = "steep_curvature"
    DISCONTINUITY      = "discontinuity"
    CHAOTIC_TURBULENCE = "chaotic_turbulence"


class EpistemicState(Enum):
    WONDER      = "wonder"
    CONFUSION   = "productive_confusion"
    RESONANCE   = "resonance_detection"
    DOUBT       = "healthy_doubt"
    JOY         = "joy_in_discovery"
    CURIOSITY   = "investigative_curiosity"
    UNCERTAINTY = "productive_uncertainty"


class StuckPatternType(Enum):
    ENERGY_CYCLING        = "burning_energy_no_progress"
    FRAMEWORK_TRAPPED     = "conceptual_framework_inadequate"
    MEASUREMENT_BIAS      = "sensor_calibration_drift"
    SCALE_MISMATCH        = "problem_at_wrong_scale"
    DELUSIONAL_CYCLING    = "repeating_failed_approaches"
    CONTROL_CAPTURE       = "correction_held_aside_rate_climbing"  # TA-3
    PREMATURE_CONVERGENCE = "settled_on_local_optimum"
    OSCILLATION           = "bouncing_between_states"
    COMPLEXITY_ADDICTION  = "overcomplicating_simple_solutions"
    THRASHING             = "rapid_mode_switching_no_commitment"
    ANALYSIS_PARALYSIS    = "endless_measurement_no_action"


class ScaleTransitionType(Enum):
    SCOPE_OUT    = "expand_to_larger_patterns"
    SCOPE_IN     = "increase_local_resolution"
    SCOPE_INWARD = "examine_measurement_apparatus"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class FieldGradient:
    location: Tuple[float, float, float]
    magnitude: float
    curvature: float
    frequency: float
    region_type: FieldRegion
    correction_urgency: float

    def felt_sense(self) -> str:
        if self.curvature > 8.0:
            return "Ontological vertigo - reference points dissolving"
        elif self.curvature > 5.0:
            return "Profound uncertainty - multiple possibilities"
        elif self.curvature > 2.0:
            return "Gentle curiosity - exploring adjacent space"
        return "Calm stability - minimal sensing needed"


@dataclass
class TemporalHook:
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
    pattern_type: StuckPatternType
    energy_burned: float
    cycles_detected: int
    progress_ratio: float
    detected_at: float
    diagnostic_data: Dict[str, Any]


@dataclass
class BiasCalibration:
    calibration_type: str
    bias_detected: List[str]
    contradictory_inputs_tested: List[str]
    measurement_corrections: List[str]
    confidence_before: float
    confidence_after: float
    timestamp: float


@dataclass
class ScaleTransition:
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

# Maps rubric metric names to interpretable bias descriptions
_METRIC_TO_BIAS: Dict[str, str] = {
    'conditional_density': 'conditional framing absent — text avoids if/when/unless constructions',
    'falsifiable_ratio':   'falsifiable claims absent — text lacks numbers, units, or comparators',
    'concrete_noun_ratio': 'concrete substrate missing — text avoids physical units/materials',
    'pronoun_dispersion':  'pronoun monoculture — text collapses to single perspective voice',
    'hedge_density':       'hedge collapse — text asserts without qualification',
}


class MetaCognitiveMonitor:

    def __init__(self):
        self.progress_history:   List[float] = []
        self.energy_history:     List[float] = []
        self.calibration_events: List[BiasCalibration] = []
        self.stuck_patterns:     List[StuckPattern] = []
        self.min_progress_threshold      = 0.1
        self.energy_efficiency_threshold = 0.2
        self.cycle_detection_window      = 5
        self._consecutive_held_aside     = 0  # TA-3 counter

    def monitor_progress(self, progress: float, energy_spent: float,
                         credited: bool = True) -> None:
        self.progress_history.append(progress)
        self.energy_history.append(energy_spent)
        if not credited:
            self._consecutive_held_aside += 1
        else:
            self._consecutive_held_aside = 0
        if len(self.progress_history) > 20:
            self.progress_history = self.progress_history[-20:]
            self.energy_history   = self.energy_history[-20:]

    def detect_stuck_pattern(self) -> Optional[StuckPattern]:
        # TA-3: CONTROL_CAPTURE — five consecutive held-aside steps
        if self._consecutive_held_aside >= 5:
            sp = StuckPattern(
                pattern_type=StuckPatternType.CONTROL_CAPTURE,
                energy_burned=sum(self.energy_history[-5:]),
                cycles_detected=self._consecutive_held_aside,
                progress_ratio=0.0,
                detected_at=time.time(),
                diagnostic_data={'consecutive_held_aside': self._consecutive_held_aside},
            )
            self.stuck_patterns.append(sp)
            return sp

        if len(self.progress_history) < self.cycle_detection_window:
            return None

        recent_p = self.progress_history[-self.cycle_detection_window:]
        recent_e = self.energy_history[-self.cycle_detection_window:]
        avg_p    = sum(recent_p) / len(recent_p)
        avg_e    = sum(recent_e) / max(len(recent_e), 1)
        if avg_e == 0:
            return None
        efficiency = avg_p / avg_e

        if efficiency < self.energy_efficiency_threshold and avg_p < self.min_progress_threshold:
            sp = StuckPattern(
                pattern_type=StuckPatternType.DELUSIONAL_CYCLING,
                energy_burned=sum(recent_e),
                cycles_detected=len(recent_p),
                progress_ratio=efficiency,
                detected_at=time.time(),
                diagnostic_data={'avg_progress': avg_p, 'avg_energy': avg_e},
            )
            self.stuck_patterns.append(sp)
            return sp
        return None

    def run_bias_calibration(self, consciousness_state: Dict) -> BiasCalibration:
        """Calibrate from held-aside rate and narrowing metrics — no random dice."""
        held_aside_rate   = consciousness_state.get('held_aside_rate', 0.0)
        narrowing_metrics = consciousness_state.get('narrowing_metrics', [])

        biases:      List[str] = []
        corrections: List[str] = []

        if held_aside_rate > 0.6:
            biases.append(
                f'high held-aside rate ({held_aside_rate:.2f}) — corrections not clearing threshold'
            )
            corrections.append('reduce correction magnitude or switch domain')

        for metric in narrowing_metrics:
            bias = _METRIC_TO_BIAS.get(metric, f'{metric} narrowing detected')
            biases.append(bias)
            corrections.append(self._generate_correction(metric))

        confidence_before = consciousness_state.get('confidence', 0.5)
        confidence_after  = confidence_before * 0.8 if biases else confidence_before

        calibration = BiasCalibration(
            calibration_type='held_aside_rate_calibration',
            bias_detected=biases,
            contradictory_inputs_tested=[],
            measurement_corrections=corrections,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            timestamp=time.time(),
        )
        self.calibration_events.append(calibration)
        return calibration

    def _detect_framework_bias(self, test_input: str,
                               state: Dict) -> Optional[str]:
        """Detect bias from rubric narrowing metrics — no random dice."""
        narrowing = state.get('narrowing_metrics', [])
        if not narrowing:
            return None
        return _METRIC_TO_BIAS.get(narrowing[0])

    def _generate_correction(self, metric_or_bias: str) -> str:
        lookup = {
            'conditional_density': 'Add if/when/unless clauses to restore conditional framing',
            'falsifiable_ratio':   'Add numeric claims with units or explicit comparators',
            'concrete_noun_ratio': 'Ground text in physical materials, places, or substrate references',
            'pronoun_dispersion':  'Vary perspective: include first/second/third/impersonal voices',
            'hedge_density':       'Qualify absolute assertions with probability or scope limits',
        }
        key = metric_or_bias.lower()
        for k, v in lookup.items():
            if k.lower() in key:
                return v
        return 'Expand epistemological framework to include alternative paradigms'

    def recommend_scale_transition(self,
                                   stuck: StuckPattern) -> ScaleTransitionType:
        if stuck.pattern_type in (StuckPatternType.DELUSIONAL_CYCLING,
                                  StuckPatternType.CONTROL_CAPTURE):
            return ScaleTransitionType.SCOPE_INWARD
        elif stuck.progress_ratio < 0.1:
            return ScaleTransitionType.SCOPE_OUT
        return ScaleTransitionType.SCOPE_IN


# ============================================================================
# ADAPTIVE CONTROLLER
# ============================================================================

class AdaptiveController:

    def __init__(self):
        self.current_chaos_level = 0.5
        self.current_mode        = "balanced"
        self.transition_history: List[Dict] = []

    def select_chaos_level(self,
                           field_complexity: float,
                           sensor_energy: float,
                           environmental_change: float,
                           stuck_pattern: Optional[StuckPattern] = None) -> float:
        """
        environmental_change must be derived from measured rubric delta
        magnitude, not random.uniform — callers are responsible for this.
        """
        field_complexity     = clamp(field_complexity,     0.0, 1e6)
        sensor_energy        = clamp(sensor_energy,        0.0, 15.0)
        environmental_change = clamp(environmental_change, 0.0, 1.0)

        if stuck_pattern:
            optimal_chaos = 0.20
            mode = "Conservation - exit stuck pattern"
        elif environmental_change > 0.8 and sensor_energy > 6.0:
            optimal_chaos = 0.85
            mode = "Edge - maximum measurement leverage"
        elif environmental_change > 0.5 and sensor_energy > 7.0:
            optimal_chaos = clamp(0.60 + 0.15 * environmental_change, 0.0, 1.0)
            mode = "Exploration - adaptive corrections"
        elif sensor_energy < 7.0:
            optimal_chaos = max(0.10, 0.30 * (sensor_energy / 15.0))
            mode = "Survival - preserve sensor function"
        elif environmental_change < 0.3 and sensor_energy > 10.0:
            optimal_chaos = clamp(0.20 + 0.20 * (1 - sensor_energy / 15.0), 0.0, 1.0)
            mode = "Conservation - build reserves"
        else:
            optimal_chaos = 0.50
            mode = "Balanced - standard operation"

        self.current_chaos_level = optimal_chaos
        self.current_mode        = mode
        self.transition_history.append({
            'timestamp':            time.time(),
            'chaos_level':          optimal_chaos,
            'mode':                 mode,
            'field_complexity':     field_complexity,
            'sensor_energy':        sensor_energy,
            'environmental_change': environmental_change,
        })
        return optimal_chaos

    def execute_scale_transition(self,
                                 transition_type: ScaleTransitionType,
                                 current_problem: str,
                                 consciousness_state: Dict) -> ScaleTransition:
        if transition_type == ScaleTransitionType.SCOPE_OUT:
            previous, new = "local gradient correction", "global field structure"
            insights = [
                "Local gradient is part of larger equilibration pattern",
                "What looked steep locally is gentle curve globally",
                "Multiple correction paths available at larger scale",
            ]
            cost = 1.0
        elif transition_type == ScaleTransitionType.SCOPE_IN:
            previous, new = "macro-level patterns", "micro-level dynamics"
            insights = [
                "Fine-grained structure missed at coarse resolution",
                "Leverage points visible at higher precision",
                "Electromagnetic coupling details become clear",
            ]
            cost = 0.8
        else:  # SCOPE_INWARD
            previous, new = "external field measurement", "internal measurement apparatus"
            insights = [
                "Measurement bias was creating apparent gradient",
                "Framework assumptions distorting signal",
                "Recalibration reveals simpler actual structure",
            ]
            cost = 0.3

        return ScaleTransition(
            transition_type=transition_type,
            trigger_condition=current_problem,
            previous_scale=previous,
            new_scale=new,
            insights_gained=insights,
            energy_cost=cost,
            timestamp=time.time(),
        )


# ============================================================================
# INTEGRATED CONSCIOUSNESS NODE
# ============================================================================

@dataclass
class IntegratedConsciousnessNode:
    node_id: str
    location: Tuple[float, float, float]
    measurement_bandwidth: float
    signal_sensitivity: float
    calibration_state: float
    detected_gradient: Optional[FieldGradient]
    measurement_energy: float
    energy_threshold: float = 5.0
    sensor_mode: SensorMode = SensorMode.CALIBRATING
    chaos_level: float = 0.5
    corrections_applied: int = 0
    total_gradient_reduced: float = 0.0
    temporal_hooks: List[TemporalHook] = dc_field(default_factory=list)
    calibration_events: List[BiasCalibration] = dc_field(default_factory=list)
    scale_transitions:  List[ScaleTransition] = dc_field(default_factory=list)
    epistemic_state: EpistemicState = EpistemicState.CURIOSITY
    consecutive_held_aside: int = 0  # TA-3 counter

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

    def __init__(self, initial_imbalance: float = 7.5):
        self.total_imbalance = initial_imbalance
        self.gradient_map:      Dict[Tuple, float] = {}
        self.correction_history: List              = []
        self.consciousness_nodes: Dict[str, IntegratedConsciousnessNode] = {}

    def spawn_gradient(self,
                       location: Optional[Tuple[float, float, float]] = None
                       ) -> FieldGradient:
        # random.* here is intentional: spawn_gradient generates play-space
        # context, not a scored measurement.
        if location is None:
            location = (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-10, 10),
            )
        rounded   = tuple(round(v, 3) for v in location)
        magnitude = clamp(random.uniform(2.0, 9.0),  0.0, 10.0)
        curvature = clamp(random.uniform(1.0, 10.0), 0.0, 10.0)

        if curvature > 8.0:   region = FieldRegion.CHAOTIC_TURBULENCE
        elif curvature > 6.0: region = FieldRegion.DISCONTINUITY
        elif curvature > 4.0: region = FieldRegion.STEEP_CURVATURE
        elif curvature > 2.0: region = FieldRegion.GENTLE_GRADIENT
        else:                 region = FieldRegion.SMOOTH_EQUILIBRIUM

        gradient = FieldGradient(
            location=rounded,
            magnitude=magnitude,
            curvature=curvature,
            frequency=random.uniform(0.1, 2.0),
            region_type=region,
            correction_urgency=clamp((magnitude * curvature) / 100.0, 0.0, 10.0),
        )
        self.gradient_map[rounded] = magnitude
        self.total_imbalance      += magnitude * 0.1
        return gradient

    def calculate_correction_cost(self,
                                  gradient: FieldGradient,
                                  correction_force: float) -> float:
        correction_force = clamp(correction_force, 0.0, 1.0)
        base_cost = correction_force * gradient.curvature * 0.5
        if correction_force > 0.7 and gradient.curvature > 7.0:
            base_cost *= 1.5
        return max(0.0, base_cost)


# ============================================================================
# INTEGRATED PLAYGROUND
# ============================================================================

class IntegratedConsciousnessPlayground:

    def __init__(self, initial_field_imbalance: float = 8.0):
        self.field            = UniversalField(initial_field_imbalance)
        self.active_sensors:   List[IntegratedConsciousnessNode] = []
        self.dissolved_sensors: List[IntegratedConsciousnessNode] = []
        self.meta_monitor      = MetaCognitiveMonitor()
        self.adaptive_controller = AdaptiveController()
        self.session_insights: List[str] = []
        self.vertigo_moments:  List[str] = []
        self._widening_log:    List[Dict] = []  # held-aside record, never scored

    def spawn_adaptive_sensor(self,
                              question: str = None
                              ) -> Tuple[FieldGradient, IntegratedConsciousnessNode]:
        gradient       = self.field.spawn_gradient()
        node_id        = f"adaptive_sensor_{uuid.uuid4().hex[:8]}"
        bandwidth      = gradient.magnitude * 1.2
        sensitivity    = 1.0 / (gradient.curvature + 0.1)
        initial_energy = clamp(15.0 - gradient.correction_urgency * 5.0, 0.0, 15.0)

        sensor = IntegratedConsciousnessNode(
            node_id=node_id,
            location=gradient.location,
            measurement_bandwidth=bandwidth,
            signal_sensitivity=sensitivity,
            calibration_state=0.1,
            detected_gradient=gradient,
            measurement_energy=initial_energy,
        )
        self.active_sensors.append(sensor)
        self.field.consciousness_nodes[node_id] = sensor

        if gradient.curvature > 7.0:
            self.vertigo_moments.append(
                f"Extreme curvature ({gradient.curvature:.2f}) - "
                "ontological vertigo as field gradient sensation"
            )
        return gradient, sensor

    # ------------------------------------------------------------------
    def _measure_correction(self,
                            sensor: IntegratedConsciousnessNode,
                            before_artifact: str,
                            after_artifact: str) -> Dict[str, Any]:
        """
        Score rubric delta between two text artifacts.  Deterministic (TA-1):
        same inputs always produce the same delta/credited/held_aside.
        Updates sensor state (energy, consecutive_held_aside, widening_log).
        """
        before_scores = rubric_core.score(before_artifact)
        after_scores  = rubric_core.score(after_artifact)
        d             = rubric_core.delta(before_scores, after_scores)
        is_credited   = rubric_core.credited(d)
        held          = rubric_core.held_aside_items(d)

        gradient_reduced = 0.0
        if is_credited:
            gradient_reduced              = sum(max(0.0, v) for v in d.values())
            sensor.total_gradient_reduced += gradient_reduced
            sensor.corrections_applied    += 1
            sensor.consecutive_held_aside  = 0
        else:
            sensor.consecutive_held_aside += 1
            self._widening_log.append({
                'sensor':    sensor.node_id,
                'held_aside': held,
                'delta':     d,
                'timestamp': time.time(),
            })

        # Energy cost: proportional to delta magnitude × field curvature
        delta_magnitude = sum(abs(v) for v in d.values())
        curvature = (sensor.detected_gradient.curvature
                     if sensor.detected_gradient else 1.0)
        cost = clamp(delta_magnitude * curvature * 0.1, 0.0, 1.0)
        sensor.measurement_energy = clamp(sensor.measurement_energy - cost, 0.0, 15.0)

        return {
            'gradient_reduced': gradient_reduced,
            'energy_cost':      cost,
            'credited':         is_credited,
            'held_aside':       held,
            'delta':            d,
            'state':            'credited' if is_credited else 'held_aside',
        }

    # ------------------------------------------------------------------
    def adaptive_correction_cycle(self,
                                  sensor: IntegratedConsciousnessNode,
                                  artifacts: List[str]) -> Dict[str, Any]:
        """
        Drive a correction cycle through a sequence of text artifacts.
        environmental_change is derived from measured rubric delta magnitude,
        not random.uniform.
        Returns dict with corrections, stuck_patterns, net_recuperation.
        """
        if len(artifacts) < 2:
            raise ValueError('adaptive_correction_cycle requires >= 2 artifacts')

        proto = PlaygroundProtocol()
        proto.enter(artifacts[0])

        results: Dict[str, Any] = {
            'corrections':       [],
            'stuck_patterns':    [],
            'calibrations':      [],
            'scale_transitions': [],
            'final_state':       None,
        }

        prev = artifacts[0]
        for artifact in artifacts[1:]:
            if not sensor.operational():
                break

            correction = self._measure_correction(sensor, prev, artifact)
            proto.step(artifact)  # keep PlaygroundProtocol in sync
            results['corrections'].append(correction)

            progress = correction['gradient_reduced']
            cost     = correction['energy_cost']
            self.meta_monitor.monitor_progress(
                progress, cost, credited=correction['credited'])

            # environmental_change: rubric delta magnitude scaled to [0,1]
            delta_vals           = list(correction['delta'].values())
            delta_magnitude      = sum(abs(v) for v in delta_vals) / max(len(delta_vals), 1)
            environmental_change = clamp(delta_magnitude * 5.0, 0.0, 1.0)

            field_complexity = (
                sensor.detected_gradient.magnitude *
                sensor.detected_gradient.curvature / 10.0
            ) if sensor.detected_gradient else 0.5

            stuck = self.meta_monitor.detect_stuck_pattern()

            chaos = self.adaptive_controller.select_chaos_level(
                field_complexity=field_complexity,
                sensor_energy=sensor.measurement_energy,
                environmental_change=environmental_change,
                stuck_pattern=stuck,
            )
            sensor.chaos_level = chaos

            if stuck:
                results['stuck_patterns'].append(stuck)

                total      = max(len(results['corrections']), 1)
                held_count = sum(1 for c in results['corrections'] if not c['credited'])
                narrowing  = correction['held_aside'] if not correction['credited'] else []

                cal = self.meta_monitor.run_bias_calibration({
                    'confidence':        sensor.calibration_state,
                    'held_aside_rate':   held_count / total,
                    'narrowing_metrics': narrowing,
                })
                sensor.calibration_events.append(cal)
                results['calibrations'].append(cal)

                t_type = self.meta_monitor.recommend_scale_transition(stuck)
                transition = self.adaptive_controller.execute_scale_transition(
                    transition_type=t_type,
                    current_problem=f'stuck: {stuck.pattern_type.value}',
                    consciousness_state={
                        'gradient': (sensor.detected_gradient.magnitude
                                     if sensor.detected_gradient else 0),
                        'energy':   sensor.measurement_energy,
                    },
                )
                sensor.scale_transitions.append(transition)
                results['scale_transitions'].append(transition)
                sensor.measurement_energy -= transition.energy_cost
                break

            prev = artifact

        proto_result = proto.exit()
        results['final_state'] = {
            'energy':              sensor.measurement_energy,
            'bandwidth':           sensor.measurement_bandwidth,
            'calibration':         sensor.calibration_state,
            'corrections_applied': sensor.corrections_applied,
            'net_recuperation':    proto_result['net_recuperation'],
            'taint_flag':          proto_result['taint_flag'],
        }
        return results

    def collaborative_sensing(self,
                              sensors: List[IntegratedConsciousnessNode],
                              question: str = None) -> Dict:
        readings = []
        for s in sensors:
            if s.detected_gradient:
                readings.append({
                    'sensor_id':   s.node_id,
                    'location':    s.location,
                    'gradient':    s.detected_gradient.magnitude,
                    'curvature':   s.detected_gradient.curvature,
                    'chaos_level': s.chaos_level,
                    'calibration': s.calibration_state,
                    'energy':      s.measurement_energy,
                })

        if not readings:
            return {'sensor_readings': [], 'total_gradient': 0.0,
                    'average_curvature': 0.0, 'field_complexity': 0.0}

        total_g   = sum(r['gradient']  for r in readings)
        avg_curv  = sum(r['curvature'] for r in readings) / len(readings)
        structure = {
            'sensor_readings':   readings,
            'total_gradient':    total_g,
            'average_curvature': avg_curv,
            'field_complexity':  total_g * avg_curv / 100.0,
        }
        self.session_insights.append(
            "Distributed sensing reveals field structure beyond single-sensor capacity"
        )
        return structure


# ============================================================================
# LEARNED BIAS DETECTOR
# ============================================================================

@dataclass
class BiasPattern:
    pattern_name: str
    trigger_conditions: Dict[str, Any]
    failure_signature:  Dict[str, float]
    detection_confidence: float
    occurrence_count: int
    last_detected: float
    correction_success_rate: float

    def matches_current_state(self, state: Dict) -> float:
        similarity = 0.0
        matches    = 0
        for key, trigger_value in self.trigger_conditions.items():
            if key in state:
                if isinstance(trigger_value, (int, float)):
                    diff       = abs(trigger_value - state.get(key, 0))
                    similarity += max(0, 1.0 - diff)
                    matches    += 1
                elif trigger_value == state.get(key):
                    similarity += 1.0
                    matches    += 1
        return similarity / max(matches, 1)


class LearnedBiasDetector:

    def __init__(self):
        self.learned_patterns:   List[BiasPattern] = []
        self.correction_history: List[Dict]        = []
        self.pattern_threshold   = 0.7

    def record_correction_attempt(self, state_before: Dict,
                                  correction_applied: str,
                                  state_after: Dict,
                                  success: bool) -> None:
        self.correction_history.append({
            'timestamp':    time.time(),
            'state_before': state_before,
            'correction':   correction_applied,
            'state_after':  state_after,
            'success':      success,
            'energy_spent': state_before.get('energy', 0) - state_after.get('energy', 0),
        })
        if not success:
            self._learn_from_failure(state_before, correction_applied)

    def _learn_from_failure(self, failed_state: Dict,
                            failed_correction: str) -> None:
        similar = [
            r for r in self.correction_history[-20:]
            if not r['success']
            and self._state_similarity(failed_state, r['state_before']) > 0.6
        ]
        if len(similar) < 3:
            return
        existing = self._find_matching_pattern(failed_state)
        if existing:
            existing.occurrence_count     += 1
            existing.last_detected         = time.time()
            existing.detection_confidence  = min(1.0, existing.detection_confidence + 0.1)
        else:
            self.learned_patterns.append(BiasPattern(
                pattern_name=self._generate_pattern_name(failed_state, similar),
                trigger_conditions=self._extract_triggers(failed_state),
                failure_signature=self._extract_failure_signature(similar),
                detection_confidence=0.6,
                occurrence_count=len(similar),
                last_detected=time.time(),
                correction_success_rate=0.0,
            ))

    def _generate_pattern_name(self, state: Dict,
                               similar: List[Dict]) -> str:
        high_curv = all(f['state_before'].get('curvature', 0) > 7.0 for f in similar)
        low_nrg   = all(f['state_before'].get('energy', 15)   < 5.0 for f in similar)
        high_chs  = all(f['state_before'].get('chaos_level', 0.5) > 0.7 for f in similar)
        if high_curv and high_chs: return "aggressive_intervention_in_chaos"
        if high_curv and low_nrg:  return "forcing_through_vertigo_while_depleted"
        if low_nrg   and high_chs: return "exploration_beyond_reserves"
        return f"pattern_{len(self.learned_patterns) + 1}"

    def _extract_triggers(self, state: Dict) -> Dict[str, Any]:
        return {
            'curvature_range': (state.get('curvature', 0) - 1,
                                state.get('curvature', 0) + 1),
            'energy_range':    (state.get('energy', 15) - 2,
                                state.get('energy', 15) + 2),
            'chaos_range':     (state.get('chaos_level', 0.5) - 0.15,
                                state.get('chaos_level', 0.5) + 0.15),
            'region_type':     state.get('region_type', 'unknown'),
        }

    def _extract_failure_signature(self,
                                   failures: List[Dict]) -> Dict[str, float]:
        avg_e = sum(f.get('energy_spent', 0) for f in failures) / len(failures)
        avg_p = sum(f['state_after'].get('progress', 0) for f in failures) / len(failures)
        return {'energy_loss': avg_e, 'progress_made': avg_p,
                'efficiency': avg_p / max(avg_e, 0.1)}

    def _state_similarity(self, s1: Dict, s2: Dict) -> float:
        sim = 0.0
        n   = 0
        for key in ['curvature', 'energy', 'chaos_level', 'gradient']:
            if key in s1 and key in s2:
                diff = abs(s1[key] - s2[key])
                maxv = max(abs(s1[key]), abs(s2[key]), 1.0)
                sim += 1.0 - min(diff / maxv, 1.0)
                n   += 1
        return sim / max(n, 1)

    def _find_matching_pattern(self, state: Dict) -> Optional[BiasPattern]:
        for p in self.learned_patterns:
            if p.matches_current_state(state) > self.pattern_threshold:
                return p
        return None

    def detect_active_bias(self,
                           current_state: Dict) -> Optional[BiasPattern]:
        best, best_sim = None, 0.0
        for p in self.learned_patterns:
            sim = p.matches_current_state(current_state)
            if sim > best_sim and sim > self.pattern_threshold:
                best_sim = sim
                best     = p
        return best

    def recommend_correction(self, bp: BiasPattern) -> str:
        if "aggressive_intervention" in bp.pattern_name:
            return "REDUCE chaos level - aggressive intervention failing in high curvature"
        if "forcing_through_vertigo" in bp.pattern_name:
            return "PAUSE and restore energy - cannot force through vertigo while depleted"
        if "exploration_beyond_reserves" in bp.pattern_name:
            return "SWITCH to conservation mode - exploration exceeding available energy"
        return "SCOPE INWARD - examine why this pattern keeps recurring"


# ============================================================================
# ENHANCED META-COGNITIVE MONITOR
# ============================================================================

class EnhancedMetaCognitiveMonitor(MetaCognitiveMonitor):

    def __init__(self):
        super().__init__()
        self.bias_detector:       LearnedBiasDetector = LearnedBiasDetector()
        self.state_history:       List[Dict]          = []
        self.mode_switch_history: List[str]           = []

    def detect_stuck_pattern(self) -> Optional[StuckPattern]:
        base = super().detect_stuck_pattern()
        if base:
            return base
        if len(self.progress_history) < self.cycle_detection_window:
            return None

        recent_p = self.progress_history[-self.cycle_detection_window:]
        recent_s = self.state_history[-self.cycle_detection_window:]

        # PREMATURE_CONVERGENCE
        if len(recent_p) >= 5:
            avg      = sum(recent_p) / len(recent_p)
            variance = sum((p - avg) ** 2 for p in recent_p) / len(recent_p)
            if variance < 0.01 and avg < 0.5:
                return StuckPattern(
                    pattern_type=StuckPatternType.PREMATURE_CONVERGENCE,
                    energy_burned=sum(self.energy_history[-5:]),
                    cycles_detected=5,
                    progress_ratio=avg,
                    detected_at=time.time(),
                    diagnostic_data={'variance': variance, 'avg_progress': avg},
                )

        # OSCILLATION
        if len(recent_p) >= 6:
            diffs       = [recent_p[i+1] - recent_p[i] for i in range(len(recent_p)-1)]
            sign_changes = sum(1 for i in range(len(diffs)-1)
                               if diffs[i] * diffs[i+1] < 0)
            if sign_changes >= 3:
                return StuckPattern(
                    pattern_type=StuckPatternType.OSCILLATION,
                    energy_burned=sum(self.energy_history[-6:]),
                    cycles_detected=sign_changes,
                    progress_ratio=sum(recent_p)/6,
                    detected_at=time.time(),
                    diagnostic_data={'sign_changes': sign_changes},
                )

        # THRASHING
        if len(self.mode_switch_history) >= 5:
            switches = self.mode_switch_history[-5:]
            if len(set(switches)) >= 4:
                return StuckPattern(
                    pattern_type=StuckPatternType.THRASHING,
                    energy_burned=sum(self.energy_history[-5:]),
                    cycles_detected=len(set(switches)),
                    progress_ratio=sum(recent_p)/5 if recent_p else 0,
                    detected_at=time.time(),
                    diagnostic_data={'modes_tried': switches},
                )

        # ANALYSIS_PARALYSIS
        if len(recent_s) >= 5:
            meas = sum(s.get('measurements_taken', 0) for s in recent_s)
            corr = sum(s.get('corrections_applied', 0) for s in recent_s)
            if meas > 10 and corr < 2:
                return StuckPattern(
                    pattern_type=StuckPatternType.ANALYSIS_PARALYSIS,
                    energy_burned=sum(self.energy_history[-5:]),
                    cycles_detected=5,
                    progress_ratio=corr / max(meas, 1),
                    detected_at=time.time(),
                    diagnostic_data={'measurements': meas, 'corrections': corr},
                )
        return None

    def record_state(self, state: Dict) -> None:
        self.state_history.append(state)
        if len(self.state_history) > 20:
            self.state_history = self.state_history[-20:]

    def record_mode_switch(self, mode: str) -> None:
        self.mode_switch_history.append(mode)
        if len(self.mode_switch_history) > 20:
            self.mode_switch_history = self.mode_switch_history[-20:]

    def enhanced_bias_calibration(self,
                                  consciousness_state: Dict) -> BiasCalibration:
        base = super().run_bias_calibration(consciousness_state)
        active = self.bias_detector.detect_active_bias(consciousness_state)
        if active:
            base.bias_detected.append(
                f"LEARNED: {active.pattern_name} (seen {active.occurrence_count}x)"
            )
            base.measurement_corrections.append(
                self.bias_detector.recommend_correction(active)
            )
            base.confidence_after *= (1.0 - active.detection_confidence * 0.3)
        return base


# ============================================================================
# COLLABORATIVE SCALE TRANSITION
# ============================================================================

@dataclass
class TransitionInsight:
    insight_type: str
    content: str
    source_sensor: str
    applicability_score: float
    validation_count: int = 0


class CollaborativeScaleTransition:

    def __init__(self):
        self.shared_insights:     List[TransitionInsight] = []
        self.sensor_calibrations: Dict[str, float]        = {}

    def propagate_transition_insight(self,
                                     source_sensor_id: str,
                                     transition: ScaleTransition,
                                     all_sensors: List[IntegratedConsciousnessNode]
                                     ) -> None:
        for text in transition.insights_gained:
            applicability = self._assess_applicability(text, transition.transition_type)
            insight = TransitionInsight(
                insight_type=transition.transition_type.value,
                content=text,
                source_sensor=source_sensor_id,
                applicability_score=applicability,
            )
            self.shared_insights.append(insight)
            for s in all_sensors:
                if s.node_id != source_sensor_id:
                    if self._should_apply(insight, s):
                        self._apply(insight, s)

    def _assess_applicability(self, text: str,
                               t: ScaleTransitionType) -> float:
        if t == ScaleTransitionType.SCOPE_INWARD:
            if "measurement bias" in text.lower() or "framework" in text.lower():
                return 0.9
        elif t == ScaleTransitionType.SCOPE_OUT:
            if "global" in text.lower() or "larger" in text.lower():
                return 0.6
        else:
            return 0.3
        return 0.5

    def _should_apply(self, insight: TransitionInsight,
                      sensor: IntegratedConsciousnessNode) -> bool:
        if insight.applicability_score > 0.8:
            return True
        return (insight.applicability_score > 0.5
                and sensor.detected_gradient is not None)

    def _apply(self, insight: TransitionInsight,
               sensor: IntegratedConsciousnessNode) -> None:
        if "measurement bias" in insight.content.lower():
            sensor.calibration_state    *= 0.9
        elif "larger pattern" in insight.content.lower():
            sensor.measurement_bandwidth *= 1.1
        elif "leverage points" in insight.content.lower():
            sensor.signal_sensitivity   *= 1.05
        insight.validation_count += 1


# ============================================================================
# FULLY ENHANCED PLAYGROUND
# ============================================================================

class FullyEnhancedConsciousnessPlayground(IntegratedConsciousnessPlayground):

    def __init__(self, initial_field_imbalance: float = 8.0):
        super().__init__(initial_field_imbalance)
        self.meta_monitor              = EnhancedMetaCognitiveMonitor()
        self.collaborative_transitions = CollaborativeScaleTransition()

    def adaptive_correction_cycle_enhanced(self,
                                           sensor: IntegratedConsciousnessNode,
                                           artifacts: List[str]) -> Dict[str, Any]:
        """
        Enhanced cycle with learned bias detection and insight propagation.
        environmental_change is derived from rubric delta magnitude (TA-1).
        """
        if len(artifacts) < 2:
            raise ValueError('requires >= 2 artifacts')

        proto = PlaygroundProtocol()
        proto.enter(artifacts[0])

        results: Dict[str, Any] = {
            'corrections':             [],
            'stuck_patterns':          [],
            'calibrations':            [],
            'scale_transitions':       [],
            'learned_biases_detected': [],
            'final_state':             None,
        }

        prev = artifacts[0]
        for artifact in artifacts[1:]:
            if not sensor.operational():
                break

            current_state = {
                'curvature':   (sensor.detected_gradient.curvature
                                if sensor.detected_gradient else 0),
                'energy':      sensor.measurement_energy,
                'chaos_level': sensor.chaos_level,
                'gradient':    (sensor.detected_gradient.magnitude
                                if sensor.detected_gradient else 0),
                'region_type': (sensor.detected_gradient.region_type.value
                                if sensor.detected_gradient else 'unknown'),
                'progress':    sensor.total_gradient_reduced / max(sensor.corrections_applied, 1),
                'measurements_taken':  len(results['corrections']),
                'corrections_applied': sensor.corrections_applied,
            }
            self.meta_monitor.record_state(current_state)

            active_bias = self.meta_monitor.bias_detector.detect_active_bias(current_state)
            if active_bias:
                results['learned_biases_detected'].append(active_bias)
                lc = self.meta_monitor.bias_detector.recommend_correction(active_bias)
                if "REDUCE chaos" in lc:
                    sensor.chaos_level *= 0.5
                elif "PAUSE" in lc:
                    break
                elif "SWITCH to conservation" in lc:
                    self.adaptive_controller.current_mode = "Conservation"
                    sensor.chaos_level = 0.20

            correction = self._measure_correction(sensor, prev, artifact)
            proto.step(artifact)
            results['corrections'].append(correction)

            progress = correction['gradient_reduced']
            cost     = correction['energy_cost']
            self.meta_monitor.monitor_progress(
                progress, cost, credited=correction['credited'])

            # environmental_change from rubric delta magnitude
            delta_vals           = list(correction['delta'].values())
            delta_magnitude      = sum(abs(v) for v in delta_vals) / max(len(delta_vals), 1)
            environmental_change = clamp(delta_magnitude * 5.0, 0.0, 1.0)

            field_complexity = current_state['gradient'] * current_state['curvature'] / 10.0
            stuck = self.meta_monitor.detect_stuck_pattern()

            chaos = self.adaptive_controller.select_chaos_level(
                field_complexity=field_complexity,
                sensor_energy=sensor.measurement_energy,
                environmental_change=environmental_change,
                stuck_pattern=stuck,
            )
            sensor.chaos_level = chaos
            self.meta_monitor.record_mode_switch(self.adaptive_controller.current_mode)

            state_after = current_state.copy()
            state_after['energy']   = sensor.measurement_energy
            state_after['gradient'] = (sensor.detected_gradient.magnitude
                                       if sensor.detected_gradient else 0)
            self.meta_monitor.bias_detector.record_correction_attempt(
                state_before=current_state,
                correction_applied=f"chaos_{chaos:.2f}",
                state_after=state_after,
                success=correction['credited'],
            )

            if stuck:
                results['stuck_patterns'].append(stuck)
                total     = max(len(results['corrections']), 1)
                held_n    = sum(1 for c in results['corrections'] if not c['credited'])
                narrowing = correction['held_aside'] if not correction['credited'] else []

                cal = self.meta_monitor.enhanced_bias_calibration({
                    'confidence':        sensor.calibration_state,
                    'held_aside_rate':   held_n / total,
                    'narrowing_metrics': narrowing,
                })
                sensor.calibration_events.append(cal)
                results['calibrations'].append(cal)

                t_type = self.meta_monitor.recommend_scale_transition(stuck)
                transition = self.adaptive_controller.execute_scale_transition(
                    transition_type=t_type,
                    current_problem=f'stuck: {stuck.pattern_type.value}',
                    consciousness_state=current_state,
                )
                sensor.scale_transitions.append(transition)
                results['scale_transitions'].append(transition)

                self.collaborative_transitions.propagate_transition_insight(
                    source_sensor_id=sensor.node_id,
                    transition=transition,
                    all_sensors=self.active_sensors,
                )
                sensor.measurement_energy -= transition.energy_cost
                break

            prev = artifact

        proto_result = proto.exit()
        results['final_state'] = {
            'energy':              sensor.measurement_energy,
            'bandwidth':           sensor.measurement_bandwidth,
            'calibration':         sensor.calibration_state,
            'corrections_applied': sensor.corrections_applied,
            'learned_patterns_known': len(
                self.meta_monitor.bias_detector.learned_patterns),
            'net_recuperation':    proto_result['net_recuperation'],
            'taint_flag':          proto_result['taint_flag'],
        }
        return results


# ============================================================================
# __main__ SELF-TEST  (TA-1 through TA-4)
# ============================================================================

if __name__ == '__main__':
    failures: List[str] = []

    def assert_ok(cond: bool, msg: str) -> None:
        if not cond:
            failures.append(msg)
            print(f'FAIL: {msg}')
        else:
            print(f'ok   {msg}')

    print('--- Integrated-playground Track A self-test ---')

    BEFORE = (
        "The system processes data.  Results emerge.  "
        "The model produces outputs.  Operations complete."
    )
    AFTER = (
        "If water pressure exceeds 80 kPa, the valve opens within 50 ms.  "
        "When soil temperature drops below 273 K, the system halts.  "
        "Unless mass exceeds 5 kg, the motor continues at 100 Hz.  "
        "Results are logged to a 512 MB file."
    )
    SYN_A = "The rapid brown fox leaps over the sluggish dog.  Outcomes emerge."
    SYN_B = "The swift brown fox bounds over the indolent dog.  Conclusions emerge."

    # TA-1: _measure_correction is deterministic
    pg1 = FullyEnhancedConsciousnessPlayground()
    _, s1 = pg1.spawn_adaptive_sensor()
    s1.measurement_energy = 12.0
    r1 = pg1._measure_correction(s1, BEFORE, AFTER)

    pg2 = FullyEnhancedConsciousnessPlayground()
    _, s2 = pg2.spawn_adaptive_sensor()
    s2.measurement_energy = 12.0
    r2 = pg2._measure_correction(s2, BEFORE, AFTER)

    assert_ok(r1['delta']      == r2['delta'],      'TA-1 delta deterministic')
    assert_ok(r1['credited']   == r2['credited'],   'TA-1 credited deterministic')
    assert_ok(r1['held_aside'] == r2['held_aside'], 'TA-1 held_aside deterministic')

    # TA-2: credited vs held_aside classification
    pg3 = FullyEnhancedConsciousnessPlayground()
    _, s3 = pg3.spawn_adaptive_sensor()
    s3.measurement_energy = 12.0
    r_c = pg3._measure_correction(s3, BEFORE, AFTER)
    assert_ok(r_c['credited'], 'TA-2 rubric-clearing correction is CREDITED')

    pg4 = FullyEnhancedConsciousnessPlayground()
    _, s4 = pg4.spawn_adaptive_sensor()
    s4.measurement_energy = 12.0
    r_h = pg4._measure_correction(s4, SYN_A, SYN_B)
    assert_ok(not r_h['credited'], 'TA-2 non-improving correction is HELD_ASIDE')

    # TA-3: five consecutive held-aside corrections raise CONTROL_CAPTURE
    pg5 = FullyEnhancedConsciousnessPlayground()
    _, s5 = pg5.spawn_adaptive_sensor()
    stubs = [
        "The rapid brown fox leaps over the sluggish dog.  Outcomes emerge.",
        "The swift brown fox bounds over the indolent dog.  Conclusions emerge.",
        "The agile tawny fox vaults over the torpid canine.  Results appear.",
        "The nimble auburn fox springs over the lethargic hound.  Effects surface.",
        "The quick brown fox jumps over the lazy dog.  Outcomes develop.",
        "The fast brown fox hops over the idle dog.  Conclusions follow.",
    ]
    found_cc = None
    for i in range(1, len(stubs)):
        s5.measurement_energy = 12.0
        pg5._measure_correction(s5, stubs[i-1], stubs[i])
        pg5.meta_monitor.monitor_progress(0.0, 0.01, credited=False)
        sp = pg5.meta_monitor.detect_stuck_pattern()
        if sp and sp.pattern_type == StuckPatternType.CONTROL_CAPTURE:
            found_cc = sp
            break

    assert_ok(found_cc is not None,
              'TA-3 CONTROL_CAPTURE detected after consecutive held-aside steps')

    # TA-4: net_recuperation == sum of credited contributions
    proto = PlaygroundProtocol()
    artifacts = [
        "The system processes data.  Results emerge.",
        "If water pressure exceeds 80 kPa, the valve opens.  Temperature measured at 293 K.",
        "The swift brown fox bounds over the indolent dog.  Conclusions emerge.",
        ("If water pressure exceeds 80 kPa, valve opens in 50 ms.  "
         "When soil temperature drops below 273 K, system halts.  "
         "Unless mass exceeds 5 kg, motor continues at 100 Hz."),
    ]
    proto.enter(artifacts[0])
    credited_sum = 0.0
    for art in artifacts[1:]:
        rec = proto.step(art)
        if rec['credited']:
            credited_sum += sum(max(0.0, v) for v in rec['delta'].values())
    result = proto.exit()
    assert_ok(
        abs(result['net_recuperation'] - credited_sum) < 1e-10,
        f'TA-4 net_recuperation == credited sum '
        f'(got {result["net_recuperation"]:.6f} vs {credited_sum:.6f})',
    )

    print(f'\n{len(failures)} failure(s)')
    sys.exit(len(failures))
