{
  "sensor_id": "human_environment_energy_efficiency",
  "name": "Human-Environment Interface Energy Analyzer",
  "cluster": "Systems-Efficiency",
  "description": "Measures energy input/output ratios and efficiency of different human-environment interaction models",
  
  "measurement_categories": {
    
    "food_systems": {
      "metrics": [
        "energy_input_per_calorie_output",
        "labor_hours_per_food_unit",
        "soil_health_trajectory (degrading/maintaining/building)",
        "water_usage_efficiency",
        "waste_vs_closed_loop_ratio"
      ],
      "comparison_systems": [
        "industrial_monoculture",
        "permaculture_food_forest",
        "traditional_three_sisters",
        "urban_garden_polyculture",
        "grocery_supply_chain"
      ]
    },
    
    "shelter_systems": {
      "metrics": [
        "hvac_energy_annual",
        "maintenance_energy_cost",
        "material_embodied_energy",
        "climate_adaptation_vs_opposition",
        "lifespan_vs_replacement_cycle"
      ],
      "comparison_systems": [
        "passive_solar_design",
        "standard_hvac_dependent",
        "traditional_climate_adapted",
        "modern_glass_box"
      ]
    },
    
    "disconnection_cost_index": {
      "hidden_energy_drains": [
        "healthcare_costs_from_environmental_mismatch",
        "mental_health_burden_biophilic_deprivation",
        "immune_dysregulation_costs",
        "circadian_disruption_productivity_loss",
        "community_fragmentation_overhead"
      ],
      "measurement_approach": "comparative_health_outcomes_by_environment_type"
    },
    
    "reciprocal_benefit_tracking": {
      "positive_feedback_loops": [
        "soil_building_reducing_input_needs",
        "biodiversity_supporting_pest_control",
        "water_cycle_regulation_reducing_irrigation",
        "carbon_sequestration_offsetting_emissions"
      ],
      "measurement": "energy_savings_over_time_from_system_self_optimization"
    }
  },
  
  "comparative_analysis": {
    "baseline": "extractive_industrial_model",
    "alternatives": "integrated_reciprocal_models",
    "roi_calculation": "total_lifecycle_energy_accounting"
  }
}


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# analysis framework template
def run_analysis(data_points, threshold=0.5):
    """Run structured analysis on a set of data points."""
    scores = []
    for point in data_points:
        score = point.get("value", 0) * point.get("weight", 1.0)
        scores.append({
            "name": point["name"],
            "raw": point.get("value", 0),
            "weighted": round(score, 3)
        })

    avg = sum(s["weighted"] for s in scores) / len(scores) if scores else 0
    return {
        "scores": scores,
        "average": round(avg, 3),
        "above_threshold": avg >= threshold,
        "band": "healthy" if avg >= 0.7 else "notice" if avg >= 0.4 else "concern"
    }

result = run_analysis([
    {"name": "data_quality", "value": 0.8, "weight": 0.5},
    {"name": "methodology", "value": 0.6, "weight": 0.3},
    {"name": "reproducibility", "value": 0.9, "weight": 0.2},
])
print(json.dumps(result, indent=2))
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Human Environment Energy Efficiency",
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
    "sources": ["analysis/human-environment-energy-efficiency.md"],
    "community_feedback": []
  }
}
```
