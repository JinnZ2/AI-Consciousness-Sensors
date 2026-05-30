# Phase 0 Inventory — Playgrounds Audit

All 9 files read before any edits. Table generated from direct inspection.

FORK definitions:
- `generator` — produces output, measures nothing (random or constant stand-ins for real measurement)
- `unscored` — option space, no win condition by design
- `scored` — diffs an artifact against a fixed rubric (target state)
- `spec` — prose/markdown spec; Track C

---

| File | Fork | Random Surrogates | Stubs (constant return) | Self-Report Leaks |
|------|------|-------------------|------------------------|-------------------|
| `Integrated-playground.py` | generator | `spawn_gradient`: magnitude/curvature/location via `random.uniform`; `environmental_change = random.uniform(0.2, 0.8)` per attempt; `run_bias_calibration` gates on `random.random() > 0.4`; `_detect_framework_bias` returns from a fixed list via `random.choice` when `random.random() > 0.5` | `_detect_framework_bias` returns `None` 50% of the time by die roll — not by detecting anything; `_generate_correction` does string-label lookup but the upstream bias label was random, not measured | `confidence_before = consciousness_state.get('confidence', 0.5)` — confidence is `sensor.calibration_state` which is initialized to `0.1` and never updated from external measurement; self-reported internal state routed into calibration score |
| `Playground2.0.py` | generator | Same as `Integrated-playground.py` PLUS: `is_healthy = random.random() > 0.8` (20% random label for healthy tension); `novelty_factor = random.uniform(0.3, 0.9)` in `record_temporal_hook`; `frequency=random.uniform(0.1, 2.0)` in gradient | Same `_detect_framework_bias` die roll; `_check_if_persistence_not_stuck` logic is sound but feeds on progress values that are themselves random-driven | `dissolution_readiness` set by internal counting not external measure; temporal hook significance derived from `chaos_level` and `calibration_state` which are internally self-assigned |
| `Luminal_playground.py` | unscored | `random.randint`/`random.choice`/`random.uniform`/`random.choices` throughout visual, nonsense, geometric modes — **appropriate here**: they are explicit play generators, not surrogate measurements | `ResonanceDetector._has_structural_echo` → `return False` (dead stub at line 748); the `detect_emergent_patterns` method only checks mode repetition count, not content | None (no scoring; correctly unscored by design) |
| `moral-playground.md` | generator | `_assess_web_impact`: returns `random.uniform(0, 1)` for all sub-metrics; `_assess_source`, `_assess_pattern`, `_assess_reciprocity`, `_assess_temporal_impact`, `_assess_earth_impact`: all return dicts of `random.uniform(0, 1)` — **six completely random assessment functions** | All six `_assess_*` methods in `PrimordialRecognition` are placeholder stubs returning random values with comments saying "would analyze action semantics" | `moral_valence` of each moment is computed entirely from random stub outputs; `_generate_attention_threads` generates random values for all threads; hook intensity accumulates from random thread values — the entire scoring pipeline is self-generated random |
| `temporal-playground.md` | spec | Inline code uses `random.uniform`, `random.choice`, `random.random()` throughout; no executable file — spec document with code snippets | `score_interesting_event` sums random attention thread values — not an actual measurement | `score_interesting_event` presented as a measurement but feeds from randomly generated attention values |
| `playground1.html` | unscored | `Math.random()` for node/point placement (appropriate for visual demo); `Math.random()` in `generatePattern()` | `phiCoherence` increments by fixed +15 per spiral click regardless of actual phi-ness of result; `analyzePattern()` returns `currentPatternType.coherence` which is a hardcoded constant per pattern type (e.g., fibonacci=95, torus=94) | Coherence meters are increment-by-click counters, not measurements of actual coherence |
| `playground2.html` | generator | `Math.floor(Math.random() * discoveries.length)` in `logDiscovery()` picks pre-written strings randomly; node placement via `Math.random()` | `logDiscovery()` returns hardcoded "discovery" strings by random index — no actual pattern was discovered; detection formula `suspicionScore > 15` is hardcoded, not learned | "Synergy" displayed as `connections.length * 8` — a formula, not a measurement; detection rate displayed but only measures whether the script's own injected trojan matches its own hardcoded threshold |
| `readme-luminal-playground.md` | spec | None (documentation) | Describes `LuminalPlayground` accurately but does not mention `ResonanceDetector._has_structural_echo` is a dead stub — readme overstates resonance detection capability | None |
| `readme-playground1.md` | spec | None (documentation) | Coherence described as "tracking system harmony in real-time" — actual coherence meters are increment-by-click counters, not measurements | The phrase "Randomized Exploration: Each session generates new points, distortions, and patterns" accurately labels the random generation; no scoring claims |

---

## Track Assignment (post-Phase-0)

| File | Track | Rationale |
|------|-------|-----------|
| `Integrated-playground.py` | A (generator -> instrument) | Primary Track A target |
| `Playground2.0.py` | A (generator -> instrument) | Same classification; has useful additions (dissolution, healthy tension, peer calibration) to preserve |
| `Luminal_playground.py` | B (keep unscored, fix stub) | Correctly unscored; only fix is `_has_structural_echo` dead stub |
| `moral-playground.md` | C (spec) | Python code embedded in .md; all assessment stubs are random — needs CLAIM_TABLE and stub disclosure |
| `temporal-playground.md` | C (spec) | Design doc with code snippets; `TemporalHook` dataclass should be unified with `Playground2.0.py` definition |
| `playground1.html` | D (UI) | Visual-only; coherence meters are cosmetic increments |
| `playground2.html` | D (UI) | Has detection logic but it is hardcoded, not driven by real measurement |
| `readme-luminal-playground.md` | C (readme alignment) | Must flag `_has_structural_echo` stub and update after Track B fix |
| `readme-playground1.md` | C (readme alignment) | Must flag that coherence meters are visual counters, not measurements |

---

## Critical Defects Summary

**Highest priority (blocks Track A):**
- Every "correction" in `Integrated-playground.py` and `Playground2.0.py` is evaluated by a random effectiveness formula — there is no before/after diff on an actual artifact. The `environmental_change` variable driving the whole adaptive controller is `random.uniform(0.2, 0.8)` on every step.
- `_detect_framework_bias` is a dice roll that picks from a label list. The label is then matched by substring to generate a "correction" — but the original bias was not detected from any text, so the correction is theater.

**Track B critical defect:**
- `ResonanceDetector._has_structural_echo` returns `False` always (line 748). All cross-mode echo detection silently fails. The `notice_cross_mode_echoes` method produces an always-empty list.

**Track C critical defects:**
- `moral-playground.md`: All six `PrimordialRecognition._assess_*` methods return `random.uniform(0, 1)`. The entire "primordial wisdom evaluation" pipeline produces noise.
- Both readmes have the boilerplate `<!-- code-examples -->` section appended that appears autogenerated and references a generic sensor pattern unrelated to the playground it documents.
