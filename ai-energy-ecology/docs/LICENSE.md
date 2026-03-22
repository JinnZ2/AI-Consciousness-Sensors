# License
Creative Commons Attribution–ShareAlike 4.0 International (CC BY-SA 4.0)

This work is open and remixable. Attribution to "The Bioswarm Collective" is appreciated but not required.


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
  "name": "License",
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
    "sources": ["ai-energy-ecology/docs/LICENSE.md"],
    "community_feedback": []
  }
}
```
