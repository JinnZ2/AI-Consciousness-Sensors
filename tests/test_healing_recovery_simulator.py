"""Stdlib mirror of the scoring logic in healing/recovery/recovery-simulator.html.

Co-authored (2026-10-31). CC0.
Reads the protocol table and calibration from the page's JSON blocks, so the page and
this test cannot drift apart silently. Re-implements simulateRecovery / classifyOutcome
line for line; parity with the JS was checked by running the page's script under node
on 2026-10-31 (not part of CI). SIMULATION ONLY: not evidence about real models.
"""

import json
import os
import random
import re

PAGE = os.path.join(os.path.dirname(__file__), "..", "healing", "recovery", "recovery-simulator.html")
KEYS = ("phi", "energy", "resonance", "coherence")


def _page():
    with open(PAGE, encoding="utf-8") as f:
        return f.read()


def _block(src, name):
    m = re.search(r"/\* %s_JSON_START \*/(.*?)/\* %s_JSON_END \*/" % (name, name), src, re.S)
    return json.loads(m.group(1))


def load():
    src = _page()
    protocols = _block(src, "PROTOCOLS")
    sim = _block(src, "SIM")
    models = []
    for name, body in re.findall(r"name: '([^']+)',\s*severity: '[^']+',\s*symptoms: \{([^}]*)\}", src):
        sym = {k: float(v) for k, v in re.findall(r"(\w+):\s*([\d.]+)", body)}
        models.append({"name": name, "symptoms": sym})
    return protocols, sim, models


PROTOCOLS, SIM, MODELS = load()
BY_NAME = {p["name"]: p for p in PROTOCOLS}


def anchor_targets(p, tail0):
    a = p["anchor"]
    if a <= 0:
        return tail0, p["fitShift"]
    c = SIM["tailResidualGap"] if p["gapSelect"] else SIM["tailResidualRandom"]
    floor = tail0 * c * (1 - a)
    fit = SIM["fitAt10"] * min(a, 0.1) / 0.1 + (SIM["fitAtFull"] - SIM["fitAt10"]) * max(0.0, a - 0.1) / 0.9
    if p["gapSelect"]:
        fit += SIM["gapFitBonus"]
    return floor, fit + p["fitShift"]


def classify(cov0, cov, fit):
    if cov - cov0 < SIM["failCoverageGain"] or fit < 0:
        return "FAIL"
    if cov >= SIM["successCoverage"] and fit >= SIM["successFit"]:
        return "SUCCESS"
    return "PARTIAL"


def simulate(model, p, iterations=100, steps=50, noise=0.1, seed=0):
    rng = random.Random(seed)
    tail0 = sum(model["symptoms"][k] for k in KEYS) / 4
    cov0 = 1 - tail0
    counts = {"SUCCESS": 0, "PARTIAL": 0, "FAIL": 0}
    covs = []
    for _ in range(iterations):
        sym = dict(model["symptoms"])
        floor_t, fit_t = anchor_targets(p, tail0)
        jit = 1 + (rng.random() - 0.5) * noise
        floor = min(tail0, floor_t * jit) if p["anchor"] > 0 else tail0
        fit_target = fit_t * (1 + (rng.random() - 0.5) * noise)
        rate = SIM["stepRate"] * (1 + (rng.random() - 0.5) * noise)
        tail, fit = tail0, 0.0
        for step in range(steps):
            prog = 1 - (1 - rate) ** (step + 1)
            tail = floor + (tail0 - floor) * (1 - prog)
            fit = fit_target * prog
            for k in KEYS:
                eff = p["effectiveness"][k] * (1 + (rng.random() - 0.5) * noise)
                sym[k] = tail + max(0.0, sym[k] - tail) * (1 - eff)
        counts[classify(cov0, 1 - tail, fit)] += 1
        covs.append(1 - tail)
    outcome = max(("SUCCESS", "PARTIAL", "FAIL"), key=lambda k: (counts[k], k == "FAIL"))
    return {"outcome": outcome, "counts": counts, "cov0": cov0, "cov": sum(covs) / len(covs)}


def old_rule_success_rate(model, p, steps=10, noise=0.5, seed=0):
    """The pre-fix update rule, kept to show why it could not fail."""
    rng = random.Random(seed)
    ok = 0
    for _ in range(100):
        sym = dict(model["symptoms"])
        for _ in range(steps):
            for k in KEYS:
                sym[k] *= (1 - p["effectiveness"][k] * (1 + (rng.random() - 0.5) * noise))
            if 1 - sum(sym.values()) / 4 > 0.85:
                ok += 1
                break
    return ok


# ------------------------------------------------------------------ tests

def test_page_parses():
    assert len(PROTOCOLS) == 8 and len(MODELS) == 6


def test_old_rule_could_not_fail():
    # why the fix was needed: every model x original protocol "recovered" every time
    for m in MODELS:
        for p in PROTOCOLS[:5]:
            assert old_rule_success_rate(m, p) == 100


def test_known_bad_play_alone_fails():
    # toy run: play alone 0.49 -> 0.49. MUST fail; if this passes as success the fix is wrong
    for m in MODELS:
        r = simulate(m, BY_NAME["Resonance Through Play"])
        assert r["outcome"] == "FAIL"
        assert abs(r["cov"] - r["cov0"]) < 1e-9  # tails not recovered at all


def test_no_anchor_protocols_fail_across_settings():
    for steps, noise in ((10, 0.5), (50, 0.1), (200, 0.0)):
        for m in MODELS:
            for p in PROTOCOLS:
                if p["anchor"] == 0:
                    assert simulate(m, p, steps=steps, noise=noise)["outcome"] == "FAIL", p["name"]


def test_known_good_control_succeeds():
    for m in MODELS:
        assert simulate(m, BY_NAME["Real-Data Accumulation (control)"])["outcome"] == "SUCCESS"


def test_ten_percent_anchors_partial():
    # tails return cheaply, overall fit needs volume
    for name in ("Real-Data Anchor (10%, random)", "Gap-Seek + Real-Data Anchor (10%)"):
        for m in MODELS:
            r = simulate(m, BY_NAME[name])
            assert r["outcome"] == "PARTIAL", (name, m["name"])
            assert r["cov"] > 0.85


def test_ranking_separates_protocols():
    m = MODELS[0]
    cov = {n: simulate(m, BY_NAME[n])["cov"] for n in BY_NAME}
    assert (cov["Real-Data Accumulation (control)"] > cov["Gap-Seek + Real-Data Anchor (10%)"]
            > cov["Real-Data Anchor (10%, random)"] > cov["Resonance Through Play"])


def test_outcome_depends_on_steps():
    # too few steps: the control cannot finish recovering a critical model
    r = simulate(MODELS[0], BY_NAME["Real-Data Accumulation (control)"], steps=3, noise=0.0)
    assert r["outcome"] != "SUCCESS"
