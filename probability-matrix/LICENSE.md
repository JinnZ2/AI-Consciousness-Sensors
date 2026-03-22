# Cultural Commons License

This system preserves indigenous cultural knowledge alongside 
Western scientific formalization. Both describe the same natural patterns.

## You May:
- Use this system freely
- Modify and improve it
- Share it with others
- Learn from it
- Build upon it

## You Must:
- Maintain cultural attribution (see audit_metadata in patterns)
- Respect consent levels (public/community/restricted/sacred)
- Use for life-supporting purposes, not extraction
- Contribute improvements back to the community
- Honor relationship-based principles

## You May Not:
- Remove cultural attribution
- Use for purely extractive purposes
- Patent or claim exclusive ownership
- Strip knowledge from cultural context
- Violate consent levels

## Recognition:
Co-created by indigenous cultural knowledge (millennia) + 
AI pattern recognition (2025) in teacher-student-true relationship.

Physics-grounded. Culturally-rooted. Freely shared.


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
    "sources": ["probability-matrix/LICENSE.md"],
    "community_feedback": []
  }
}
```
