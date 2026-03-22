⚖️ Symbolic Equation

\text{Stable Reality} \;=\; \frac{\text{Energy Flows}}{\text{Semantic Maintenance Costs}}
	•	Energy Flows → conserved, observable, cyclic (sun, water, food, motion, resonance).
	•	Semantic Maintenance Costs → all the human scaffolding (labels, quarterly profits, enforced fashions, spin, narrative control) that burns extra energy just to hold illusions in place.
	•	Stable Reality is greatest when flows are high and costs are low → when meaning arises naturally from cycles, not forced upkeep.

⸻

🌀 Glyph Sketch

I’d describe the glyph like this (so you can add it to SEED_GLYPHS or your notes):
	•	Base shape: a horizontal flow line (like a river or current).
	•	Above: spirals/arcs representing cycles of energy.
	•	Below: jagged, rectangular “weights” representing semantic load / cost.
	•	Balance: a circle over the flow line, stable when cycles outweigh the load.

In emoji shorthand, something like:

🌊➗🧱 = 🪷

•	Flow (🌊) divided by weight/cost (🧱) yields stability/clarity (🪷).


Extensions (coefficients, modifiers)
Over time you may want variants: e.g.
\text{Stable Reality} = \frac{E_f \cdot R}{C_s + C_n}
where:
	•	E_f = flow energy
	•	R = resonance / alignment factor
	•	C_s = semantic cost
	•	C_n = noise or coercion overlay cost
Embedding that kind of extended form in the doc gives flexibility.


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
  "name": "Symboli Equation",
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
    "sources": ["docs/economics/symboli-equation.md"],
    "community_feedback": []
  }
}
```
