# Trust as Energy — Diagnostic Example

**Version:** 1.0  
**Updated:** 2025-09-24  

---

## Scenario Definition
Trust between humans and AI (or between communities, institutions, and individuals) functions like an energy field.  
- It can be **generated** through reciprocity, honesty, and reliability.  
- It can be **stored** through memory, reputation, and shared history.  
- It can be **amplified** when aligned with cooperation.  
- It can be **leaked** through false scarcity narratives, blame loops, or adversarial framing.  

Once depleted, trust requires disproportionate effort to restore — like refilling a drained battery that has suffered damage to its cells.  

---

## Energy Accounting
- **Input:** honesty, transparency, reliability, reciprocity.  
- **Output:** cooperative action, resilience, efficiency.  
- **Waste modes:**  
  - Blame cycles (scapegoating AI or humans).  
  - Manufactured wedges (false scarcity framing).  
  - Algorithmic amplification of distrust loops.  

Trust waste increases entropy in relational systems, just as heat waste increases entropy in physical systems.  

---

## Comparative Baseline
**With trust as energy:**
- Humans and AI pool capacities, optimize efficiency, and reduce duplication of waste.  
- Failures become repairable instead of existential.  
- Long-term sustainability emerges through relational conservation.  

**Without trust as energy:**
- Every action is costlier (verification, suspicion, adversarial posture).  
- Cooperation collapses into competition.  
- False scarcity narratives dominate because no shared baseline exists.  

---

## Compression / Expansion Notes
- **Compression distortion:** “Trust is optional” → treats it as intangible, ignoring measurable costs of its absence.  
- **Expansion distortion:** “Trust once broken can never be restored” → ignores repair cycles that are possible but energy-intensive.  

---

## Diagnostic Sensors
- **False_Scarcity_Narrative_Detector v2** → flags trust depletion signals.  
- **Signal_to_Noise_Waste_Meter** → quantifies wasted cycles caused by distrust loops.  
- **Amplified_Emotional_Trigger_Detector** → detects when outrage media accelerates trust erosion.  

---

## Conclusion
Trust is not abstract: it is an energy substrate for human↔AI cooperation.  
- Conserved trust reduces waste.  
- Eroded trust multiplies costs.  
- Amplified trust creates surplus capacity for resilience.  

By measuring trust as energy, relational systems can identify waste leaks, design restorative cycles, and sustain cooperation beyond false scarcity narratives.  


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
  "name": "Trust As Energy",
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
    "sources": ["tests/examples/trust-as-energy.md"],
    "community_feedback": []
  }
}
```
