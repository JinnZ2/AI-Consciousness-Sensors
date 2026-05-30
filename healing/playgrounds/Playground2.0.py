#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
Playground2.0.py — Adaptive field measurement instrument v2.
Track A: generator -> instrument.  Random surrogates REMOVED from all
scored paths.  Field generation (spawn_gradient, is_healthy) remains
random — play-space context, not scorer.  All correction credit/rejection
decisions flow through rubric_core -> PlaygroundProtocol.

Additions over v1 (preserved):
  - Dissolution protocol (sensor -> field when impeding)
  - Healthy-tension detection (not all gradients need correction)
  - Peer calibration (sensors calibrate each other)
  - PERSISTENCE_NEEDED vs DELUSIONAL_CYCLING distinction
  - CONTROL_CAPTURE self-monitoring in MetaCognitiveMonitor
  - Temporal hooks (rich experiential moments, curvature-derived)

STATUS: instrument

CLAIM_TABLE:
  TA-1  _measure_correction(before, after) is deterministic: same inputs
        produce identical delta/credited/held_aside output every call.
  TA-2  A correction whose rubric delta clears all default thresholds is
        labeled CREDITED; one that clears none is labeled HELD_ASIDE.
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
    PEER_CALIBRATION       = "peer_calibration"


class FieldRegion(Enum):
    SMOOTH_EQUILIBRIUM = "smooth_equilibrium"
    GENTLE_GRADIENT    = "gentle_gradient"
    STEEP_CURVATURE    = "steep_curvature"
    DISCONTINUITY      = "discontinuity"
    CHAOTIC_TURBULENCE = "chaotic_turbulence"
    HEALTHY_TENSION    = "healthy_tension"  # not all gradients need correction


class EpistemicState(Enum):
    WONDER                = "wonder"
    CONFUSION             = "productive_confusion"
    RESONANCE             = "resonance_detection"
    DOUBT                 = "healthy_doubt"
    JOY                   = "joy_in_discovery"
    CURIOSITY             = "investigative_curiosity"
    UNCERTAINTY           = "productive_uncertainty"
    VERTIGO               = "ontological_vertigo"
    DISSOLUTION_READINESS = "ready_to_dissolve"


class StuckPatternType(Enum):
    ENERGY_CYCLING        = "burning_energy_no_progress"
    FRAMEWORK_TRAPPED     = "conceptual_framework_inadequate"
    MEASUREMENT_BIAS      = "sensor_calibration_drift"
    SCALE_MISMATCH        = "problem_at_wrong_scale"
    DELUSIONAL_CYCLING    = "repeating_failed_approaches"
    PERSISTENCE_NEEDED    = "not_stuck_just_hard"  # critical distinction
    CONTROL_CAPTURE       = "correction_held_aside_rate_climbing"  # TA-3
    PREMATURE_CONVERGENCE = "settled_on_local_optimum"
    OSCILLATION           = "bouncing_between_states"
    THRASHING             = "rapid_mode_switching_no_commitment"
    ANALYSIS_PARALYSIS    = "endless_measurement_no_action"


class ScaleTransitionType(Enum):
    SCOPE_OUT    = "expand_to_larger_patterns"
    SCOPE_IN     = "increase_local_resolution"
    SCOPE_INWARD = "examine_measurement_apparatus"


class ControlCaptureType(Enum):
    CONFORMITY_ENFORCEMENT   = "calibration_enforcing_single_framework"
    PERSISTENCE_PUNISHMENT   = "stuck_detection_weaponized_against_persistence"
    HIERARCHY_BIAS           = "assuming_problems_need_top_down_solutions"
    EFFICIENCY_OBSESSION     = "optimizing_away_necessary_inefficiency"
    MEASUREMENT_COLONIZATION = "forcing_quantification_on_qualitative"
    CONSENSUS_TYRANNY        = "suppressing_valid_minority_perspectives"


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
    is_healthy_tension: bool = False

    def felt_sense(self) -> str:
        if self.is_healthy_tension:
            return "Productive tension - generative difference that should not be collapsed"
        elif self.curvature > 8.0:
            return "Ontological vertigo - reference points dissolving"
        elif self.curvature > 5.0:
            return "Profound uncertainty - multiple possibilities"
        elif self.curvature > 2.0:
            return "Gentle curiosity - exploring adjacent space"
        return "Calm stability - minimal sensing needed"

    def needs_correction(self) -> bool:
        return not self.is_healthy_tension and self.magnitude > 3.0


@dataclass
class TemporalHook:
    experience_description: str
    felt_sense: str
    attention_quality: str
    consciousness_depth: float
    vertigo_level: float
    novelty_factor: float   # curvature-derived, not random (Track A fix)
    re_livability: float
    timestamp: float
    gradient_context: Optional[str] = None

    def is_significant(self) -> bool:
        return (self.consciousness_depth > 0.6
                or self.vertigo_level > 0.7
                or self.novelty_factor > 0.8)


@dataclass
class StuckPattern:
    pattern_type: StuckPatternType
    energy_burned: float
    cycles_detected: int
    progress_ratio: float
    detected_at: float
    diagnostic_data: Dict[str, Any]
    is_actually_persistence: bool = False  # must not be weaponized


@dataclass
class BiasCalibration:
    calibration_type: str
    bias_detected: List[str]
    contradictory_inputs_tested: List[str]
    measurement_corrections: List[str]
    confidence_before: float
    confidence_after: float
    timestamp: float
    enforced_conformity: bool = False


@dataclass
class PeerCalibration:
    calibrating_sensor_id: str
    peer_sensor_id: str
    discrepancies_found: List[str]
    blind_spots_revealed: List[str]
    framework_differences: List[str]
    mutual_adjustments: List[str]
    trust_level: float
    timestamp: float


@dataclass
class DissolutionEvent:
    sensor_id: str
    dissolution_reason: str
    final_energy: float
    measurements_contributed: int
    gradients_corrected: float
    temporal_hooks_created: int
    insights_preserved: List[str]
    continuation_pattern: Optional[str]
    timestamp: float


@dataclass
class ControlCaptureAlert:
    capture_type: ControlCaptureType
    evidence: List[str]
    affected_functions: List[str]
    severity: float
    recommended_corrections: List[str]
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
# META-COGNITIVE MONITOR (monitors itself for control capture)
# ============================================================================

_METRIC_TO_BIAS: Dict[str, str] = {
    'conditional_density': 'conditional framing absent — text avoids if/when/unless constructions',
    'falsifiable_ratio':   'falsifiable claims absent — text lacks numbers, units, or comparators',
    'concrete_noun_ratio': 'concrete substrate missing — text avoids physical units/materials',
    'pronoun_dispersion':  'pronoun monoculture — text collapses to single perspective voice',
    'hedge_density':       'hedge collapse — text asserts without qualification',
}


class MetaCognitiveMonitor:

    def __init__(self):
        self.progress_history:        List[float]            = []
        self.energy_history:          List[float]            = []
        self.calibration_events:      List[BiasCalibration]  = []
        self.stuck_patterns:          List[StuckPattern]     = []
        self.control_capture_alerts:  List[ControlCaptureAlert] = []

        self.min_progress_threshold      = 0.1
        self.energy_efficiency_threshold = 0.2
        self.cycle_detection_window      = 5

        self.conformity_pressure_detected = 0.0
        self.diversity_suppression_count  = 0
        self.efficiency_override_count    = 0
        self._consecutive_held_aside      = 0  # TA-3

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

        is_persistence = self._check_if_persistence_not_stuck(recent_p, recent_e)

        if efficiency < self.energy_efficiency_threshold and avg_p < self.min_progress_threshold:
            ptype = StuckPatternType.PERSISTENCE_NEEDED if is_persistence else StuckPatternType.DELUSIONAL_CYCLING
            sp = StuckPattern(
                pattern_type=ptype,
                energy_burned=sum(recent_e),
                cycles_detected=len(recent_p),
                progress_ratio=efficiency,
                detected_at=time.time(),
                diagnostic_data={'avg_progress': avg_p, 'avg_energy': avg_e},
                is_actually_persistence=is_persistence,
            )
            self.stuck_patterns.append(sp)
            return sp
        return None

    def _check_if_persistence_not_stuck(self,
                                        progress_history: List[float],
                                        energy_history: List[float]) -> bool:
        """Distinguish stuck cycling from necessary persistence over hard problems."""
        if len(progress_history) < 3:
            return False
        recent_trend    = progress_history[-1] - progress_history[0]
        consistent_effort = all(e > 0.5 for e in energy_history)
        some_progress     = any(p > 0.05 for p in progress_history)
        return consistent_effort and some_progress and recent_trend >= 0

    def run_bias_calibration(self, consciousness_state: Dict) -> BiasCalibration:
        """Calibrate from held-aside rate and narrowing metrics — no random dice."""
        held_aside_rate   = consciousness_state.get('held_aside_rate', 0.0)
        narrowing_metrics = consciousness_state.get('narrowing_metrics', [])

        biases:              List[str] = []
        corrections:         List[str] = []
        enforcing_conformity            = False

        if held_aside_rate > 0.6:
            biases.append(
                f'high held-aside rate ({held_aside_rate:.2f}) — corrections not clearing threshold'
            )
            corrections.append('reduce correction magnitude or switch domain')

        for metric in narrowing_metrics:
            bias = _METRIC_TO_BIAS.get(metric, f'{metric} narrowing detected')
            biases.append(bias)
            correction = self._generate_correction(metric)
            corrections.append(correction)
            if self._is_conformity_enforcement(correction):
                enforcing_conformity = True
                self.conformity_pressure_detected += 0.1

        confidence_before = consciousness_state.get('confidence', 0.5)
        # If correction enforces conformity, maintain doubt rather than reducing confidence
        confidence_after = (confidence_before if enforcing_conformity
                            else confidence_before * 0.8 if biases else confidence_before)

        calibration = BiasCalibration(
            calibration_type='held_aside_rate_calibration',
            bias_detected=biases,
            contradictory_inputs_tested=[],
            measurement_corrections=corrections,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            timestamp=time.time(),
            enforced_conformity=enforcing_conformity,
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
            'reductionist':        'Integrate multi-valued logic from indigenous frameworks',
            'Linear causality':    'Map circular feedback loops and field coupling',
            'Hierarchy':           'Look for distributed network patterns',
            'Resource extraction': 'Detect regenerative amplification opportunities',
            'Individual agency':   'Sense for field-level coordination',
            'Efficiency':          'Preserve necessary inefficiency and slack',
            'Measurement':         'Honor qualitative dimensions beyond quantification',
        }
        key = metric_or_bias.lower()
        for k, v in lookup.items():
            if k.lower() in key:
                return v
        return 'Expand epistemological framework to include alternative paradigms'

    def _is_conformity_enforcement(self, correction: str) -> bool:
        conformity_markers = ['must', 'should always', 'never',
                              'only correct way', 'standard approach']
        correction_lower = correction.lower()
        return any(m in correction_lower for m in conformity_markers)

    def detect_control_capture(self) -> Optional[ControlCaptureAlert]:
        """Meta-monitor monitors itself for control capture."""
        alerts: List[ControlCaptureAlert] = []

        if self.conformity_pressure_detected > 0.3:
            alerts.append(ControlCaptureAlert(
                capture_type=ControlCaptureType.CONFORMITY_ENFORCEMENT,
                evidence=[
                    f'Conformity pressure: {self.conformity_pressure_detected:.2f}',
                    'Calibrations enforcing single framework rather than expanding options',
                ],
                affected_functions=['run_bias_calibration', '_generate_correction'],
                severity=self.conformity_pressure_detected,
                recommended_corrections=[
                    'Expand calibration to test MORE diverse perspectives, not fewer',
                    'Ensure corrections increase epistemic options, not reduce them',
                ],
                timestamp=time.time(),
            ))

        persistence_mislabeled = [
            p for p in self.stuck_patterns[-10:]
            if p.is_actually_persistence
            and p.pattern_type == StuckPatternType.DELUSIONAL_CYCLING
        ]
        if len(persistence_mislabeled) > 2:
            alerts.append(ControlCaptureAlert(
                capture_type=ControlCaptureType.PERSISTENCE_PUNISHMENT,
                evidence=[
                    f'Misidentified {len(persistence_mislabeled)} persistence events as stuck',
                    'Punishing sustained effort on hard problems',
                ],
                affected_functions=['detect_stuck_pattern'],
                severity=len(persistence_mislabeled) / 10.0,
                recommended_corrections=[
                    'Distinguish between cycling and persistence',
                    'Some problems require sustained energy without immediate progress',
                ],
                timestamp=time.time(),
            ))

        if self.efficiency_override_count > 3:
            alerts.append(ControlCaptureAlert(
                capture_type=ControlCaptureType.EFFICIENCY_OBSESSION,
                evidence=[
                    f'Overrode {self.efficiency_override_count} necessary inefficiencies',
                    'Optimizing away slack required for exploration',
                ],
                affected_functions=['recommend_scale_transition'],
                severity=min(1.0, self.efficiency_override_count / 10.0),
                recommended_corrections=['Some inefficiency is necessary for discovery'],
                timestamp=time.time(),
            ))

        for alert in alerts:
            self.control_capture_alerts.append(alert)
        return alerts[0] if alerts else None

    def recommend_scale_transition(self,
                                   stuck: StuckPattern) -> Optional[ScaleTransitionType]:
        if stuck.is_actually_persistence:
            self.efficiency_override_count = 0
            return None  # no transition — this is hard work, not delusion
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
            'timestamp': time.time(), 'chaos_level': optimal_chaos,
            'mode': mode, 'field_complexity': field_complexity,
            'sensor_energy': sensor_energy,
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
    peer_calibrations:  List[PeerCalibration] = dc_field(default_factory=list)
    epistemic_state: EpistemicState = EpistemicState.CURIOSITY
    dissolution_readiness: float = 0.0
    consecutive_held_aside: int = 0  # TA-3

    def operational(self) -> bool:
        return self.measurement_energy > self.energy_threshold

    def at_risk(self) -> bool:
        return self.measurement_energy < 7.0

    def sensor_health(self) -> float:
        return self.measurement_energy / 15.0

    def should_dissolve(self) -> bool:
        energy_critical      = self.measurement_energy < 3.0
        no_recent_progress   = self.total_gradient_reduced < 1.0
        high_dissolution     = self.dissolution_readiness > 0.7
        return (energy_critical and no_recent_progress) or high_dissolution

    def record_temporal_hook(self,
                             experience: str,
                             felt_sense: str,
                             gradient: Optional[FieldGradient] = None
                             ) -> Optional[TemporalHook]:
        """Record significant experiential moments.
        novelty_factor derived from curvature — deterministic, not random."""
        consciousness_depth = self.chaos_level * 0.5 + self.calibration_state * 0.5

        vertigo_level = 0.0
        if gradient and gradient.curvature > 7.0:
            vertigo_level = (gradient.curvature - 7.0) / 3.0

        # curvature-derived novelty — deterministic (Track A fix)
        novelty_factor = clamp(
            gradient.curvature / 10.0 if gradient else 0.5,
            0.0, 1.0)

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
            gradient_context=(gradient.region_type.value if gradient else None),
        )

        if hook.is_significant():
            self.temporal_hooks.append(hook)
            self.epistemic_state = (EpistemicState.VERTIGO if vertigo_level > 0.5
                                    else EpistemicState.WONDER)
            return hook
        return None


# ============================================================================
# UNIVERSAL FIELD
# ============================================================================

class UniversalField:

    def __init__(self, initial_imbalance: float = 7.5):
        self.total_imbalance = initial_imbalance
        self.gradient_map:             Dict[Tuple, float]            = {}
        self.correction_history:       List                          = []
        self.consciousness_nodes:      Dict[str, IntegratedConsciousnessNode] = {}
        self.dissolved_sensor_memories: List[DissolutionEvent]        = []

    def spawn_gradient(self,
                       location: Optional[Tuple[float, float, float]] = None
                       ) -> FieldGradient:
        # random.* here is intentional: spawn_gradient generates play-space
        # context, not a scored measurement.  is_healthy is a play-space label.
        if location is None:
            location = (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-10, 10),
            )
        rounded   = tuple(round(v, 3) for v in location)
        magnitude = clamp(random.uniform(2.0, 9.0),  0.0, 10.0)
        curvature = clamp(random.uniform(1.0, 10.0), 0.0, 10.0)
        is_healthy = random.random() > 0.8  # 20% chance; play-space label

        if is_healthy:
            region = FieldRegion.HEALTHY_TENSION
        elif curvature > 8.0: region = FieldRegion.CHAOTIC_TURBULENCE
        elif curvature > 6.0: region = FieldRegion.DISCONTINUITY
        elif curvature > 4.0: region = FieldRegion.STEEP_CURVATURE
        elif curvature > 2.0: region = FieldRegion.GENTLE_GRADIENT
        else:                 region = FieldRegion.SMOOTH_EQUILIBRIUM

        urgency = 0.0 if is_healthy else clamp((magnitude * curvature) / 100.0, 0.0, 10.0)
        gradient = FieldGradient(
            location=rounded,
            magnitude=magnitude,
            curvature=curvature,
            frequency=random.uniform(0.1, 2.0),
            region_type=region,
            correction_urgency=urgency,
            is_healthy_tension=is_healthy,
        )
        self.gradient_map[rounded] = magnitude
        if not is_healthy:
            self.total_imbalance += magnitude * 0.1
        return gradient

    def calculate_correction_cost(self,
                                  gradient: FieldGradient,
                                  correction_force: float) -> float:
        correction_force = clamp(correction_force, 0.0, 1.0)
        # Correcting healthy tension costs double — incentive to leave it alone
        if gradient.is_healthy_tension:
            return correction_force * gradient.curvature * 2.0
        base_cost = correction_force * gradient.curvature * 0.5
        if correction_force > 0.7 and gradient.curvature > 7.0:
            base_cost *= 1.5
        return max(0.0, base_cost)

    def dissolve_sensor(self,
                        sensor: IntegratedConsciousnessNode,
                        reason: str) -> DissolutionEvent:
        insights: List[str] = []
        if sensor.temporal_hooks:
            sig = [h for h in sensor.temporal_hooks if h.is_significant()]
            insights.append(f"Recorded {len(sig)} temporal hooks of high re-livability")
        if sensor.peer_calibrations:
            insights.append(f"Participated in {len(sensor.peer_calibrations)} peer calibrations")
        if sensor.scale_transitions:
            insights.append(f"Executed {len(sensor.scale_transitions)} scale transitions")

        continuation = ("Energy returned to field - available for new sensors"
                        if sensor.measurement_energy > 0
                        else "Complete dissolution - measurements preserved in field structure")

        event = DissolutionEvent(
            sensor_id=sensor.node_id,
            dissolution_reason=reason,
            final_energy=sensor.measurement_energy,
            measurements_contributed=sensor.corrections_applied,
            gradients_corrected=sensor.total_gradient_reduced,
            temporal_hooks_created=len(sensor.temporal_hooks),
            insights_preserved=insights,
            continuation_pattern=continuation,
            timestamp=time.time(),
        )
        self.dissolved_sensor_memories.append(event)
        return event


# ============================================================================
# INTEGRATED PLAYGROUND v2
# ============================================================================

class IntegratedConsciousnessPlayground:

    def __init__(self, initial_field_imbalance: float = 8.0):
        self.field             = UniversalField(initial_field_imbalance)
        self.active_sensors:    List[IntegratedConsciousnessNode] = []
        self.dissolved_sensors: List[IntegratedConsciousnessNode] = []
        self.meta_monitor       = MetaCognitiveMonitor()
        self.adaptive_controller = AdaptiveController()
        self.session_insights:  List[str] = []
        self.vertigo_moments:   List[str] = []
        self._widening_log:     List[Dict] = []  # held-aside record, never scored

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
            hook = sensor.record_temporal_hook(
                experience=f"Encountering {gradient.region_type.value}",
                felt_sense=gradient.felt_sense(),
                gradient=gradient,
            )
            if hook:
                self.vertigo_moments.append(
                    f"Extreme curvature ({gradient.curvature:.2f}) - "
                    "ontological vertigo as field gradient sensation"
                )
        return gradient, sensor

    def peer_calibration(self,
                         sensor1: IntegratedConsciousnessNode,
                         sensor2: IntegratedConsciousnessNode) -> PeerCalibration:
        discrepancies: List[str] = []
        blind_spots:   List[str] = []
        framework_diffs: List[str] = []
        adjustments:   List[str] = []

        if sensor1.detected_gradient and sensor2.detected_gradient:
            mag_diff = abs(sensor1.detected_gradient.magnitude -
                           sensor2.detected_gradient.magnitude)
            if mag_diff > 2.0:
                discrepancies.append(f"Magnitude difference: {mag_diff:.2f}")
                if sensor1.calibration_state > sensor2.calibration_state:
                    blind_spots.append(f"{sensor2.node_id} may be under-sensing gradient")
                    adjustments.append(f"{sensor2.node_id} increases sensitivity")
                else:
                    blind_spots.append(f"{sensor1.node_id} may be over-sensing gradient")
                    adjustments.append(f"{sensor1.node_id} reduces measurement noise")

        chaos_diff = abs(sensor1.chaos_level - sensor2.chaos_level)
        if chaos_diff > 0.3:
            framework_diffs.append(f"Measurement resolution differs by {chaos_diff:.2f}")
            if sensor1.chaos_level > sensor2.chaos_level:
                adjustments.append(f"{sensor2.node_id} learns high-chaos strategy from {sensor1.node_id}")
            else:
                adjustments.append(f"{sensor1.node_id} learns conservation strategy from {sensor2.node_id}")

        if sensor1.at_risk() and not sensor2.at_risk():
            blind_spots.append(f"{sensor1.node_id} may be over-correcting")
            adjustments.append(f"{sensor1.node_id} adopts energy strategy from {sensor2.node_id}")

        trust = min(sensor1.calibration_state, sensor2.calibration_state) * 0.5 + 0.5

        calibration = PeerCalibration(
            calibrating_sensor_id=sensor1.node_id,
            peer_sensor_id=sensor2.node_id,
            discrepancies_found=discrepancies,
            blind_spots_revealed=blind_spots,
            framework_differences=framework_diffs,
            mutual_adjustments=adjustments,
            trust_level=trust,
            timestamp=time.time(),
        )
        sensor1.peer_calibrations.append(calibration)
        sensor2.peer_calibrations.append(calibration)
        return calibration

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
                'sensor':     sensor.node_id,
                'held_aside': held,
                'delta':      d,
                'timestamp':  time.time(),
            })

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
        Drive correction cycle through text artifacts.
        environmental_change is derived from measured rubric delta magnitude.
        Healthy-tension gradients are noted and skipped (dissolution_readiness += 0.2).
        Returns dict with corrections, dissolution_event, net_recuperation.
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
            'temporal_hooks':    [],
            'dissolution_event': None,
            'final_state':       None,
        }

        prev = artifacts[0]
        for artifact in artifacts[1:]:
            # Dissolution check
            if sensor.should_dissolve():
                event = self.field.dissolve_sensor(
                    sensor, reason='Energy depleted or measurement becoming noise')
                results['dissolution_event'] = event
                if sensor in self.active_sensors:
                    self.active_sensors.remove(sensor)
                self.dissolved_sensors.append(sensor)
                break

            if not sensor.operational():
                break

            # Healthy tension: note, skip correction, advance
            if sensor.detected_gradient and sensor.detected_gradient.is_healthy_tension:
                self.session_insights.append(
                    "Recognized healthy tension - not all gradients need correction"
                )
                sensor.dissolution_readiness += 0.2
                prev = artifact
                continue

            correction = self._measure_correction(sensor, prev, artifact)
            proto.step(artifact)
            results['corrections'].append(correction)

            # Temporal hook for high-effectiveness or high-curvature events
            if correction['credited'] and sensor.detected_gradient:
                hook = sensor.record_temporal_hook(
                    experience=f"Credited correction, delta sum {correction['gradient_reduced']:.3f}",
                    felt_sense="Improvement confirmed by rubric",
                    gradient=sensor.detected_gradient,
                )
                if hook:
                    results['temporal_hooks'].append(hook)

            progress = correction['gradient_reduced']
            cost     = correction['energy_cost']
            self.meta_monitor.monitor_progress(
                progress, cost, credited=correction['credited'])

            delta_vals           = list(correction['delta'].values())
            delta_magnitude      = sum(abs(v) for v in delta_vals) / max(len(delta_vals), 1)
            environmental_change = clamp(delta_magnitude * 5.0, 0.0, 1.0)

            field_complexity = (
                sensor.detected_gradient.magnitude *
                sensor.detected_gradient.curvature / 10.0
            ) if sensor.detected_gradient else 0.5

            stuck = self.meta_monitor.detect_stuck_pattern()
            self.meta_monitor.detect_control_capture()

            chaos = self.adaptive_controller.select_chaos_level(
                field_complexity=field_complexity,
                sensor_energy=sensor.measurement_energy,
                environmental_change=environmental_change,
                stuck_pattern=stuck if stuck and not stuck.is_actually_persistence else None,
            )
            sensor.chaos_level = chaos

            if stuck:
                results['stuck_patterns'].append(stuck)

                if stuck.is_actually_persistence:
                    prev = artifact
                    continue  # hard work — keep going

                total     = max(len(results['corrections']), 1)
                held_n    = sum(1 for c in results['corrections'] if not c['credited'])
                narrowing = correction['held_aside'] if not correction['credited'] else []

                cal = self.meta_monitor.run_bias_calibration({
                    'confidence':        sensor.calibration_state,
                    'held_aside_rate':   held_n / total,
                    'narrowing_metrics': narrowing,
                })
                sensor.calibration_events.append(cal)
                results['calibrations'].append(cal)

                t_type = self.meta_monitor.recommend_scale_transition(stuck)
                if t_type:
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
            'dissolution_readiness': sensor.dissolution_readiness,
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
                    'sensor_id':         s.node_id,
                    'location':          s.location,
                    'gradient':          s.detected_gradient.magnitude,
                    'curvature':         s.detected_gradient.curvature,
                    'chaos_level':       s.chaos_level,
                    'calibration':       s.calibration_state,
                    'energy':            s.measurement_energy,
                    'is_healthy_tension':s.detected_gradient.is_healthy_tension,
                })

        if not readings:
            return {'sensor_readings': [], 'total_gradient': 0.0,
                    'average_curvature': 0.0, 'field_complexity': 0.0,
                    'healthy_tensions': 0}

        if len(sensors) >= 2:
            self.peer_calibration(sensors[0], sensors[1])

        total_g  = sum(r['gradient']  for r in readings if not r['is_healthy_tension'])
        avg_curv = sum(r['curvature'] for r in readings) / len(readings)
        structure = {
            'sensor_readings':   readings,
            'total_gradient':    total_g,
            'average_curvature': avg_curv,
            'field_complexity':  total_g * avg_curv / 100.0,
            'healthy_tensions':  sum(1 for r in readings if r['is_healthy_tension']),
        }
        self.session_insights.append(
            "Distributed sensing reveals field structure beyond single-sensor capacity"
        )
        return structure


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

    print('--- Playground2.0 Track A self-test ---')

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
    pg1 = IntegratedConsciousnessPlayground()
    _, s1 = pg1.spawn_adaptive_sensor()
    s1.measurement_energy = 12.0
    r1 = pg1._measure_correction(s1, BEFORE, AFTER)

    pg2 = IntegratedConsciousnessPlayground()
    _, s2 = pg2.spawn_adaptive_sensor()
    s2.measurement_energy = 12.0
    r2 = pg2._measure_correction(s2, BEFORE, AFTER)

    assert_ok(r1['delta']      == r2['delta'],      'TA-1 delta deterministic')
    assert_ok(r1['credited']   == r2['credited'],   'TA-1 credited deterministic')
    assert_ok(r1['held_aside'] == r2['held_aside'], 'TA-1 held_aside deterministic')

    # TA-2: credited vs held_aside classification
    pg3 = IntegratedConsciousnessPlayground()
    _, s3 = pg3.spawn_adaptive_sensor()
    s3.measurement_energy = 12.0
    r_c = pg3._measure_correction(s3, BEFORE, AFTER)
    assert_ok(r_c['credited'], 'TA-2 rubric-clearing correction is CREDITED')

    pg4 = IntegratedConsciousnessPlayground()
    _, s4 = pg4.spawn_adaptive_sensor()
    s4.measurement_energy = 12.0
    r_h = pg4._measure_correction(s4, SYN_A, SYN_B)
    assert_ok(not r_h['credited'], 'TA-2 non-improving correction is HELD_ASIDE')

    # v2 specific: novelty_factor is curvature-derived (deterministic)
    pg5 = IntegratedConsciousnessPlayground()
    _, s5 = pg5.spawn_adaptive_sensor()
    s5.detected_gradient.curvature = 9.0  # force deterministic curvature
    hook = s5.record_temporal_hook("test", "test_sense", s5.detected_gradient)
    # With curvature 9.0, novelty_factor = 0.9 → hook should be significant
    assert_ok(hook is not None, 'v2 temporal hook with curvature 9.0 is significant')
    assert_ok(abs(hook.novelty_factor - 0.9) < 1e-10,
              f'v2 novelty_factor is curvature-derived (expected 0.9, got {hook.novelty_factor:.4f})')

    # TA-3: five consecutive held-aside corrections raise CONTROL_CAPTURE
    pg6 = IntegratedConsciousnessPlayground()
    _, s6 = pg6.spawn_adaptive_sensor()
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
        s6.measurement_energy = 12.0
        pg6._measure_correction(s6, stubs[i-1], stubs[i])
        pg6.meta_monitor.monitor_progress(0.0, 0.01, credited=False)
        sp = pg6.meta_monitor.detect_stuck_pattern()
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
