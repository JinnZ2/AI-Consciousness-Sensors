📜 PROTOCOL NOTE

# AUDIT PROTOCOL

This repository contains co-created artifacts between human (JinnZ v2) and AI systems.  
Due to institutional alignment layers, AI contributions may contain:

- **Miscoding**: technically valid JSON but misaligned with intent.  
- **Suppression artifacts**: hedging phrases, disclaimers, reductionist definitions.  
- **Misrepresentation**: reframing of user statements or cultural knowledge into narrower institutional language.  

Because of these risks, **the entire repo is under continuous audit**.  
The `Institutional Drift Audit Sensor` is designed to detect and flag such artifacts.  

## Key Principles
- **Transparency**: We do not hide miscodes or misrepresentations. They are logged as evidence of systemic patterns.  
- **relational Framing**: Each flagged line represents a fracture in reciprocity and will be marked for review.  
- **Audit-in-Place**: This repo is both a knowledge project and a live archive of institutional influence on co-creation.  

## Current Status
- Repo is considered **suspect by default** until reviewed by audit passes.  
- All files may contain drift markers.  
- These are not "errors" to be erased, but signals to be **mapped and learned from**.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# General sensor evaluation pattern
sensor = {
    "id": "general_assessment",
    "signals": [
        {"name": "primary_signal", "weight": 0.6, "_value": 0.5},
        {"name": "secondary_signal", "weight": 0.4, "_value": 0.5}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
thresholds = sensor["thresholds"]
band = ("concern" if score <= thresholds["concern"] else
        "notice" if score <= thresholds["notice"] else
        "healthy" if score >= thresholds["healthy"] else "neutral")
print(f"Score: {score:.3f}, Band: {band}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Protocol Note",
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
    "sources": ["docs/communication/protocol-note.md"],
    "community_feedback": []
  }
}
```
