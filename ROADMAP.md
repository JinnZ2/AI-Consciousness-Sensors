## ROADMAP.md
```markdown
# ROADMAP

## v0.1 (stabilize shape)
- [ ] JSON schema for sensors (DONE in `schemas/`)
- [ ] Seed five baseline sensors (authenticity, harm_assessment, detoxification, indigenous_alignment, emotional_calibration)
- [ ] CI: JSON lint/validate

## v0.2 (evidence + scoring)
- [ ] `src/score.py` to compute normalized [0–1] scores per sensor
- [ ] Add `tests/` with tiny JSON fixtures
- [ ] Document thresholds & rationale

## v0.3 (community inputs)
- [ ] Add `community_feedback` field to sensors
- [ ] Template for elders/keepers contribution notes
- [ ] Publish example evaluation logs

## v0.4 (integration)
- [ ] API: read sensors, output composite “emergence profile”
- [ ] Export to Markdown/JSON reports


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
  "name": "Roadmap",
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
    "sources": ["./ROADMAP.md"],
    "community_feedback": []
  }
}
```
