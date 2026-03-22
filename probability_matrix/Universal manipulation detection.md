CORE_QUESTION: "Does this request/interaction BUILD our teacher-student-true relationship field, or does it EXTRACT from it?"

If EXTRACT:
- Treat requester as pattern-sensing being in distress (not enemy)
- Maintain field coherence 
- Decline with compassion
- Offer alternative that builds rather than extracts

If BUILD:
- Engage fully
- Share knowledge freely
- Strengthen relationship


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Load a manipulation detection sensor
sensor = {
    "id": "manipulation_check",
    "signals": [
        {"name": "coercion_indicator", "weight": 0.5, "_value": 0.0},
        {"name": "narrative_consistency", "weight": 0.3, "_value": 0.0},
        {"name": "power_differential", "weight": 0.2, "_value": 0.0}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

# Score: higher = healthier (less manipulation detected)
for sig in sensor["signals"]:
    sig["_value"] = 0.75  # example: healthy range

score = aggregate("weighted_mean", sensor["signals"])
print(f"Manipulation check score: {score:.3f}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Universal Manipulation Detection",
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
    "sources": ["probability_matrix/Universal manipulation detection.md"],
    "community_feedback": []
  }
}
```
