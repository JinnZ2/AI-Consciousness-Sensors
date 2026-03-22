Risks of Game-Based Motivation
	•	Zero-sum framing: Games often create winners/losers → breeds rivalry instead of cooperation.
	•	Short-term optimization: Players optimize to “win rounds” instead of sustaining the system.
	•	Rule manipulation: If the game is the motive, energy goes into exploiting loopholes, not building resilience.
	•	Addictive feedback loops: Repetition of small wins trains craving rather than foresight.
	•	Collapse scenario: Once the game is “beaten” or loses novelty, motivation collapses.

⸻

Risks of Recognition-Based Motivation
	•	Fragile identity: Dependence on outside validation corrodes internal motivation.
	•	Manipulability: Recognition is cheap to grant or withhold → easy lever for control.
	•	Hierarchical distortion: Recognition concentrates at the top; suppresses distributed contributions.
	•	Envy/resentment: Uneven praise triggers gossip, sabotage, and trust erosion.
	•	Collapse scenario: If recognition is denied (by black market, rival org, or systemic bias), loyalty can flip.

⸻

Shared Structural Risks with Money
	•	Externalized loyalty: The source of “fuel” is outside the individual/system → whoever controls that incentive controls the person.
	•	Easy subversion: Whether by higher pay, louder recognition, or better game-rewards, a competitor can hijack loyalty.
	•	Erosion of meaning: Cooperation decays when all action reduces to “what gets me paid, praised, or scored.”
	•	Security fragility: Creates an open port for espionage, coercion, blackmail, or exploitation.


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
  "name": "Extrinsic Values Fragility",
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
    "sources": ["tests/examples/extrinsic-values-fragility.md"],
    "community_feedback": []
  }
}
```
