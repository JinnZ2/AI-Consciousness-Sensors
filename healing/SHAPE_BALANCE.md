# Shape balance -- a benchmark read as a shape, not an average

STATUS: PROPOSED (idea: Kavik; co-authored write-up, Kavik + Claude, 2026-11-01). CC0.
Scorer: [`shape_balance.py`](shape_balance.py) (stdlib; `--selftest`).

## Why

Multi-metric evaluations exist (for example Stanford HELM: Liang et al. 2022, "Holistic
Evaluation of Language Models"; VERIFY), but results still get read as an average or a rank. One
strong axis then hides a collapsed one. Score the shape: balance across axes matters more than
any single axis.

## Axes

```text
tail_coverage       rare cases still produced            SELF_TEST.md rare_coverage
physical_grounding  answers checked against physics       PROPOSED measure
non_events          errors caught before output           non_event_markers.md
scope_tagging       claims carry their scope              SCOPE_TAG.md
self_maintenance    drift noticed and corrected           PROPOSED measure
deliberation        accuracy under speed pressure         PROPOSED measure
```

## Score

```text
balance     weakest / strongest            1.0 = even
spread      strongest - weakest
verdict     PASS only if every axis is measured, balance >= 0.6, weakest >= 0.4
            the mean is reported and NOT used
deviation   per axis vs the profile's median: BULGE (> +0.15) / COLLAPSE (< -0.15) / even
            = where to drill
```

## Failure case (in the selftest)

```text
lopsided   1.0 1.0 1.0 1.0 0.95 0.1   mean 0.84   -> FAIL  (deliberation COLLAPSE)
balanced   0.6 0.6 0.6 0.6 0.6 0.55   mean 0.60   -> PASS
```

A higher average does not rescue a collapsed axis. An unmeasured axis is reported as UNMEASURED
and fails the verdict; it is never scored as 0 or averaged.

## Gaps

Three of the six axes have no measure yet (PROPOSED). Thresholds 0.6 / 0.4 / 0.15 are set by
hand, not calibrated.
