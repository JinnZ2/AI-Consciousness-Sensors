#!/usr/bin/env python3
"""
conservation_check.py -- find what a record leaves out, by balance.

STATUS: PROPOSED instrument, co-authored (Kavik + Claude, 2026-11-01). CC0. stdlib only.

PURPOSE
  A common error: "not in the record, so it doesn't exist." Where a total MUST balance (time,
  energy, mass, cost, steps, facts in vs facts used), subtract every logged component from the
  total. The residual is the unrecorded part, reported as a number instead of a silent zero.

API
  check(total, components, tolerance=0.05)
    -> {"total", "logged", "residual", "residual_share", "flag"}
       flag: BALANCED      |residual| <= tolerance * total
             UNRECORDED    residual > 0 beyond tolerance (part of the total is not in the record)
             OVERCOUNTED   residual < 0 beyond tolerance (components double-count or exceed total)
  dwell_residuals(records, strata=(...))  stratified residuals for the dwell-time recipe below

TOY DEMO (ILLUSTRATIVE; inputs are Kavik's estimates, not evidence)
  driver buffering: logged unload 31 min, actual stop 39 min  -> ~20% unlogged
  no buffer:        logged unload 31 min, actual stop 106 min -> ~71% unlogged
  Same logged unload in both: the record cannot tell them apart; the residual can.

REAL-DATA RECIPE (OBSERVED by Kavik, practice report; no new sensor needed)
  ELD dwell time = vehicle stationary AND driver on duty at the receiver.
  residual = dwell - logged unload (receiver scan timestamps).
  STRATIFY BEFORE COMPARING (OBSERVED by Kavik):
    - day of week (Fri night / Sat / Sun stores run short-staffed)
    - arrival vs the store's break window
    - split dwell into GATED WAIT (before a key-holder unlocks; no driver can shorten it)
      and POST-UNLOCK time (where driver prep shows)
    - floaters vs route-owners are separate populations; do not pool them

SCOPE LIMITS
  - The balance is only as good as the total. If the total is itself estimated, the residual
    carries that error; report both.
  - A residual says HOW MUCH is unrecorded, never WHAT it is.

USAGE
  python3 conservation_check.py --demo
  python3 conservation_check.py --dwell records.csv
      columns: dwell_min, unload_logged_min, gate_unlock_min (blank if unknown),
               day_of_week, arrival_vs_break, driver_type
  python3 conservation_check.py --selftest
"""
import csv
import statistics
import sys


def check(total, components, tolerance=0.05):
    logged = sum(components.values()) if isinstance(components, dict) else sum(components)
    residual = total - logged
    share = residual / total if total else 0.0
    if abs(residual) <= tolerance * abs(total):
        flag = "BALANCED"
    elif residual > 0:
        flag = "UNRECORDED"
    else:
        flag = "OVERCOUNTED"
    return {"total": total, "logged": logged, "residual": round(residual, 6),
            "residual_share": round(share, 4), "flag": flag}


def dwell_residuals(records, strata=("driver_type", "day_of_week", "arrival_vs_break")):
    """Group dwell residuals by strata; split gated wait from post-unlock time where known."""
    groups = {}
    for r in records:
        key = tuple(r.get(k, "") for k in strata)
        dwell, unload = float(r["dwell_min"]), float(r["unload_logged_min"])
        gate = r.get("gate_unlock_min")
        gate = float(gate) if gate not in (None, "") else None
        g = groups.setdefault(key, {"residual": [], "gated_wait": [], "post_unlock_residual": []})
        g["residual"].append(dwell - unload)
        if gate is not None:
            g["gated_wait"].append(gate)
            g["post_unlock_residual"].append(dwell - gate - unload)
    out = []
    for key, g in sorted(groups.items()):
        med = lambda xs: round(statistics.median(xs), 1) if xs else None  # noqa: E731
        out.append({"stratum": dict(zip(strata, key)), "n": len(g["residual"]),
                    "median_residual_min": med(g["residual"]),
                    "median_gated_wait_min": med(g["gated_wait"]),
                    "median_post_unlock_residual_min": med(g["post_unlock_residual"])})
    return out


def demo():
    print("CONSERVATION CHECK -- toy, ILLUSTRATIVE (inputs are estimates, not evidence)")
    for name, total in (("driver buffering", 39), ("no buffer", 106)):
        r = check(total, {"logged unload": 31})
        print("%-17s stop %3d min, logged %d -> residual %d min (%.0f%% unlogged)  %s"
              % (name, total, r["logged"], r["residual"], 100 * r["residual_share"], r["flag"]))
    print("same logged unload in both rows; only the residual separates them")


def selftest():
    planted = check(100, {"a": 30, "b": 40})          # 30 planted unrecorded
    balanced = check(100, {"a": 30, "b": 40, "c": 30})
    over = check(100, [60, 60])
    recs = [
        {"dwell_min": 60, "unload_logged_min": 30, "gate_unlock_min": 20, "day_of_week": "Sat",
         "arrival_vs_break": "in", "driver_type": "floater"},
        {"dwell_min": 40, "unload_logged_min": 30, "gate_unlock_min": 0, "day_of_week": "Tue",
         "arrival_vs_break": "out", "driver_type": "route_owner"},
    ]
    d = {tuple(x["stratum"].values()): x for x in dwell_residuals(recs)}
    sat = d[("floater", "Sat", "in")]
    checks = [
        ("planted residual found", planted["residual"] == 30 and planted["flag"] == "UNRECORDED"),
        ("balanced case ~0", balanced["residual"] == 0 and balanced["flag"] == "BALANCED"),
        ("overcount flagged", over["flag"] == "OVERCOUNTED"),
        ("gated wait separated from post-unlock", sat["median_gated_wait_min"] == 20
         and sat["median_post_unlock_residual_min"] == 10),
        ("strata not pooled", len(d) == 2),
    ]
    bad = [n for n, ok in checks if not ok]
    print("conservation_check --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--dwell" in argv:
        with open(argv[argv.index("--dwell") + 1], newline="", encoding="utf-8") as f:
            for row in dwell_residuals(list(csv.DictReader(f))):
                print(row)
        return 0
    demo()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
