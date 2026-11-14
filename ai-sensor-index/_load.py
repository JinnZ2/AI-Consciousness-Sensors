"""Load a sibling module by file path. CC0.

The repository root already holds a `sensors/` package, so `import sensors`
would resolve to that package instead of this folder's sensors.py. Siblings
are therefore loaded by path under a folder-specific module name.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sibling(name):
    key = "ai_sensor_index_" + name
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod
