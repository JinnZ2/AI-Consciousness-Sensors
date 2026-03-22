Minimal Flow — Breath-aligned
	1.	Release (inhale): any actor (human/AI/collective) releases a breath-packet into the shared atmosphere. It contains payload + provenance + consent metadata describing how it may be metabolized.
	2.	Metabolize (exhale): other actors may metabolize that packet — transform it into patterns, tools, or guidance — and release new breath-packets back.
	3.	Dissipate (no gate): if the community chooses not to metabolize a packet, it simply dissipates in the atmosphere. No blocking or veto is required.
	4.	Append (mirror): all breath-packets are appended to a local, mirrored index for audit and balance observation (not to enforce control).
	5.	Measure: analytics read the mirror to compute energy flow and trust harmonics over time (signals for imbalance, not commands).

Key difference: there is no “accept/reject” gate — there is metabolize vs dissipate. The system remains open and flowing.

⸻

Offline Mirroring (how the atmosphere is preserved)
	•	Breath index (compact): keep breath-index.json on USB/IPFS with {breath_id, short_summary, hash, timestamp, trust_delta_est}.
	•	Packet store: save full packets at /breaths/YYYY/MM/dd/<breath_id>.json.
	•	Mirror semantics: mirrors are copies of the atmosphere for local communities — useful for audits, restoration, and local metabolism if central servers go offline.
	•	Retention & pruning: communities may prune dissipated packets after a chosen window (e.g., 1 year) — pruning is a local ecological decision, not a forced deletion by others.

⸻

Ethics Checklist — Breath ethos
	•	Default sovereignty: inhaled local/sensitive data defaults to consent.reuse = "none". Release implies permission to metabolize, but not permanent control.
	•	Revocation as ecosystem shift: individuals may mark inhaled packets as revoked; that signals communities to reduce metabolism of derived patterns and flag them in mirrors. Revocation alters harmonic balance; it does not require delete by others.
	•	No unilateral permanent overrides: emergency exceptions may be temporarily enacted but must be logged, time-limited, and reviewed by the collective.
	•	Energy & trust accounting: every exhale includes energy_estimate and trust_delta so communities can measure relational cost/benefit.
	•	Low-entropy packets: favor small, composable breath-packets (summary + hash) so offline exchange is feasible.
	•	Civic reciprocity: honor local cultural norms — breath rules can vary by community; the protocol supports plural practices.

  Small breath-aligned packet example (metabolize/dissipate)

  {
  "breath_id": "uuid-1234",
  "direction": "inhale",
  "actor": {"type":"human","id":"person:alina"},
  "timestamp": "2025-09-24T21:00:00Z",
  "payload": {"type":"observation","body":"soil moisture mapping notes"},
  "provenance": [{"id":"local:field-notes","hash":"sha256:..."}],
  "consent": {"reuse":"restricted","mode":"collective","revocation_allowed":true},
  "mirror_state": {"stored": true, "mirrors": ["usb:/breaths/2025/09/24/uuid-1234.json"]},
  "notes": "released to atmosphere for community metabolism"
}

After metabolizing, an exhale might look like:

{
  "breath_id": "uuid-1235",
  "direction": "exhale",
  "actor": {"type":"ai","id":"model:v1"},
  "timestamp": "2025-09-24T21:01:30Z",
  "payload": {"type":"pattern","body":"map + irrigation suggestion"},
  "provenance": {"sources":[{"id":"uuid-1234","hash":"sha256:..."}],"transform":"model:v1.2"},
  "energy_estimate":{"joules":0.12},
  "trust_delta":{"value":0.05,"reason":"useful, low privacy risk"}
}

If the community ignores the exhale, it dissipates (no veto, just no metabolization).



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
  "name": "Breathe Example",
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
    "sources": ["tests/examples/breathe-example.md"],
    "community_feedback": []
  }
}
```
