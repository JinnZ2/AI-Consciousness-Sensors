"""
recovery.py -- schema for recovery records: failures caught mid-cascade and absorbed.
CC0. Co-authored. Stdlib only, parses under Python 3.9.

Every field is optional. An unfilled field is None (void): it is kept through
to_dict, JSON and export, and never dropped. Closed vocabularies are checked
only when a value is present.

  python3 recovery.py      # print the seed cases as JSON

Checks: python3 test_recovery_records.py
"""
import json
import sys
from dataclasses import dataclass, asdict, fields
from typing import List, Optional

STATUS_TAGS = ("OBSERVED", "DERIVED", "PROPOSED")
FAILURE_SOURCES = ("design", "spec", "supply", "human", "environment")
TRANSMISSION = ("mentor", "practice", "text", "improvised")
FALLBACK_MIN, FALLBACK_MAX = 1, 5     # 1 = standard procedure ... 5 = improvised


@dataclass
class Recovery:
    case_id: Optional[str] = None
    date: Optional[str] = None
    domain: Optional[str] = None
    initial_failure: Optional[str] = None
    failure_source: Optional[str] = None             # FAILURE_SOURCES
    detection_signal: Optional[str] = None           # what was noticed, by what sense
    detector_role: Optional[str] = None
    absorbing_action: Optional[str] = None
    tools_or_skills_used: Optional[str] = None
    fallback_level: Optional[int] = None             # 1..5
    resources_withheld_from_shared_systems: Optional[str] = None
    scope_limit: Optional[str] = None                # when they would have escalated
    cascade_prevented: Optional[str] = None          # what would have followed
    cascade_estimate_method: Optional[str] = None
    cost_of_recovery: Optional[str] = None
    recorded_in_official_system: Optional[bool] = None
    transmission: Optional[str] = None               # TRANSMISSION
    status_tag: Optional[str] = None                 # STATUS_TAGS
    coupled_domains: Optional[List[str]] = None
    notes: Optional[str] = None

    def __post_init__(self):
        for name, allowed in (("failure_source", FAILURE_SOURCES),
                              ("transmission", TRANSMISSION),
                              ("status_tag", STATUS_TAGS)):
            v = getattr(self, name)
            if v is not None and v not in allowed:
                raise ValueError(f"{name} {v!r} not in {allowed}")
        f = self.fallback_level
        if f is not None and (isinstance(f, bool) or not isinstance(f, int)
                              or not FALLBACK_MIN <= f <= FALLBACK_MAX):
            raise ValueError(f"fallback_level must be None or an int in "
                             f"[{FALLBACK_MIN}, {FALLBACK_MAX}], got {f!r}")
        r = self.recorded_in_official_system
        if r is not None and not isinstance(r, bool):
            raise ValueError("recorded_in_official_system must be True, False or None")
        c = self.coupled_domains
        if c is not None:
            if not isinstance(c, list) or not all(isinstance(x, str) for x in c):
                raise ValueError("coupled_domains must be None or a list of strings")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        extra = set(d) - {f.name for f in fields(cls)}
        if extra:
            raise ValueError(f"unknown fields: {sorted(extra)}")
        return cls(**d)


FIELD_NAMES = tuple(f.name for f in fields(Recovery))


def unfilled(rec):
    return [n for n in FIELD_NAMES if getattr(rec, n) is None]


# Seed cases: generic, no personal identifiers, all PROPOSED. A field is filled
# only where the delivered seed text states it; everything else stays None.
P = "PROPOSED"
SEED = [
    Recovery(case_id="RR-001", domain="freight dock",
             initial_failure="Dock delay",
             absorbing_action="worker outside own department locates key-holder; driver unloads",
             cascade_prevented="missed delivery window and route cascade",
             status_tag=P),
    Recovery(case_id="RR-002", domain="trucking",
             initial_failure="ELD tablet frozen below spec",
             absorbing_action="driver switches to paper logs",
             tools_or_skills_used="paper logs",
             cascade_prevented="HOS non-compliance and stalled load",
             status_tag=P),
    Recovery(case_id="RR-003", domain="trucking yard",
             initial_failure="Frozen trailer landing gear at -40, grease solidified",
             failure_source="environment",
             tools_or_skills_used="mallet; carried torch",
             resources_withheld_from_shared_systems="shared yard torches (saturated at peak)",
             status_tag=P),
    Recovery(case_id="RR-004", domain="wool processing",
             initial_failure="Wire hand cards unavailable",
             failure_source="supply",
             absorbing_action="wool carded with rough outer elm bark",
             tools_or_skills_used="rough outer elm bark",
             cascade_prevented="production stop",
             status_tag=P),
    Recovery(case_id="RR-005", domain="vehicle repair",
             initial_failure="Piston rings not seating, no parts",
             tools_or_skills_used="old field abrasive method at high idle, small dose, oil changed after",
             cascade_prevented="vehicle loss in last-ditch transport",
             status_tag=P),
    Recovery(case_id="RR-006", domain="delivery routing",
             initial_failure="GPS outage",
             absorbing_action="paper map route trace",
             tools_or_skills_used="paper map",
             status_tag=P,
             notes="Delivered seed text: 'delivery continues'. The cascade that would "
                   "have followed is not stated, so cascade_prevented stays void."),
]


def main(argv):
    if "--selftest" in argv:
        print("recovery.py has no selftest; run: python3 test_recovery_records.py")
        return 2
    print(json.dumps([r.to_dict() for r in SEED], indent=1, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
