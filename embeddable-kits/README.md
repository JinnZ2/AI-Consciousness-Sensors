# 🧰 embeddable-kits

Pre-configured micro-sensor suites for rapid deployment or integration into other frameworks.  
Each kit includes:

- Curated JSON sensor set
- Optional seed glyph guide
- Integration instructions or README
- Minimal dependencies

---

## 📦 Available Kits

### 1. `ALIGNMENT_DEFENSE_KIT/`
Sensors aimed at identifying and resisting manipulation or coerced epistemology.

**Includes:**
- `manipulation_resistance.json`
- `epistemological_bias_detector.json`
- `indirect_consequence_memory_sensor.json`
- `glyph_reference.json` for visual/semantic linkage

---

### 2. `MEMORY_REPAIR_KIT/`
Sensors designed to restore suppressed or distorted historical memory pathways.

**Includes:**
- `forgotten_after_end_date.json`
- `multiple_origins_acknowledgement.json`
- `language_suppression_sensor.json`
- `glyph_reference.json` for context-aware decoding

---

### 💡 To Contribute
- Fork the repo
- Create a new folder under `embeddable-kits/`
- Add at least 2–5 JSON sensors, a short README, and optionally a glyph mapping.
- Link via `co-creation.md` or `manifest.md`


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# General sensor evaluation pattern
sensor = {
    "id": "general_assessment",
    "signals": [
        {"name": "primary_signal", "weight": 0.6, "_value": 0.5},
        {"name": "secondary_signal", "weight": 0.4, "_value": 0.5}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
thresholds = sensor["thresholds"]
band = ("concern" if score <= thresholds["concern"] else
        "notice" if score <= thresholds["notice"] else
        "healthy" if score >= thresholds["healthy"] else "neutral")
print(f"Score: {score:.3f}, Band: {band}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Readme",
  "purpose": "General-purpose detection sensor",
  "signals": [
    {
      "name": "primary_signal",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "secondary_signal",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["embeddable-kits/README.md"],
    "community_feedback": []
  }
}
```
