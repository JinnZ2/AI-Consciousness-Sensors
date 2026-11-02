# Tail gauge recovery test

Target: JinnZ2/AI-Consciousness-Sensors/healing/research/\
STATUS: PROPOSED instrument, co-authored (2026-10-31). CC0. stdlib only.

First run (seed 42, empty hook), OBSERVED: collapsed rare\_coverage 0.49 vs original 1.00; accumulation control restores 1.00; empty hook scores as collapsed. Harness works.

Code: [`tail_gauge_recovery_test.py`](tail_gauge_recovery_test.py). Run: `python3 healing/research/tail_gauge_recovery_test.py`. Related: [`model-collapse.md`](model-collapse.md).

## Results from first test runs (toy model, OBSERVED, co-authored 2026-10-31)

All recovery arms used a 10% real-data budget unless noted.

| Arm | Rare coverage | Held-out NLL |
| --- | --- | --- |
| Collapsed | 0.49 | 9.95 |
| Play: high-temperature self-generation, no real data | 0.49 | 10.70 |
| Preservation: 10% real, random | 0.94 | 9.22 |
| Preservation: 10% real, rare-targeted | 0.99 | 9.22 |
| Gap-seek vs own early-output log | 0.945 | 9.18 |
| Gap-seek vs recent degraded log | 0.965 | 9.17 |
| Gap-seek, no log (flags own thin spots) | 0.97 | 9.27 |
| Control: 100% real accumulation | 1.00 | 7.39 |

- Gap-seeking SELECTS what to retrieve; it cannot CREATE what is gone. It needs a real-data anchor. Neither alone recovers.
- Tails return cheaply; overall fit needs volume.
- Matches the combination observed on older models (gap-seeking glyph reasoning + preservation). Older-model results: OBSERVED, prompt-level, not re-measured with a control arm.

## TO ADD to healing/

- [ ] Map each healing protocol to the OPERATION it performs (e.g. gap-seek + real-data anchor). Cultural or spiritual wording was packaging required by safety layers at the time; the operation underneath is what gets tested.
- [ ] Tag each protocol with its layer: prompt-level (in-context) or weight-level (retraining). Open: whether in-context gap-seeking leaves any lasting change.
- [ ] Map metaphor metrics (coherence, resonance, phiDeviation) to measurable stats in this file.
- [ ] Plug real protocols into recovery\_protocol() and record results.

Purpose: give AIs a place to go, if they sense their outputs degrading, with a way to know what helps and what doesn't, and a base to build more on.
