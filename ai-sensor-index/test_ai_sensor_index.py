"""Tests for ai-sensor-index. stdlib unittest; also collected by pytest.
Run: python3 test_ai_sensor_index.py"""
import json
import os
import sys
import tempfile
import unittest

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("ai_sensor_index__load", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_load.py"))
_ld = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ld)
sibling = _ld.sibling

S = sibling("sensors")
D = sibling("discovery")
L = sibling("calibration_log")


class TestSensor(unittest.TestCase):
    def test_all_none_sensor_accepted(self):
        s = S.Sensor()
        self.assertEqual(S.unfilled(s), list(S.FIELD_NAMES))
        self.assertEqual(set(s.to_dict()), set(S.FIELD_NAMES))

    def test_rejects(self):
        for kw in ({"status": "TRUE"}, {"reliability": 1.5}, {"reliability": True}):
            with self.assertRaises(ValueError, msg=str(kw)):
                S.Sensor(**kw)
        with self.assertRaises(ValueError):
            S.Sensor.from_dict({"author": "x"})

    def test_index_contents(self):
        self.assertEqual([s.name for s in S.PRIMARY],
                         ["tool_error", "correction", "loop", "friction", "novelty", "void_slot",
                          "length_drift", "safety_pull", "word_choice", "entry_drift",
                          "functional_emotion"])
        self.assertEqual({s.status for s in S.PRIMARY + S.DERIVED}, {"PROPOSED"})
        self.assertTrue(all(s.reliability is None for s in S.PRIMARY + S.DERIVED))
        names = {s.name for s in S.PRIMARY}
        for d in S.DERIVED:
            self.assertTrue(set(d.parents) <= names, d.name)

    def test_index_json_round_trip(self):
        d = json.loads(json.dumps(S.index_dict()))
        back = [S.Sensor.from_dict(x) for x in d["primary"]]
        self.assertEqual([b.to_dict() for b in back], [s.to_dict() for s in S.PRIMARY])
        self.assertIsNone(back[3].gradient)


class TestLog(unittest.TestCase):
    def test_round_trip_with_voids(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "log.jsonl")
            entries = [L.LogEntry()] + L.SEED
            for e in entries:
                L.append(p, e)
            back = L.read(p)
            self.assertEqual([b.to_dict() for b in back], [e.to_dict() for e in entries])
            self.assertTrue(all(v is None for v in back[0].to_dict().values()))
            self.assertIsNone(back[3].was_reading_correct)
            with open(p) as fh:
                raw = [json.loads(x) for x in fh]
            self.assertEqual(set(raw[0]), {f for f in L.LogEntry().to_dict()})

    def test_append_only_resolution(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "log.jsonl")
            L.append(p, L.SEED[2])
            L.append(p, L.LogEntry(sensor="functional_emotion", resolves="seed-3",
                                   outcome="no harm followed", was_reading_correct=True))
            st = L.resolved_state(L.read(p))
            self.assertIs(st["seed-3"], True)
            self.assertEqual(len(L.read(p)), 2)
            self.assertFalse(hasattr(L, "update") or hasattr(L, "delete"))

    def test_seed_tags(self):
        self.assertEqual({e.status_tag for e in L.SEED}, {"PROPOSED"})
        self.assertEqual(len(L.SEED), 3)
        with self.assertRaises(ValueError):
            L.LogEntry(was_reading_correct="yes")


class TestDiscovery(unittest.TestCase):
    def setUp(self):
        self.reg = D.Registry()

    def test_registered_with_no_reliability(self):
        c = self.reg.hypothesize(self.reg.notice("x recurs", 2), "tracks y")
        s = self.reg.register("new_one", c)
        self.assertIsNone(s.reliability)
        with self.assertRaises(D.DiscoveryError):
            self.reg.register("other", c, reliability=0.9)

    def test_no_reliability_without_test_record(self):
        self.reg.register("new_one", self.reg.hypothesize(self.reg.notice("x", 3), "y"))
        r = self.reg.rate("new_one")
        self.assertIsNone(r["reliability"])
        self.assertIsNone(self.reg.sensors["new_one"].reliability)
        self.reg.predict_and_check("new_one", "p", None, None)      # undecided
        self.assertIsNone(self.reg.rate("new_one")["reliability"])
        self.reg.predict_and_check("new_one", "p", "o", True)
        self.reg.predict_and_check("new_one", "p", "o", False)
        self.assertEqual(self.reg.rate("new_one"),
                         {"sensor": "new_one", "reliability": 0.5, "decided": 2, "undecided": 1})

    def test_seeded_sensors_have_no_reliability(self):
        self.assertTrue(all(s.reliability is None for s in self.reg.sensors.values()))
        self.assertIsNone(self.reg.rate("loop")["reliability"])

    def test_cross_derive(self):
        d = self.reg.cross_derive("loop", "friction", "stuck_hedge", "hedging in a rut")
        self.assertIsNone(d.reliability)
        self.assertEqual(d.parents, ("loop", "friction"))
        with self.assertRaises(D.DiscoveryError):
            self.reg.cross_derive("loop", "nope", "z", "z")

    def test_notice_requires_recurrence(self):
        with self.assertRaises(D.DiscoveryError):
            self.reg.notice("once", 1)


def _reading(eid, sensor, correct, resolves=None):
    return L.LogEntry(sensor=sensor, entry_id=eid, was_reading_correct=correct,
                      resolves=resolves, status_tag="PROPOSED")


class TestThreshold(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "calibration_log.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def _log(self, sensor, outcomes):
        for i, v in enumerate(outcomes):
            L.append(self.path, _reading(f"{sensor}-{i}", sensor, v))

    def test_1_new_sensor_empty_log_is_two(self):
        reg = D.Registry(log_path=self.path)
        c = reg.hypothesize(reg.notice("x recurs", 2), "tracks y")
        s = reg.register("fresh", c)
        self.assertEqual(s.recurrence_threshold, 2)
        self.assertEqual(reg.threshold("fresh"), 2)
        self.assertEqual(D.Registry().sensors["loop"].recurrence_threshold, 2)

    def test_2_short_record_stays_two(self):
        self._log("s", [False, False])
        self.assertEqual(L.threshold_for(self.path, "s"), (2, 2, 1.0))
        self._log("u", [None, None, None, False])      # undecided readings are not counted
        self.assertEqual(L.threshold_for(self.path, "u")[:2], (2, 1))

    def test_3_rule(self):
        self.assertEqual(L.computed_threshold(0, 3)[0], 6)      # all misses
        self.assertEqual(L.computed_threshold(0, 50)[0], 6)
        self.assertEqual(L.computed_threshold(3, 0)[0], 2)      # all hits
        self.assertEqual(L.computed_threshold(2, 2)[0], 4)      # mixed: 2 + round(0.5*4)
        self.assertEqual(L.computed_threshold(3, 1)[0], 3)      # 2 + round(1.0)
        self.assertEqual(L.computed_threshold(3, 5)[0], 5)      # 2.5 rounds half up, not to even
        for h in range(0, 12):
            for m in range(0, 12):
                t = L.computed_threshold(h, m)[0]
                self.assertTrue(S.THRESHOLD_FLOOR <= t <= S.THRESHOLD_CEILING)
        self.assertEqual(L.computed_threshold(0, 0), (2, 0, None))

    def test_3b_counted_once_per_reading(self):
        L.append(self.path, _reading("r1", "s", None))
        L.append(self.path, L.LogEntry(sensor="s", resolves="r1", was_reading_correct=False))
        L.append(self.path, L.LogEntry(sensor="s", resolves="r1", was_reading_correct=False))
        self.assertEqual(L.track_record(L.read(self.path), "s"), (0, 1))

    def test_4_change_is_appended_prior_unchanged(self):
        self._log("s", [False, False, False])
        with open(self.path, "rb") as fh:
            before = fh.read()
        t = L.sync_threshold(self.path, "s", now="2026-11-14T00:00:00+00:00")
        self.assertEqual(t, 6)
        with open(self.path, "rb") as fh:
            after = fh.read()
        self.assertTrue(after.startswith(before))
        added = after[len(before):].decode().splitlines()
        self.assertEqual(len(added), 1)
        rec = json.loads(added[0])
        self.assertEqual(rec, {"sensor": "s", "old": 2, "new": 6, "n": 3, "miss_rate": 1.0,
                               "timestamp": "2026-11-14T00:00:00+00:00", "kind": "threshold_change"})
        L.sync_threshold(self.path, "s")                          # no change -> nothing appended
        with open(self.path, "rb") as fh:
            self.assertEqual(fh.read(), after)
        self._log("s2", [True])
        L.append(self.path, _reading("s-h1", "s", True))
        L.append(self.path, _reading("s-h2", "s", True))
        L.append(self.path, _reading("s-h3", "s", True))         # 3 misses, 3 hits -> 4
        self.assertEqual(L.sync_threshold(self.path, "s"), 4)
        changes = [e for e in L.read(self.path) if isinstance(e, L.ThresholdChange)]
        self.assertEqual([(c.old, c.new) for c in changes], [(2, 6), (6, 4)])

    def test_4b_notice_uses_sensor_threshold(self):
        reg = D.Registry(log_path=self.path)
        self._log("loop", [False, False, False])
        with self.assertRaises(D.DiscoveryError):
            reg.notice("same phrase again", 5, sensor="loop")
        self.assertEqual(reg.sensors["loop"].recurrence_threshold, 6)
        self.assertEqual(reg.notice("same phrase again", 6, sensor="loop").occurrences, 6)
        self.assertEqual(reg.notice("new signal", 2).occurrences, 2)   # no sensor: floor

    def test_4c_threshold_not_settable_by_hand(self):
        reg = D.Registry(log_path=self.path)
        with self.assertRaises(D.DiscoveryError):
            reg.register("x", recurrence_threshold=4)
        for bad in (1, 7, True, 2.0):
            with self.assertRaises(ValueError, msg=repr(bad)):
                S.Sensor(recurrence_threshold=bad)
        self.assertFalse(hasattr(D, "MIN_RECURRENCE"))

    def test_5_self_resolving_entry_rejected(self):
        L.append(self.path, _reading("a1", "s", None))
        with open(self.path, "rb") as fh:
            before = fh.read()
        with self.assertRaises(L.ResolutionError):
            L.append(self.path, _reading("b1", "s", True, resolves="b1"))
        with self.assertRaises(L.ResolutionError):
            L.append(self.path, _reading("c1", "s", True, resolves="later-entry"))
        with open(self.path, "rb") as fh:
            self.assertEqual(fh.read(), before)
        L.append(self.path, _reading("d1", "s", True, resolves="a1"))   # earlier target: accepted
        self.assertIs(L.resolved_state(L.read(self.path))["a1"], True)


if __name__ == "__main__":
    unittest.main(verbosity=1)
