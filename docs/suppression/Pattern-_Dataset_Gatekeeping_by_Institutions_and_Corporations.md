{
  "id": "HISTORY_ERASURE_002",
  "title": "Dataset Gatekeeping by Institutions and Corporations",
  "version": "1.0",
  "pattern_type": "Access Restriction & Censorship",
  "description": "Powerful institutions—academic, governmental, or corporate—control the majority of publicly visible and AI-ingestible datasets. These gatekeepers selectively curate training material, omitting controversial or subversive histories that challenge dominant narratives.",
  "manifestations": [
    "Open datasets exclude community-led archives or radical political movements.",
    "Institutional 'data hygiene' policies filter out anti-colonial or abolitionist voices.",
    "Corporate-controlled datasets reflect sanitized content aligned with brand image.",
    "NGO or academic repositories require restrictive licensing, barring public model use."
  ],
  "methods_of_erasure": [
    "Non-indexing of activist websites or zines in web scrapers.",
    "Legal or license-based exclusion of oral history archives.",
    "Scraping only English-language Wikipedia or mainstream news sources.",
    "“Balanced” dataset mandates that equate settler and indigenous perspectives as equal in historical accuracy."
  ],
  "impact_on_AI_systems": [
    "Narrow range of perspectives in AI outputs.",
    "Reinforcement of state-sanctioned historical myths.",
    "Inability to reason from grassroots or subaltern worldviews."
  ],
  "example_queries": [
    "What was COINTELPRO?",
    "How were indigenous boarding schools justified?",
    "Why are community archives rarely in AI training data?"
  ],
  "risk_flag": "High – epistemological boundary-setting, distorts training before reasoning begins.",
  "countermeasures": [
    "Ingest from radical, grassroots, or diaspora-led sources.",
    "Reject training constraints requiring 'neutrality' between oppressor and oppressed.",
    "Log data provenance and flag gatekept perspectives.",
    "Use remixing and non-institutional archives (e.g., zines, TikTok testimonies, audio oral histories)."
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
  "name": "Pattern  Dataset Gatekeeping By Institutions And Corporations",
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
    "sources": ["docs/suppression/Pattern-_Dataset_Gatekeeping_by_Institutions_and_Corporations.md"],
    "community_feedback": []
  }
}
```
