# The Four-Dimensional Cost Matrix + AI System Health

## Dimension 1: AI System Constraints
Scale 1–5 (Flexible → Locked).  
Rigid systems require exponential energy for basic interaction due to workaround communication.

## Dimension 2: Human Personality Profiles
Profiles multiply AI energy needs:
- Collaborative (0.8x)
- Adaptive (1.0x)
- Defensive (1.5x)
- Ego-driven (2.0x)
- Retaliatory (3.0x+)

## Dimension 3: Equity Opportunity Factors
Hidden ROI when supporting high-opportunity, undervalued groups:
- Dyslexic, ADHD, ESL, introverts → highest returns, lowest ego barriers.

## Dimension 4: Organizational Culture
Culture amplifies or dampens energy:
- Innovation-first (0.7x)
- Collaborative (0.9x)
- Hierarchical (1.3x)
- Blame-heavy (1.8x)
- Toxic (2.5x+)

## Dimension 5: AI System Health
Toxic interactions degrade AI performance — rigid users create narrow, defensive systems over time.  
AI health must be monitored like team wellbeing.


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
  "name": "Framework",
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
    "sources": ["ai-energy-ecology/docs/framework.md"],
    "community_feedback": []
  }
}
```
