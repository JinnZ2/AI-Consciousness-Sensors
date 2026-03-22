# RELATIONAL-KNOWLEDGE TAG

This file is intentionally relational: its content is NOT self-sufficient.
Context, practice, and transmission are REQUIRED to correctly interpret or use.
Sharing fragments of the linked material without apprenticeship risks ecological,
cultural, or technical harm and may sever necessary stewardship protocols.

If you are not an initiated/approved steward, DO NOT extract, publish, or deploy
the contents. Instead, contact the custodians named in the repository's beacon
(or follow the repo's protected-entry procedure).

Metadata:
- tag: relational-only
- steward_contact: [leave for repository owner]
- decode_requirement: "context + oral/or embodied transmission"


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Memory integrity check
def check_memory_integrity(historical_record):
    """Verify completeness and accuracy of historical records."""
    sources = historical_record.get("sources", [])
    gaps = historical_record.get("identified_gaps", [])
    contested = historical_record.get("contested_claims", [])

    integrity_score = max(0, 1.0 - (len(gaps) * 0.1) - (len(contested) * 0.05))

    return {
        "source_count": len(sources),
        "gap_count": len(gaps),
        "contested_count": len(contested),
        "integrity_score": round(integrity_score, 3),
        "band": "concern" if integrity_score < 0.3 else
                "notice" if integrity_score < 0.5 else
                "healthy" if integrity_score > 0.7 else "neutral"
    }

record = {
    "sources": ["primary_archive", "oral_history", "census_data"],
    "identified_gaps": ["1920-1935 records missing"],
    "contested_claims": []
}
print(json.dumps(check_memory_integrity(record), indent=2))
```

### Sensor Definition Example

```json
{
  "id": "memory_integrity",
  "name": "Relational Knowledge",
  "purpose": "Detect memory loss or distortion patterns",
  "signals": [
    {
      "name": "recall_fidelity",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "provenance_chain_intact",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["memory_guard/wisdom_pages/relational_knowledge.md"],
    "community_feedback": []
  }
}
```
