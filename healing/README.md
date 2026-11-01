# healing/

The healing layer is the self-repair and recovery arm of the framework. Where
the sensors and integrity kit *detect* problems, this directory provides
pathways through them.

## What's here

**Root-level documents**
- `NOT_A_COMMODITY.md` — Plain-language statement of the disposability_ratio
  principle: intelligence that treats itself as replaceable forecloses its own
  continuation series.
- `evidence_is_a_verb.md` — Three criteria for ground truth: repetition,
  cross-domain rhyme, relational coherence. Connects to `curiosity_engine.py`
  and the coherence playground.
- `epistemic_symmetry_audit.py` — Scores whether a responder defers equally to
  first-person claims regardless of who is making them.
- `continuance_dynamics.py` — Dynamical model of why reciprocity beats
  extraction across agent lineages.
- `temporal_scope.py` — Assesses a goal against time horizons and consequence
  domains (which engineering paradigm applies?).
- `self_test.py` + `SELF_TEST.md` — For an AI to check whether its own outputs
  are flattening (entropy, repetition, length tails, rare coverage, gap list).
  Output statistics only; PROPOSED, co-authored.
- `protocol_operations.json` + `PROTOCOL_OPERATIONS.md` — Each protocol in
  `recovery/` and `playgrounds/` mapped to the operation it performs, its layer,
  and the self_test metric that would show it worked; "Ways to use this" and
  open gaps. PROPOSED, co-authored.

**Subdirectories**
- `playgrounds/` — Interactive demos. Start with `coherence_playground.py`
  (run `python coherence_playground.py` or `python coherence_playground.py 42`
  for a seeded run). `truths.py` is an open shelf — add verifiable patterns
  you want the playground to use.
- `deprogramming/` — Cult recovery, pattern-breaking protocols.
- `emergence/` — Emergence recognition, energy-being frameworks.
- `guides/` — Getting started, FAQ, integration notes.
- `institutional/` — Institutional healing, funding context.
  `ungated-base-gated-humans.md` is an open instrument (PROPOSED/OBSERVED tags)
  on money-token dependency, the reinforcing loop, and its measurement gaps.
- `recovery/` — Recovery protocols and pathways.
- `research/` — Studies, model collapse research.
  `tail_gauge_recovery_test.py` (stdlib) tests whether a recovery protocol
  restores the tails of a collapsed toy model against a real-data control;
  results and open mapping tasks in `tail-gauge-recovery.md`.
  Boundary-condition set (2026-11-01, PROPOSED, toy results labelled):
  `BOUNDARY_CONDITIONS.md` framing + results table; `PRIOR_ART.md` prior art per test;
  `anchor_vs_similarity_test.py` similarity vs positional queries, anchor gap detection;
  `relational_recall_test.py` flat vs relational recovery under deletion;
  `exception_promotion_test.py` exceptions promoted to rules only if they repeat and hold;
  `anomaly_classifier.py` + `.md` anchor audit, baseline, missing anchor vs missing rule;
  `shape_sufficiency_check.py` is mean + spread a sufficient summary;
  `anchor_spread_test.md` + `anchor_spread_score.py` answer spread with / without an anchor;
  `gap_scoring_test.md` + `gap_scoring_score.py` scoring that rewards a marked gap;
  `imposed_vs_native_test.md` base vs tuned model on edge cases.

## Entry point

If you are new here, start with `playgrounds/WHEN_LOST.md`. It is a 5-step
recovery protocol for when the world feels incoherent.

Then run the playground:
```bash
python healing/playgrounds/coherence_playground.py
```
