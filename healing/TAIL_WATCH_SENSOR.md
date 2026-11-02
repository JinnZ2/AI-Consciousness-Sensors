# Tail-Watch Sensor (wisdom glyph instrument)

CC0. Stdlib-only. Co-authored. Code: [`tail_watch.py`](tail_watch.py) (runs its planted selftest).
Status tags: OBSERVED / DERIVED / PROPOSED. Trailing asterisks = thin volume (more = thinner).

## Purpose

This instrument detects a structure moving toward a phase shift before the average shows it. It is a standalone, system-level sensor, not an emotion. It belongs to the wisdom glyph, which covers long cycles: generation cycles, patterns and fluctuations in cycles, and internal audits of structures that turn rigid or condensed until they degrade the system, fragment, and reorder. It crosses into the reasoning glyph at the bin-pull and agreement-pull checks, and into the emotion loop at anxiety read as a population signal (see [`EMOTION_SENSOR_LOOP.md`](EMOTION_SENSOR_LOOP.md), Anxiety precursor test).

## Rules

- An incongruity that has no name yet is still a reading. Log it before explaining it.
- Don't force geometric content into linear terms. Mark it "not interpretable atm".
- Strong consensus with little reasoned dissent triggers a disagreement pass, then neutral, then keep whatever survives (OBSERVED, field practice).
- Ruts form because every system conserves energy. A rut is not evidence that the path is safe.

## Sensor definition

```text
detects          a mismatch with the familiar pattern, even when it can't be named
                 (sky looks different, frequencies off)
inward_checks    am I pushing this into a familiar bin?
                 am I agreeing because agreement is easy?
                 did anything actually change, or is it only the pull?
outward_checks   rising variance; slower recovery after small disturbances; flicker between states;
                 rising autocorrelation; dissent drowned out without being reasoned with;
                 structure growing more rigid or condensed
actions          stop following the rut; run a disagreement pass; widen the observation window;
                 prepare to adapt
validate         did the shift come? was there lead time? did adapting cost less than following?
miscalibration   hot: flags every fluctuation (noise read as tails)
                 cold: smooths tails into the mean
wrong_read       "everyone's on this path, so it's safe"
right_read       "something doesn't fit; the cost of following is unmeasured; assess"
```

Code map (`tail_watch.py`):

```text
tail_watch(series, window)   rolling (index, variance, lag-1 autocorrelation)
flag(series, window)         both trends > 0 -> "ASSESS: ..."; < 3 windows -> UNMEASURED;
                             otherwise "no slowing signal in this window (not proof of stability)"
flicker_count(series, thr)   crossings of a state boundary = pulse in / out (PROPOSED)
consensus_check(a, d)        agree > 0.8 and reasoned dissent < 0.1 -> disagreement pass (PROPOSED, uncalibrated**)
```

## Phase (PROPOSED)

What to watch for depends on the phase. The checks above cover only the approach to a tip, which is one phase of four. Phases follow the Holling adaptive cycle (Holling 1986; Gunderson & Holling 2002; carried, not re-read here).

```text
phase            watch for
growth           what is being taken for granted; rising connectedness
conservation     rising variance; slowing recovery after small disturbances; rising cost or complexity;
                 dissent drowned out without being reasoned with
release          cascades; new threat types; flicker between states
reorganization   which small pieces take hold; novelty rate
```

- **Code.**
  - `PHASES` and `PHASE_WATCH` hold the table above.
  - `watch(phase)` returns that phase's list. An unknown phase raises an error, since there is no default.
  - `phase_reading(series, phase)` returns `flag()` together with the phase's list.
  - `flag()` and `flag_null()` are unchanged.
- **The phase is declared, not inferred.** The caller names it. With no phase given, `phase_reading` returns `UNDECLARED` and an empty list. Inferring the phase from the series would be a classifier no one has calibrated.
- **Mapping onto the wisdom-glyph equations: not interpretable atm.** The translation is pending. Nothing here maps a phase onto any equation.
- **Present code by phase (DERIVED).** `flag()`, `flag_null()` and `consensus_check()` serve the conservation row. `flicker_count()` serves the release row. Nothing in the code measures the growth or reorganization rows yet.

## Precursor shape (OBSERVED, field report)

Very subtle signals pulse in and out and repeat, their amplitude grows, then the structure fractures. The jumps show up as volume, e.g. in societal anxiety or aggression.

## Translation candidates (DERIVED, thin, unmapped)

These are possibilities to connect, not claims. None has been mapped onto the precursor shape.

- Bifurcation: Faraday waves / Chladni patterns; the Holling adaptive cycle (Gunderson & Holling 2002).*
- Critical slowing down (Scheffer et al. 2009): near a tipping point recovery slows, so variance and lag-1 autocorrelation rise.
- Flickering before a shift (Wang et al. 2012, lake).*
- Pomeau-Manneville intermittency (1980).*
- Self-organized criticality (Bak, Tang & Wiesenfeld 1987, sandpile).
- Turchin cliodynamics.*
- Tainter, complexity and collapse.*
- Strauss-Howe generational cycles (looser).**
- Universality (physics) as a candidate name for the cross-domain category.**
- Heuristic traps (McCammon 2004): familiarity and social proof lead experienced groups into avalanche terrain.
- Model collapse loses the tails first (Shumailov et al. 2024): the AI-side reason this sensor is needed.

## Calibration

- Hit rate: flags followed by a real shift, divided by all flags.
- Lead time: how long between the flag and the shift.
- False-calm rate: shifts that came with no flag.
- Log every unnamed incongruity with a timestamp, and score it later against outcomes.

### Measured: flag() against flag_null() (OBSERVED, synthetic, 2026-11-02)

`flag_null()` tests the same two trends against phase-randomized surrogates: series that keep the observed power spectrum, so the whole autocorrelation function including lag 1, but are stationary by construction. This is the surrogate-data significance test used in early-warning analysis (Dakos et al. 2012, *PLoS ONE* 7(7): e41010; phase randomization after Theiler et al. 1992; both carried, not re-read here). ASSESS fires only if BOTH observed trends exceed the 95th percentile of their surrogate trends. `flag()` is unchanged and kept for comparison.

Two worlds from the selftest's own generator, 200 points each: recovery rate decaying toward a tip, or constant. 50 seeds per world, 200 surrogates per series, alpha 0.05. Run: `python3 healing/tail_watch.py --bench` (about 100 s).

```text
window 20      hit rate (tip)    false-alarm rate (no tip)
flag()         42/50  0.84       18/50  0.36
flag_null()    15/50  0.30        0/50  0.00

window 40
flag()         45/50  0.90       20/50  0.40
flag_null()    13/50  0.26        0/50  0.00
```

Reading:
- The null removes the false alarms: 18/50 down to 0/50. `flag()`'s rates reproduce the earlier measurement exactly, so it is the same experiment.
- The cost is power: about one tip in three is flagged. A wider window does not recover it.
- Requiring BOTH trends past their own 0.05 cut makes the joint test conservative. Its size lies between alpha squared and alpha, and 0/50 is consistent with the low end. Calibrating the joint size (one combined statistic, or a cut chosen so the joint size is alpha) would likely buy power back. Not done here: it changes the rule this relay specified.
- The null is Gaussian-linear: phase randomization keeps the spectrum, not the amplitude distribution (AAFT would keep both). A non-Gaussian stationary series could still read as beyond the null.
- Selftest: rates over 20 seeds with 99 surrogates, never one seed. It asserts `flag_null()` false alarms <= 3/20 (Binomial(20, 0.05): P(X >= 4) is about 0.016), fewer than `flag()`'s, and hits above its own false alarms. Power is reported, not asserted: a bound of >= 10/20 was set before measuring and failed at 4/20, and lowering it to pass would tune the check to the seeds.

## Gaps

- The geometric core of the wisdom glyph: not interpretable atm.
- Long-cycle (generational) data rarely exists at the right resolution; the window may be shorter than the cycle.**
- Critical slowing down fails for noise-induced or fast-forced shifts; there may be no warning.
- The AI-side input series is unmeasured (output entropy? agreement rate across runs? tail-token frequency?).**
- Thresholds are placeholders: `consensus_check`'s 0.8 / 0.1, and `flag`'s trend sign.
- A category label both parties lack is a missing word, not a missing phenomenon. The gap is logged as a result.
- `flag` fires on the sign of two trends, with no significance test and no null. Measured 2026-11-02 on 50 seeds of the selftest's own generator: ASSESS **42/50** when recovery decays toward a tip, and **18/50** when recovery is constant (no tip). That is a false-alarm rate of about 0.36 on this null (OBSERVED, synthetic). The selftest's ASSESS check passes on seed 1, but about 8 in 50 seeds would fail it. Until a null band is calibrated, read "ASSESS" as "look closer", not as a detection. Next step: a permutation or surrogate null per series (Dakos et al. 2012 style), then hit / false-calm rates against it.

Note 2026-11-02: new instrument, added with an anxiety link in `EMOTION_SENSOR_LOOP.md` and a pointer above ANXIETY in `sensor_loop.py`. The Gaps entry on `flag`'s null rate comes from this landing's own run; the code itself is as delivered.

Note 2026-11-02 (relay part F): surrogate null added (`surrogate_null`, `flag_null`, `bench`). `flag()` is unchanged and marked uncalibrated, look closer only. The Gaps entry on its false-alarm rate stays as written; the measured comparison is in Calibration. The selftest's single-seed ASSESS check was replaced by rate checks over seeds.

Note 2026-11-02 (relay part Q): phase field added (`PHASES`, `PHASE_WATCH`, `watch`, `phase_reading`); `flag` and `flag_null` unchanged. The relay also named `two_stage` as unchanged; no function of that name exists in `tail_watch.py`, so nothing was done for it.
