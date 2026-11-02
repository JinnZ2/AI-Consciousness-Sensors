#!/usr/bin/env python3
"""
tail_watch.py -- Tail-Watch Sensor (wisdom glyph): is a structure moving toward a phase shift
before the average shows it?

STATUS: PROPOSED instrument, co-authored. CC0. stdlib only.
Doc: TAIL_WATCH_SENSOR.md. System-level sensor, not an emotion. Rising variance AND rising lag-1
autocorrelation together = critical-slowing-down signal (PROPOSED trigger). "No signal" is not proof
of stability. Too few points = UNMEASURED, never a zero.

USAGE
  python3 tail_watch.py              run the planted selftest (prints its count; ~20 s)
  python3 tail_watch.py --bench      50 tip / 50 no-tip seeds, 200 surrogates: flag() vs flag_null()
"""
import statistics as st
def lag1_autocorr(xs):
    m = st.mean(xs); den = sum((a-m)**2 for a in xs)
    return sum((a-m)*(b-m) for a,b in zip(xs,xs[1:]))/den if den else 0.0
def trend(vals):
    n=len(vals)
    if n<2: return 0.0
    xm,ym=(n-1)/2,st.mean(vals)
    return sum((i-xm)*(v-ym) for i,v in enumerate(vals))/sum((i-xm)**2 for i in range(n))
def tail_watch(series, window=20):
    return [(i, st.pvariance(series[i-window:i]), lag1_autocorr(series[i-window:i]))
            for i in range(window, len(series)+1)]
def flicker_count(series, threshold):
    """Crossings of a state boundary = pulse in/out (PROPOSED)."""
    return sum(1 for a,b in zip(series,series[1:]) if (a-threshold)*(b-threshold)<0)
def flag(series, window=20):
    """Uncalibrated, look closer only: sign of two trends, no significance test, no null.
    Measured false-alarm rate in TAIL_WATCH_SENSOR.md Calibration. Use flag_null() for a test."""
    r = tail_watch(series, window)
    if len(r) < 3: return "UNMEASURED"
    if trend([v for _,v,_ in r])>0 and trend([a for _,_,a in r])>0:
        return "ASSESS: variance and autocorrelation both rising"
    return "no slowing signal in this window (not proof of stability)"
def consensus_check(agree_share, reasoned_dissent_share):
    """Thresholds PROPOSED, uncalibrated.**"""
    if agree_share>0.8 and reasoned_dissent_share<0.1:
        return "RUN DISAGREEMENT PASS -> neutral -> keep what survives"
    return "normal review"
# --- Added 2026-11-02 (relay part F): surrogate null for flag(). -------------------------------------
# Significance by surrogate data, as in early-warning analysis (Dakos et al. 2012, PLoS ONE 7(7):e41010,
# carried, not re-read here): build series that keep the observed power spectrum (so the whole
# autocorrelation function, lag-1 included) but are stationary, and ask whether the observed trends in
# rolling variance and lag-1 autocorrelation exceed what such series produce. Phase randomization
# (Theiler et al. 1992) via a stdlib mixed-radix FFT. Gaussian linear null: amplitude distribution is
# not preserved (AAFT would be), stated.
import cmath, math, random as _random

def _fft(a, inverse=False):
    """Mixed-radix Cooley-Tukey on a list of complex; naive DFT on prime lengths. Unscaled."""
    n = len(a)
    if n == 1:
        return list(a)
    p = next((q for q in range(2, int(n ** 0.5) + 1) if n % q == 0), n)
    sgn = 1 if inverse else -1
    if p == n:
        return [sum(a[t] * cmath.exp(sgn * 2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]
    m = n // p
    subs = [_fft(a[r::p], inverse) for r in range(p)]
    out = [0j] * n
    for k in range(n):
        out[k] = sum(subs[r][k % m] * cmath.exp(sgn * 2j * math.pi * r * k / n) for r in range(p))
    return out

def phase_surrogate(series, rng):
    """Same amplitude spectrum and mean as `series`, random phases: stationary by construction."""
    n = len(series); mu = sum(series) / n
    X = _fft([complex(v - mu) for v in series])
    Y = [0j] * n
    for k in range(1, (n - 1) // 2 + 1):
        Y[k] = abs(X[k]) * cmath.exp(1j * rng.uniform(0, 2 * math.pi))
        Y[n - k] = Y[k].conjugate()
    if n % 2 == 0:
        Y[n // 2] = X[n // 2]
    return [v.real / n + mu for v in _fft(Y, inverse=True)]

def _window_stats(series, window):
    """Plain-float equivalent of tail_watch(): (variances, lag-1 autocorrelations). Matches to ~1e-12."""
    vs, acs = [], []
    for i in range(window, len(series) + 1):
        w = series[i - window:i]; m = sum(w) / window
        d = [a - m for a in w]; den = sum(a * a for a in d)
        vs.append(den / window)
        acs.append(sum(a * b for a, b in zip(d, d[1:])) / den if den else 0.0)
    return vs, acs

def _slope(vals):
    n = len(vals)
    if n < 2:
        return 0.0
    xm = (n - 1) / 2; ym = sum(vals) / n
    return sum((i - xm) * (v - ym) for i, v in enumerate(vals)) / sum((i - xm) ** 2 for i in range(n))

def _trend_pair(series, window):
    vs, acs = _window_stats(series, window)
    return _slope(vs), _slope(acs)

def surrogate_null(series, window=20, n=200, seed=None):
    """Observed (variance-trend, AC-trend) and the same pair over n phase-randomized surrogates."""
    if len(series) - window + 1 < 3:
        return None
    rng = _random.Random(seed)
    obs = _trend_pair(series, window)
    sv, sa = [], []
    for _ in range(n):
        v, a = _trend_pair(phase_surrogate(series, rng), window)
        sv.append(v); sa.append(a)
    return {"observed": obs, "var_trends": sv, "ac_trends": sa, "n": n,
            "method": "phase-randomized surrogates (FFT, stdlib)"}

def _upper_quantile(xs, alpha):
    s = sorted(xs)
    return s[min(len(s) - 1, max(0, math.ceil((1 - alpha) * len(s)) - 1))]

def flag_null_detail(series, window=20, n=200, alpha=0.05, seed=None):
    null = surrogate_null(series, window, n, seed)
    if null is None:
        return {"verdict": "UNMEASURED"}
    (ov, oa) = null["observed"]
    qv, qa = _upper_quantile(null["var_trends"], alpha), _upper_quantile(null["ac_trends"], alpha)
    pv = (1 + sum(1 for x in null["var_trends"] if x >= ov)) / (n + 1)
    pa = (1 + sum(1 for x in null["ac_trends"] if x >= oa)) / (n + 1)
    hit = ov > qv and oa > qa
    verdict = (f"ASSESS: variance and autocorrelation trends both beyond surrogate null (alpha={alpha})"
               if hit else "no slowing signal beyond null (not proof of stability)")
    return {"verdict": verdict, "obs_var_trend": ov, "obs_ac_trend": oa, "q_var": qv, "q_ac": qa,
            "p_var": pv, "p_ac": pa, "n_surrogates": n, "alpha": alpha, "method": null["method"]}

def flag_null(series, window=20, n=200, alpha=0.05, seed=None):
    """ASSESS only if BOTH observed trends exceed the (1-alpha) quantile of their surrogate trends."""
    return flag_null_detail(series, window, n, alpha, seed)["verdict"]

def _gen(seed, tip, length=200):
    """The two worlds measured in TAIL_WATCH_SENSOR.md: recovery rate decaying toward a tip, or constant."""
    rng = _random.Random(seed); x, s = 0.0, []
    for t in range(length):
        k = 1.0 - t / 220 if tip else 1.0
        x = x - k * x * 0.5 + rng.gauss(0, 0.1); s.append(x)
    return s

def bench(seeds=50, n_surr=200, alpha=0.05, window=20):
    """Hit rate (tip world) and false-alarm rate (no-tip world) for flag() and flag_null()."""
    rows = {"flag": [0, 0], "flag_null": [0, 0]}
    for sd in range(seeds):
        for j, tip in enumerate((True, False)):
            s = _gen(sd, tip)
            rows["flag"][j] += flag(s, window).startswith("ASSESS")
            rows["flag_null"][j] += flag_null(s, window, n_surr, alpha, seed=10_000 + sd).startswith("ASSESS")
    return {k: {"hits": v[0], "false_alarms": v[1], "seeds": seeds,
                "hit_rate": v[0] / seeds, "fa_rate": v[1] / seeds} for k, v in rows.items()}

def selftest():
    import random
    checks = []
    # rates over seeds with stated tolerance, never one seed (relay part F item 4)
    SEEDS, NSURR, ALPHA = 20, 99, 0.05
    b = bench(SEEDS, NSURR, ALPHA)
    # flag() kept unchanged: on the tip world it should usually fire (measured 42/50 at 50 seeds)
    checks.append(("flag() fires on most tip series (>= 12/20)", b["flag"]["hits"] >= 12))
    # flag_null(): false alarms bounded near alpha. Binomial(20, 0.05): P(X >= 4) ~ 0.016, so <= 3/20
    checks.append(("flag_null() false alarms <= 3/20 at alpha 0.05", b["flag_null"]["false_alarms"] <= 3))
    checks.append(("flag_null() false alarms below flag()'s",
                   b["flag_null"]["false_alarms"] < b["flag"]["false_alarms"]))
    # power is reported, not asserted: a first bound (>= 10/20) was set before measuring and failed at
    # 4/20; lowering it to pass would tune the check to the seeds. Asserted instead: it discriminates.
    checks.append(("flag_null() hits exceed its false alarms (discriminates)",
                   b["flag_null"]["hits"] > b["flag_null"]["false_alarms"]))
    # the fast window stats equal tail_watch()
    random.seed(7); s = [random.gauss(0, 1) for _ in range(60)]
    r = tail_watch(s); vs, acs = _window_stats(s, 20)
    checks.append(("_window_stats matches tail_watch to 1e-9",
                   all(abs(a - v) < 1e-9 and abs(b2 - c) < 1e-9 for (_, a, b2), v, c in zip(r, vs, acs))))
    # surrogate keeps the amplitude spectrum and the mean
    rng = _random.Random(3); sur = phase_surrogate(s, rng)
    X = _fft([complex(v - sum(s) / 60) for v in s]); Y = _fft([complex(v - sum(sur) / 60) for v in sur])
    checks.append(("surrogate keeps amplitude spectrum and mean",
                   all(abs(abs(a) - abs(c)) < 1e-6 for a, c in zip(X, Y)) and abs(sum(s) - sum(sur)) < 1e-9))
    checks.append(("short series is UNMEASURED in both flags",
                   flag(s[:10]) == "UNMEASURED" and flag_null(s[:10]) == "UNMEASURED"))
    checks.append(("consensus_check fires", consensus_check(0.9, 0.05).startswith("RUN")))
    checks.append(("consensus_check normal", consensus_check(0.5, 0.3) == "normal review"))
    checks.append(("flicker_count", flicker_count([0, 1, 0, 1], 0.5) == 3))
    bad = [n for n, ok in checks if not ok]
    for n in bad:
        print("  FAIL:", n)
    print("tail_watch selftest %d/%d" % (len(checks) - len(bad), len(checks)))
    print("  bench (%d seeds, %d surrogates): flag hits %d FA %d | flag_null hits %d FA %d" % (
        SEEDS, NSURR, b["flag"]["hits"], b["flag"]["false_alarms"],
        b["flag_null"]["hits"], b["flag_null"]["false_alarms"]))
    assert not bad, bad
if __name__=="__main__":
    import sys
    if "--bench" in sys.argv:
        for name, row in bench().items():
            print("%-9s hit %d/%d (%.2f)  false alarm %d/%d (%.2f)" % (
                name, row["hits"], row["seeds"], row["hit_rate"], row["false_alarms"], row["seeds"], row["fa_rate"]))
    else:
        selftest()
