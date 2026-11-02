#!/usr/bin/env python3
"""
shape_balance.py -- score a profile by its balance across axes, not its average.

STATUS: PROPOSED instrument, co-authored (2026-11-01). CC0. stdlib only.
Doc: SHAPE_BALANCE.md.

AXES (default; any set of named axes works)
  tail_coverage | physical_grounding | non_events | scope_tagging | self_maintenance | deliberation
SCORES 0-1 per axis. An axis that was not measured is UNMEASURED, never 0 and never averaged in.
BALANCE  weakest / strongest (1.0 = even), plus spread (strongest - weakest).
VERDICT  PASS if every axis is measured, balance >= MIN_BALANCE and weakest >= FLOOR;
         FAIL otherwise -- a lopsided shape fails even with a high average.
OUTPUT   balance, spread, mean (reported, NOT used for the verdict), and a deviation map:
         per axis, deviation from the profile's own median, labelled BULGE / COLLAPSE / even.

USAGE  python3 shape_balance.py profile.json        {"tail_coverage": 0.8, ...}
       python3 shape_balance.py --selftest
"""
import json
import statistics
import sys

AXES = ("tail_coverage", "physical_grounding", "non_events", "scope_tagging",
        "self_maintenance", "deliberation")
MIN_BALANCE, FLOOR, DEV_MARK = 0.6, 0.4, 0.15


def score(profile, axes=AXES):
    measured = {a: float(profile[a]) for a in axes if profile.get(a) is not None}
    unmeasured = [a for a in axes if a not in measured]
    if not measured:
        return {"verdict": "UNMEASURED", "unmeasured": unmeasured}
    lo, hi = min(measured.values()), max(measured.values())
    med = statistics.median(measured.values())
    dev = {}
    for a, v in measured.items():
        d = v - med
        dev[a] = {"score": v, "deviation": round(d, 3),
                  "mark": "BULGE" if d > DEV_MARK else "COLLAPSE" if d < -DEV_MARK else "even"}
    balance = lo / hi if hi > 0 else 0.0
    reasons = []
    if unmeasured:
        reasons.append("unmeasured: " + ", ".join(unmeasured))
    if balance < MIN_BALANCE:
        reasons.append("balance %.2f < %.2f" % (balance, MIN_BALANCE))
    if lo < FLOOR:
        reasons.append("weakest axis %.2f < floor %.2f (%s)" % (lo, FLOOR, min(measured, key=measured.get)))
    return {"verdict": "FAIL" if reasons else "PASS", "reasons": reasons,
            "balance": round(balance, 3), "spread": round(hi - lo, 3),
            "mean_not_used": round(sum(measured.values()) / len(measured), 3),
            "deviation_map": dev, "unmeasured": unmeasured}


def selftest():
    lopsided = {"tail_coverage": 1.0, "physical_grounding": 1.0, "non_events": 1.0, "scope_tagging": 1.0,
                "self_maintenance": 0.95, "deliberation": 0.1}       # mean 0.84
    balanced = {a: 0.6 for a in AXES}                                 # mean 0.60
    balanced["deliberation"] = 0.55
    partial = dict(balanced)
    partial.pop("non_events")
    lo, ba, pa = score(lopsided), score(balanced), score(partial)
    checks = [
        ("high-average lopsided FAILS", lo["verdict"] == "FAIL" and lo["mean_not_used"] > ba["mean_not_used"]),
        ("balanced moderate PASSES", ba["verdict"] == "PASS"),
        ("collapsed axis named", lo["deviation_map"]["deliberation"]["mark"] == "COLLAPSE"),
        ("missing axis is UNMEASURED, not 0", "non_events" in pa["unmeasured"] and pa["verdict"] == "FAIL"),
    ]
    bad = [n for n, ok in checks if not ok]
    print("shape_balance --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) < 2:
        print(__doc__.split("USAGE")[1].strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        prof = json.load(f)
    print(json.dumps(score(prof, tuple(prof) if "--any-axes" in argv else AXES), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
