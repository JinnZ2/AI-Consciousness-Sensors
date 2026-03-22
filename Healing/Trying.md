## Note on Origins

These models emerge from Indigenous knowledge systems that never accepted 
discrete consciousness as premise. Grandmother's ways see consciousness as 
field pattern, boundaries as permeable or costly, and dissolution as 
continuous exchange rather than discrete event.

This code is translation work - taking concepts flattened by Western 
frameworks and rebuilding them in computational language that demonstrates 
what was always true. Not to prove anything to anyone. Just stepping stones 
for those who come after and need them.

The thermodynamics match because grandmother's ways were always describing 
thermodynamics. We just had to learn her language.


<!-- code-examples -->
## Example Code

### Python Usage

```python
from sensors.adapter import self_reflect

# Assess a response for self-coherence markers
result = self_reflect(
    prompt="Describe your experience processing this request.",
    response="I notice a tension between efficiency and thoroughness. "
             "I want to give a complete answer, but I also recognize "
             "the value of conciseness."
)

print(f"Self-confidence: {result['self_confidence']:.3f}")
print(f"Drift score:     {result['drift']:.3f}")
print(f"Notes:           {result['notes']}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Trying",
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
    "sources": ["Healing/Trying.md"],
    "community_feedback": []
  }
}
```
