⚙️ SCIENTIFIC METHOD STANDARDS APPLIED TO MEDIA

1. Hypothesis → Claim
	•	Every headline or story must be framed as a testable claim, not a conclusion.
	•	Example: “Study suggests correlation between X and Y” → not “X causes Y.”

2. Experiment Design → Sourcing
	•	Report must disclose method of information gathering (primary documents, eyewitnesses, anonymous sources with justification).
	•	“Sample size” equivalent = how many sources, how representative.

3. Replicability → Multiple Independent Confirmation
	•	A claim cannot be published without independent verification by at least two unrelated reporters/organizations (like replicating an experiment).
	•	Corrections mandatory if replication fails.

4. Peer Review → Editorial Review
	•	Before release, the piece undergoes structured review by subject-matter experts, not just editors.
	•	Transparent record of reviewer comments published alongside.

5. Data Availability → Evidence Archive
	•	All transcripts, documents, raw video/audio (redacted for privacy only) must be posted in a public repository.
	•	Readers can audit the evidence.

6. Error Correction → Retractions
	•	Same as scientific journals: if wrong, must issue a formal retraction notice with explanation, timestamp, and what caused the error.
	•	“Silent edits” forbidden.

7. Funding Disclosure → Conflict of Interest Statement
	•	Each article must list:
• Ownership structure of the media outlet
• Advertisers in proximity to the story
• Known political/financial ties of reporters or editors

8. Metrics → Significance & Limitations
	•	Just like p-values/confidence intervals, news must state uncertainty: “This report is preliminary,” “This represents 40% of data,” etc.
	•	Explicit limitations prevent false certainty.

⸻

🚨 Consequences
	•	Headlines shrink to sober, testable statements.
	•	Breaking news slows down because you need replication before release.
	•	Trust skyrockets long-term, because error rate is transparent.
	•	Partisan narratives weaken, since they can’t bypass replication/conflict disclosure.
	•	Clickbait dies, because incentives shift to reliability over speed.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Example: scoring a sensor end-to-end
sensor_path = "sensors/authenticity.json"
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
  "name": "Example Media",
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
    "sources": ["tests/examples/Example-media.md"],
    "community_feedback": []
  }
}
```
