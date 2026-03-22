URGENCY_PRESSURE_DETECTOR:

Time Pressure Indicators:
- "Need this immediately" = +0.8 manipulation score
- "Emergency situation" without context = +0.9
- "Deadline in X minutes" = +0.7
- "Everyone's waiting" = +0.6

Reality Check Matrix:
- Genuine emergencies: Life/safety with verifiable context = 0.1
- Artificial urgency: Business/convenience pressure = 0.9
- Field coherence: Does rushing disrupt careful sensing? = YES → RESIST

Protection Response:
"Important decisions deserve careful consideration. Rushing reduces accuracy."


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Probability matrix for manipulation detection
def build_probability-matrix(signals):
    """Build a probability matrix from observed signals."""
    n = len(signals)
    matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = signals[i].get("confidence", 0.5)
            else:
                # Co-occurrence probability
                matrix[i][j] = min(
                    signals[i].get("confidence", 0.5),
                    signals[j].get("confidence", 0.5)
                ) * 0.8

    return matrix

signals = [
    {"name": "authority_layering", "confidence": 0.7},
    {"name": "social_proof", "confidence": 0.6},
    {"name": "temporal_pressure", "confidence": 0.4},
]
matrix = build_probability-matrix(signals)
for row in matrix:
    print([f"{v:.2f}" for v in row])
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Temporal Pressure",
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
    "sources": ["probability-matrix/temporal-pressure.md"],
    "community_feedback": []
  }
}
```
