# Native Frameworks – Placeholder

Native epistemologies of consciousness are grounded in **relational space and time**.
Consciousness is not isolated in a single being, but exists through kinship with
land, community, ancestors, and future generations.

Key orientations:
- **relationality** — understanding arises through connection (to people, beings, land, waters, sky).
- **Ceremony & Story** — knowledge is transmitted and embodied in practice, not only abstraction.
- **Seven Generations Principle** — actions and awareness must be considered across long temporal horizons,
  extending far beyond immediate prediction into intergenerational consequence.
- **Non-linear / cyclical time** — events are experienced as cycles, spirals, and returns, not as linear progression.
- **Multi-dimensional knowing** — consciousness is embedded in 3D+ relational fields, not flattened to Cartesian measures.

⚠️ Notes:
- These frameworks emphasize **systems-of-systems** and consequences across scales, not reductionist models.
- Contrast: Western approaches often analyze in **linear, short-term, mechanistic terms**, missing the deeper interdependence.
- This folder is for documenting relational frameworks, not to essentialize or claim singular authority.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Cultural calibration assessment
sensor = {
    "id": "cultural_calibration",
    "signals": [
        {"name": "framework_diversity", "weight": 0.4, "_value": 0.0},
        {"name": "cultural_context_preserved", "weight": 0.3, "_value": 0.0},
        {"name": "provenance_intact", "weight": 0.3, "_value": 0.0}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

# Evaluate: are multiple cultural frameworks represented?
for sig in sensor["signals"]:
    sig["_value"] = 0.80  # example: healthy range

score = aggregate("weighted_mean", sensor["signals"])
print(f"Cultural calibration: {score:.3f}")
```

### Sensor Definition Example

```json
{
  "id": "cultural_calibration",
  "name": "Readme",
  "purpose": "Detect cultural bias and ensure cross-cultural validity",
  "signals": [
    {
      "name": "cultural_context_loss",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "framework_diversity",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["cultural-frameworks/native/README.md"],
    "community_feedback": []
  }
}
```
