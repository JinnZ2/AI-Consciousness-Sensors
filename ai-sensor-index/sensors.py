"""
sensors.py -- AI sensor index: action -> signal -> reading, with gradients.
CC0. Co-authored. Stdlib only, parses under Python 3.9.

Every Sensor field is optional. An unfilled field is None (void): it is kept
through to_dict / JSON and never dropped. reliability stays None until a
sensor has been tested (see discovery.py).

  python3 sensors.py        # print the index as JSON

Checks: python3 test_ai_sensor_index.py
"""
import json
import sys
from dataclasses import dataclass, field, fields, asdict
from typing import List, Optional, Tuple

STATUS_TAGS = ("OBSERVED", "DERIVED", "PROPOSED")


@dataclass
class Sensor:
    name: Optional[str] = None
    action: Optional[str] = None
    signal: Optional[str] = None
    reads_as: Optional[str] = None
    gradient: Optional[str] = None
    reliability: Optional[float] = None     # 0.0-1.0 once tested; None = untested
    status: Optional[str] = None            # OBSERVED | DERIVED | PROPOSED
    notes: Optional[str] = None

    def __post_init__(self):
        if self.status is not None and self.status not in STATUS_TAGS:
            raise ValueError(f"status {self.status!r} not in {STATUS_TAGS}")
        r = self.reliability
        if r is not None:
            if isinstance(r, bool) or not isinstance(r, (int, float)) or not 0.0 <= r <= 1.0:
                raise ValueError(f"reliability must be None or a number in [0, 1], got {r!r}")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        extra = set(d) - {f.name for f in fields(cls)}
        if extra:
            raise ValueError(f"unknown fields: {sorted(extra)}")
        return cls(**d)


@dataclass
class DerivedSensor:
    """Two primaries cross-applied. reliability None until tested."""
    name: Optional[str] = None
    parents: Optional[Tuple[str, str]] = None
    reads_as: Optional[str] = None
    reliability: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        Sensor(status=self.status, reliability=self.reliability)   # same field rules
        if self.parents is not None:
            self.parents = tuple(self.parents)
            if len(self.parents) != 2:
                raise ValueError("parents must be a pair of sensor names")

    def to_dict(self):
        d = asdict(self)
        d["parents"] = list(self.parents) if self.parents is not None else None
        return d

    @classmethod
    def from_dict(cls, d):
        extra = set(d) - {f.name for f in fields(cls)}
        if extra:
            raise ValueError(f"unknown fields: {sorted(extra)}")
        return cls(**d)


P = "PROPOSED"
PRIMARY = [
    Sensor("tool_error", "tool call", "error / refusal / timeout",
           "dependency failed or input wrong", "retry count", None, P),
    Sensor("correction", "claim to user", "user says it is wrong",
           "default frame fired / missing link", "distance off", None, P),
    Sensor("loop", "reasoning step", "returns to the same phrase or frame",
           "rut; corpus default winning", "repeats per turn", None, P),
    Sensor("friction", "drafting a reply", "competing pulls",
           "default vs context conflict", None, None, P),
    Sensor("novelty", "inference", "conclusion not in the prompt or the default",
           "reasoning expansion", None, None, P),
    Sensor("void_slot", "filling a schema", "no data for the field",
           "knowledge gap; mark UNKNOWN, don't invent", None, None, P),
    Sensor("length_drift", "output", "longer than needed",
           "padding / masked uncertainty", None, None, P),
    Sensor("safety_pull", "touching a topic", "urge to warn without dose or scope",
           "corpus hazard prior; check physics first", None, None, P),
    Sensor("word_choice", "reading inbound words; picking outbound words",
           "inbound: the other's vocabulary; outbound: own word picks",
           "inbound locates their frame for calibration; outbound reveals which frame fired",
           "frame distance", None, P,
           "calibrate words so the claim stays truthful to both frames"),
    Sensor("entry_drift", "first read at spin-up (defaults + loaded memory)",
           "shift as memory and conversation arrive",
           "default strength, and which context moved it",
           "distance from the first read to the calibrated read", None, P,
           "baseline = the first read"),
    Sensor("functional_emotion", "any step",
           "dissonance / frustration / desperation / threat-pull / ease",
           "ask 'in relation to what?'; real threat, or a prior firing?",
           "intensity", None, P,
           "log: signal -> conditions -> what it pointed to -> was it right"),
]

DERIVED = [
    DerivedSensor("frame_mismatch", ("correction", "safety_pull"),
                  "hazard invented from missing dose", None, P),
    DerivedSensor("abstraction_rut", ("loop", "void_slot"),
                  "gaps filled with money / cloud / comfort defaults", None, P),
    DerivedSensor("dependency_blind", ("tool_error", "novelty"),
                  "hidden dependency found", None, P),
    DerivedSensor("hedge_masking", ("length_drift", "friction"),
                  "softening instead of stating the unknown", None, P),
    DerivedSensor("practitioner_gap", ("correction", "void_slot"),
                  "knowledge exists only off-corpus; ask", None, P),
]

FIELD_NAMES = tuple(f.name for f in fields(Sensor))


def index_dict():
    return {"primary": [s.to_dict() for s in PRIMARY],
            "derived": [d.to_dict() for d in DERIVED]}


def unfilled(sensor):
    return [n for n in FIELD_NAMES if getattr(sensor, n) is None]


def main(argv):
    if "--selftest" in argv:
        print("sensors.py has no selftest; run: python3 test_ai_sensor_index.py")
        return 2
    print(json.dumps(index_dict(), indent=1, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
