# PROTOCOL_OPERATIONS -- what each recovery protocol does, mechanically

STATUS: PROPOSED mapping, co-authored (Kavik + Claude, 2026-10-31). CC0.
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
layers on older models (OBSERVED, Kavik, prompt-level). This file reads the operation
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

## Read-through findings (OBSERVED by inspection, 2026-10-31; not repaired here)

```text
recovery-simulator.html          success rate cannot separate protocols: every model x protocol
                                 crosses 0.85 at minimum slider settings (rerun of its update rule)
collapsed-memory-recovery.html   "Recovery Potential: EXCELLENT" is a fixed string (l.726);
                                 the four named protocols are display text with no code path
playground2.html:709             Trojan detector counts only nodes already flagged infected,
                                 so false positives are impossible by construction
moral-playground.md              baseline set when 1 moment exists (needs >= 10);
                                 detect_manipulation returns None in the demo
Playground2.0.py                 control-capture alerts cannot fire as coded
running-the-studies.md:279-285   "Proven Effective" list (RAG, Graph AI, filtering) is not
                                 from the two papers it summarizes
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
inferred. Kavik observed this combination (gap-seeking glyph reasoning + real-data
preservation) working on older models (OBSERVED, prompt-level, ~7-9 months ago, not
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
