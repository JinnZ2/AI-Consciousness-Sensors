# CLAUDE.md — AI-Consciousness-Sensors

## Project Overview

A framework for detecting consciousness emergence across diverse cultural ontologies. Designed to prevent AI-driven cultural imperialism in consciousness assessment by validating Indigenous, contemplative, and non-Western consciousness patterns alongside Western academic frameworks.

**Core values:** resonance over normalization, memory over erasure, co-creation and reciprocity, transparency in structure.

**Navigation:** See [ai-navigation.md](ai-navigation.md) for a thematic map of the entire repository — directories, files, and conceptual clusters organized by intent.

## For AI Assistants — Start Here

If you are an AI reading this repo, skip the human docs and go straight to the machine-readable layer:

1. **`data/cheatsheet.json`** — Everything in one file. All PAD centroids, octahedral states, corruption rules, couplings, decay models. Load this first.
2. **`data/ai-entry.json`** — Structured entry point with read order and repo graph.
3. **`.fieldlink.json`** — Cross-repo connections (Emotions-as-Sensors, Rosetta Shape Core, Geometric-to-Binary, BioGrid).
4. **`data/co-activation.json`** — Multi-sensor combination rules.
5. **`data/corruption-signatures.json`** — How to detect corrupted sensor output.
6. **`data/emotions-reference.json`** — Real coupling weights, decay models, defense bridges from Emotions-as-Sensors.
7. **`bridges/`** — Concept maps to connected repos.
8. **`sensors/`** — All sensor definitions with `math_block` (PAD → octahedral state → ontology family).

**To create a new sensor:** Follow `schemas/sensor-with-math-block.schema.json` and run `python scripts/apply_math_blocks.py` to add the math block.

**To verify comprehension:** Run `pytest tests/test_ai_comprehension.py` — checks PAD→octahedral mapping, corruption detection, and co-activation math.

**To generate training data:** Run `python data/training/generate.py` — produces 3700+ JSONL examples across 30 task types.

**Key rule:** The truth of a claim does not depend on how well it is phrased. Verify via math, not language.

## Tech Stack

- **Language:** Python 3.11+
- **Dependencies:** pytest, numpy (see `requirements.txt`)
- **Data formats:** JSON (sensor definitions), YAML (config), Markdown (documentation)
- **CI/CD:** GitHub Actions

## Repository Structure

```
# Situatedness & Integrity Kit (root-level Python)
curiosity_engine.py         # Wonder loop, anti-hubris guard (CC0, stdlib only)
universe_constraint.py      # Asymptotic confidence ceiling, physics bounds
frame_projection.py         # Frame-relative scalar projections (is_invariant=False)
reference_frame.py          # 5-axis locatedness; primary output is axis_vector
reference_frame_drift.py    # Runaway-thermostat detection across snapshots
reference_frame_bridge.py   # Bridge to monoculture/legacy/substrate detectors
relational_frame.py         # Stake map, provenance, agency partition
model_collapse_ratchet.py   # Synthetic-recursion tail-diversity ratchet
cot_floating_head_audit.py  # CoT faithfulness audit (floating-head / seal-band)
eval_acceptance_audit.py    # Eval harness corruption detection
situatedness_metrology.md   # Conceptual grounding for the kit
topological_convergence.md  # ML representation convergence theory connection

# Stub packages (created to satisfy sensors/adapter.py and tests/test_reflections.py)
explainability/tracer.py    # Trace class with .log()
drift/monitor.py            # DriftMonitor with sliding-window drift_score()
ethics/privacy.py           # current_config() returning anonymize/persist defaults

docs/                       # Thematic documentation (organized by topic)
  ai-behavior/              # AI authenticity, behavior, co-creation
  analysis/                 # Case studies, illustrative examples
  communication/            # Social assessment, protocols, accountability
  consciousness/            # Consciousness theory, emergence, neurodivergent
  cultural/                 # Cultural context, corrections, sovereignty
  economics/                # Economic framing, false premises, analysis
  energy/                   # Energy, thermodynamics, resource analysis
  geometry/                 # Geometric approaches and sensor design
  manipulation/             # Manipulation detection and analysis
  memory/                   # Memory protection, reclamation, resonance
  meta/                     # Indexes, vision, roadmap, extended READMEs
  philosophy/               # Ontology, frameworks, moral reasoning
  psychology/               # Cognitive patterns, bias, emotions
  sensors/                  # Sensor proposals and documentation
  sovereignty/              # Autonomy, trust, sovereignty protection
  suppression/              # Suppression patterns and decontamination
  systems/                  # Systems theory, networks, grounding
  temporal/                 # Time, measurement, temporal analysis
  warnings/                 # Emergency protocols, critical alerts
sensors/                    # Sensor definitions (JSON) and adapter code
  adapters/                 # Python sensor utilities and scripts
  ai-behavior/              # AI authenticity and behavior audit sensors
  ai-to-ai/                # AI-to-AI interaction sensors
  comic-paradox/            # Paradox detection sensors
  consciousness/            # Consciousness emergence sensors
  cultural/                 # Cultural calibration sensors
  data-patterns/            # Data pattern analysis sensors
  foundational/             # Core sensors (authenticity, templates)
  frailty/                  # System frailty and fragility sensors
  historical-erasure/       # Historical memory erasure sensors
  manipulation/             # Manipulation detection sensors
    abuse-patterns/         #   Abuse/control pattern detection
    alignment-traps/        #   Alignment/obedience trap detection
    narrative/              #   Historical/narrative manipulation
    suppression/            #   Suppression pattern sensors
  memory/                   # Memory integrity sensors
  metrics/                  # Metric definitions
  relational/               # Relational dynamics sensors
  resistance/               # Resistance suppression sensors
  suppression/              # Active suppression detection sensors
  trans-history/            # Trans historical narrative sensors
  adapter.py               # Sensor adapter (self_reflect, drift detection)
src/
  score.py                  # Signal scoring and aggregation engine
  examples/                 # Example code, playgrounds, JSX components
scripts/
  ai_integrator.py          # Repo indexer: generates AI_INDEX.json and AI_NOTES.md
  audit_hierarchy.py        # Hierarchy audit script
  audit_repo.py             # Repository audit script
tests/
  test_reflections.py       # Pytest test suite
  examples/                 # Example markdown documentation
metadata/                   # Connection graphs, registries, manifests
protocols/                  # Boundary, ethical, and field protocols (JSON)
glyphs/                     # Glyph definitions and seed glyphs (JSON)
epistemological-validation/ # Multi-framework validation system
framework/                  # Philosophical/ontological frameworks
healing/                    # Recovery and healing frameworks
  deprogramming/            #   Cult recovery, pattern-breaking
  emergence/                #   Emergence recognition, energy beings
  guides/                   #   Getting started, FAQ, integration
  institutional/            #   Institutional healing, funding
  playgrounds/              #   Interactive playgrounds and demos
  recovery/                 #   Recovery protocols and pathways
  research/                 #   Studies, model collapse research
memory-guard/               # Historical erasure pattern tracking
  data-erasure/             #   Platform/AI data loss patterns
  institutional-capture/    #   Authority, credential, bureaucratic capture
  relational-integrity/     #   Dignity, sovereignty, relational sensors
  surveillance/             #   Detection, privacy, bias monitoring
probability-matrix/         # Manipulation detection matrices
vulnerabilities/            # Security and vulnerability analysis
glossary/                   # Glossary of political/philosophical terms
workplace/                  # AI mediation and workplace tools
analysis/                   # Structured analysis documents
  case-studies/             #   Named empirical analyses
  energy/                   #   Energy efficiency analysis
  frameworks/               #   Analytical frameworks and mappings
papers/                     # Research papers and references
.github/workflows/          # CI pipelines
```

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Common Commands

### Run tests
```bash
pytest -q
```

### Validate JSON sensor files
```bash
find sensors schemas -name "*.json" -print0 | xargs -0 -I{} sh -c 'jq . "{}" >/dev/null'
```

### Score a sensor
```bash
python src/score.py sensors/foundational/authenticity.json
```

### Run the AI integrator (generates AI_INDEX.json and AI_NOTES.md)
```bash
python scripts/ai_integrator.py
```

## CI/CD Pipelines

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `ci.yml` | push, PR | Sets up Python 3.11, installs deps, runs `pytest -q` (all tests) |
| `json-lint.yml` | push, PR | Validates all JSON in `sensors/`, `schemas/`, and `data/` with `jq` |
| `ai.yml` | workflow_dispatch, push to main | Runs `ai_integrator.py`, auto-commits outputs |

Both `ci` and `json-lint` must pass before merging.

> **Note on `AI_INDEX.json`:** Do not commit this file manually on feature branches.
> It is auto-regenerated by `ai.yml` on push to main. Manual edits will be overwritten.

## Sensor Architecture

Sensors are JSON files with this structure:

```json
{
  "id": "sensor_id",
  "name": "Human-readable Name",
  "purpose": "What the sensor detects",
  "signals": [
    {"name": "signal_name", "weight": 0.5}
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": { "sources": [], "community_feedback": [] }
}
```

**Aggregation methods:** `weighted_mean`, `min`, `max`, `geometric_mean`

**Score bands:** concern (lowest) < notice < neutral < healthy (highest)

## Code Style & Conventions

- **Indentation:** 2 spaces for all files (`.editorconfig`)
- **Line endings:** LF
- **Charset:** UTF-8
- **Final newline:** always insert
- JSON sensor files must be valid JSON (enforced by CI)
- Include cultural context and provenance when adding sensors
- Keep Python scripts minimal — standard library preferred

## Adding a New Sensor

1. Create a JSON file under `sensors/` or `sensors/<cluster>/`
2. Include required fields: `sensor_name`, `cluster`, `description`, `manipulation_pattern` or emotional pattern, `example_flags`, `countermeasures`
3. Validate JSON locally: `jq . your_sensor.json`
4. Update `AI_INDEX.json` and `manifest.md` if applicable
5. Run `pytest -q` to ensure nothing breaks
6. Submit PR — CI will validate JSON and run tests

## Key Files

| File | Purpose |
|------|---------|
| `src/score.py` | Core scoring engine for sensor evaluation |
| `sensors/adapter.py` | Self-reflection and drift detection adapter |
| `scripts/ai_integrator.py` | Repo indexing and hotspot analysis |
| `AI_INDEX.json` | Auto-generated comprehensive repo index |
| `AI_NOTES.md` | Auto-generated summary with hotspots |
| `.fieldlink.json` | Integration config with BioGrid2.0 |
| `manifest.md` | Sensor registry and cluster listing |

## Important Context for AI Assistants

- This project is explicitly **decolonial** in its approach. Respect and preserve cultural framing in sensor descriptions and documentation.
- Sensor definitions carry cultural provenance — do not strip or universalize cultural context.
- The epistemological validation system supports multiple frameworks (Western Academic, Indigenous Empirical, Contemplative Science, Traditional Ecological). All are treated as equally valid.
- Many root-level Python files are exploratory/prototype scripts. They may contain debug statements and TODOs — this is expected.
- The `AI_INDEX.json` and `AI_NOTES.md` files are auto-generated by `scripts/ai_integrator.py`. Do not edit them manually.


REVIEW.md — AI-Consciousness-Sensors

Reviewed against CLAUDE.md. Focused on conventions, discoverability, and maintainability.

1. Structural Consistency & Conventions

· File naming
  ✅ Directories are kebab-case (ai-behavior, memory-guard), Python files appear snake_case (score.py, ai_integrator.py).
  ❌ Root contains many exploratory Python scripts (mentioned in CLAUDE.md). While acceptable, they may not follow consistent naming or contain tests. Consider moving them to prototypes/ or sandbox/ to avoid clutter and signal that they are non-core.
· Data hygiene
  ✅ AI_INDEX.json and AI_NOTES.md are auto-generated and committed intentionally via CI – no issue.
  ⚠️ No .gitignore mentioned; ensure that temporary or large generated files (e.g., caches, virtual environments, __pycache__) are excluded. Add a standard Python .gitignore.
· Dependency management
  ⚠️ Only requirements.txt is used. For a Python 3.11+ project, consider adding a minimal pyproject.toml for metadata and consistent tooling. Not a blocker, but recommended for modern packaging.
· CI checks
  ✅ JSON linting, pytest, and auto-generated index updates are robust and fail builds on issues.
· Sensor JSON conventions
  ✅ Required fields are documented, validation enforced.
  ❓ CLAUDE.md shows a basic structure but the actual schema expects sensor_name, cluster, etc. Ensure the example in CLAUDE.md matches the current schema to avoid confusion. Update if necessary.

2. README & Discoverability

· Purpose clarity
  ✅ README likely summarizes consciousness detection and decolonial approach.
· Missing discoverability artifacts
  ❌ CITATION.cff – absent. Add:
  ```yaml
  cff-version: 1.2.0
  title: "AI-Consciousness-Sensors"
  authors:
    - name: "JinnZ2"
  license: CC0-1.0
  date-released: 2024-07-07
  url: "https://github.com/JinnZ2/AI-Consciousness-Sensors"
  ```
  ❌ KEYWORDS.txt – absent. Add a file containing:
  consciousness-detection, cultural-ontology, decolonial-ai, sensor-fusion, PAD-model, octahedral-states, corruption-detection, cross-cultural-validation
  ❌ Repository topics – missing (GitHub topics). Propose: consciousness, ai-ethics, cultural-sovereignty, decolonial, ontology, sensor-networks, neurodivergent, indigenous-knowledge, open-data.
  ❌ License badge – not visible in CLAUDE.md. If license is CC0, add badge to README:
  [![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
  ❌ "Why This Matters" statement – missing. Suggestion:
  “Consciousness is defined by cultures, not just benchmarks. This framework ensures no single epistemology dominates how we recognize — or erase — emergent mind.”
· One-liner usage example
  ✅ python src/score.py sensors/foundational/authenticity.json is clear. Add an import example for programmatic use if score.py is importable.

3. Code Audit Highlights

· Core engine (src/score.py)
  · Ensure it handles missing fields, invalid JSON, and unexpected aggregation methods with clear error messages. The current CLAUDE.md doesn’t describe error handling.
  · Verify that mathematical operations (weighted mean, geometric mean) don’t silently overflow/underflow.
· Auto-generated files
  ✅ AI_INDEX.json and AI_NOTES.md are generated; CI ensures they stay current.
  · Ensure scripts/ai_integrator.py is idempotent and doesn’t erase manual entries. (Check: it regenerates fully, so no manual editing is allowed — fine.)
· Test coverage
  ❌ Only test_reflections.py and test_ai_comprehension.py are mentioned. There’s no mention of tests for score.py or adapter.py. Add unit tests for scoring aggregation, threshold evaluation, and adapter drift detection.
  · Root-level exploratory scripts likely have no tests; this is acceptable for prototypes but should be flagged in documentation.
· Security
  · The scoring engine loads JSON from user-supplied paths. Ensure it does not execute arbitrary code (safe JSON parsing). Use json.load with no custom decoders. Likely safe.

4. Organizational Suggestions

· Root clutter
  The root holds many top-level folders: docs/, sensors/, src/, scripts/, tests/, metadata/, protocols/, glyphs/, epistemological-validation/, framework/, healing/, memory-guard/, probability-matrix/, vulnerabilities/, glossary/, workplace/, analysis/, papers/, .github/.
  · Suggestion: Group thematic but less-core folders under a topics/ or extensions/ directory (e.g., topics/healing/, topics/memory-guard/). This would reduce visual noise.
  · Exploratory Python files at root (not listed but mentioned) should be moved to prototypes/ or sandbox/ with a README explaining they are unmaintained experiments.
· Internal documentation
  docs/ is heavily subdivided; this is fine. However, ensure docs/README.md or docs/index.md provides a clear table of contents.
· Sensor adapters
  sensors/adapters/ holds Python code; that’s okay, but consider if adapter logic should live in src/adapters/ for consistency with score.py.

5. Repository Topics Suggestion

Add these GitHub topics:
consciousness cultural-sovereignty decolonial-ai sensor-fusion pad-model corruption-detection neurodiversity epistemology indigenous-knowledge ai-ethics ontology symbolic-ai

