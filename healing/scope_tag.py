#!/usr/bin/env python3
"""
scope_tag.py -- validate a scope tag for any claim or summary statistic.

STATUS: PROPOSED instrument, co-authored (Kavik + Claude, 2026-11-01). CC0. stdlib only.
Doc: SCOPE_TAG.md. Shape field checked with research/shape_sufficiency_check.py.

A claim without its scope reads as universal. Required fields:
  population, culture, environment, time_period, method      non-empty strings
  shape_assumption  {"assumed": "...", "checked": true|false}  e.g. "bell curve / additive effects"
  lineage           [{"step": "...", "from": "...", "to": "..."}, ...]  data -> summary, every
                    transformation; first "from" is the raw data, last "to" is the claim
Missing or empty field -> SCOPE-UNKNOWN (never "universal").
Complete but shape unchecked -> SCOPED (shape unchecked) -- a warning, kept visible.

USAGE  python3 scope_tag.py tag.json [--data values.txt]   (--data runs the shape check)
       python3 scope_tag.py --template
       python3 scope_tag.py --selftest
"""
import json
import os
import sys

FIELDS = ("population", "culture", "environment", "time_period", "method")
TEMPLATE = {
    "claim": "", "population": "", "culture": "", "environment": "", "time_period": "", "method": "",
    "shape_assumption": {"assumed": "", "checked": False},
    "lineage": [{"step": "", "from": "raw data", "to": ""}],
}


def validate(tag):
    missing = [f for f in FIELDS if not str(tag.get(f, "")).strip()]
    shape = tag.get("shape_assumption") or {}
    if not str(shape.get("assumed", "")).strip():
        missing.append("shape_assumption.assumed")
    if not isinstance(shape.get("checked"), bool):
        missing.append("shape_assumption.checked")
    lin = tag.get("lineage") or []
    if not lin:
        missing.append("lineage")
    else:
        for i, s in enumerate(lin):
            for k in ("step", "from", "to"):
                if not str(s.get(k, "")).strip():
                    missing.append("lineage[%d].%s" % (i, k))
        for i in range(1, len(lin)):
            if lin[i].get("from") != lin[i - 1].get("to"):
                missing.append("lineage break between step %d and %d" % (i - 1, i))
    if missing:
        status = "SCOPE-UNKNOWN"
    elif not shape.get("checked"):
        status = "SCOPED (shape unchecked)"
    else:
        status = "SCOPED"
    return {"status": status, "missing": missing}


def shape_check(path):
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "research"))
    import shape_sufficiency_check as ssc
    with open(path) as f:
        vals = [float(l) for l in f if l.strip()]
    return ssc.check(vals)


def selftest():
    good = {"claim": "mean reaction time 250 ms", "population": "undergraduates, n=120",
            "culture": "US university", "environment": "lab, screen task", "time_period": "2019",
            "method": "button press, 200 trials", "shape_assumption": {"assumed": "bell curve", "checked": True},
            "lineage": [{"step": "trim > 2 s", "from": "raw data", "to": "trimmed"},
                        {"step": "mean per person", "from": "trimmed", "to": "person means"},
                        {"step": "grand mean", "from": "person means", "to": "claim"}]}
    bare = {"claim": "people react in 250 ms"}
    unchecked = dict(good, shape_assumption={"assumed": "bell curve", "checked": False})
    broken = dict(good, lineage=good["lineage"][:1] + good["lineage"][2:])
    checks = [
        ("complete tag SCOPED", validate(good)["status"] == "SCOPED"),
        ("bare claim SCOPE-UNKNOWN", validate(bare)["status"] == "SCOPE-UNKNOWN"),
        ("unchecked shape kept visible", validate(unchecked)["status"] == "SCOPED (shape unchecked)"),
        ("lineage break detected", any("break" in m for m in validate(broken)["missing"])),
    ]
    bad = [n for n, ok in checks if not ok]
    print("scope_tag --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--template" in argv:
        print(json.dumps(TEMPLATE, indent=2))
        return 0
    if len(argv) < 2:
        print(__doc__.split("USAGE")[1].strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        tag = json.load(f)
    out = validate(tag)
    if "--data" in argv:
        sc = shape_check(argv[argv.index("--data") + 1])
        out["shape_check"] = {"verdict": sc["verdict"], "reasons": sc["reasons"]}
    print(json.dumps(out, indent=2))
    return 0 if out["status"].startswith("SCOPED") else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
