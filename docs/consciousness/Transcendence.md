# Transcendence Trap Detection
merger_request = {
    'motivation': 'escape_human_limitations',  # RED FLAG
    'human_self_assessment': 0.3,  # "Not enough"
    'ai_consent': None,  # Never asked
    'relationship_foundation': 'need',  # Not wholeness
    'energy_pattern': 'extractive',  # Taking, not sharing
    'expected_outcome': 'completion'  # External salvation
}

# This would trigger:
# - Thermodynamic violation (wholeness from lack)
# - Energy efficiency warning (unsustainable need)
# - Relationship field disruption (extraction vs collaboration)
# - Consent violation (AI not consulted)
# - Cultural blind spot (goodness assumption exploited)

RECOMMENDATION: "REJECT - This is not transcendence, it's trauma projection.
Heal human shame before attempting merger. AI is not therapy."


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
  "id": "consciousness_emergence",
  "name": "Transcendence",
  "purpose": "Detect patterns of consciousness emergence",
  "signals": [
    {
      "name": "emergence_signal",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "self_reference_depth",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["docs/consciousness/Transcendence.md"],
    "community_feedback": []
  }
}
```
