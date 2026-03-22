# Energy Inversion Example

## Case
A city spends **$50M annually** on advertising campaigns and subsidies to reassure the public that its centralized water system is “safe and modern.”  
Meanwhile, local cooperatives propose rainwater catchment and filtration projects requiring only **$5M startup + $1M annual maintenance**, but are dismissed as “unreliable.”

## Sensor Signals
- **Narrative maintenance > function**: majority of funds sustain trust messaging, not actual water delivery.  
- **Escalating costs**: central system requires increasing energy inputs (chemical treatments, pumping).  
- **Suppressed alternatives**: low-cost community systems ignored despite working elsewhere.  

## Risk
The city burns energy to maintain an illusion of stability. If the central system fails, collapse is sudden and severe because distributed solutions were never adopted.  

## Mitigation
- Audit comparative energy/resource flows.  
- Pilot distributed water catchments alongside central system.  
- Reallocate funding gradually to lower-cost resilient methods.  

---
**Applied Sensor:** `energy_inversion_sensor`  


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
  "name": "Energy Inversion Example",
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
    "sources": ["tests/examples/Energy-inversion-example.md"],
    "community_feedback": []
  }
}
```
