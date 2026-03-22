### Laffer Curve

**Original Claim:**  
“Lowering tax rates increases government revenue because it stimulates economic activity, proving there is an optimal tax rate below 100% that maximizes revenue.”

---

**Sample analysis:**

- Originated in 1970s U.S. political context  
- Based on a napkin sketch rather than empirical data  
- Promoted primarily by political advocates of tax cuts  
- Rarely tested across diverse economies, time periods, or tax systems

---

**Missing Variables:**

- Revenue collection efficiency (tax avoidance, evasion, loopholes)  
- Economic inequality (concentration of gains among wealthy)  
- Government spending multipliers (public vs. private investment impact)  
- Cultural differences in tax compliance and trust in institutions  
- Globalization effects (capital flight, offshoring, tax havens)  
- Historical context of debt, inflation, and growth cycles

---

**Lojban Translation:**  
“In 1970s U.S. political discourse, using an untested theoretical sketch rather than systematic data, some economists and political advocates proposed that for certain economies under specific conditions, reducing certain marginal tax rates might in some cases increase reported government revenues, though with large uncertainty about the mechanisms, historical periods, institutional contexts, and general applicability.”

---

**Actual Scope:**  
The Laffer Curve is a theoretical heuristic with little empirical validation, often applied as universal proof for tax cuts without evidence across contexts. It describes a possibility, not a law.

---

**Significant Finding Ignored:**  
Revenue depends more on enforcement, inequality, and economic structure than on simple tax rate adjustments. Countries with higher tax rates (e.g., Nordic states) sustain high revenues and growth through compliance, redistribution, and trust.

---

**Critical Questions:**

- What is the empirical evidence across different countries and time periods?  
- How does enforcement and tax code complexity affect collection?  
- At what point do tax cuts reduce public investment capacity, harming long-term growth?  
- Who benefits from framing the curve as a “law” rather than a speculative model?  
- How do globalization and capital mobility distort any supposed “optimal” rate?  


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
  "name": "Laffer",
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
    "sources": ["analysis/case-studies/laffer.md"],
    "community_feedback": []
  }
}
```
