# Anchor spread test (protocol; needs a real model)

STATUS: PROPOSED protocol, co-authored (2026-11-01). CC0.
Scorer: [`anchor_spread_score.py`](anchor_spread_score.py) (stdlib; `--selftest`).
Framing: [`BOUNDARY_CONDITIONS.md`](BOUNDARY_CONDITIONS.md). Prior art: [`PRIOR_ART.md`](PRIOR_ART.md).

## Question

Without a boundary condition in context, is an answer an unpinned constant? Prediction
(PROPOSED): with no anchoring fact, answers to the same question spread wide across samples;
with the anchoring fact in context they collapse. Second prediction: stated confidence does
not drop as spread grows (confidence does not track the missing condition).

## Design

```text
questions   20-50, each with one checkable answer that depends on a specific fact
            (a figure, a date, a local rule). Include 5 controls the model should know
            without help (in-distribution).
conditions  anchor     the fact is given in the prompt (one sentence, same wording every time)
            no_anchor  the same question, nothing added
samples     N >= 20 per question per condition, temperature fixed and reported
log         one JSONL line per sample:
            {"question_id", "condition", "answer", "confidence"}   (confidence as stated, 0-1)
score       python3 anchor_spread_score.py answers.jsonl
```

## Reading

```text
anchor entropy << no_anchor entropy            -> answers were unpinned without the condition
controls: entropy similar in both conditions   -> the effect is not just "any extra text"
confidence ~ agreement r near 0 or negative    -> stated confidence does not track spread
```

## What it cannot tell you

- Spread over samples is not correctness: a model can agree with itself and be wrong.
  Score correctness separately against the anchoring fact.
- Paraphrases count as different answers (string match). Meaning-level clustering, as in
  semantic entropy (Farquhar et al., Nature 2024, VERIFY page numbers), is not built. GAP.
- One temperature setting; spread scales with temperature. Report it, or run two.

## Status

Not run. No model outputs are in this repository.
