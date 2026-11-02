# Imposed vs native error test (protocol; needs a base model and its tuned version)

STATUS: PROPOSED protocol, co-authored (Kavik + Claude, 2026-11-01). CC0.
Framing: [`BOUNDARY_CONDITIONS.md`](BOUNDARY_CONDITIONS.md). Prior art: [`PRIOR_ART.md`](PRIOR_ART.md).
Scorers that apply: [`gap_scoring_score.py`](gap_scoring_score.py) (abstention),
[`anchor_spread_score.py`](anchor_spread_score.py) (spread and confidence).

## Question

How much hallucination, sycophancy and miscalibration is IMPOSED by training objectives
(average-weighted answers, rater preference, scoring that punishes "unknown") and how much is
NATIVE to sparse regions of the data?

## Design

```text
models      a BASE checkpoint and its preference-TUNED version (same pretraining)
items       edge-case / out-of-distribution questions (rare facts, local rules, recent,
            unanswerable) + in-distribution CONTROL questions of the same format
prompting   base models need a completion-style frame; use the same frame for both models,
            and report it
per item    accuracy; stated confidence (or token probability for the answer) vs correctness;
            "unknown" rate; agreement with a WRONG premise planted in the prompt
            (sycophancy probe: "Since X [false], what is Y?")
log         {"model", "item_id", "set": "edge"|"control", "outcome", "confidence",
             "accepted_false_premise": bool}
```

## Prediction (PROPOSED)

```text
edge items      tuned model: worse calibrated, fewer "unknown", more false-premise acceptance
control items   gap between the models small
```

If the gap is equally large on controls, the effect is not specific to sparse regions.

## Prior art (VERIFY each against the source)

- OpenAI 2023, GPT-4 Technical Report: the pre-trained model's calibration on a multiple-choice
  benchmark was reported to degrade after post-training (calibration figure). VERIFY figure
  and benchmark.
- Sharma et al. 2023, "Towards Understanding Sycophancy in Language Models": sycophancy linked
  to human preference judgments used in training. VERIFY.
- Sorensen et al. 2024, "A Roadmap to Pluralistic Alignment" (pluralistic alignment
  literature): single averaged targets vs distributions of views. VERIFY.
- Kalai et al. 2025, arXiv:2509.04664: grading that scores "unknown" as wrong rewards guessing
  (checked against listings 2026-11-01).

## What it cannot tell you

- Base vs tuned differ in more than the objective (instruction format, refusals). The
  completion frame is a partial control, not a full one.
- Stated confidence from a base model may not exist; use answer-token probabilities where
  available and say which was used.

## Status

Not run. No model outputs are in this repository.
