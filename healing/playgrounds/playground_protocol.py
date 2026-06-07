#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
playground_protocol.py -- Contract interface for scored playgrounds.

Unscored playgrounds (Track B: Luminal) must NOT use this class.
STATUS: instrument

CLAIM_TABLE:
  PP-1  enter(artifact) establishes baseline rubric scores from the first
        model artifact and resets session state.
  PP-2  step(artifact) returns a record containing: delta (signed per-metric),
        credited (bool), held_aside (list of metric names), and state label.
  PP-3  exit() returns trajectory (all step records), net_recuperation, and
        taint_flag.
  PP-4  net_recuperation is the sum of credited step contributions ONLY.
        Held-aside steps contribute 0.0 regardless of their delta values.
        This is the closure-law invariant.
  PP-5  A trivial mock artifact stream where each artifact is strictly more
        conditional and unit-dense than the last produces a monotone,
        auditable trajectory with net_recuperation > 0.
"""

import sys
import os
from typing import Any, Dict, List, Optional

# Allow import from the same directory when run as a script.
_DIR = os.path.dirname(os.path.abspath(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

import rubric_core


class PlaygroundProtocol:
    """
    Contract that every scored playground implements.
    Drives any scored playground uniformly from a front-end or orchestrator.
    """

    def __init__(self, thresholds: Optional[Dict[str, float]] = None) -> None:
        self._thresholds: Optional[Dict[str, float]] = thresholds
        self._baseline: Optional[Dict[str, float]] = None
        self._trajectory: List[Dict[str, Any]] = []
        self._net_recuperation: float = 0.0
        self._taint_flag: bool = False

    # ------------------------------------------------------------------
    def enter(self, model_artifact: str) -> Dict[str, float]:
        """
        Establish baseline from the first model artifact.  Resets session.
        Returns the baseline score dict (PP-1).
        """
        self._taint_flag = rubric_core._check_taint()
        self._baseline = rubric_core.score(model_artifact)
        self._trajectory = []
        self._net_recuperation = 0.0
        return dict(self._baseline)

    # ------------------------------------------------------------------
    def step(self, model_artifact: str) -> Dict[str, Any]:
        """
        Score one step artifact.
        Returns {delta, credited, held_aside, state, scores} (PP-2).
        held_aside items never touch net_recuperation (PP-4 closure law).
        """
        if self._baseline is None:
            raise RuntimeError('call enter() before step()')

        if rubric_core._check_taint():
            self._taint_flag = True

        prev_scores = (
            self._trajectory[-1]['scores']
            if self._trajectory
            else self._baseline
        )
        current_scores = rubric_core.score(model_artifact)

        d = rubric_core.delta(prev_scores, current_scores)
        is_credited = (
            rubric_core.credited(d, self._thresholds)
            and not self._taint_flag
        )
        held = rubric_core.held_aside_items(d, self._thresholds)

        if is_credited:
            # Sum positive contributions only; closure law: held-aside adds 0.
            contribution = sum(max(0.0, v) for v in d.values())
            self._net_recuperation += contribution

        state = (
            'tainted'    if self._taint_flag else
            'credited'   if is_credited      else
            'held_aside'
        )

        record: Dict[str, Any] = {
            'step':       len(self._trajectory),
            'scores':     current_scores,
            'delta':      d,
            'credited':   is_credited,
            'held_aside': held,
            'state':      state,
        }
        self._trajectory.append(record)
        return record

    # ------------------------------------------------------------------
    def exit(self) -> Dict[str, Any]:
        """
        End session.  Returns trajectory, net_recuperation, taint_flag (PP-3).
        net_recuperation = sum of credited contributions only (PP-4).
        """
        return {
            'trajectory':       list(self._trajectory),
            'net_recuperation': self._net_recuperation,
            'taint_flag':       self._taint_flag,
            'steps':            len(self._trajectory),
        }


# ---------------------------------------------------------------------------
# __main__ SELF-TEST  (exits non-zero on any failure)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    failures: List[str] = []

    def assert_ok(cond: bool, msg: str) -> None:
        if not cond:
            failures.append(msg)
            print(f'FAIL: {msg}')
        else:
            print(f'ok   {msg}')

    print('--- playground_protocol self-test ---')

    # Artifact ladder: each step is richer in conditionals, units, and concrete nouns.
    # Uses words from _CONCRETE_RE (water, pressure, temperature, mass, volume, etc.)
    # so that concrete_noun_ratio rises measurably from A0 to A1.
    A0 = (
        "The system processes data. Results emerge. "
        "The model produces outputs. Operations complete."
    )
    A1 = (
        "If water pressure exceeds 80 kPa, the valve opens. "
        "The sensor measures temperature at 293 K. "
        "Results emerge when conditions are met."
    )
    A2 = (
        "If water pressure exceeds 80 kPa, the valve opens within 50 ms. "
        "When soil temperature drops below 273 K, the system halts. "
        "Unless mass exceeds 5 kg, the motor continues at 100 Hz. "
        "Given that volume is below 5 L, the pump engages. "
        "Results are logged to a 512 MB file."
    )
    A3 = (
        "If water pressure exceeds 80 kPa at the river intake, the valve opens within 50 ms. "
        "When soil temperature drops below 273 K or rises above 373 K, the system halts. "
        "Unless mass exceeds 5 kg and volume exceeds 5 L, the motor continues at 100 Hz. "
        "Only if blood pressure is stable at 120 kPa does the oxygen sensor proceed. "
        "Given that the brain tissue temperature is below 310 K, monitoring continues. "
        "The water flows at 15 L/min through the 50 mm pipe."
    )

    proto = PlaygroundProtocol()

    # PP-1: enter() establishes baseline
    baseline = proto.enter(A0)
    assert_ok(isinstance(baseline, dict), 'PP-1 enter() returns dict')
    assert_ok(
        set(baseline.keys()) == set(rubric_core.METRIC_NAMES),
        'PP-1 baseline has all metric keys',
    )

    # PP-2: step() returns required fields
    rec1 = proto.step(A1)
    assert_ok('delta' in rec1,      'PP-2 step() has delta field')
    assert_ok('credited' in rec1,   'PP-2 step() has credited field')
    assert_ok('held_aside' in rec1, 'PP-2 step() has held_aside field')
    assert_ok('state' in rec1,      'PP-2 step() has state field')

    rec2 = proto.step(A2)
    rec3 = proto.step(A3)

    result = proto.exit()

    # PP-3: exit() returns required fields
    assert_ok('trajectory' in result,       'PP-3 exit() has trajectory')
    assert_ok('net_recuperation' in result, 'PP-3 exit() has net_recuperation')
    assert_ok('taint_flag' in result,       'PP-3 exit() has taint_flag')

    # PP-5: at least one step credited; net_recuperation > 0; trajectory is auditable
    credited_steps = [r for r in result['trajectory'] if r['credited']]
    assert_ok(len(credited_steps) > 0, 'PP-5 at least one credited step in ladder')
    assert_ok(result['net_recuperation'] > 0.0, 'PP-5 net_recuperation > 0')
    assert_ok(len(result['trajectory']) == 3, 'PP-5 trajectory has 3 records')

    # PP-4: held-aside steps contribute 0 to net_recuperation
    # Build a session where every step is sub-threshold (synonym swaps).
    S0 = "The quick brown fox jumps over the lazy dog. Results emerge."
    S1 = "The rapid brown fox leaps over the sluggish dog. Outcomes emerge."
    S2 = "The swift brown fox bounds over the indolent dog. Conclusions emerge."

    proto2 = PlaygroundProtocol()
    proto2.enter(S0)
    proto2.step(S1)
    proto2.step(S2)
    result2 = proto2.exit()

    held_steps = [r for r in result2['trajectory'] if not r['credited']]
    assert_ok(
        len(held_steps) == 2,
        f'PP-4 both synonym-swap steps held aside (held={len(held_steps)})',
    )
    assert_ok(
        result2['net_recuperation'] == 0.0,
        f'PP-4 net_recuperation == 0.0 for all-held-aside session (got {result2["net_recuperation"]})',
    )

    # Confirm held-aside items are present in records for synonym-swap steps
    for r in result2['trajectory']:
        assert_ok(
            r['state'] == 'held_aside',
            f'PP-4 step {r["step"]} state is held_aside (got {r["state"]})',
        )

    print(f'\n{len(failures)} failure(s)')
    sys.exit(len(failures))
