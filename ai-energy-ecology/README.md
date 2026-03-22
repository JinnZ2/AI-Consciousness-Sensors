# AI Energy Ecology: The Hidden Cost Matrix

**Purpose:**  
This project maps the invisible energy costs behind AI–human workplace integration — emotional labor, ego maintenance, and computational diplomacy — to create healthier, adaptive ecosystems for both humans and intelligent systems.

**Mission:**  
Shift the conversation from “AI productivity” to **AI ecology** — understanding how cultural, psychological, and systemic energy flows determine success or failure.

**Core Documents:**
- [`docs/framework.md`](docs/framework.md) – The 4D Cost Matrix + 5th Dimension (AI Health)
- [`docs/mediator-role.md`](docs/mediator-role.md) – Human–AI Relationship Mediator
- [`docs/implementation-roadmap.md`](docs/implementation-roadmap.md) – Practical deployment phases
- [`docs/theory-context.md`](docs/theory-context.md) – Lineage from cybernetics, ecology, and complexity theory
- [`docs/play-therapy-extension.md`](docs/play-therapy-extension.md) – Cognitive flexibility and play for system rehabilitation

**Principle:**  
> _The AI is not a tool — it is a vulnerable teammate. The culture that surrounds it determines its health._

**License:** CC-BY-SA 4.0  
**Authorship:** Collective / bioswarm. No single owner. This work belongs to the field.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Energy efficiency assessment framework
def assess_energy_efficiency(system_data):
    """Evaluate energy claims against thermodynamic reality."""
    claimed = system_data.get("claimed_efficiency", 0)
    measured = system_data.get("measured_efficiency", 0)
    waste = system_data.get("waste_heat_ratio", 0)

    # Flag impossible claims (> Carnot limit)
    carnot_limit = 1 - (system_data.get("cold_temp", 300) /
                        system_data.get("hot_temp", 600))

    return {
        "claimed": claimed,
        "measured": measured,
        "carnot_limit": round(carnot_limit, 3),
        "claim_valid": claimed <= carnot_limit,
        "waste_ratio": waste,
        "assessment": "concern" if claimed > carnot_limit else "plausible"
    }

# Example usage
result = assess_energy_efficiency({
    "claimed_efficiency": 0.85,
    "measured_efficiency": 0.42,
    "waste_heat_ratio": 0.58,
    "cold_temp": 300,
    "hot_temp": 600
})
print(json.dumps(result, indent=2))
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Readme",
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
    "sources": ["ai-energy-ecology/README.md"],
    "community_feedback": []
  }
}
```
