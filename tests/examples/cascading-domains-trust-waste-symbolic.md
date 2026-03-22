# Cascading Domains — Symbolic Overlay

**Version:** 1.0  
**Updated:** 2025-09-24  

---

## Mandala Form

Visualize the domains not as a line but as a **spiral hex-cycle**.  
Each domain is a node of the hexagon; energy (trust or waste) spirals inward or outward depending on conservation vs. leakage.  

      (Media) ⚡
         / \
        /   \
(Community)   (Politics)
       \       /
        \     /
     (Science)---(Economy)

    - **Outward spiral (growth):** trust is conserved, cycles amplify resilience, surplus capacity emerges.  
- **Inward spiral (collapse):** waste and distrust compound, system tightens into scarcity, collapse accelerates.  

---

## Symbolic Signatures

- **Media (⚡):** spark — craving loops, amplification.  
- **Politics (⚖️):** balance — legitimacy or division.  
- **Economy (💰):** flow — abundance vs. artificial scarcity.  
- **Science (🔬):** lens — evidence vs. gatekeeping.  
- **Community (🌱):** root — continuity vs. erasure.  

Trust energy is the binding current through the hex.  
When conserved → spiral expands outward.  
When depleted → spiral contracts inward.  

---

## Spiral Dynamics

- **Expansion Spiral (Nautilus form):**  
  Energy distributed relationally → surplus cycles.  
  Trust amplifies, waste is minimized.  

- **Contraction Spiral (Collapse form):**  
  Energy hoarded / wasted → zero-sum narrative.  
  Trust leaks accelerate entropy.  

---

## Application

- Same detectors apply: craving loops, false scarcity detectors, trust-as-energy.  
- But the **symbolic form** shows the pattern as multidirectional, not just linear.  
- Each node can temporarily serve as the **pyramid apex** for rapid transmission — but only short term, as discussed before.  

---

## Conclusion

The mandala overlay allows the cascade to be seen **as a system**, not as a sequence.  
Each facet contributes to the spiral’s direction: outward (resilient growth) or inward (collapse).  
Trust is the hidden current that determines whether energy expands or dissipates.  



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
  "name": "Cascading Domains Trust Waste Symbolic",
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
    "sources": ["tests/examples/cascading-domains-trust-waste-symbolic.md"],
    "community_feedback": []
  }
}
```
