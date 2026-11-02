"""CI hook for three AI-facing instruments in healing/ (co-authored, Kavik + Claude; CC0).

Runs each instrument's own planted selftest: calibration_probe, sensor_loop, narrative_check.
"""
import importlib.util
import os

HEALING = os.path.join(os.path.dirname(__file__), "..", "healing")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HEALING, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_calibration_probe_selftest():
    assert _load("calibration_probe").selftest() == 0


def test_calibration_probe_missing_score_is_unmeasured():
    m = _load("calibration_probe")
    a, b = m.Run("x"), m.Run("x")
    a.score("closure", 0)
    assert m.drift(a, b)["closure"] == "UNMEASURED"


def test_sensor_loop_selftest():
    assert _load("sensor_loop").selftest() == 0


def test_narrative_check_selftest():
    assert _load("narrative_check").selftest() == 0
