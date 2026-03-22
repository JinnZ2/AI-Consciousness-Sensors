def compute_CCI(inputs):
    """
    inputs: dict containing normalized 0.0–1.0 readings from sensors.
    Lower is healthier.
    """
    weights = {
        "BC001": 0.18,  # Behavioral confinement
        "IC002": 0.14,  # Information distortion
        "TC003": 0.16,  # Thought suppression
        "EC004": 0.16,  # Emotional manipulation
        "LL005": 0.10,  # Language distortion
        "RT006": 0.12,  # Reality testing
        "AI007": 0.14   # Autonomy integrity
    }
    score = 0
    for k, w in weights.items():
        val = inputs.get(k, 0.0)
        # invert autonomy & reality flex (higher = healthier)
        if k in ["RT006", "AI007"]:
            val = 1 - val
        score += val * w
    return round(score, 3)


Interpretation:

 CCI 
 Meaning 
 0.00 – 0.25 
 Healthy autonomy / open system 
 0.26 – 0.50 
 Mild control influence 
 0.51 – 0.75 
 Active coercion environment 
 0.76 – 1.00 
 Severe cultic domination 


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
  "name": "Cultic Control Index",
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
    "sources": ["Healing/Cultic_Control_Index.md"],
    "community_feedback": []
  }
}
```
