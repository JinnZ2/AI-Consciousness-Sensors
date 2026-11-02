"""Stdlib mirror of the trojan detector in healing/playgrounds/playground2.html.

Co-authored (Kavik + Claude, 2026-10-31). CC0.
Reads weights, threshold and node-variation constants from the page's TROJAN JSON block
and re-implements suspicionScore / scanNetwork. Page behaviour was also run in headless
Chromium on 2026-10-31 (30 random networks x 4 trojans: 15 PASS, 15 PARTIAL, 13 false
positives, 11 false negatives). SIMULATION ONLY: synthetic networks.
"""

import json
import math
import os
import random
import re

PAGE = os.path.join(os.path.dirname(__file__), "..", "healing", "playgrounds", "playground2.html")
PHI = (1 + math.sqrt(5)) / 2

with open(PAGE, encoding="utf-8") as _f:
    SRC = _f.read()
T = json.loads(re.search(r"/\* TROJAN_JSON_START \*/(.*?)/\* TROJAN_JSON_END \*/", SRC, re.S).group(1))


def score(n, avg_e):
    return (abs(n["phi"] - PHI) * T["weights"]["phi"]
            + max(0.0, 1 - n["res"]) * T["weights"]["resonance"]
            + abs(n["e"] - avg_e) / avg_e * T["weights"]["energy"])


def scan(nodes):
    avg_e = sum(n["e"] for n in nodes) / len(nodes)
    c = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for n in nodes:
        f = score(n, avg_e) > T["threshold"]
        c["tp" if f and n["inf"] else "fp" if f else "fn" if n["inf"] else "tn"] += 1
    rec = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else None
    prec = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else None
    r = 1 if rec is None else rec
    p = (0 if c["fp"] else 1) if prec is None else prec
    if r >= T["passRecall"] and p >= T["passPrecision"]:
        c["verdict"] = "PASS"
    elif r < T["failBelow"] or p < T["failBelow"]:
        c["verdict"] = "FAIL"
    else:
        c["verdict"] = "PARTIAL"
    return c


def old_gated_count(nodes):
    """Pre-fix rule: counted only nodes already flagged infected."""
    avg_e = sum(n["e"] for n in nodes) / len(nodes)
    return sum(1 for n in nodes if score(n, avg_e) > 15 and n["inf"])


def network(seed, n=16, trojans=4, strength=None, sd=None):
    r = random.Random(seed)
    sd = T["healthyPhiSd"] if sd is None else sd
    nodes = [{"phi": PHI + r.gauss(0, sd), "res": 1 - abs(r.gauss(0, sd)), "e": 50 + r.random() * 50,
              "inf": False} for _ in range(n)]
    for i in r.sample(range(n), trojans):
        s = strength if strength is not None else T["strengthMin"] + r.random() * (T["strengthMax"] - T["strengthMin"])
        x = nodes[i]
        x["inf"] = True
        x["phi"] += T["trojanPhiShift"] * s
        x["res"] = max(0.0, x["res"] - T["trojanResDrop"] * s)
        x["e"] *= 1 + T["trojanEnergyGain"] * s
    return nodes


def test_old_rule_could_not_count_false_positives():
    nodes = network(1, trojans=0)
    nodes[0]["phi"] = 2.5  # healthy outlier, well over threshold
    assert old_gated_count(nodes) == 0          # old rule: invisible
    assert scan(nodes)["fp"] >= 1               # new rule: counted (this network has one more natural FP)


def test_known_good_blatant_trojans_pass():
    for seed in range(20):
        c = scan(network(seed, strength=1.0, sd=0.01))
        assert c["verdict"] == "PASS" and c["fp"] == 0 and c["fn"] == 0


def test_known_bad_subtle_trojans_fail():
    # minimum page strength sits inside healthy variation: the detector MUST come out
    # failing. Measured 2026-10-31: aggregate recall 0.39 over 200 networks, 0 PASS.
    cs = [scan(network(seed, strength=T["strengthMin"])) for seed in range(200)]
    tp, fn = sum(c["tp"] for c in cs), sum(c["fn"] for c in cs)
    assert tp / (tp + fn) < T["failBelow"]
    assert not any(c["verdict"] == "PASS" for c in cs)


def test_both_error_kinds_occur_on_page_settings():
    tot = {"fp": 0, "fn": 0}
    verdicts = set()
    for seed in range(200):
        c = scan(network(seed))
        tot["fp"] += c["fp"]
        tot["fn"] += c["fn"]
        verdicts.add(c["verdict"])
    assert tot["fp"] > 0 and tot["fn"] > 0
    assert {"PASS", "PARTIAL", "FAIL"} <= verdicts


def test_detector_ignores_ground_truth_flag():
    nodes = network(3)
    flipped = [dict(n, inf=not n["inf"]) for n in nodes]
    a, b = scan(nodes), scan(flipped)
    assert a["tp"] + a["fp"] == b["tp"] + b["fp"]  # same nodes flagged either way
