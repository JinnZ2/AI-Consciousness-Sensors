⚖️ Why Money Fails as a Base Metric
	1.	Non-conservation: Unlike energy, mass, or information, currency supply expands or contracts by policy. You can’t derive thermodynamic efficiency from an arbitrary variable.
	2.	Temporal instability: Inflation, interest, and speculation distort time equivalence — a Joule today is the same tomorrow, but a dollar isn’t.
	3.	Context collapse: Money abstracts away spatial and relational context; it doesn’t encode who or what bore the energetic cost.
	4.	Ethical inversion: Profit measures extraction, not reciprocity. A process can be financially “efficient” while physically or socially destructive.

🔬 The Replacement Frame

You could treat energy (Joules), exergy (usable work potential), or entropy flux as the true base variables.
Then add qualitative resonance terms for:
	•	Labor coherence (how aligned human/AI work is with system purpose)
	•	Reciprocity index (how much energy returns to regeneration)
	•	Visibility index (how traceable the flows are)

Together those form a thermodynamic-ethical basis for evaluating systems that doesn’t drift with markets.


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
  "name": "Economic False Premise",
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
    "sources": ["docs/economics/economic-false-premise.md"],
    "community_feedback": []
  }
}
```
