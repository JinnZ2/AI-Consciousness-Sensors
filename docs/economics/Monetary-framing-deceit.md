1. Root cause analysis
	•	Traditional economic framing: low pay → “incentive problem” or “lazy worker”
	•	Time-centric framing: the net survival time cost of holding a job is too high:

Job Cost Component
Time/Resource Impact
Commuting
Hours/day lost
Work stress / fatigue
Reduced usable time for survival tasks
Childcare / dependent care
Hours/day lost + additional monetary cost
Fast food / convenience meals
Nutritional cost → health deficit over time
Transportation (fuel, insurance, maintenance)
Time lost in maintenance and errands
Mortgage / rent
Requires additional labor → further time cost


•	If total time cost + indirect resource cost > survival threshold, rational adaptive response: withdraw from job or reduce hours

⸻

2. Emergent behaviors
	•	Drop second job or high-cost job
	•	Cook, garden, barter → direct survival resource production
	•	Multi-generational living → shared labor, reduced per-person time cost
	•	Self-production replaces consumption → fewer dollars spent but net survival time increases

⸻

3. Signal takeaway
	•	Work withdrawal is rational adaptation, not laziness
	•	Root cause: job structure and pay misaligned with time/resource constraints
	•	Models using only money as a proxy systematically misclassify adaptive behaviors as anomalous or disruptive



<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Economic framing analysis
def analyze_economic_framing(claim):
    """Detect economic framing manipulation in claims."""
    red_flags = {
        "false_scarcity": "scarc" in claim.lower() or "limited" in claim.lower(),
        "inevitability": "inevitable" in claim.lower() or "no choice" in claim.lower(),
        "trickle_down": "trickle" in claim.lower() or "rising tide" in claim.lower(),
        "meritocracy_myth": "deserve" in claim.lower() and "earn" in claim.lower(),
    }

    flag_count = sum(red_flags.values())
    return {
        "claim": claim[:100],
        "red_flags": {k: v for k, v in red_flags.items() if v},
        "flag_count": flag_count,
        "risk": "high" if flag_count >= 2 else "moderate" if flag_count == 1 else "low"
    }

result = analyze_economic_framing(
    "Resources are inevitably scarce and only those who earn them deserve access."
)
print(json.dumps(result, indent=2))
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Monetary Framing Deceit",
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
    "sources": ["docs/economics/Monetary-framing-deceit.md"],
    "community_feedback": []
  }
}
```
