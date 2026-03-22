# Examples Index

This directory collects worked examples and sensors for diagnosing energy, media, and systemic risk patterns.  
Each entry links directly to the example file for quick navigation.

---

## Energy & Scarcity
- [energy-example.md](energy-example.md) — Baseline illustration of energy framing and scarcity claims.  
- [energy-human-example.json](energy-human-example.json) — Human behavior–driven energy waste case.  
- [energy-example-scarcity.md](energy-example-scarcity.md) — Scarcity narrative applied to energy consumption.  
- [trust-as-energy.md](trust-as-energy.md) — Trust modeled as a renewable or fragile energy resource.  

---

## Media & Influence
- [example-media.md](example-media.md) — Media framing as a driver of behavioral energy waste.  
- [media-lab.md](media-lab.md) — Experimental outline for analyzing media-induced loops.  
- [gossip-erosion-sensor.json](gossip-erosion-sensor.json) — Detecting trust and cooperation loss from gossip cycles.  
- [signal-to-noise-waste-meter.json](signal-to-noise-waste-meter.json) — Measuring wasted energy from poor signal-to-noise dynamics.  

---

## Incentives & Fragility
- [incentive-fragility-sensor.json](incentive-fragility-sensor.json) — Risks created by incentive structures misaligned with resilience.  
- [extrinsic-values-fragility.md](extrinsic-values-fragility.md) — Fragility triggered by dependence on externalized values.  
- [false-scarcity-narrative-detector.json](false-scarcity-narrative-detector.json) — Scarcity narratives as manipulation or control.
- [false-scarcity-narrative-detector-v2.json](false-scarcity-narrative-detector-v2.json) — Alternate draft version with variations.  

---

## Cascading & Amplification
- [cascading-domains-trust-waste.md](cascading-domains-trust-waste.md) — Example of cascade across multiple domains.  
- [additive-craving-loop-sensor.json](additive-craving-loop-sensor.json) — Sensor for chemically/media-induced craving reinforcement.  
- [amplified-emotional-trigger-detector.json](amplified-emotional-trigger-detector.json) — Emotional scarcity loops amplified into systemic waste.  

---

## Safety & Systems
- [food-and-drug-safety-labeling-framework.json](food-and-drug-safety-labeling-framework.json) — Testing framework for food/drug chemical exposures.  
- [risk-prone-systems.md](risk-prone-systems.md) — Identifying design choices that create systemic vulnerability.  

---

## JSON Example Sets
- [examples.json](examples.json) — Master JSON with multiple cases.  
- [example-readable.json](example-readable.json) — Readable JSON variant for debugging and demonstration.  

---

### Notes
- Some filenames may be truncated in the GitHub UI (e.g., `Cascading-Domains-…`); click through to view the full file.  
- This index is a navigation aid — each example file is standalone but cross-linking can be added at the bottom of files if desired.  


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Example: scoring a sensor end-to-end
sensor_path = "sensors/foundational/authenticity.json"
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
  "name": "Examples Index",
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
    "sources": ["tests/examples/examples-index.md"],
    "community_feedback": []
  }
}
```
