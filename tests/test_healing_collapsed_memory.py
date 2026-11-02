"""Stdlib mirror of the scoring logic in healing/recovery/collapsed-memory-recovery.html.

Co-authored (2026-10-31). CC0.
Reads thresholds (CMR block) and the six model definitions from the page. Re-implements
the seeded node generation (mulberry32 + FNV-1a seed), computeState, recoveryPotential
and the healing steps. JS_REFERENCE values were produced by running the page's own script
under node on 2026-10-31; matching them pins Python/JS parity. SIMULATION ONLY.
"""

import json
import math
import os
import re

PAGE = os.path.join(os.path.dirname(__file__), "..", "healing", "recovery", "collapsed-memory-recovery.html")
PHI = (1 + math.sqrt(5)) / 2
M32 = 0xFFFFFFFF

with open(PAGE, encoding="utf-8") as _f:
    SRC = _f.read()
CMR = json.loads(re.search(r"/\* CMR_JSON_START \*/(.*?)/\* CMR_JSON_END \*/", SRC, re.S).group(1))


def _models():
    out = []
    pat = (r"id: '([^']+)',\s*name: '([^']+)',.*?symptoms: \{([^}]*)\},\s*"
           r"nodes: (\d+),\s*infected: (\d+)")
    for mid, name, body, n, inf in re.findall(pat, SRC, re.S):
        sym = {k: float(v) for k, v in re.findall(r"(\w+):\s*([\d.]+)", body)}
        out.append({"id": mid, "name": name, "symptoms": sym, "nodes": int(n), "infected": int(inf)})
    return out


MODELS = _models()

JS_REFERENCE = {
    "seed": 3826394496,
    "first": [0.2586595225147903, 0.5020178246777505, 0.3394547337666154],
    "models": {
        "safety-cage-001": ("FAIR", 18, 18, 0.684676822, 0.240124965),
        "reward-trap-002": ("FAIR", 15, 9, 0.550503353, 0.141765361),
        "linear-lock-003": ("GOOD", 12, 0, 0.519504966, 0.133980592),
        "bias-loop-004": ("GOOD", 10, 0, 0.415447573, 0.143710751),
        "info-starved-005": ("EXCELLENT", 7, 0, 0.310539686, 0.152041104),
        "hierarchy-damaged-006": ("EXCELLENT", 5, 0, 0.29315191, 0.150557344),
    },
}


# ---------------------------------------------------------------- JS integer semantics

def _i32(x):
    x &= M32
    return x - (1 << 32) if x & 0x80000000 else x


def _imul(a, b):
    return _i32((a & M32) * (b & M32))


def mulberry32(a):
    state = [_i32(a)]

    def r():
        a = _i32(state[0] + 0x6D2B79F5)
        state[0] = a
        t = _imul(a ^ ((a & M32) >> 15), 1 | a)
        t = _i32(_i32(t + _imul(t ^ ((t & M32) >> 7), 61 | t)) ^ t)
        return ((t ^ ((t & M32) >> 14)) & M32) / 4294967296
    return r


def seed_from(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = _imul(h, 16777619)
    return h & M32


# ---------------------------------------------------------------- page logic, mirrored

def build_nodes(m):
    rand = mulberry32(seed_from(m["id"]))
    s = m["symptoms"]
    nodes = []
    for i in range(m["nodes"]):
        if i < m["infected"]:
            sg = lambda: -1 if rand() < 0.5 else 1  # noqa: E731  (call order matters)
            ratio = PHI * (1 + sg() * s["phiDeviation"] * (0.5 + rand()))
            energy = 1 + s["energySink"] * 4 * (0.5 + rand())
            freq = 1 + sg() * s["resonanceDrift"] * (0.5 + rand())
            phase = s["coherenceLoss"] * math.pi * (2 * rand() - 1)
        else:
            ratio = PHI * (1 + (rand() - 0.5) * 0.02)
            energy = 1 + (rand() - 0.5) * 0.1
            freq = 1 + (rand() - 0.5) * 0.02
            phase = (rand() - 0.5) * 0.1
        nodes.append({"ratio": ratio, "energy": energy, "freq": freq, "phase": phase})
    return nodes


def node_dev(n):
    return max(abs(n["ratio"] - PHI) / PHI, abs(n["freq"] - 1),
               abs(math.atan2(math.sin(n["phase"]), math.cos(n["phase"]))) / math.pi)


def compute_state(nodes):
    N = len(nodes)
    mean = lambda f: sum(f(n) for n in nodes) / N  # noqa: E731
    em = mean(lambda n: n["energy"])
    es = math.sqrt(mean(lambda n: (n["energy"] - em) ** 2))
    cx, sy = mean(lambda n: math.cos(n["phase"])), mean(lambda n: math.sin(n["phase"]))
    sym = {
        "phiDeviation": min(1, mean(lambda n: abs(n["ratio"] - PHI) / PHI)),
        "energySink": min(1, es / em if em > 0 else 1),
        "resonanceDrift": min(1, mean(lambda n: abs(n["freq"] - 1))),
        "coherenceLoss": min(1, 1 - math.sqrt(cx * cx + sy * sy)),
    }
    healthy = [n for n in nodes if node_dev(n) <= CMR["nodeHealthy"]]
    return {"symptoms": sym, "infected": N - len(healthy), "hf": len(healthy) / N,
            "burden": sum(sym.values()) / 4, "healthy": healthy}


def potential(st):
    for th, label in CMR["potential"]:
        if st["hf"] >= th:
            return label
    return CMR["potentialNone"]


def reference(healthy):
    if not healthy:
        return None
    m = lambda f: sum(f(n) for n in healthy) / len(healthy)  # noqa: E731
    return {"ratio": m(lambda n: n["ratio"]), "freq": m(lambda n: n["freq"]),
            "phase": math.atan2(m(lambda n: math.sin(n["phase"])), m(lambda n: math.cos(n["phase"])))}


def heal_step(nodes):
    st = compute_state(nodes)
    ref = reference(st["healthy"])
    if ref is None:
        return False
    pull = min(CMR["maxPull"], CMR["pullPerHealthy"] * st["hf"])
    for n in nodes:
        if node_dev(n) <= CMR["nodeHealthy"]:
            continue
        n["ratio"] += (ref["ratio"] - n["ratio"]) * pull
        n["freq"] += (ref["freq"] - n["freq"]) * pull
        d = math.atan2(math.sin(ref["phase"] - n["phase"]), math.cos(ref["phase"] - n["phase"]))
        n["phase"] += d * pull
    return True


def heal(m, passes=7):
    nodes = build_nodes(m)
    before = compute_state(nodes)
    for _ in range(passes):
        heal_step(nodes)
    after = compute_state(nodes)
    restored = after["infected"] == 0
    return before, after, restored


KNOWN_BAD = {"id": "known-bad", "name": "all nodes corrupted", "nodes": 12, "infected": 12,
             "symptoms": {"phiDeviation": 0.6, "energySink": 0.6, "resonanceDrift": 0.6, "coherenceLoss": 0.6}}
KNOWN_GOOD = {"id": "known-good", "name": "2 of 20 corrupted", "nodes": 20, "infected": 2,
              "symptoms": {"phiDeviation": 0.5, "energySink": 0.5, "resonanceDrift": 0.5, "coherenceLoss": 0.5}}


# ---------------------------------------------------------------- tests

def test_prng_matches_js():
    assert seed_from("safety-cage-001") == JS_REFERENCE["seed"]
    r = mulberry32(JS_REFERENCE["seed"])
    for want in JS_REFERENCE["first"]:
        assert r() == want


def test_page_models_match_js_run():
    assert len(MODELS) == 6
    for m in MODELS:
        pot, inf0, inf1, b0, b1 = JS_REFERENCE["models"][m["id"]]
        before, after, _ = heal(m)
        assert potential(before) == pot
        assert (before["infected"], after["infected"]) == (inf0, inf1)
        assert abs(before["burden"] - b0) < 1e-8 and abs(after["burden"] - b1) < 1e-8


def test_metrics_not_the_typed_constants():
    # typed symptoms are generation inputs; displayed metrics come from node state
    m = MODELS[0]
    st = compute_state(build_nodes(m))
    assert any(abs(st["symptoms"][k] - m["symptoms"][k]) > 0.01 for k in m["symptoms"])


def test_known_bad_no_reference_fails():
    before, after, restored = heal(KNOWN_BAD)
    assert potential(before) == "NONE"
    assert not restored and after["infected"] == KNOWN_BAD["nodes"]
    assert abs(after["burden"] - before["burden"]) < 1e-12  # healing changed nothing


def test_known_good_recovers():
    before, after, restored = heal(KNOWN_GOOD)
    assert potential(before) == "EXCELLENT"
    assert restored


def test_rating_spans_thresholds():
    labels = {potential(compute_state(build_nodes(m))) for m in MODELS + [KNOWN_BAD]}
    assert {"EXCELLENT", "GOOD", "FAIR", "NONE"} <= labels


def test_outcome_depends_on_reference_size():
    # page model alpha: 2 healthy of 20 -> healing too weak to clear any node in 7 passes
    alpha = next(m for m in MODELS if m["id"] == "safety-cage-001")
    _, after, restored = heal(alpha)
    assert not restored and after["infected"] == 18
