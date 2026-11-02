#!/usr/bin/env python3
"""
shape_sufficiency_check.py -- are mean + spread a sufficient summary, or is a bell curve assumed?

STATUS: PROPOSED instrument, co-authored (Kavik + Claude, 2026-11-01). CC0. stdlib only.
Toy results are mechanism demos. Prior art: PRIOR_ART.md (Micceri 1989; Quetelet; Daniels 1952).

WHY: a bell curve arises under one condition -- many small independent ADDED effects (central
limit theorem). The shape is a fingerprint of the generating process: multiplied effects ->
skewed / log-normal; feedback -> power law; mixed groups -> several peaks. A mean and a
standard deviation only describe the first case well.

CHECKS (each compared with what a normal distribution gives)
  skew                 normal 0
  excess kurtosis      normal 0
  tail mass > 3 sd     normal 0.27%  -> reported as a ratio
  share within 0.25 sd normal 19.7%  -> how much data sits near the mean
  peak count           direct count on a smoothed histogram (1st-99th percentile)
  bimodality coeff.    reported, NOT used for the verdict: it falsely flags extreme skew
VERDICT: SUFFICIENT only if |skew| < 0.5, |excess kurtosis| < 1, tail ratio < 2, one peak,
  near-mean share within 0.75-1.25x normal; otherwise NOT SUFFICIENT with the reasons.

RESULTS (OBSERVED, toy, this file, 2026-11-01; n = 20000 each)
  added       SUFFICIENT      skew 0.01, ex.kurt -0.03, tails 0.8x, 19.9% near mean, 1 peak
  multiplied  NOT SUFFICIENT  skew 4.72, ex.kurt 42, tails 6.5x
  mixed       NOT SUFFICIENT  2 peaks, 3.2% near the mean (normal 19.7%)
  Pareto 1.5  NOT SUFFICIENT  skew 36, ex.kurt 1689
  FAILURES recorded:
    - bimodality coefficient says "multimodal" for Pareto (BC 0.76): it breaks under extreme
      skew, so the verdict uses the direct peak count (1 peak), never BC alone.
    - tail-mass check reads only 1.6x normal for Pareto: with infinite variance the extreme
      values inflate the sd, so "beyond 3 sd" undercounts the heaviest tails. The tail check
      alone would PASS this set; skew and kurtosis catch it.
  Earlier first run (Kavik + Claude, other code): added sufficient; multiplied tails 6x;
  mixed 2 peaks, 2% near mean; Pareto extreme skew; BC false flag on Pareto. Same pattern.

Prior cases (DOCUMENTED; VERIFY details): Micceri 1989 found all 440 large achievement and
psychometric distributions he examined significantly non-normal; Daniels 1952 (USAF) found none
of 4,063 airmen within the middle band on all ten body dimensions used for cockpit design.

USAGE  python3 shape_sufficiency_check.py values.txt       one number per line
       python3 shape_sufficiency_check.py --demo           toy generating processes
       python3 shape_sufficiency_check.py --selftest
"""
import math
import random
import sys

NORMAL_TAIL3 = 0.0027
NORMAL_NEAR = 0.1974   # P(|z| < 0.25)


def moments(x):
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    m2 = sum(v * v for v in d) / n
    m3 = sum(v ** 3 for v in d) / n
    m4 = sum(v ** 4 for v in d) / n
    sd = math.sqrt(m2)
    return m, sd, (m3 / sd ** 3 if sd else 0.0), (m4 / m2 ** 2 - 3 if m2 else 0.0)


def peak_count(x, bins=40):
    s = sorted(x)
    lo, hi = s[int(0.01 * len(s))], s[int(0.99 * len(s)) - 1]
    if hi <= lo:
        return 1
    h = [0] * bins
    for v in s:
        if lo <= v <= hi:
            h[min(bins - 1, int((v - lo) / (hi - lo) * bins))] += 1
    sm = [sum(h[max(0, i - 1):i + 2]) / len(h[max(0, i - 1):i + 2]) for i in range(bins)]
    top = max(sm)
    peaks = [i for i in range(bins) if sm[i] >= 0.1 * top
             and (i == 0 or sm[i] > sm[i - 1]) and (i == bins - 1 or sm[i] >= sm[i + 1])]
    kept = []
    for p in peaks:
        if kept:
            q = kept[-1]
            if min(sm[q:p + 1]) > 0.7 * min(sm[q], sm[p]):   # no real dip between them
                if sm[p] > sm[q]:
                    kept[-1] = p
                continue
        kept.append(p)
    return len(kept)


def check(x):
    n = len(x)
    m, sd, sk, ek = moments(x)
    tail = sum(1 for v in x if abs(v - m) > 3 * sd) / n
    near = sum(1 for v in x if abs(v - m) < 0.25 * sd) / n
    bc = (sk ** 2 + 1) / ((ek + 3) + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)) - 3)   # with excess kurtosis
    peaks = peak_count(x)
    reasons = []
    if abs(sk) >= 0.5:
        reasons.append("skew %.2f" % sk)
    if abs(ek) >= 1:
        reasons.append("excess kurtosis %.2f" % ek)
    if tail / NORMAL_TAIL3 >= 2:
        reasons.append("tail mass %.1fx normal" % (tail / NORMAL_TAIL3))
    if peaks != 1:
        reasons.append("%d peaks" % peaks)
    if not 0.75 <= near / NORMAL_NEAR <= 1.25:
        reasons.append("%.1f%% near the mean (normal 19.7%%)" % (100 * near))
    return {"n": n, "mean": m, "sd": sd, "skew": round(sk, 3), "excess_kurtosis": round(ek, 3),
            "tail3_share": round(tail, 4), "tail3_ratio": round(tail / NORMAL_TAIL3, 2),
            "near_mean_share": round(near, 3), "peaks": peaks,
            "bimodality_coeff": round(bc, 3), "bc_says_multimodal": bc > 0.555,
            "verdict": "SUFFICIENT" if not reasons else "NOT SUFFICIENT", "reasons": reasons}


def demo_sets(seed=2, n=20000):
    r = random.Random(seed)
    return {
        "added (sum of 30 small effects)": [sum(r.random() for _ in range(30)) for _ in range(n)],
        "multiplied (product of 30 factors)": [math.prod(1 + 0.3 * (r.random() - 0.5) * 2 for _ in range(30)) for _ in range(n)],
        "mixed groups (two populations)": [r.gauss(0, 1) if r.random() < 0.5 else r.gauss(5, 1) for _ in range(n)],
        "feedback (Pareto, alpha 1.5)": [r.paretovariate(1.5) for _ in range(n)],
    }


def demo():
    print("SHAPE SUFFICIENCY -- toy generating processes, OBSERVED here")
    for name, x in demo_sets().items():
        c = check(x)
        print("%-36s %-15s skew %6.2f  ex.kurt %7.2f  tails %5.1fx  near-mean %4.1f%%  peaks %d  BC %.2f%s"
              % (name, c["verdict"], c["skew"], c["excess_kurtosis"], c["tail3_ratio"], 100 * c["near_mean_share"],
                 c["peaks"], c["bimodality_coeff"], "  (BC: multimodal)" if c["bc_says_multimodal"] else ""))


def selftest():
    d = {k.split()[0]: check(v) for k, v in demo_sets().items()}
    checks = [
        ("added -> SUFFICIENT", d["added"]["verdict"] == "SUFFICIENT"),
        ("multiplied -> NOT (skew/tails)", d["multiplied"]["verdict"] == "NOT SUFFICIENT"),
        ("mixed -> 2 peaks", d["mixed"]["peaks"] == 2),
        ("feedback -> NOT", d["feedback"]["verdict"] == "NOT SUFFICIENT"),
        ("Pareto: direct count says 1 peak", d["feedback"]["peaks"] == 1),
        ("Pareto: BC falsely says multimodal (recorded failure)", d["feedback"]["bc_says_multimodal"]),
    ]
    bad = [n for n, ok in checks if not ok]
    print("shape_sufficiency_check --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--demo" in sys.argv or len(sys.argv) < 2:
        demo()
        sys.exit(0)
    with open(sys.argv[1]) as f:
        vals = [float(l) for l in f if l.strip()]
    c = check(vals)
    for k, v in c.items():
        print("%-18s %s" % (k, v))
