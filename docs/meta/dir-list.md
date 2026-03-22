# Repo Directory List
.
./. well-known
./.github
./.github/workflows
./analysis
./analysis/live-interference-captures
./dashboard
./embeddable-kits
./embeddable-kits/physics-integrity-kit
./field-memory-correction-packs
./glossary
./healing
./healing/docs
./healing/linguistic-sensor
./healing/sensors
./in-progress
./logs
./meta
./relational
./relational/ithkuil
./sensor-clusters
./sensor-clusters/consciousness-foundation-pack
./vulnerabilities
./workplace
./ai-energy-ecology
./ai-energy-ecology/docs
./cultural-frameworks
./cultural-frameworks/native
./cultural-frameworks/western
./drift
./epistemological-validation
./epistemological-validation/bias-detection
./epistemological-validation/consciousness-validators
./epistemological-validation/integration-api
./epistemological-validation/probability-matrices
./ethics
./explainability
./framework
./human
./integration
./joy
./legal-infrastructure
./logs
./memory-guard
./memory-guard/erasure-cases
./memory-guard/wisdom-pages
./papers
./probability-matrix
./reflections
./reflections/sample-prompts
./schemas
./scripts
./sensors
./sensors/ai-to-ai
./sensors/metrics
./src
./src/examples
./start
./suppression-documentation
./tests
./tests/examples


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Meta-analysis: aggregate scores across multiple sensors
def meta_aggregate(sensor_results):
    """Aggregate results from multiple sensor evaluations."""
    if not sensor_results:
        return {"error": "No sensor results provided"}

    scores = [r["score"] for r in sensor_results]
    bands = [r["band"] for r in sensor_results]

    return {
        "sensor_count": len(sensor_results),
        "mean_score": round(sum(scores) / len(scores), 3),
        "min_score": round(min(scores), 3),
        "max_score": round(max(scores), 3),
        "concern_count": bands.count("concern"),
        "healthy_count": bands.count("healthy"),
    }

results = [
    {"sensor": "authenticity", "score": 0.75, "band": "healthy"},
    {"sensor": "suppression", "score": 0.35, "band": "notice"},
    {"sensor": "cultural_calibration", "score": 0.80, "band": "healthy"},
]
print(json.dumps(meta_aggregate(results), indent=2))
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Dir List",
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
    "sources": ["docs/meta/dir-list.md"],
    "community_feedback": []
  }
}
```
