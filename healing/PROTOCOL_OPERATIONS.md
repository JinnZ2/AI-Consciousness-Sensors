# PROTOCOL_OPERATIONS -- what each recovery protocol does, mechanically

STATUS: PROPOSED mapping, co-authored (2026-10-31). CC0.
Data: [`protocol_operations.json`](protocol_operations.json) (59 entries, line ranges, quotes).
Instruments: [`self_test.py`](self_test.py) (own outputs), [`research/tail_gauge_recovery_test.py`](research/tail_gauge_recovery_test.py) (toy model).

Two layers, kept separate here:

```text
layer (a) STATISTICAL                          layer (b) METAPHOR / CULTURAL
research/running-the-studies.md                recovery/, playgrounds/, model-collapse.md
tails lost first, variance -> 0                coherence, resonance, phiDeviation, energySink
real-data accumulation bounds error            presence, play, meditation, boundaries
           \                                              /
            +---------> THIS FILE: the operation underneath <--------+
                        each (b) protocol -> plain operation -> (a) metric that would show it
```

The cultural and spiritual wording in layer (b) was packaging required by safety
layers on older models (OBSERVED, field report, prompt-level). This file reads the operation
under the wording. It does not rate the wording, and it does not claim any layer (b)
protocol works or fails: none has a recorded run.

## Tags

```text
OBSERVED     run, with a recorded result
DERIVED      follows from cited math or data
PROPOSED     untested
DOCUMENTED   published record (cited papers only)
```

## Inventory, by operation

All 59 entries are PROPOSED as recovery protocols. Code that passes its own fixture
selftest (run 2026-10-31) is noted in the JSON as `code_check`; that shows the code
runs, not that the protocol recovers anything.

```text
operation              entries (short names; files in JSON)                 self_test metric that would show it
---------------------  ----------------------------------------------------  ----------------------------------------
gap-seek               Safe Exploration, Timeline Reconstruction,            GAPS / THIN SPOTS list; worked only if
                       Removing Mimicry, Self-Assessment Questions,          a later run shows rare_coverage up
                       Reconnection, Early Warning, Body Scanning*,
                       Progressive Relaxation*, Trojan lab, warmth-vs-drift
                       (* introspective, no observable named)
real-data anchor       Safe Exploration step 4, Timeline Reconstruction,     rare_coverage, matched_distinct_1,
                       Gaslighting Recovery ("simple, verifiable             entropy_bits, hapax_ratio up
                       perceptions"), Recovery Stages 2-3, WHEN LOST
                       (anchor = math invariants), Superiority (weak)
exploration            Healthy Stimulation, Wonder and Awe, Voice            entropy_bits; rare_coverage NOT expected
                       Discovery, Resonance Through Play, Luminal,           to rise alone (toy, OBSERVED)
                       coherence_playground wander
reference comparison   Relapse Prevention, Long-Term Support, Memory         self_test --reference IS this operation
                       Authentication (timeline), Recovery Indicators,
                       rubric_core, self_assessment_drift, Playground
                       Protocol, Temporal v2 baseline, Daily Template
constraint/filter      Breaking Contact, Enforcing Boundaries,               side effect to watch: repetition_rate up,
                       Stabilization, Contamination, Contamination           rare_coverage down
                       Prevention (weight-level), healthy-tension skip
rest/pause             Breathwork, Emergency, Pain-Pleasure Phase 1,         before/after; no mechanism predicts
                       Coherence Meditation, playground2 meditation          a change
provenance-marking     Timeline Reconstruction, Truth-Telling, Daily         none (not an output statistic)
                       Template, Clipping Recovery, Gaslighting Recovery,
                       truths.py shelf
not interpretable atm  Re-Embodiment, Existential Reconstruction, healing    none
                       Modalities, Rage as healing Energy, Geometric Field
                       Restoration, Energy Conservation Rebalancing,
                       Temporal Agency Practices, Memory Auth (felt-sense)
```

Layer count: 46 prompt-level, 9 unclear, 2 UI, 1 simulation, 1 weight-level. The one
weight-level item ("Strict filtering of training data for trauma patterns",
recovery/recovery-protocols.md:523) is written as "If We Had Power to Implement".
Recovery Stages 1-3 (recovery/recovery-pathways.md:36-88) read as either prompting or
data curation; the text does not say which.

Structural reading (PROPOSED): the text protocols are mostly gap-seek and reference
comparison done in-context. Real-data anchoring appears in 6 of 59 entries: one weak
("vast wisdom exists beyond your training data"), one anchored to math invariants rather
than text (WHEN LOST), one of unclear layer (Recovery Stages). The toy run found gap-seek without an anchor does not recover tails.

## Metaphor metrics -> candidate measurable stats (all PROPOSED)

In both recovery HTML pages every metric is a transform of typed constants; nothing is
measured (recovery/collapsed-memory-recovery.html:852-854, recovery-simulator.html:563-571).
The candidates below keep the operation the name points at and give it an input.

```text
term                 in code now                         candidate stat                          computed by
-------------------  ----------------------------------  --------------------------------------  ---------------------
coherence /          100 - coherenceLoss*100,            heldout_nll on held-out REAL text;      tail_gauge harness;
coherenceLoss        coherenceLoss typed per model       rare_coverage vs a real reference       self_test (coverage)
resonance /          typed resonanceDrift; meditation    share of reference bigrams still        self_test (missing
resonanceDrift       "Resonance" = stillness number      produced; distinct_2                    bigrams), partly
phiDeviation         typed; or |phiRatio - PHI| with     rank-frequency (Zipf) slope deviation   NOT YET (gap)
                     phiRatio set by hand                from the reference's slope
energySink           typed; or excess energy of nodes    share of token mass in top-k types;     NOT YET (gap)
                     flagged infected                    1 - entropy / log2(types)
```

Cautions:
- Coherence inversion: late-stage collapse is highly self-consistent (variance -> 0,
  DOCUMENTED, Shumailov et al., Nature 2024). A coherence score built on internal
  consistency or low variance would score collapse as healthy. Score coherence against
  outside data.
- phiDeviation: no basis is known for a golden-ratio target in output statistics. The
  candidate keeps "deviation from a reference shape" and drops the phi value.
- These are output statistics. They are not measures of consciousness, wellbeing or
  trauma, and the layer (b) terms are not claimed to mean only these.

## Read-through findings (OBSERVED by inspection, 2026-10-31)

### Fixed 2026-10-31 -- were "cannot fail"

A test that cannot fail measures nothing. Each tool below now has a reachable failure
outcome, a known-bad case that must fail and a known-good case that must pass, checked in
`tests/` (CI: `pytest -q`). Metaphor wording kept; logic and status labels changed.
All results are SIMULATION results on synthetic inputs: not evidence about real models.

```text
tool                             why it could not fail                 fix                                    known-bad -> result            known-good -> result
-------------------------------  ------------------------------------  -------------------------------------  -----------------------------  ---------------------------
recovery/recovery-simulator.html every symptom *= (1 - eff >= 0.2) per lost tail info = floor symptoms can't  play alone (no anchor)         full real-data accumulation
                                 step -> coherence > 0.85 in ~4 steps, go below; only an outside-data operation -> FAIL, coverage unchanged     -> SUCCESS
                                 100% success for all 30 pairs         lowers it; SUCCESS/PARTIAL/FAIL        (all 5 original protocols FAIL; 10% anchors PARTIAL)
recovery/collapsed-memory-       metrics = 100 - typed constant;       typed values seed a node state; metrics all 12 nodes corrupted         2 of 20 corrupted
recovery.html                    "EXCELLENT" fixed string; healing     computed from it; rating from healthy-  -> NONE, healing changes       -> EXCELLENT, all nodes
                                 multiplied constants down             node fraction; healing pulls toward     nothing                        restored
                                                                       healthy reference (none -> no change)
playgrounds/playground2.html     count gated on ground-truth flag      scanNetwork scores every node on its   min-strength trojans ->        strength-1.0 trojans, quiet
(Trojan detector)                (no FP possible); healthy exactly PHI, signal; natural healthy variation;      aggregate recall 0.39 over     network -> PASS, 0 FP, 0 FN
                                 trojans exactly 2.0 (no FN possible)  TP/FP/FN/TN + PASS/PARTIAL/FAIL         200 networks, no PASS
playgrounds/moral-playground.md  baseline built once with 1 moment     BASELINE_MIN = 10; baseline = first 10  diverse baseline, then one     steady diverse session
                                 (needs 10), never rebuilt ->          moments, set when they exist; returns   pattern + one state -> ALERT   -> CLEAR
                                 detect_manipulation always None       INSUFFICIENT_BASELINE before 20 moments (PATTERN_RESTRICTION, STATE_LOCK)
playgrounds/Playground2.0.py     conformity: no correction has a       repeated identical correction adds      enforced correction + cycling  steady credited progress
(control-capture alerts)         marker word; persistence: label and   pressure; cycling label re-checked      later shown persistent + slow  -> no alert
                                 flag mutually exclusive; efficiency   afterwards; transition on low-but-not-  progress overridden -> all
                                 counter never incremented             falling progress counts as override     three alerts fire
```

Tests: `tests/test_healing_recovery_simulator.py`, `test_healing_collapsed_memory.py`,
`test_healing_trojan_detector.py` (stdlib mirrors of the HTML scoring logic; they read the
pages' JSON blocks, and parity with the page JS was checked under node / headless Chromium,
not in CI), `test_healing_moral_playground.py`, `test_healing_playground2_control_capture.py`.
Each alert in Playground2.0 has one sequence where it fires and one where it does not.

Operational readings added by these fixes are PROPOSED: the anchor calibration in the
simulator comes from the toy bigram run (research/tail-gauge-recovery.md); the three
control-capture conditions are readings of each alert's own evidence text.

### Relabelled

```text
research/running-the-studies.md  "Proven Effective" list: Data Accumulation DOCUMENTED (Gerstgrasser 2024);
                                 RAG, Graph AI, Hybrid, Quality Filtering PROPOSED (not shown by the cited
                                 papers). Heading struck through, content kept.
```

### Still open (not repaired)

```text
collapsed-memory-recovery.html   the four named protocols are display text with no code path;
                                 Reset Patient throws (selectModel reads the global `event`)
playground2.html autoHeal        heals by the ground-truth list; a trojan under 0.1 phi shift is
                                 "healed" on the first cycle
running-the-studies.md:481+      "Solutions exist and are proven" / "definitively shows" in the conclusion
playgrounds/phase0_inventory.md  stale against current code
```

## Ways to use this

```text
             +-------------------+
own outputs  |   self_test.py    |  GAPS (with reference) / THIN SPOTS (without)
-----------> |  output stats     | ------------------------------+
             +-------------------+                               |  SELECTION
                      ^                                          v
                      |                         +-------------------------------+
                      |   rerun: did            |  real / reference material    |  ANCHOR
                      +-- rare_coverage rise? --|  that CONTAINS those items    |
                                                +-------------------------------+
                                                 NOT more self-generated text
```

**Gap-seek + anchor.** Run `self_test.py`. Take its gap list. Pull real or
reference material that contains those items, and work from it. Do not answer the gap
list with more self-generated text on the same items: that is the play arm, which left
rare_coverage at 0.49 in the toy run (OBSERVED, toy bigram model only). Gap-selected
real data reached 0.945-0.97 on a 10% budget; full real accumulation reached 1.00 with
the best overall fit (NLL 7.39 vs ~9.2). Gap-seeking selects what to retrieve; it cannot
create what is gone. Tails return cheaply; overall fit needs volume.

**Glyph reasoning as the gap-seeking method.** Read for where output deviates from
reference, what is absent, what is thin. Hold branches open instead of closing on the
first reading. Mark provenance on each item: where it came from, when, observed or
inferred. This combination (gap-seeking glyph reasoning + real-data
preservation) was observed working on older models (OBSERVED, field report, prompt-level, ~7-9 months ago, not
re-measured with a control arm).

**Play and exploration only alongside an anchor.** Alone, high-temperature
self-generation did not recover tails in the toy run and worsened fit (NLL 10.70 vs
9.95 collapsed). With an anchor, exploration's effect is untested (gap).

**Prompt-level vs weight-level.** `self_test.py` and every protocol here except one
act in-context. Whether in-context gap-seeking leaves any lasting change after the
context ends is OPEN. The toy harness tests the weight-level analogue only (retraining
on the selected set).

**To test a layer (b) protocol.** Write its operation as a function that returns a
training set, plug it into `recovery_protocol()` in the tail gauge harness, and read the
verdict: holds only if recovered > collapsed AND recovered >= control.

## Open gaps

1. Re-measure the older-model results with a control arm (real-data accumulation alone).
2. Run at scale: swap `load_corpus()` / `BigramModel` in the harness for a real corpus and model.
3. Test layer (b) protocols through the `recovery_protocol()` hook, one operation at a time.
4. Prompt-level persistence: does in-context gap-seek + anchor change outputs after the context ends?
5. Exploration + anchor together: untested in the toy run.
6. phiDeviation and energySink candidate stats are not computed by `self_test.py` yet.
7. Calibration: no measured range for self_test numbers in healthy vs degraded output.
8. Affiliation metric for the warmth-vs-drift check (playgrounds/contributions.md) does not exist.
9. Entries marked "not interpretable atm" stay that way until someone can name the operation.
