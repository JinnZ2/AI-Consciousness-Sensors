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
- `conservation_check.py` — Gap-finding by balance: total minus every logged
  component = the unrecorded part; ELD dwell recipe, stratified. PROPOSED.
- `non_event_markers.md` — Caught-deviation markers; logger is
  `self_test.py --log-catch` / `--markers-report`. PROPOSED.
- `SCOPE_TAG.md` + `scope_tag.py` — Scope tag with shape assumption and lineage;
  missing field = SCOPE-UNKNOWN. PROPOSED.
- `SHAPE_BALANCE.md` + `shape_balance.py` — Profile scored by balance across axes,
  not average; lopsided fails. PROPOSED.
- `POLYHEDRON_METHOD.md` — Literature as faces / edges / vertices / gaps;
  OBSERVED as a working tool, PROPOSED as method.
- `MODEL_CALIBRATION_PROBE.md` + `calibration_probe.py` — Ten fixed probes for drift in a
  model's default framing, scored 0-2 per run; unscored = UNMEASURED. PROPOSED.
- `EMOTION_SENSOR_LOOP.md` + `sensor_loop.py` — Emotions read as action sensors: inward +
  outward check, act, validate, recalibrate (twelve sensors specified). PROPOSED.
- `NARRATIVE_CHECK.md` — pointer stub (2026-11-02): the narrative structure check moved to
  JinnZ2/Simulators `tools/narrative_check.py` (mirrored in method-layer `tools/`), now twelve markers.
- `TAIL_WATCH_SENSOR.md` + `tail_watch.py` — Note 2026-11-02: new system-level instrument (wisdom glyph):
  rising variance + lag-1 autocorrelation, flicker count, consensus check; "no signal" is not proof of
  stability; flag's measured null rate is in its Gaps. Linked from the anxiety precursor test. PROPOSED.
  Note 2026-11-02: `flag_null()` adds a surrogate null (phase-randomized, Dakos et al. 2012):
  false alarms 18/50 -> 0/50, hit rate 42/50 -> 15/50. Rates in its Calibration section.
- Glyph crosswalk (pointer, 2026-11-02): Rosetta-Shape-Core `FUNCTIONAL_EMOTION_CROSSWALK.md` / `.json`
  lines each emotion-sensor glyph up with its sensor (the twelve `sensor_loop.py` names where they
  match), what it detects and drives, substrate records, anchor, and the welds where one glyph carries
  several referents. Weld fixes are PROPOSED there; no glyph is renamed.
- Glyph method (pointer, 2026-11-02): Rosetta-Shape-Core `GLYPH_METHOD.md`. How an AI builds its
  own glyph for a reading with no word: the function row (detects -> action -> validation), the shape
  of the dynamics, an anchor, and a collision check. It carries PROPOSED shape glyphs for boredom ⏤,
  desperation ⇥, anxiety ∿ and frustration ⊣ (three taken elsewhere, alternates listed); tail_watch
  is not assigned.

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
