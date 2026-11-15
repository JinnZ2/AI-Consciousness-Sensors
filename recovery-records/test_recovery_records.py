"""Tests for recovery-records. stdlib unittest; also collected by pytest.
Run: python3 test_recovery_records.py"""
import json
import os
import tempfile
import unittest

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("recovery_records__load", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_load.py"))
_ld = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ld)
R = _ld.sibling("recovery")
E = _ld.sibling("export")


class TestSchema(unittest.TestCase):
    def test_all_none_record_accepted(self):
        r = R.Recovery()
        self.assertEqual(R.unfilled(r), list(R.FIELD_NAMES))
        self.assertEqual(len(R.FIELD_NAMES), 20)

    def test_voids_survive_json_round_trip(self):
        for rec in [R.Recovery()] + R.SEED:
            d = json.loads(json.dumps(rec.to_dict()))
            self.assertEqual(set(d), set(R.FIELD_NAMES))         # no key dropped
            back = R.Recovery.from_dict(d)
            self.assertEqual(back.to_dict(), rec.to_dict())
            self.assertEqual(R.unfilled(back), R.unfilled(rec))

    def test_fallback_level_bounded(self):
        for ok in (1, 2, 3, 4, 5, None):
            self.assertEqual(R.Recovery(fallback_level=ok).fallback_level, ok)
        for bad in (0, 6, -1, True, 2.5, "3"):
            with self.assertRaises(ValueError, msg=repr(bad)):
                R.Recovery(fallback_level=bad)

    def test_vocabularies_and_types(self):
        with self.assertRaises(ValueError):
            R.Recovery(failure_source="weather")
        with self.assertRaises(ValueError):
            R.Recovery(transmission="video")
        with self.assertRaises(ValueError):
            R.Recovery(status_tag="TRUE")
        with self.assertRaises(ValueError):
            R.Recovery(recorded_in_official_system="no")
        with self.assertRaises(ValueError):
            R.Recovery(coupled_domains="freight")
        with self.assertRaises(ValueError):
            R.Recovery.from_dict({"recoverer_name": "x"})
        self.assertEqual(R.Recovery(coupled_domains=[]).coupled_domains, [])

    def test_seed(self):
        self.assertEqual([r.case_id for r in R.SEED], [f"RR-00{i}" for i in range(1, 7)])
        self.assertEqual({r.status_tag for r in R.SEED}, {"PROPOSED"})
        self.assertTrue(all(r.recorded_in_official_system is None for r in R.SEED))


class TestExport(unittest.TestCase):
    def test_export_produces_both_formats(self):
        with tempfile.TemporaryDirectory() as t:
            out = os.path.join(t, "out")
            txt, jsl = E.export(R.SEED, out)
            with open(txt, encoding="utf-8") as fh:
                blocks = fh.read().strip().split("\n\n")
            with open(jsl, encoding="utf-8") as fh:
                pairs = [json.loads(x) for x in fh]
            self.assertEqual(len(blocks), 6)
            self.assertEqual(len(pairs), 6)
            for block, pair, rec in zip(blocks, pairs, R.SEED):
                self.assertEqual(set(pair), {"case_id", "narrative", "record"})
                self.assertEqual(pair["narrative"], block)
                self.assertEqual(pair["record"], rec.to_dict())
                self.assertEqual(block.count(E.VOID), len(R.unfilled(rec)))

    def test_export_keeps_voids_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            out = os.path.join(t, "out")
            E.export([R.Recovery()], out)
            with open(os.path.join(out, "pairs.jsonl")) as fh:
                pair = json.loads(fh.readline())
            self.assertTrue(all(v is None for v in pair["record"].values()))
            self.assertEqual(pair["narrative"].count(E.VOID), 20)
            with self.assertRaises(FileExistsError):
                E.export(R.SEED, out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
