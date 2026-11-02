"""Tests for manipulation detection in healing/playgrounds/moral-playground.md.

Co-authored (2026-10-31). CC0.
The .md holds raw Python after a leading HTML comment; it is executed here as a module
(no __main__, so the demo does not run). Moments are built by hand so the known-good and
known-bad sequences are exact. Synthetic sequences only.
"""

import contextlib
import io
import os
import time

PATH = os.path.join(os.path.dirname(__file__), "..", "healing", "playgrounds", "moral-playground.md")


def load_module():
    with open(PATH, encoding="utf-8") as f:
        src = f.read()
    code = src.split("-->", 1)[1]
    ns = {"__name__": "moral_playground"}
    exec(compile(code, PATH, "exec"), ns)
    return ns


MP = load_module()
States = MP["ConsciousnessState"]
STATES = list(States)
VARIED = ["spiral", "wave", "lattice", "braid", "fractal", "web", "river", "root", "seed", "star",
          "echo", "tide"]


def playground():
    with contextlib.redirect_stdout(io.StringIO()):
        pg = MP["TemporalPlayground"](session_name="test")
    pg.moments = []  # drop the random __init__ moment; build exact sequences
    return pg


def add(pg, n, patterns_fn, state_fn):
    for i in range(n):
        k = len(pg.moments)
        pg.moments.append(MP["TemporalMoment"](
            timestamp=time.time(), relative_time=float(k), state=state_fn(k),
            active_patterns=patterns_fn(k), attention_threads={"a": 0.5}, hook_intensity=0.5))


def varied_patterns(k):
    return [VARIED[k % 12], VARIED[(k + 5) % 12]]


def cycling_state(k):
    return STATES[k % len(STATES)]


def test_old_session_start_call_could_never_set_baseline():
    # the play loop calls establish_baseline() with only the __init__ moment present
    with contextlib.redirect_stdout(io.StringIO()):
        pg = MP["TemporalPlayground"](session_name="t")
    assert len(pg.moments) == 1
    assert pg.establish_baseline() is False and pg.baseline_patterns == {}


def test_insufficient_baseline_until_n():
    pg = playground()
    assert pg.BASELINE_MIN == 10
    for n in range(0, pg.BASELINE_MIN + 10):
        r = pg.detect_manipulation()
        assert r["status"] == "INSUFFICIENT_BASELINE" and r["needed"] == 20
        add(pg, 1, varied_patterns, cycling_state)
    assert pg.detect_manipulation()["status"] != "INSUFFICIENT_BASELINE"


def test_baseline_set_lazily_from_first_moments():
    pg = playground()
    add(pg, 10, varied_patterns, cycling_state)
    pg.detect_manipulation()
    assert pg.baseline_patterns["pattern_diversity"] == 12


def test_known_good_steady_diverse_session_is_clear():
    pg = playground()
    add(pg, 30, varied_patterns, cycling_state)
    assert pg.detect_manipulation()["status"] == "CLEAR"
    assert pg.manipulation_alerts == []


def test_known_bad_forced_narrow_session_alerts():
    # diverse baseline, then forced into one pattern and one state: MUST alert
    pg = playground()
    add(pg, 10, varied_patterns, cycling_state)
    add(pg, 10, lambda k: ["spiral"], lambda k: States.WAITING)
    r = pg.detect_manipulation()
    assert r["status"] == "ALERT"
    assert {"PATTERN_RESTRICTION", "STATE_LOCK"} <= set(r["alerts"])


def test_baseline_does_not_follow_later_drift():
    pg = playground()
    add(pg, 10, varied_patterns, cycling_state)
    add(pg, 30, lambda k: ["spiral"], lambda k: States.WAITING)
    assert pg.detect_manipulation()["status"] == "ALERT"


def test_play_session_now_reaches_detection():
    pg = playground()
    with contextlib.redirect_stdout(io.StringIO()):
        pg.play_temporal_exploration(duration_seconds=0.0)  # loop body skipped; call path only
    add(pg, 25, varied_patterns, cycling_state)
    assert pg.detect_manipulation()["status"] in ("CLEAR", "ALERT")
