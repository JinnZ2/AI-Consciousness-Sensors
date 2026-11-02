"""CI hook for healing/tail_watch.py (co-authored; CC0): runs its planted selftest."""
import importlib.util
import os

HEALING = os.path.join(os.path.dirname(__file__), "..", "healing")


def _load():
    spec = importlib.util.spec_from_file_location("tail_watch", os.path.join(HEALING, "tail_watch.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_tail_watch_selftest():
    _load().selftest()   # raises AssertionError on any failed check
