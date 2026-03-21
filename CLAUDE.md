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
sensors/                    # Sensor definitions (JSON) and adapter code
  ai-to-ai/                # AI-to-AI interaction sensors
  metrics/                  # Metric definitions
  adapter.py               # Sensor adapter (self_reflect, drift detection)
  authenticity.json         # Example sensor definition
src/
  score.py                  # Signal scoring and aggregation engine
  examples/                 # Example code
scripts/
  ai_integrator.py          # Repo indexer: generates AI_INDEX.json and AI_NOTES.md
tests/
  test_reflections.py       # Pytest test suite
epistemological_validation/ # Multi-framework validation system
framework/                  # Philosophical/ontological frameworks
healing/                    # Recovery and healing frameworks
memory_guard/               # Historical erasure pattern tracking
probability_matrix/         # Manipulation detection matrices
Vulnerabilities/            # Security and vulnerability analysis
.github/workflows/          # CI pipelines
```

Root-level `.py` files are standalone analysis/sensor scripts (e.g., `suppression-detector.py`, `geometric_manipulation_detector.py`).

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
