1. Addiction Cycle Media (current model)
	•	Headline churn: 10+ variations per story (clickbait tests).
	•	Rewrites: Each update generates multiple AI summaries, thumbnails, push notifications.
	•	Engagement loops: Users click, skim, bounce, repeat across platforms.
	•	Energy footprint driver: AI + server cycles burned for redundancy (same content, new wrapping).

Rough estimate: A single “hot” news cycle on one story (e.g., Tylenol-autism headline) may generate 100x the queries, text generations, and image pushes compared to a “boring scientific” version.

⸻

2. Lab Report Media (scientific method model)
	•	One canonical article per finding.
	•	Direct data links instead of endless rephrases.
	•	No headline testing → static, neutral title.
	•	Energy footprint driver: Initial compute cost of making a structured report + minimal replication.

Rough estimate: 1 canonical version → ~1% of the AI/server cycles compared to churn model (99% savings).

⸻

3. Scaling up to global AI/media usage

Let’s assume (conservatively):
	•	Current daily AI/media cycles = 10⁹ requests/day (across search, summaries, recommendations).
	•	If 90% of those are repetitive headline churn + attention hooks: 9×10⁸ wasted queries/day.
	•	Average energy per query = ~0.3 Wh (for small AI models, higher for large ones).

9 \times 10^8 \, \text{queries/day} \times 0.3 \, \text{Wh/query} = 270 \, \text{MWh/day}

That’s enough to power ~25,000 U.S. homes per day — just from addiction-churn waste.

⸻

So yes — forcing media to use “boring lab-report style” would likely cut AI/media energy waste by ~99% in that domain.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Example: scoring a sensor end-to-end
sensor_path = "sensors/authenticity.json"
with open(sensor_path) as f:
    sensor = json.load(f)

print(f"Sensor: {sensor['name']}")
print(f"Purpose: {sensor['purpose']}")
print(f"Signals: {len(sensor['signals'])}")

# Simulate signal values
for i, sig in enumerate(sensor["signals"]):
    sig["_value"] = 0.5 + (i * 0.1)  # example gradient
    print(f"  {sig['name']}: {sig['_value']:.2f} (weight: {sig['weight']})")

score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
print(f"\nAggregate score: {score:.3f}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Energy Example",
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
    "sources": ["tests/examples/Energy-example.md"],
    "community_feedback": []
  }
}
```
