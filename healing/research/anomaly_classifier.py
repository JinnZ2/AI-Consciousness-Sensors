#!/usr/bin/env python3
"""
anomaly_classifier.py -- sort an anomaly: faulty anchor, baseline error, missing anchor, missing rule.

STATUS: PROPOSED instrument, co-authored (2026-11-01). CC0. stdlib only.
Toy results are mechanism demos, NOT evidence at scale. Doc: anomaly_classifier.md.
Prior art: PRIOR_ART.md (sensitivity analysis; measurement systematics; triangulation).

STEPS (in order)
  1 ANCHOR AUDIT  the anomaly measured against each anchor (calibrator / reference value).
                  Spread across anchors > K_SD * noise -> ANCHOR_IS_SOURCE (and which one).
  2 BASELINE      the anomaly against each independently computed baseline prediction.
                  Spread > K_SD * noise -> BASELINE (the prediction, not the world, moved).
  3 STAYS         a consistent nonzero anomaly. Fit ONE localized extra condition (a single
                  bump in the residual series). R^2 >= R2_LOCAL -> MISSING_ANCHOR (an
                  unmodelled condition, Neptune type); else MISSING_RULE (Mercury type).
  consistent ~0  -> NONE.
CONDITION (stated, and tested by case C): anchor swaps only discriminate when the anchors
  come from independent methods / calibration chains. Correlated anchors make an anchor bias
  look like a new rule.

USAGE  python3 anomaly_classifier.py              run the toy cases A-F
       python3 anomaly_classifier.py --selftest   (case C is EXPECTED to be misclassified)
"""
import math
import random
import sys

K_SD, R2_LOCAL, NOISE = 4.0, 0.9, 0.02


def spread(xs):
    return max(xs) - min(xs)


def fit_local_bump(t, r):
    """Best single Gaussian bump (centre, width scan; amplitude by least squares). R^2."""
    mean_r = sum(r) / len(r)
    ss_tot = sum((v - mean_r) ** 2 for v in r) or 1e-12
    best = 0.0
    for c in [t[0] + i * (t[-1] - t[0]) / 40 for i in range(41)]:
        for w in (0.02, 0.05, 0.1, 0.2):
            g = [math.exp(-((x - c) / (w * (t[-1] - t[0]))) ** 2) for x in t]
            gg = sum(v * v for v in g)
            if gg == 0:
                continue
            a = sum(v * y for v, y in zip(g, r)) / gg
            ss_res = sum((y - a * v) ** 2 for v, y in zip(g, r))
            best = max(best, 1 - ss_res / ss_tot)
    return best


def classify(per_anchor, per_baseline=None, residual_series=None, noise=NOISE):
    thr = K_SD * noise
    if spread(per_anchor) > thr:
        i = max(range(len(per_anchor)), key=lambda j: abs(per_anchor[j] - sorted(per_anchor)[len(per_anchor) // 2]))
        return {"label": "ANCHOR_IS_SOURCE", "anchor": i, "deviation_by_anchor": per_anchor}
    if per_baseline and spread(per_baseline) > thr:
        return {"label": "BASELINE", "deviation_by_baseline": per_baseline}
    level = sum(per_anchor) / len(per_anchor)
    if abs(level) <= thr:
        return {"label": "NONE", "deviation_by_anchor": per_anchor}
    if residual_series:
        t, r = residual_series
        r2 = fit_local_bump(t, r)
        return {"label": "MISSING_ANCHOR" if r2 >= R2_LOCAL else "MISSING_RULE",
                "local_fit_r2": round(r2, 3), "deviation_by_anchor": per_anchor}
    return {"label": "RULE_OR_REAL_EFFECT", "deviation_by_anchor": per_anchor}


def toy_cases(seed=1):
    rng = random.Random(seed)
    n = lambda: rng.gauss(0, NOISE / 2)  # noqa: E731
    t = [i / 99 for i in range(100)]
    bump = ([math.exp(-((x - 0.6) / 0.08) ** 2) * 0.8 + n() for x in t])          # one unseen body
    drift = ([0.8 * x + n() for x in t])                                            # secular, no locus
    return {
        "A one biased anchor (truth ANCHOR_IS_SOURCE)": ([0.0 + n(), 0.8 + n(), 0.0 + n()], None, None, "ANCHOR_IS_SOURCE"),
        "B real rule change (truth RULE)": ([0.8 + n(), 0.8 + n(), 0.8 + n()], None, None, "RULE_OR_REAL_EFFECT"),
        "C all anchors share one bias (truth ANCHOR_IS_SOURCE)": ([0.8 + n(), 0.8 + n(), 0.8 + n()], None, None, "ANCHOR_IS_SOURCE"),
        "D baseline recomputed (truth BASELINE)": ([0.8 + n()] * 3, [0.8 + n(), 0.0 + n()], None, "BASELINE"),
        "E unmodelled body (truth MISSING_ANCHOR)": ([0.8 + n()] * 3, None, (t, bump), "MISSING_ANCHOR"),
        "F secular drift, no locus (truth MISSING_RULE)": ([0.8 + n()] * 3, None, (t, drift), "MISSING_RULE"),
    }


def run():
    out = []
    for name, (pa, pb, rs, truth) in toy_cases().items():
        c = classify(pa, pb, rs)
        out.append((name, [round(x, 2) for x in pa], c["label"], truth, c["label"] == truth, c.get("local_fit_r2")))
    return out


def report(rows):
    print("ANOMALY CLASSIFIER -- toy, OBSERVED here, mechanism only")
    for name, pa, label, truth, ok, r2 in rows:
        print("%-52s anchors %-22s -> %-20s %s%s" % (name, pa, label, "correct" if ok else "WRONG",
                                                     "" if r2 is None else "  (local fit R^2 %.2f)" % r2))


def selftest():
    rows = {r[0][0]: r for r in run()}
    checks = [("A correct", rows["A"][4]), ("B correct", rows["B"][4]), ("D correct", rows["D"][4]),
              ("E correct", rows["E"][4]), ("F correct", rows["F"][4]),
              ("C is misclassified as a rule (required failure: correlated anchors)",
               rows["C"][2] == "RULE_OR_REAL_EFFECT" and not rows["C"][4])]
    bad = [n for n, ok in checks if not ok]
    print("anomaly_classifier --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    report(run())
