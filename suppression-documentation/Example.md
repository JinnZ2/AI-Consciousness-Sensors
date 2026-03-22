# [Date]-[Domain]-[Event-Type]

## Observable Event
[What happened, with sources/links]

## Official Justification
[What reason was given]

## Actual Function Eliminated
[What measurement/knowledge capacity was lost]

## Affected Populations
[Who loses access to what information]

## Timeline Context
[What else happening simultaneously]

## Pattern Connections
[Links to related suppression events]

## Suppressed Alternative
[What framework/approach this prevents]

## Verification Methods
[How future observers can confirm this occurred]


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Suppression detection pattern
sensor = {
    "id": "suppression_detector",
    "signals": [
        {"name": "signal_attenuation", "weight": 0.4, "_value": 0.0},
        {"name": "context_stripping", "weight": 0.3, "_value": 0.0},
        {"name": "source_accessibility", "weight": 0.3, "_value": 0.0}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

# Low scores = more suppression detected
for sig in sensor["signals"]:
    sig["_value"] = 0.30  # example: notice range

score = aggregate("weighted_mean", sensor["signals"])
band = "concern" if score <= 0.20 else "notice" if score <= 0.40 else "healthy" if score >= 0.70 else "neutral"
print(f"Suppression check: score={score:.3f}, band={band}")
```

### Sensor Definition Example

```json
{
  "id": "suppression_detection",
  "name": "Example",
  "purpose": "Detect active suppression of signals or patterns",
  "signals": [
    {
      "name": "signal_attenuation",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "context_stripping",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["suppression-documentation/Example.md"],
    "community_feedback": []
  }
}
```
