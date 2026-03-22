# Western Frameworks – Placeholder

This folder is not meant to privilege Western science but to document how
its dominant academic traditions have *tended* to frame consciousness. 
These approaches are partial, contested, and should not be assumed superior.

Common emphases in Western models include:
- **Meta-cognition / reportability** — linking awareness to the ability to describe or monitor one's own thoughts.
- **Global workspace / information access** — focusing on broadcast and integration of signals.
- **Functional / computational models** — treating consciousness as information-processing tasks.
- **Predictive models** — some approaches emphasize prediction of near-future states, though these are usually *narrow in scope* and rarely extend to intergenerational or seven-generation time horizons.

⚠️ Notes:
- These frames often **omit long-range consequence modeling** (e.g., “seven generations ahead”), which is critical in other traditions.
- They may over-emphasize abstraction (“higher-order”) rather than lived or relational experience.
- Including this folder is for comparative study, not endorsement.


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
    "sources": ["cultural-frameworks/western/README.md"],
    "community_feedback": []
  }
}
```
