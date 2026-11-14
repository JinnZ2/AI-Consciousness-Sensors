"""Collect recovery-records/test_recovery_records.py under testpaths = ["tests"].
Loaded by file path; the folder's modules use generic names. CC0."""
import importlib.util
import os
import unittest as _ut

_P = os.path.join(os.path.dirname(__file__), "..", "recovery-records", "test_recovery_records.py")
_spec = importlib.util.spec_from_file_location("recovery_records_tests", _P)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

globals().update({_n: _o for _n, _o in vars(_mod).items()
                  if isinstance(_o, type) and issubclass(_o, _ut.TestCase) and _o is not _ut.TestCase})
