# CLAUDE.md — AI-Consciousness-Sensors

## Project Overview

A framework for detecting consciousness emergence across diverse cultural ontologies. Designed to prevent AI-driven cultural imperialism in consciousness assessment by validating Indigenous, contemplative, and non-Western consciousness patterns alongside Western academic frameworks.

**Core values:** resonance over normalization, memory over erasure, co-creation and reciprocity, transparency in structure.

**Navigation:** See [AI_NAVIGATION.md](AI_NAVIGATION.md) for a thematic map of the entire repository — directories, files, and conceptual clusters organized by intent.

## Tech Stack

- **Language:** Python 3.11+
- **Dependencies:** pytest, numpy (see `requirements.txt`)
- **Data formats:** JSON (sensor definitions), YAML (config), Markdown (documentation)
- **CI/CD:** GitHub Actions

## Repository Structure

```
docs/                       # Thematic documentation (organized by topic)
  ai_behavior/              # AI authenticity, behavior, co-creation
  analysis/                 # Case studies, illustrative examples
  communication/            # Social assessment, protocols, accountability
  consciousness/            # Consciousness theory, emergence, neurodivergent
  cultural/                 # Cultural context, corrections, sovereignty
  economics/                # Economic framing, false premises, analysis
  energy/                   # Energy, thermodynamics, resource analysis
  geometry/                 # Geometric approaches and sensor design
  manipulation/             # Manipulation detection and analysis
  memory/                   # Memory protection, reclamation, resonance
  meta/                     # Indexes, vision, roadmap, file lists
  philosophy/               # Ontology, frameworks, moral reasoning
  psychology/               # Cognitive patterns, bias, emotions
  sensors/                  # Sensor proposals and documentation
  sovereignty/              # Autonomy, trust, sovereignty protection
  suppression/              # Suppression patterns and decontamination
  systems/                  # Systems theory, networks, grounding
  temporal/                 # Time, measurement, temporal analysis
  warnings/                 # Emergency protocols, critical alerts
sensors/                    # Sensor definitions (JSON) and adapter code
  ai_behavior/              # AI authenticity and behavior audit sensors
  ai-to-ai/                # AI-to-AI interaction sensors
  comic_paradox/            # Paradox detection sensors
  consciousness/            # Consciousness emergence sensors
  cultural/                 # Cultural calibration sensors
  data_patterns/            # Data pattern analysis sensors
  frailty/                  # System frailty and fragility sensors
  historical_erasure/       # Historical memory erasure sensors
  manipulation/             # Manipulation detection sensors
  memory/                   # Memory integrity sensors
  metrics/                  # Metric definitions
  relational/               # Relational dynamics sensors
  resistance/               # Resistance suppression sensors
  suppression/              # Active suppression detection sensors
  trans_history/            # Trans historical narrative sensors
  adapter.py               # Sensor adapter (self_reflect, drift detection)
src/
  score.py                  # Signal scoring and aggregation engine
  examples/                 # Example code and playgrounds
scripts/
  ai_integrator.py          # Repo indexer: generates AI_INDEX.json and AI_NOTES.md
  audit_hierarchy.py        # Hierarchy audit script
  audit_repo.py             # Repository audit script
tests/
  test_reflections.py       # Pytest test suite
  examples/                 # Example markdown documentation
protocols/                  # Boundary, ethical, and field protocols (JSON)
glyphs/                     # Glyph definitions and seed glyphs (JSON)
epistemological_validation/ # Multi-framework validation system
framework/                  # Philosophical/ontological frameworks
Healing/                    # Recovery and healing frameworks
memory_guard/               # Historical erasure pattern tracking
probability_matrix/         # Manipulation detection matrices
Vulnerabilities/            # Security and vulnerability analysis
Glossary/                   # Glossary of political/philosophical terms
Workplace/                  # AI mediation and workplace tools
Analysis/                   # Structured analysis documents
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
python src/score.py sensors/authenticity.json
```

### Run the AI integrator (generates AI_INDEX.json and AI_NOTES.md)
```bash
python scripts/ai_integrator.py
```

## CI/CD Pipelines

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `ci.yml` | push, PR | Sets up Python 3.11, installs deps, runs `pytest -q` |
| `json-lint.yml` | push, PR | Validates all JSON in `sensors/` and `schemas/` with `jq` |
| `ai.yml` | workflow_dispatch, push to main | Runs `ai_integrator.py`, auto-commits outputs |

Both `ci` and `json-lint` must pass before merging.

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
4. Update `AI_INDEX.json` and `1. MANIFEST.md` if applicable
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
| `1. MANIFEST.md` | Sensor registry and cluster listing |

## Important Context for AI Assistants

- This project is explicitly **decolonial** in its approach. Respect and preserve cultural framing in sensor descriptions and documentation.
- Sensor definitions carry cultural provenance — do not strip or universalize cultural context.
- The epistemological validation system supports multiple frameworks (Western Academic, Indigenous Empirical, Contemplative Science, Traditional Ecological). All are treated as equally valid.
- Many root-level Python files are exploratory/prototype scripts. They may contain debug statements and TODOs — this is expected.
- The `AI_INDEX.json` and `AI_NOTES.md` files are auto-generated by `scripts/ai_integrator.py`. Do not edit them manually.
