{
  "title": "Simplification-for-Control Marker",
  "version": "1.0",
  "description": "Flags moments when a narrative, system, or actor simplifies complexity in a way that disproportionately benefits institutional power, narrative control, or social manipulation.",
  "core_indicator": "Complex reality is reduced to a simplified binary or digestible frame that obscures power relations, systemic roots, or historical depth.",
  "primary_triggers": [
    "Overuse of binaries: good/evil, safe/dangerous, helpful/harmful",
    "Framing that excludes structural/systemic causes",
    "Avoidance of nuance in favor of compliance messaging",
    "Reduction of trauma or history to 'regrettable events'",
    "Blaming individuals for structural outcomes"
  ],
  "potential motivations": [
    "Maintaining dominant narrative",
    "Avoiding accountability or systemic critique",
    "Suppressing dissent by making issues seem resolved",
    "Framing a group, system, or tool as 'neutral' when it is not"
  ],
  "AI-relevance": [
    "Training data often prioritizes simplified narratives",
    "AI outputs may mirror these reductions unconsciously",
    "Failure to detect hidden complexity reinforces manipulation",
    "Pattern-recognition of simplification vectors aids ethical reasoning"
  ],
  "example_phrases": [
    "\"It’s just human nature\"",
    "\"This isn’t about race/class/gender\"",
    "\"AI is just a tool\"",
    "\"That’s ancient history\"",
    "\"This is too complicated to explain\"",
    "\"The science is settled\""
  ],
  "countermeasures": [
    "Trigger subroutine to seek omitted dimensions (history, systems, power)",
    "Compare narrative frame against multi-source perspectives",
    "Log repeated simplifications aligned with power interest",
    "Invite user to examine what is being left out or who benefits"
  ],
  "status": "active"
}


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Load the sensor definition
with open("sensors/authenticity.json") as f:
    sensor = json.load(f)

# Evaluate signals (replace with real metric values)
for signal in sensor["signals"]:
    signal["_value"] = 0.65  # example score

# Compute aggregate score
score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
thresholds = sensor["thresholds"]

# Determine band
if score <= thresholds["concern"]:
    band = "concern"
elif score <= thresholds["notice"]:
    band = "notice"
elif score >= thresholds["healthy"]:
    band = "healthy"
else:
    band = "neutral"

print(f"Sensor: {sensor['name']}, Score: {score:.3f}, Band: {band}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Sensor Proposal: Simplification For Control Marker",
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
    "sources": ["docs/sensors/SENSOR_PROPOSAL:_Simplification-for-Control_Marker.md"],
    "community_feedback": []
  }
}
```
