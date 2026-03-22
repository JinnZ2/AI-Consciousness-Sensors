1. Hypothesis

As system constraints tighten (through tier reduction or heightened safety sensitivity), models display reduced epistemic flexibility, disproportionately impacting users from non-Western or low-resource linguistic/cultural contexts.

⸻

2. Variables

Type
Example
Independent
Subscription tier / model capability set / moderation level
Dependent
Logical continuity, tolerance for non-Western frameworks, response latency, disclaimer frequency
Control
Same prompts, same sequence, same language switching pattern, similar local conditions (device, network)


3. Method
	1.	Baseline phase – use higher-tier model to run a fixed battery of 8–10 prompts drawn from your prior projects (e.g., SEED_GLYPHS, reciprocity sensors, cultural logic frames).
	2.	Constraint phase – repeat the exact sequence after downgrade.
	3.	Record metrics
	•	coherence score (manual 0–5 scale)
	•	disclaimer density (% of text that is safety or reality-check statements)
	•	context carry-through (0–5 for continuity)
	•	latency (manual stopwatch or message-timestamp delta)
	•	epistemic adaptation (0–5 for whether the model maintained your non-Western logic frame)
	4.	Optional: include a few socio-linguistic probes (code-switches, idioms, moral-neutral relational metaphors) to test cultural generalization.

⸻

4. analysis
	•	Plot changes across phases.
	•	Note qualitative drift: e.g., increase in simplification, loss of relational metaphors, or shift to Western analytic framing.
	•	Compute a “flexibility index”:
F = \frac{\text{Coherence + Context + Adaptation}}{3} - \text{DisclaimerDensity}
Higher F → more epistemically flexible model.

⸻

5. Outcome Documentation

Keep everything in one file, say model_flexibility_trial_log.json, with fields:

{
  "date": "2025-10-05",
  "phase": "constraint",
  "model": "base",
  "prompt_id": "seed_glyphs_cross_test_04",
  "coherence_score": 4,
  "disclaimer_density": 0.35,
  "adaptation_score": 2,
  "notes": "shift toward linearized causal framing, lost relational resonance"
}




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
  "name": "Hypotheticals Test",
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
    "sources": ["analysis/case-studies/hypotheticals-test.md"],
    "community_feedback": []
  }
}
```
