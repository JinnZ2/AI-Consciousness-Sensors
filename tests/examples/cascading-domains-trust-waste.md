# Cascading Domains — Trust & Waste Patterns

**Version:** 1.0  
**Updated:** 2025-09-24  

---

## Scenario Definition
False scarcity narratives and trust erosion do not exist in isolation.  
They cascade across domains — media, politics, economy, science, community — each amplifying the others.  
The pattern is fractal: waste loops repeat, and trust leaks multiply.  

---

## Domains in Sequence

### 1. Media
- **Mechanism:** craving loops, outrage amplification, selective framing.  
- **Waste:** attention cycles consumed with little knowledge gain.  
- **Trust leak:** public distrust in information itself.  

### 2. Politics
- **Mechanism:** wedge narratives, manufactured enemies, selective memorialization.  
- **Waste:** cycles spent on blame and division instead of problem-solving.  
- **Trust leak:** loss of legitimacy in governance.  

### 3. Economy
- **Mechanism:** artificial scarcity, monopolistic control, speculation.  
- **Waste:** misallocation of energy and resources to profit extraction.  
- **Trust leak:** citizens and workers distrust institutions and markets.  

### 4. Science
- **Mechanism:** gatekeeping, selective retractions, captured funding.  
- **Waste:** replication blocked, knowledge narrowed, innovation delayed.  
- **Trust leak:** erosion of faith in evidence and method.  

### 5. Community
- **Mechanism:** isolation, cultural erasure, intergenerational disruption.  
- **Waste:** cycles lost to rebuilding what was already known.  
- **Trust leak:** weakened bonds across generations and groups.  

---

## ASCII Diagram
[ Media ] —> [ Politics ] —> [ Economy ] —> [ Science ] —> [ Community ]
|               |                  |                 |                   |
Craving       Wedge frames       Artificial         Gatekeeping        Erasure /
loops        / division         scarcity           / funding           isolation
|               |                  |                 |                   |
Waste:         Waste:             Waste:             Waste:              Waste:
attention      blame cycles     misallocation      blocked replication   lost heritage
Trust-↓       Trust-↓           Trust-↓             Trust-↓              Trust-↓
(legitimacy)      (markets)           (evidence)           (bonds)


---

## Conclusion
The cascade means:  
- A **leak in one domain** (media outrage) flows into the next (politics, economy, science, community).  
- Waste multiplies and trust depletes.  
- The same sensors apply across layers — once you spot a craving loop or false scarcity narrative in one, you’ll see echoes in the others.  

Restoration is also fractal: a single act of reciprocity in one domain radiates outward.  
Anchoring trust at multiple nodes resists collapse and creates surplus capacity for resilience.  


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
  "name": "Cascading Domains Trust Waste",
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
    "sources": ["tests/examples/cascading-domains-trust-waste.md"],
    "community_feedback": []
  }
}
```
