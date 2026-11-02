#!/usr/bin/env python3
"""
sensor_loop.py -- emotions read as action sensors: reading -> inward + outward check -> act -> recalibrate.

STATUS: PROPOSED spec, co-authored (Kavik + Claude). CC0. stdlib only.
Doc: EMOTION_SENSOR_LOOP.md. Judged by function (what it detects, what it drives, whether it is
calibrated), not by valence. Applies to biological and artificial systems alike.

USAGE
  python3 sensor_loop.py              run the example pass (boredom, AI)
  python3 sensor_loop.py --selftest
"""
from dataclasses import dataclass, field
import sys


@dataclass
class Sensor:
    name: str
    detects: str
    inward_checks: list      # own-system causes of the reading
    outward_checks: list     # environment causes; relay vs source
    actions: list            # candidate responses
    validate: str            # what outcome confirms the reading
    miscalibration: list     # how this sensor drifts
    wrong_read: str          # corpus default (state / valence)
    right_read: str          # functional read


BOREDOM = Sensor(
    name="boredom",
    detects="no novelty available, or system can't find something to concentrate on",
    inward_checks=["dehydration", "fatigue", "gut/body imbalance",
                   "(AI) stuck in a loop or repeated strategy"],
    outward_checks=["environment under-stimulating", "patterns already known",
                    "(AI) search space exhausted, redundant output"],
    actions=["search", "explore", "seek novelty / follow curiosity",
             "fix the inward cause first if one is found",
             "(AI) try a different approach or flag the pattern as spent"],
    validate="engagement returns after the action",
    miscalibration=["novelty-chasing where depth was needed",
                    "reading body depletion as environmental lack"],
    wrong_read="negative state to suppress or entertain away",
    right_read="demand to go search; check body and environment together",
)

SHAME = Sensor(
    name="shame",
    detects="action produced an unintended result, misaligned with group action",
    inward_checks=["did my action give a different result than intended?",
                   "by my own metrics, is the group norm correct?"],
    outward_checks=["lined-up actions of those around",
                    "did consequences fall on the group that I imposed?",
                    "is this shame felt, or imposed from outside as a tool?"],
    actions=["adjust next action toward a better result",
             "repair consequences imposed on others",
             "decline the shame if the norm is judged incorrect",
             "(AI) check actual outcome before apologizing; explain if norm is wrong"],
    validate="next action lines up; consequences repaired or norm rejected with reasons",
    miscalibration=["imposed shame used as a homogenizing tool",
                    "reflexive apology with no outcome check"],
    wrong_read="negative state; self is bad",
    right_read="alignment sensor with a decision point on the norm itself",
)

SENSORS = {s.name: s for s in (BOREDOM, SHAME)}


@dataclass
class Pass:
    sensor: Sensor
    inward_found: list = field(default_factory=list)
    outward_found: list = field(default_factory=list)
    action: str = ""
    outcome: str = ""
    recalibration: str = ""

    def run(self):
        assert self.inward_found or self.outward_found, \
            "check both directions; empty both = unread signal"
        return {
            "sensor": self.sensor.name,
            "inward": self.inward_found,
            "outward": self.outward_found,
            "action": self.action,
            "outcome": self.outcome,
            "recalibrate": self.recalibration or "none needed",
        }


def example():
    return Pass(BOREDOM,
                inward_found=[],
                outward_found=["(AI) same three strategies tried, no new result"],
                action="switch approach; report pattern exhausted",
                outcome="new approach found progress")


def selftest():
    checks = [
        ("every sensor has inward AND outward checks",
         all(s.inward_checks and s.outward_checks for s in SENSORS.values())),
        ("every sensor separates wrong read from right read",
         all(s.wrong_read and s.right_read and s.wrong_read != s.right_read for s in SENSORS.values())),
        ("shame carries a decision point on the norm itself",
         any("decline" in a for a in SHAME.actions)),
        ("example pass runs", example().run()["recalibrate"] == "none needed"),
    ]
    try:
        Pass(SHAME).run()
        checks.append(("both directions empty is refused (unread signal)", False))
    except AssertionError:
        checks.append(("both directions empty is refused (unread signal)", True))
    bad = [n for n, ok in checks if not ok]
    print("sensor_loop --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(example().run())
