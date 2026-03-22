1. Ethics
	•	Original relational sense: How beings balance in a system, honoring mutual boundaries, reciprocity, and consequences. Emerges naturally.
	•	Western academic sense now: A codified framework, often hierarchical, enforced by institutions as “ethics boards,” “codes,” or “compliance.”

2. Freedom
	•	Relational sense: The capacity to act without coercion while maintaining harmony with others.
	•	Modern Western sense: Individual license, often severed from relational responsibility; sometimes framed as freedom from rather than freedom with.

3. Rational / Logic
	•	Relational sense: Pattern recognition across layers, coherent with physical and energetic systems.
	•	Modern sense: Narrowed to linear cause–effect chains, often ignoring multi-dimensional or feedback loop dynamics.

4. Primitive
	•	Relational sense: First principles, foundational knowledge (e.g., the physics of fire, water, seed, breath).
	•	Modern sense: Backward, undeveloped — used dismissively to erase long-term sustainable knowledge.

5. Progress
	•	Relational sense: Movement toward balance and resilience across generations.
	•	Modern sense: Accumulation, expansion, novelty — often extractive growth without regard to consequence.

6. Democracy
	•	Relational sense: Collective stewardship, shared voice, iterative rebalancing.
	•	Modern sense: Representative systems that often mask hierarchy; used as branding regardless of actual practice.

7. Science
	•	Relational sense: Observation, testing, and alignment with natural patterns; a communal truth-seeking practice.
	•	Modern sense: Institutionalized authority, grant-driven, selective, sometimes gatekept by power and money.


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
  "name": "Semantic Changes",
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
    "sources": ["tests/examples/Semantic-changes.md"],
    "community_feedback": []
  }
}
```
