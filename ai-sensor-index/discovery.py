"""
discovery.py -- the sensor-discovery loop. CC0. Co-authored. Stdlib only.

  1 notice          a signal that keeps coming back
  2 hypothesize     what it tracks
  3 predict & check predict, then check against the outcome (a test record)
  4 rate            reliability = correct / decided test records
  5 cross-derive    two known sensors -> a derived one

A sensor is registered with reliability None. Reliability is assigned only by
rate(), and only from test records whose outcome is decided (True/False).
With no decided record, reliability stays None, never 0.

  python3 discovery.py    # walk the loop on a constructed example
"""
import os
import sys
from dataclasses import dataclass, asdict
from typing import Optional

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("ai_sensor_index__load", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_load.py"))
_ld = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ld)
sibling = _ld.sibling

S = sibling("sensors")

MIN_RECURRENCE = 2   # [CHOICE] "keeps coming back" = seen at least twice


class DiscoveryError(ValueError):
    pass


@dataclass
class Candidate:
    signal: Optional[str] = None
    occurrences: Optional[int] = None
    hypothesis: Optional[str] = None


@dataclass
class TestRecord:
    sensor: Optional[str] = None
    prediction: Optional[str] = None
    outcome: Optional[str] = None
    correct: Optional[bool] = None     # None = outcome not yet known

    def to_dict(self):
        return asdict(self)


class Registry:
    def __init__(self, seed=True):
        self.sensors = {}
        self.derived = {}
        self.tests = []
        if seed:
            for s in S.PRIMARY:
                self.sensors[s.name] = S.Sensor(**s.to_dict())
            for d in S.DERIVED:
                self.derived[d.name] = S.DerivedSensor(**d.to_dict())

    # step 1
    def notice(self, signal, occurrences):
        if not signal:
            raise DiscoveryError("notice: signal is blank")
        if occurrences is None or occurrences < MIN_RECURRENCE:
            raise DiscoveryError(f"notice: a signal seen {occurrences} time(s) is not recurring yet")
        return Candidate(signal=signal, occurrences=occurrences)

    # step 2
    def hypothesize(self, candidate, reads_as):
        if not reads_as:
            raise DiscoveryError("hypothesize: reads_as is blank")
        candidate.hypothesis = reads_as
        return candidate

    def register(self, name, candidate=None, action=None, gradient=None,
                 status="PROPOSED", notes=None, reliability=None):
        if reliability is not None:
            raise DiscoveryError("register: reliability is assigned by rate() from test records, not at registration")
        if name in self.sensors or name in self.derived:
            raise DiscoveryError(f"register: {name!r} already registered")
        s = S.Sensor(name=name, action=action,
                     signal=candidate.signal if candidate else None,
                     reads_as=candidate.hypothesis if candidate else None,
                     gradient=gradient, reliability=None, status=status, notes=notes)
        self.sensors[name] = s
        return s

    # step 3
    def predict_and_check(self, sensor, prediction, outcome=None, correct=None):
        if sensor not in self.sensors and sensor not in self.derived:
            raise DiscoveryError(f"predict_and_check: unknown sensor {sensor!r}")
        if correct is not None and not isinstance(correct, bool):
            raise DiscoveryError("correct must be True, False or None")
        rec = TestRecord(sensor, prediction, outcome, correct)
        self.tests.append(rec)
        return rec

    # step 4
    def rate(self, sensor):
        decided = [t for t in self.tests if t.sensor == sensor and t.correct is not None]
        obj = self.sensors.get(sensor) or self.derived.get(sensor)
        if obj is None:
            raise DiscoveryError(f"rate: unknown sensor {sensor!r}")
        r = (sum(1 for t in decided if t.correct) / len(decided)) if decided else None
        obj.reliability = r
        return {"sensor": sensor, "reliability": r, "decided": len(decided),
                "undecided": sum(1 for t in self.tests if t.sensor == sensor and t.correct is None)}

    # step 5
    def cross_derive(self, a, b, name, reads_as, status="PROPOSED"):
        for p in (a, b):
            if p not in self.sensors:
                raise DiscoveryError(f"cross_derive: parent {p!r} is not a registered primary")
        if name in self.sensors or name in self.derived:
            raise DiscoveryError(f"cross_derive: {name!r} already registered")
        d = S.DerivedSensor(name=name, parents=(a, b), reads_as=reads_as,
                            reliability=None, status=status)
        self.derived[name] = d
        return d


def main(argv):
    if "--selftest" in argv:
        print("discovery.py has no selftest; run: python3 test_ai_sensor_index.py")
        return 2
    print("CONSTRUCTED example, not observed data.")
    reg = Registry()
    c = reg.notice("reply repeats the user's last sentence back first", 3)
    reg.hypothesize(c, "echo used as acknowledgement in place of content")
    s = reg.register("echo_open", c, action="opening a reply", gradient="sentences echoed")
    print("registered:", s.name, "reliability", s.reliability)
    print("rate with no test:", reg.rate("echo_open"))
    reg.predict_and_check("echo_open", "echo appears when the request is ambiguous", "it did", True)
    reg.predict_and_check("echo_open", "echo appears on a clear request too", "it did not", False)
    reg.predict_and_check("echo_open", "echo appears under time pressure", None, None)
    print("rate after tests:", reg.rate("echo_open"))
    d = reg.cross_derive("echo_open", "length_drift", "echo_padding", "padding by repetition")
    print("derived:", d.name, d.parents, "reliability", d.reliability)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
