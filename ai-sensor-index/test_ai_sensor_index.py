"""Tests for ai-sensor-index. stdlib unittest; also collected by pytest.
Run: python3 test_ai_sensor_index.py"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _load import sibling  # noqa: E402

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


if __name__ == "__main__":
    unittest.main(verbosity=1)
