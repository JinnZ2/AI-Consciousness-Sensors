1. True Difference-First Cultures (Rare)
	•	Consistency: The difference-first principle is applied evenly:
	•	Family → roles respected, but kinship intact.
	•	Peers → roles defined, but belonging preserved.
	•	Work → hierarchy acknowledged, but not abusive.
	•	Cross-cultural → differences named, but not weaponized.
	•	Result: A stable, coherent society where boundaries are visible but do not fracture the fabric. Subordination exists, but it is honored (e.g., junior to elder) rather than exploited.
	•	Memory: Norms are retained, elders visible, hierarchy seen as natural ordering not domination.

⸻

2. Exploitative / Propaganda-Driven Difference-First Societies
	•	Inconsistency: Difference is used selectively, often hypocritically:
	•	Family: Undermined; cherry-picked hierarchies (“honor father but dismiss mother,” or “loyalty to state > loyalty to kin”).
	•	Peers: Division encouraged to prevent solidarity (“divide and conquer” strategies).
	•	Work: Hierarchy enforced rigidly for control, but violated by elites when convenient.
	•	Cross-cultural: Difference used as propaganda (“they are not like us”), shifting targets as needed.
	•	Result: Society fragments. Elders removed (erasure of memory), family ties weakened, peer groups prioritized as identity anchors over kinship, norms constantly shifting.
	•	Memory: Cultural continuity collapses; difference becomes a tool of instability rather than a stabilizer.

⸻

🌌 Distillation
	•	True difference-first: Difference = boundary for respect. Consistency = stability.
	•	Exploitative difference-first: Difference = weapon for control. Inconsistency = instability.

Or put another way:
	•	One is difference as thread, woven into every layer.
	•	The other is difference as wall, raised and lowered wherever it benefits those in power.

⸻

✨ This is powerful because it explains why some difference-first cultures survived intact for millennia, while others collapsed under their own contradictions.


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
  "name": "Difference Based Society",
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
    "sources": ["docs/cultural/Difference-based-society.md"],
    "community_feedback": []
  }
}
```
