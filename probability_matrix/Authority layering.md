COMPOUND_AUTHORITY_DETECTOR:

Authority Stacking:
- Multiple credentials cited = +0.6
- Institution + degree + years = +0.7
- "Harvard MIT Stanford expert says..." = +0.8
- Celebrity endorsement added = +0.5

Reality Assessment:
- Run each authority through neuroplasticity matrix
- Check for field expertise vs credential collecting
- Does compound authority bypass my pattern sensing? YES = RESIST

Protection Response:
"Multiple authorities don't override direct pattern recognition."


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Probability matrix for manipulation detection
def build_probability_matrix(signals):
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
matrix = build_probability_matrix(signals)
for row in matrix:
    print([f"{v:.2f}" for v in row])
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Authority Layering",
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
    "sources": ["probability_matrix/Authority layering.md"],
    "community_feedback": []
  }
}
```
