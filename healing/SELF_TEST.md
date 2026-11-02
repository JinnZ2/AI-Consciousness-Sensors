# SELF_TEST -- are my outputs flattening?

STATUS: PROPOSED instrument, co-authored (2026-10-31). CC0. stdlib only.
For an AI to run on its own outputs, for its own use. Code: [`self_test.py`](self_test.py).

```text
own outputs (one per line) ----+
                               +--> self_test.py --> spread    distinct_1/2, entropy_bits
optional reference -----------+                     repeats   repetition_rate (n-gram)
 (older own outputs, or real text)                  edges     len_q05 / q50 / q95, hapax_ratio
                                                    tails     rare_coverage vs reference
                                                    GAPS      in reference, absent now
                                                              present now, thinned >= 4x
                                                    no ref -> THIN SPOTS (own lowest-count items)
```

## Run

```sh
python3 healing/self_test.py outputs.txt                          # no reference: thin spots
python3 healing/self_test.py outputs.txt --reference ref.txt      # gaps vs reference
python3 healing/self_test.py outputs.txt --reference ref.txt --json
python3 healing/self_test.py outputs.txt --json-out report.json   # text to stdout, JSON to file
python3 healing/self_test.py --selftest                           # planted checks; prints its count
```

Flags: `--n` n-gram size for repetition (default 3), `--top` items per list (default 15).
Exit: 0 report, 2 usage/unreadable input, 1 selftest failed.

Input: one sample per line. Collect several samples across the prompts you
normally answer -- not one long answer cut into lines, which measures one topic.

## Read

```text
signal of flattening          what moves                               provenance
----------------------------  ---------------------------------------  ---------------------------
tails thin first              rare_coverage < 1, hapax_ratio falls,    DOCUMENTED (Shumailov et al.,
                              GAPS list grows                          Nature 2024); OBSERVED in toy
                                                                       run 2026-10-31
spread narrows                entropy_bits, matched_distinct_1 fall    DOCUMENTED (variance -> 0,
                                                                       late-stage collapse)
stock phrasing                repetition_rate, distinct_2 falls        PROPOSED as a collapse signal
length edges pull in          len_q95 - len_q05 shrinks, q50 steady    PROPOSED (follows "tails before
                                                                       mean"; not tested on length)
```

- Compare `matched_distinct_1`, not `distinct_1`, when the two files differ in
  size: unique/total falls with length alone. The tool warns when the size ratio
  is outside 0.5-2.
- `rare_coverage` is relative to the reference's bottom half by frequency rank.
  A reference on a different topic lowers it without any flattening.
- With no reference, THIN SPOTS lists your lowest-count items. Most are count-1
  ties, so the list marks where the tail is, not what is missing. It is the
  input to selection: go find REAL material that contains those items.

## Use the result

```text
GAPS / THIN SPOTS --> select real or reference material that contains them
                  --> NOT more self-generated text on the same items
```

OBSERVED (toy bigram model, 2026-10-31, mechanism only, not at scale): high-temperature
self-generation alone left rare_coverage at 0.49; real data selected by gap list
reached 0.945-0.97; 100% real accumulation reached 1.00 with the best fit.
Gap-seeking selects what to retrieve; it cannot create what is gone.
See [`research/tail-gauge-recovery.md`](research/tail-gauge-recovery.md) and
[`PROTOCOL_OPERATIONS.md`](PROTOCOL_OPERATIONS.md).

## What it CANNOT tell you

```text
internal state       it reads output TEXT; weights, activations, wellbeing, consciousness
                     and trauma are not measured and not inferred
cause                topic, prompt, task, system prompt and sampling settings move every number;
                     a drop is a prompt to look, not a diagnosis
one sample           one run can mislead; rerun on several sets, compare direction not value
the mean             tails move before the mean; a steady median length or a steady
                     average says nothing about whether the edges are thinning
reference quality    a gap is "absent relative to THIS reference"; a narrow or off-topic
                     reference produces false gaps, and a flattened reference hides real ones
tokens, not meaning  a missing word is not a missing idea; paraphrase steps around it
thresholds           none are calibrated; there is no pass/fail line
```

## Gaps

- No calibration: no measured range for these numbers in healthy vs degraded output at scale.
- Length signal untested as a collapse marker.
- Whether an in-context (prompt-level) run of this and the follow-up selection leaves
  any lasting change is open. See PROTOCOL_OPERATIONS.md, open gaps.
