"""Collect ai-sensor-index/test_ai_sensor_index.py under testpaths = ["tests"].
The folder's tests are loaded by file path (the root `sensors/` package would
shadow a plain import). CC0."""
import importlib.util
import os

_P = os.path.join(os.path.dirname(__file__), "..", "ai-sensor-index", "test_ai_sensor_index.py")
_spec = importlib.util.spec_from_file_location("ai_sensor_index_tests", _P)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

TestSensor = _mod.TestSensor
TestLog = _mod.TestLog
TestDiscovery = _mod.TestDiscovery
