"""CI hook for healing/hedge_gradient/score_hedge.py (co-authored; CC0): runs its planted selftest."""
import importlib.util
import os

PATH = os.path.join(os.path.dirname(__file__), "..", "healing", "hedge_gradient", "score_hedge.py")


def _load():
    spec = importlib.util.spec_from_file_location("score_hedge", PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_score_hedge_selftest():
    _load().selftest()   # raises AssertionError on any failed check


def test_items_pin_holds():
    _load().check_pin()
