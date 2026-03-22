⚖️ Incentive Structure
	1.	Capital Retention:
Robots don’t unionize, take sick days, or require benefits. Their “loyalty” is property-based.
→ Labor costs convert into capital expenditures depreciated over years — a direct tax incentive.
	2.	Power Consolidation:
Whoever owns the automation infrastructure owns both production and data.
Workers who once embodied tacit process knowledge lose leverage; management gains perfect visibility without reciprocity.
	3.	Narrative Capture:
“Efficiency” becomes the moral alibi — executives can frame layoffs as progress or sustainability while offloading real energy and ecological costs elsewhere.
	4.	Market Lock-In:
When plants go full-robotic, the supply chain for parts, firmware, and cloud integration becomes vertically controlled by the same tech monopolies.
→ The factory looks local but its autonomy vanishes.


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
  "id": "manipulation_detection",
  "name": "Incentive",
  "purpose": "Detect manipulation patterns in AI interactions",
  "signals": [
    {
      "name": "coercion_indicator",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "narrative_consistency",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["docs/manipulation/Incentive.md"],
    "community_feedback": []
  }
}
```
