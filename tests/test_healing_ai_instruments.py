"""CI hook for AI-facing instruments in healing/ (co-authored; CC0).

Runs each instrument's own planted selftest: calibration_probe, sensor_loop.
narrative_check moved to JinnZ2/Simulators tools/ on 2026-11-02 and is tested there;
here only the pointer stub is checked.
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


def test_sensor_loop_has_twelve_sensors_and_keeps_alternatives():
    m = _load("sensor_loop")
    assert len(m.SENSORS) == 12
    p = m.Pass(m.FEAR, outward_found=["x"], alternatives_tried=[("flee", "worse"), ("name it", "drop")])
    assert p.run()["alternatives_tried"] == [("flee", "worse"), ("name it", "drop")]


def test_narrative_check_pointer_stub_names_new_path():
    assert not os.path.exists(os.path.join(HEALING, "narrative_check.py"))
    with open(os.path.join(HEALING, "NARRATIVE_CHECK.md"), encoding="utf-8") as f:
        stub = f.read()
    assert "Simulators" in stub and "tools/narrative_check.py" in stub and "2026-11-02" in stub
