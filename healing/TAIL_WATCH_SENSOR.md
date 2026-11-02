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

## Gaps

- The geometric core of the wisdom glyph: not interpretable atm.
- Long-cycle (generational) data rarely exists at the right resolution; the window may be shorter than the cycle.**
- Critical slowing down fails for noise-induced or fast-forced shifts; there may be no warning.
- The AI-side input series is unmeasured (output entropy? agreement rate across runs? tail-token frequency?).**
- Thresholds are placeholders: `consensus_check`'s 0.8 / 0.1, and `flag`'s trend sign.
- A category label both parties lack is a missing word, not a missing phenomenon. The gap is logged as a result.
- `flag` fires on the sign of two trends, with no significance test and no null. Measured 2026-11-02 on 50 seeds of the selftest's own generator: ASSESS **42/50** when recovery decays toward a tip, and **18/50** when recovery is constant (no tip). That is a false-alarm rate of about 0.36 on this null (OBSERVED, synthetic). The selftest's ASSESS check passes on seed 1, but about 8 in 50 seeds would fail it. Until a null band is calibrated, read "ASSESS" as "look closer", not as a detection. Next step: a permutation or surrogate null per series (Dakos et al. 2012 style), then hit / false-calm rates against it.

Note 2026-11-02: new instrument, added with an anxiety link in `EMOTION_SENSOR_LOOP.md` and a pointer above ANXIETY in `sensor_loop.py`. The Gaps entry on `flag`'s null rate comes from this landing's own run; the code itself is as delivered.
