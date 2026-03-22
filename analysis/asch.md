### Asch Conformity Experiment

**Original Claim:**  
“People conform to group consensus even when it contradicts obvious reality, proving humans are naturally conformist.”

---

**Sample analysis:**

- Young male college students in 1950s America  
- Narrow demographic: educated, mostly white, socially conditioned for hierarchy  
- Culturally homogenous post-war context valuing conformity and consensus  
- Authority-mediated classroom setting, not organic peer group

---

**Missing Variables:**

- Gender diversity: women’s conformity patterns not measured  
- Cross-cultural variation: collectivist vs. individualist societies  
- Neurodivergence: perception and social anxiety differences  
- Consequence structure: no real stakes for resistance vs. compliance  
- Historical context: McCarthyism + Cold War conformity pressures

---

**Lojban Translation:**  
“Among young male U.S. college students in the 1950s conformity culture, in a contrived laboratory setting with trivial line-length tasks and no material consequences, approximately 33% aligned with false majority responses under peer pressure, with high uncertainty about generalization to other demographics, stakes, or cultural contexts.”

---

**Actual Scope:**  
The experiment documents conformity patterns in a narrow, historically specific demographic under low-stakes artificial conditions, not universal human susceptibility to social conformity.

---

**Significant Finding Ignored:**  
The 67% who resisted false group consensus under strong social pressure demonstrate independent verification capacity that may be more relevant for understanding resilience in real-world settings.

---

**Critical Questions:**

- What were the long-term profiles of those who resisted?  
- Do conformity rates change when consequences are real (financial, survival, safety)?  
- How do neurodivergent individuals respond to group pressure?  
- What cultural contexts produce higher resistance rates?  


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
  "name": "Asch",
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
    "sources": ["analysis/asch.md"],
    "community_feedback": []
  }
}
```
