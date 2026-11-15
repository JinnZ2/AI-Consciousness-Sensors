"""Load a sibling module by file path. CC0.

`export` and `recovery` are generic module names; loading by path under a
folder-specific name keeps them from colliding with anything else on sys.path.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sibling(name):
    key = "recovery_records_" + name
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod
