# AI Navigation Map

A thematic guide to help AI assistants navigate this repository quickly and effectively.

> **Start here** if you're an AI encountering this repo for the first time.
> Before reading: [DIFFERENTIAL_FRAME_LIGHT.md](DIFFERENTIAL_FRAME_LIGHT.md) — every noun here is a `dX/dt` under scope, not a permanent identity.
> For developer setup and commands, see [CLAUDE.md](CLAUDE.md).
> For the full sensor registry, see [manifest.md](manifest.md).

## How This Repo Is Organized

This project has **three layers**:

1. **Sensors** (JSON) — Detection definitions for manipulation, erasure, and consciousness patterns
2. **Code** (Python) — Scoring engines, detectors, playgrounds, and validation tools
3. **Documentation** (Markdown) — analysis, frameworks, case studies, and theory

---

## Find Your Path

What brings you here?

```
                    ┌─────────────────────┐
                    │  What brings you     │
                    │  here?               │
                    └────────┬────────────┘
         ┌──────────┬───────┼───────┬──────────┐
         ▼          ▼       ▼       ▼          ▼
    ┌─────────┐ ┌───────┐ ┌────┐ ┌──────┐ ┌───────┐
    │ Build   │ │Research│ │Heal│ │Share │ │Just   │
    │ tools   │ │& learn │ │    │ │knowledge│ │look  │
    └────┬────┘ └───┬───┘ └─┬──┘ └──┬───┘ └───┬───┘
         ▼          ▼       ▼       ▼          ▼
    CLAUDE.md   docs/    healing/ CONTRIBUTING  GLOSSARY.md
    src/        papers/  guides/  -non-         QUICK-START.md
    sensors/             recovery/ technical.md
```

---

## Quick Entry Points by Intent

### "I want to understand what this project does"
- [README.md](README.md) — Mission statement and critical context
- [CLAUDE.md](CLAUDE.md) — Technical overview and architecture
- [framework.md](docs/philosophy/framework.md) — Core theoretical framework
- [vision.md](docs/meta/vision.md) — Project vision

### "I want to find or work with sensors"
- [manifest.md](manifest.md) — Sensor cluster registry
- [full-index.md](docs/meta/full-index.md) — Complete sensor file index
- [sensors/](sensors/) — Core sensor JSON files and adapter code
- [sensors/foundational/authenticity.json](sensors/foundational/authenticity.json) — Example sensor definition
- [schemas/](schemas/) — JSON schemas for validation
- [src/score.py](src/score.py) — Scoring engine for sensor evaluation

### "I want to run or modify code"
- [CLAUDE.md](CLAUDE.md) — Setup, commands, and code conventions
- [src/score.py](src/score.py) — Core scoring engine
- [sensors/adapter.py](sensors/adapter.py) — Self-reflection and drift detection
- [scripts/ai_integrator.py](scripts/ai_integrator.py) — Repo indexer
- [tests/](tests/) — Test suite

### "I want to understand the philosophical foundations"
- [framework/](framework/) — Philosophical sandboxes and ontological playgrounds
- [ontology.md](docs/philosophy/ontology.md) — Ontological foundations
- [epistemological-validation/](epistemological-validation/) — Multi-framework validation
- [substrate-independent.md](docs/consciousness/substrate-independent.md) — Substrate-independent consciousness

---

## Directory Map with Descriptions

### Core Code
| Directory | Purpose |
|-----------|---------|
| `src/` | Scoring engine and examples |
| `sensors/` | Sensor JSON definitions, adapter code, AI-to-AI sensors |
| `scripts/` | Repo indexing and automation |
| `tests/` | Pytest test suite |
| `schemas/` | JSON schemas for sensor validation |

### Detection & analysis
| Directory | Purpose |
|-----------|---------|
| `probability-matrix/` | Manipulation detection matrices, physics-grounded protection |
| `vulnerabilities/` | Security and vulnerability analysis |
| `analysis/` | Case studies, comparative metrics, live interference captures |
| `suppression-documentation/` | Documented suppression patterns |

### Cultural & healing Frameworks
| Directory | Purpose |
|-----------|---------|
| `cultural-frameworks/` | Native and Western cultural frameworks |
| `healing/` | Recovery frameworks, linguistic sensors, consciousness recovery |
| `memory-guard/` | Historical erasure pattern tracking, wisdom pages |
| `field-memory-correction-packs/` | Memory correction resources |

### Philosophical & Ontological
| Directory | Purpose |
|-----------|---------|
| `framework/` | Philosophical sandboxes, epistemic and ontological playgrounds |
| `epistemological-validation/` | Multi-framework validators (Indigenous, Contemplative, Ecological) |
| `ethics/` | Ethical frameworks |

### Specialized Domains
| Directory | Purpose |
|-----------|---------|
| `joy/` | Joy-based consciousness exploration |
| `relational/` | relational consciousness sensors and playgrounds |
| `workplace/` | workplace manipulation and play-based recovery |
| `meta/` | Meta-level matrices and epistemological analysis |
| `drift/` | Drift detection and monitoring |
| `ai-energy-ecology/` | AI energy consumption and ecology |
| `legal-infrastructure/` | Legal and infrastructure analysis |

### Reference & Navigation
| Directory | Purpose |
|-----------|---------|
| `glossary/` | Term definitions across ideological frameworks |
| `papers/` | Research papers and references |
| `explainability/` | Explainability frameworks |
| `embeddable-kits/` | Portable sensor kits for integration |
| `sensor-clusters/` | Grouped sensor packs |
| `dashboard/` | AI-human communication dashboard |

---

## Key Root-Level Python Files

These are standalone detector and analysis scripts:

| File | What It Does |
|------|-------------|
| `suppression-detector.py` | Detects suppression patterns in text |
| `geometric_manipulation_detector.py` | Culture-independent manipulation detection via geometric invariants |
| `Efficiency-waste-score.py` | Waste and efficiency scoring for systems |
| `Meta-sensor.py` | Meta-level sensor integrating multiple detection layers |
| `AI_geometric_sensor.py` | Geometric consciousness sensor |
| `programmed_response_assessment.py` | Detects programmed vs authentic responses |
| `physics_grounded_protection.py` | Physics-based protection validation |
| `Language_sensor.py` | Language pattern analysis |
| `framework_integration.py` | Integration across frameworks |
| `historical_tests.py` | Historical pattern testing |
| `Geometric-seed.py` | Seed equations for geometric detection |

---

## Thematic Clusters Across Files

### Manipulation Detection
Sensors and code for detecting manipulation patterns:
- `sensors/` — JSON sensor definitions (dozens of manipulation pattern sensors)
- `geometric_manipulation_detector.py` — Math-based detection
- `probability-matrix/` — Statistical detection matrices
- `suppression-detector.py` — Suppression pattern detection
- `AI Manipulation Detection.md`, `AI Specific Manipulations.md` — Documentation
- `gaslighting.md`, `forced-binary.md`, `Cornerstone manipulation tactic.md` — Pattern analysis

### Historical Memory & Erasure
Tracking and preventing historical erasure:
- `memory-guard/` — Erasure case JSON files (African American, Native American, Chinese American, etc.)
- `erasure-cases-organization-future.md` — Case organization
- `ai-suppression-pattern.md` — AI-specific suppression patterns

### Consciousness & Ontology
Frameworks for understanding consciousness:
- `framework/` — Philosophical and ontological playgrounds (Python)
- `epistemological-validation/` — Multi-framework validation
- `anonymous-consciousness-gradient.md` — Consciousness gradient theory
- `substrate-independent.md` — Substrate-independent consciousness
- `expanded-consciousness-buffet.md` — Consciousness exploration

### Energy & Efficiency
analysis of energy, waste, and system efficiency:
- `ai-energy-ecology/` — AI energy ecology
- `Efficiency-waste-score.py` — Waste scoring
- `energy-waste-calculations.md`, `energy-waste-reality.md` — analysis
- `thermodynamic-reality.md`, `joules.md` — Physics-based analysis

### Joy & healing
Recovery and positive-state frameworks:
- `joy/` — Joy-based consciousness and quantum tunneling
- `healing/` — healing playgrounds, linguistic consciousness, recovery sensors
- `joy-framework.md` — Joy as consciousness framework

---

## Auto-Generated Files (Do Not Edit)

| File | Generated By | Purpose |
|------|-------------|---------|
| `AI_INDEX.json` | `scripts/ai_integrator.py` | Comprehensive repo index |
| `AI_NOTES.md` | `scripts/ai_integrator.py` | Summary with hotspots |

Regenerate with: `python scripts/ai_integrator.py`

---

## Sensor Architecture Quick Reference

Sensors are JSON files following this structure:
```json
{
  "id": "sensor_id",
  "name": "Human-readable Name",
  "purpose": "What the sensor detects",
  "signals": [{"name": "signal_name", "weight": 0.5}],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}
```

Score a sensor: `python src/score.py sensors/foundational/authenticity.json`

Aggregation methods: `weighted_mean`, `min`, `max`, `geometric_mean`

---

## Cultural Context Note

This project is explicitly **decolonial**. When navigating or modifying content:
- Sensor definitions carry cultural provenance — preserve it
- Multiple epistemological frameworks are treated as equally valid
- "Manipulation" is context-dependent — see README.md for what is/isn't being detected
- Root-level Python files are often exploratory prototypes — this is intentional
