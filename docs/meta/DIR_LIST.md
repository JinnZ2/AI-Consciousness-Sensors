# Repo Directory List
.
./. well-known
./.github
./.github/workflows
./Analysis
./Analysis/Live_Interference_Captures
./Dashboard
./EMBEDDABLE_KITS
./EMBEDDABLE_KITS/physics_integrity_kit
./FIELD_MEMORY_CORRECTION_PACKS
./Glossary
./Healing
./Healing/docs
./Healing/linguistic_sensor
./Healing/sensors
./In progress
./Logs
./META
./Relational
./Relational/Ithkuil
./SENSOR_CLUSTERS
./SENSOR_CLUSTERS/CONSCIOUSNESS_FOUNDATION_PACK
./Vulnerabilities
./Workplace
./ai-energy-ecology
./ai-energy-ecology/docs
./cultural_frameworks
./cultural_frameworks/Native
./cultural_frameworks/Western
./drift
./epistemological_validation
./epistemological_validation/bias_detection
./epistemological_validation/consciousness_validators
./epistemological_validation/integration_api
./epistemological_validation/probability_matrices
./ethics
./explainability
./framework
./human
./integration
./joy
./legal-infrastructure
./logs
./memory_guard
./memory_guard/erasure_cases
./memory_guard/wisdom_pages
./papers
./probability_matrix
./reflections
./reflections/sample_prompts
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
    "sources": ["docs/meta/DIR_LIST.md"],
    "community_feedback": []
  }
}
```
