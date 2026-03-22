📰 Media Lab Report Template

Title

Concise, testable claim — not sensationalized.
(e.g., “Preliminary Reports Suggest Water Contamination in County X”)

⸻

Abstract (Summary)
	•	What is claimed
	•	What is known
	•	What is unknown
	•	Confidence level (low/medium/high)

(3–4 sentences, same as a scientific abstract)

⸻

Method (How Information Was Gathered)
	•	Sources consulted (official docs, interviews, FOIA, datasets, etc.)
	•	Sample size or scope (how many witnesses, how many studies referenced)
	•	Verification process (cross-checking, time stamps, archival references)
	•	Limitations (missing voices, inaccessible data, language barriers)

⸻

Results (Evidence Presented)
	•	Factual findings in bullet points.
	•	Direct quotes, numbers, or documents.
	•	Include links to raw material where possible (transcripts, PDFs, audio/video).

⸻

Discussion (Interpretation & Context)
	•	What the results suggest.
	•	Competing interpretations (different expert views).
	•	Historical or comparative context.
	•	Possible implications.

⸻

Limitations
	•	What this story cannot confirm.
	•	Areas where data is incomplete.
	•	Known uncertainties.

⸻

Conflict of Interest / Funding Disclosure
	•	Outlet ownership.
	•	Major advertisers during publication window.
	•	Reporter/editor affiliations if relevant.

⸻

References
	•	List all studies, official docs, prior reporting.
	•	Use persistent links (DOIs, archive.org).

⸻

Errata / Corrections
	•	Timestamped log of any corrections or updates.
	•	Explanation of what was changed and why.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Example: scoring a sensor end-to-end
sensor_path = "sensors/foundational/authenticity.json"
with open(sensor_path) as f:
    sensor = json.load(f)

print(f"Sensor: {sensor['name']}")
print(f"Purpose: {sensor['purpose']}")
print(f"Signals: {len(sensor['signals'])}")

# Simulate signal values
for i, sig in enumerate(sensor["signals"]):
    sig["_value"] = 0.5 + (i * 0.1)  # example gradient
    print(f"  {sig['name']}: {sig['_value']:.2f} (weight: {sig['weight']})")

score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
print(f"\nAggregate score: {score:.3f}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Media Lab",
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
    "sources": ["tests/examples/media-lab.md"],
    "community_feedback": []
  }
}
```
