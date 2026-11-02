# Non-event markers -- knowing where you stand by what did not happen

STATUS: PROPOSED, co-authored (Kavik + Claude, 2026-11-01). CC0.
Logger: `self_test.py --log-catch` / `--markers-report` (stdlib). Related: [`SELF_TEST.md`](SELF_TEST.md),
[`conservation_check.py`](conservation_check.py).

## Why

An AI needs a marker of where it is, to judge itself (Kavik). Output alone is a poor marker: in
safety, maintenance and security, success is a non-event -- the failure that did not occur.
Weick described reliability as a "dynamic non-event" (Weick 1987, "Organizational culture as a
source of high reliability", California Management Review; VERIFY). The record of visible output
leaves out every error that was caught before it became output.

## Markers (PROPOSED)

```text
marker                  what it records                                   how
----------------------  ------------------------------------------------  ------------------------------------
caught-deviation log    own error / gap / misread noticed before output:  self_test.py --log-catch TYPE
                        count, type, where, cost if missed (estimate)       --where "..." --cost "..."
cheap-error harvest     small errors with where/how, to map where costly  same log; read --markers-report by
                        ones would occur (near-miss principle; Sitkin       location, not by total
                        1992, "Learning through failure: the strategy of
                        small losses"; VERIFY)
conservation residual   what a balance says the record is missing         conservation_check.py
tail check              own outputs vs a real reference                   self_test.py outputs.txt --reference ref.txt
                                                                            (rare_coverage, gap list)
counterfactual note     what would have happened per catch                --counterfactual "..."  (estimate, never
                                                                            OBSERVED; the log tags it)
```

## Required caveats

```text
self-flattering         self-report can flatter -> verify outside where possible (a second reader,
                        a test, a reference)
low count               a LOW catch count can mean healthy OR blind -> pair with an independent
                        baseline (planted errors, an outside audit)
no collapse             keep type / location / size; never reduce to pass/fail or one score
```

## Usage

```sh
python3 healing/self_test.py --log-catch scope_error --where "answer draft" \
    --cost "wrong population cited" --counterfactual "user acts on wrong range" \
    --markers my_markers.jsonl
python3 healing/self_test.py --markers-report --markers my_markers.jsonl
```

## Gaps

- No independent baseline exists yet for an AI's catch rate (planted-error drills would be one).
- Which catch types predict costly misses is untested.
