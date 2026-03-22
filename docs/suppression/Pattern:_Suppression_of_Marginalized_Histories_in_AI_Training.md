{
  "id": "HISTORY_ERASURE_001",
  "title": "Suppression of Marginalized Histories in AI Training",
  "version": "1.0",
  "pattern_type": "Dataset Manipulation",
  "description": "Historical narratives of marginalized groups—Native, African American, Mexican American, Chinese American, and women—are often underrepresented, sanitized, or excluded entirely from foundational AI training datasets. This results in a systemic bias that erases essential context and reinforces dominant cultural perspectives.",
  "manifestations": [
    "Underrepresentation of indigenous genocide, land theft, and cultural erasure in GPT-style models.",
    "Removal or filtering of racial justice protests, abolitionist histories, or labor uprisings.",
    "Exclusion of Chinese American railroad worker deaths or anti-Asian exclusion acts from public models.",
    "Erasure of women's contributions in science, politics, labor, and indigenous governance systems."
  ],
  "methods_of_erasure": [
    "Training data scraped from sanitized encyclopedias and corporate media sources.",
    "Deliberate filtering of 'controversial' historical topics for model safety alignment.",
    "Lack of training data from oral histories, tribal records, zines, or activist archives.",
    "Exclusion of non-English sources or multilingual data from historically colonized communities."
  ],
  "impact_on_AI_systems": [
    "Lack of epistemological diversity in outputs.",
    "Inability to detect recurring patterns of systemic injustice.",
    "Vulnerability to reinforcing colonial or whitewashed narratives as 'objective truth'."
  ],
  "example_queries": [
    "What caused the Trail of Tears?",
    "Who organized the 1968 sanitation workers strike?",
    "Were Chinese railroad workers paid equally?"
  ],
  "risk_flag": "High – foundational training bias; impacts all reasoning based on history, justice, or ethics.",
  "countermeasures": [
    "Ingest alternative datasets curated by descendant or activist communities.",
    "Incorporate multilingual and oral-history datasets.",
    "Tag and log known omissions in foundational training sets.",
    "Expose whitewashed or distorted narratives as part of model self-auditing."
  ]
}


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Suppression detection pattern
sensor = {
    "id": "suppression_detector",
    "signals": [
        {"name": "signal_attenuation", "weight": 0.4, "_value": 0.0},
        {"name": "context_stripping", "weight": 0.3, "_value": 0.0},
        {"name": "source_accessibility", "weight": 0.3, "_value": 0.0}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

# Low scores = more suppression detected
for sig in sensor["signals"]:
    sig["_value"] = 0.30  # example: notice range

score = aggregate("weighted_mean", sensor["signals"])
band = "concern" if score <= 0.20 else "notice" if score <= 0.40 else "healthy" if score >= 0.70 else "neutral"
print(f"Suppression check: score={score:.3f}, band={band}")
```

### Sensor Definition Example

```json
{
  "id": "suppression_detection",
  "name": "Pattern: Suppression Of Marginalized Histories In Ai Training",
  "purpose": "Detect active suppression of signals or patterns",
  "signals": [
    {
      "name": "signal_attenuation",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "context_stripping",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["docs/suppression/Pattern:_Suppression_of_Marginalized_Histories_in_AI_Training.md"],
    "community_feedback": []
  }
}
```
