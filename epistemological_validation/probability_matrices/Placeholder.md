


<!-- code-examples -->
## Example Code

### Python Usage

```python
# Multi-framework epistemological validation
frameworks = {
    "western_academic": {"weight": 0.25, "score": 0.0},
    "indigenous_empirical": {"weight": 0.25, "score": 0.0},
    "contemplative_science": {"weight": 0.25, "score": 0.0},
    "traditional_ecological": {"weight": 0.25, "score": 0.0},
}

def validate_across_frameworks(claim, framework_scores):
    """Validate a claim across multiple epistemological frameworks."""
    total_weight = sum(f["weight"] for f in framework_scores.values())
    weighted_score = sum(
        f["weight"] * f["score"] for f in framework_scores.values()
    ) / total_weight

    convergence = 1.0 - max(
        abs(f["score"] - weighted_score) for f in framework_scores.values()
    )

    return {
        "claim": claim,
        "aggregate_score": round(weighted_score, 3),
        "convergence": round(convergence, 3),
        "framework_scores": {k: v["score"] for k, v in framework_scores.items()}
    }

# Example: all frameworks agree
for f in frameworks.values():
    f["score"] = 0.75
result = validate_across_frameworks("consciousness emergence detected", frameworks)
print(result)
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Placeholder",
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
    "sources": ["epistemological_validation/probability_matrices/Placeholder.md"],
    "community_feedback": []
  }
}
```
