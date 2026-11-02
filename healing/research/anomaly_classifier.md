# Anomaly classifier

STATUS: PROPOSED method, co-authored (2026-11-01). CC0.
Code: [`anomaly_classifier.py`](anomaly_classifier.py) (stdlib; `--selftest`).
Framing: [`BOUNDARY_CONDITIONS.md`](BOUNDARY_CONDITIONS.md). Prior art: [`PRIOR_ART.md`](PRIOR_ART.md).

An anomaly = an exception to an established rule. Three ways it arises, plus a step that
audits the anchor the anomaly is measured against.

```text
                      anomaly measured against each anchor and each baseline
                                            |
   1 ANCHOR AUDIT  swap anchors ------------+-- moves --> ANCHOR_IS_SOURCE   the reference itself deviates
                                            |
   2 BASELINE      recompute the prediction-+-- moves --> BASELINE           (c) error in baseline / measurement
                   by an independent method |
                                            | stays
   3 MISSING TERM  one localized extra condition fits the residual?
                         yes -> MISSING_ANCHOR   (a) a condition left out of the model   (Uranus -> Neptune)
                         no  -> MISSING_RULE     (b) the rule is out of scope             (Mercury -> GR)
```

## Anchor audit (step raised in review)

The chosen anchor is itself inside the frame.

1. List every anchor the result depends on: calibrators, reference values, constants.
2. Audit each: provenance, method, scope, drift history.
3. Perturb: replace one anchor with an independent one; rerun.
4. If the anomaly moves with the anchor, the anchor is the source. If it stays, a rule or a
   real effect. Record the deviation from each anchor as data, not only the verdict.

**Condition:** anchor swaps only discriminate when the anchors come from independent methods
or calibration chains. Correlated anchors make an anchor bias look like a new rule (toy case C).
Real parallels: anchors sharing one calibration chain; AI models trained on overlapping data
used to check each other.

## Toy results (OBSERVED, synthetic, this file, 2026-11-01)

```text
case                                     deviation per anchor     verdict              truth
A one biased anchor                      -0.01 / 0.82 / 0.00      ANCHOR_IS_SOURCE     correct
B real rule change                        0.80 / 0.80 / 0.81      RULE_OR_REAL_EFFECT  correct
C all anchors share one bias              0.82 / 0.80 / 0.80      RULE_OR_REAL_EFFECT  WRONG (required failure)
D baseline recomputed                     0.81 x3; baselines 0.8 / 0.0   BASELINE      correct
E unmodelled body (one bump in residual)  0.81 x3; local fit R^2 0.97    MISSING_ANCHOR correct
F secular drift, no locus                 0.80 x3; local fit R^2 0.15    MISSING_RULE  correct
```

Earlier first run (co-authored, other code): A 0.02 / 0.79 / -0.01 -> ANCHOR (correct);
B 0.81 / 0.79 / 0.80 -> RULE (correct); C 0.81 / 0.81 / 0.80 -> RULE (WRONG). Same result.

Limits of the toy: the MISSING_ANCHOR / MISSING_RULE split rests on a chosen cap on bump width
(at most 20% of the span); a wide enough "bump" fits a drift. "One localized condition" is a
stand-in for "a condition with few parameters that predicts somewhere else to look".

## Worked examples (status per line; VERIFY = not checked against a primary source here)

```text
(a) MISSING ANCHOR   Uranus' orbit deviated from prediction; Le Verrier (and Adams) computed an
                     unseen planet; Galle found Neptune near the predicted place, Sept 1846.
                     DOCUMENTED (standard history; VERIFY dates against a primary account)
(b) MISSING RULE     Mercury's perihelion advance exceeded Newtonian prediction by ~43 arcsec per
                     century; the proposed planet "Vulcan" was never found; general relativity
                     (1915) accounts for it. DOCUMENTED (VERIFY figure)
(c) BASELINE         muon g-2: the final Fermilab result (127 ppb) agrees with the 2025 Theory
                     Initiative prediction that uses lattice-QCD hadronic vacuum polarization;
                     the earlier discrepancy came mostly from the data-driven baseline. Tension
                     between data-driven and lattice HVP is unresolved. DOCUMENTED (search
                     summaries of the Fermilab report and White Paper 2025, arXiv:2505.21476;
                     VERIFY numbers against the papers)
anchor audit         Hubble tension: distance-ladder anchors give different H0 -- Cepheid-based
                     (SH0ES, ~73 km/s/Mpc) vs tip-of-the-red-giant-branch (CCHP, ~70); CMB-based
                     ~67. Anchor choice shifts the result; still debated. VERIFY all values.
anchor audit         Kilogram: the international prototype and its official copies drifted
                     relative to each other by up to ~50 micrograms over about a century; the
                     kilogram was redefined via the Planck constant, in force 20 May 2019. The
                     anchor itself was deviating. DOCUMENTED (prior knowledge; VERIFY)
anchor audit         Measured physical constants clustering near the previously accepted value
                     (e.g. Henrion & Fischhoff 1986, "Assessing uncertainty in physical
                     constants", Am. J. Phys.; the Millikan charge story in Feynman's 1974
                     "Cargo Cult Science"). Anchoring inside measurement history. VERIFY.
open fork            Dark matter: missing anchor (unseen mass) or missing rule (modified
                     gravity)? Neptune-or-Vulcan, unresolved. PROPOSED framing.
```

## Status

Toy only. No real anomaly data processed.
