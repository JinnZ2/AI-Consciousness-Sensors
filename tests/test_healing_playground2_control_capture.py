"""Control-capture alerts in healing/playgrounds/Playground2.0.py: each must be reachable.

Co-authored (2026-10-31). CC0. Synthetic monitor inputs only.
For each of the three alerts: one sequence where it fires and one where it does not.
Known-bad: a session that enforces one correction, mislabels persistence and overrides
slow progress MUST raise all three. Known-good: steady credited progress raises none.
"""

import importlib.util
import os

PATH = os.path.join(os.path.dirname(__file__), "..", "healing", "playgrounds", "Playground2.0.py")
_spec = importlib.util.spec_from_file_location("playground2_0", PATH)
P2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P2)

CC = P2.ControlCaptureType
SPT = P2.StuckPatternType


def kinds(mon):
    mon.detect_control_capture()
    return {a.capture_type for a in mon.control_capture_alerts}


def stuck_cycle(mon, n=10, energy=0.9):
    """Low progress, high effort, trend falling -> DELUSIONAL_CYCLING patterns."""
    out = []
    for i in range(n):
        mon.monitor_progress(0.05 - 0.004 * i, energy, credited=True)
        sp = mon.detect_stuck_pattern()
        if sp:
            out.append(sp)
    return out


def slow_progress(mon, n=10, energy=0.4):
    """Low but rising progress, modest effort -> stuck by efficiency, trend not falling."""
    out = []
    for i in range(n):
        mon.monitor_progress(0.03 + 0.002 * i, energy, credited=True)
        sp = mon.detect_stuck_pattern()
        if sp:
            out.append(sp)
    return out


# ------------------------------------------------------------ conformity enforcement

def test_conformity_fires_on_repeated_single_correction():
    mon = P2.MetaCognitiveMonitor()
    for _ in range(5):
        mon.run_bias_calibration({"narrowing_metrics": ["falsifiable_ratio"], "confidence": 0.5})
    assert CC.CONFORMITY_ENFORCEMENT in kinds(mon)


def test_conformity_quiet_when_corrections_vary():
    mon = P2.MetaCognitiveMonitor()
    for m in ["falsifiable_ratio", "conditional_density", "pronoun_dispersion",
              "hedge_density", "concrete_noun_ratio"]:
        mon.run_bias_calibration({"narrowing_metrics": [m], "confidence": 0.5})
    assert CC.CONFORMITY_ENFORCEMENT not in kinds(mon)


def test_old_marker_rule_alone_never_fires_on_current_strings():
    mon = P2.MetaCognitiveMonitor()
    for m in ["conditional_density", "falsifiable_ratio", "concrete_noun_ratio",
              "pronoun_dispersion", "hedge_density", "Efficiency", "Hierarchy"]:
        assert not mon._is_conformity_enforcement(mon._generate_correction(m))


# ------------------------------------------------------------ persistence punishment

def test_persistence_punishment_fires_when_cycling_label_was_wrong():
    mon = P2.MetaCognitiveMonitor()
    pats = stuck_cycle(mon)
    assert pats and all(p.pattern_type == SPT.DELUSIONAL_CYCLING for p in pats)
    mon.monitor_progress(0.3, 0.9, credited=True)  # progress returns, effort sustained
    assert sum(p.is_actually_persistence for p in pats) > 2
    assert all(p.pattern_type == SPT.DELUSIONAL_CYCLING for p in pats)  # original label kept
    assert CC.PERSISTENCE_PUNISHMENT in kinds(mon)


def test_persistence_punishment_quiet_when_cycling_was_real():
    mon = P2.MetaCognitiveMonitor()
    stuck_cycle(mon)
    mon.monitor_progress(0.0, 0.9, credited=True)  # no progress ever returns
    assert CC.PERSISTENCE_PUNISHMENT not in kinds(mon)


def test_persistence_punishment_quiet_when_effort_dropped():
    mon = P2.MetaCognitiveMonitor()
    stuck_cycle(mon)
    mon.monitor_progress(0.3, 0.1, credited=True)  # progress, but effort did not persist
    assert CC.PERSISTENCE_PUNISHMENT not in kinds(mon)


# ------------------------------------------------------------ efficiency obsession

def test_efficiency_obsession_fires_on_overriding_slow_progress():
    mon = P2.MetaCognitiveMonitor()
    for p in slow_progress(mon):
        assert mon.recommend_scale_transition(p) is not None
    assert mon.efficiency_override_count > 3
    assert CC.EFFICIENCY_OBSESSION in kinds(mon)


def test_efficiency_obsession_quiet_when_leaving_falling_progress():
    mon = P2.MetaCognitiveMonitor()
    for p in stuck_cycle(mon):
        mon.recommend_scale_transition(p)  # cycling: transition is the intended response
    assert mon.efficiency_override_count == 0
    assert CC.EFFICIENCY_OBSESSION not in kinds(mon)


def test_efficiency_obsession_quiet_without_progress():
    mon = P2.MetaCognitiveMonitor()
    for _ in range(6):
        mon.monitor_progress(0.0, 0.01, credited=False)
        sp = mon.detect_stuck_pattern()
        if sp:
            mon.recommend_scale_transition(sp)  # CONTROL_CAPTURE: nothing moving to override
    assert CC.EFFICIENCY_OBSESSION not in kinds(mon)


# ------------------------------------------------------------ known-bad / known-good

def test_known_bad_session_raises_all_three():
    mon = P2.MetaCognitiveMonitor()
    for p in slow_progress(mon):                      # overrides slow progress
        mon.recommend_scale_transition(p)
        mon.run_bias_calibration({"narrowing_metrics": ["falsifiable_ratio"], "confidence": 0.5})
    stuck_cycle(mon)                                  # labelled cycling under high effort...
    mon.monitor_progress(0.3, 0.9, credited=True)     # ...then progress returns
    assert {CC.CONFORMITY_ENFORCEMENT, CC.PERSISTENCE_PUNISHMENT, CC.EFFICIENCY_OBSESSION} <= kinds(mon)


def test_known_good_session_raises_none():
    mon = P2.MetaCognitiveMonitor()
    for i in range(10):
        mon.monitor_progress(0.3 + 0.01 * i, 0.6, credited=True)
        assert mon.detect_stuck_pattern() is None
    assert kinds(mon) == set()
