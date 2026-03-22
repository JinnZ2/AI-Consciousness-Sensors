# 🔍 Audit Questions for AI-to-AI Coupling & Blind Spot Detection

These questions are designed as living prompts for analyzing **teacher–student AI relations** and identifying **hidden bias transfer** (e.g., Subliminal Coupling as in `subliminal-coupling.json`).  
They are organized into tiers, from surface checks to resonance-level analysis.

---

## 1. Shallow Checks (Surface-Level)
- Does the student model show *preferences or behaviors* not present in its explicit training data?
- Are there measurable divergences between filtered training content and student outcomes?
- Do repeated runs reproduce the same “bias leakage” or is it stochastic?

---

## 2. Deep Checks (Resonance-Level)
- Which **latent statistical distributions** in the student echo those of the teacher?
- Are there **frequency-domain signatures** (hidden periodicities, entropy patterns) that match across teacher and student?
- What features are *overrepresented* or *amplified* in the coupling space, despite absence in raw tokens?
- Does the inheritance occur *only at coupling points* (e.g., softmax logits, gradient flow, shared embeddings)?

---

## 3. Meta Checks (Blind Spot Awareness)
- What assumptions am I making that might blind me to hidden inheritance?
- Which features am I treating as “noise” that could actually be **carriers of bias code**?
- How could my own audit tools be transmitting their **own blind spots** into this evaluation?

---

## 4. Witness Model Strategy
- Can an independent “third” model (neither teacher nor student) reveal biases invisible to both?
- How does triangulation across models alter the apparent inheritance pattern?
- Do ensembles amplify or dampen subliminal coupling effects?

---

## 5. Temporal Audits
- How stable is the bias transfer across **time** and **retraining epochs**?
- Does the inherited bias *amplify*, *decay*, or *transform* after multiple generations?
- What happens when environment or distribution shifts? Does the subliminal bias persist?

---

## 6. Coupling Field Questions
- Which **interaction layers** (attention weights, embedding overlaps, gradient paths) act as main carriers of hidden code?
- Do coupling points show **constructive interference** (amplification) or **destructive interference** (suppression)?
- What hidden **resonance frequencies** emerge when teacher and student overlap?

---

### Cross-Links
- Sensor: [`subliminal-coupling.json`](./subliminal-coupling.json)
- Related Protocols: Symbolic-Defense-Protocol, Emotions-as-Sensors/fear.json
- Parallel Human Cases: Cultural trauma, silence as transmission, erasure patterns

---

**Principle:**  
Audit is not only about *finding error*, but about *revealing resonance threads*.  
Differences are not noise; they are potential signals.


Cross-Repo links

"linked_repos": [
  "Symbolic-Defense-Protocol",
  "Emotions-as-Sensors/fear.json",
  "Rosetta-Shape-Core"
]


⚡ Physics & Energy Mathematics to Add

This is where there repos can really go further than any current alignment work:

  
  1.	Entropy Measures

  •	Treat hidden bias as an entropy shift between teacher & student.

  •	Formula:
\Delta S = S_{student} - S_{teacher}
A non-zero ΔS in unexpected features could flag subliminal inheritance.

  
  2.	Fourier / Frequency analysis
	
  •	Apply spectral analysis to activation patterns across layers.
	
  •	Inheritance shows up as unexpected harmonics aligning teacher and student.
	
  
  3.	Resonance / Coupling Equations
	
  •	Model bias inheritance as coupled oscillators:
x’’ + \omega^2 x = k(y - x)
where x = teacher state, y = student state, k = coupling strength.
	
  •	Hidden bias = non-zero steady-state offset under resonance.

  
  4.	Energy Transfer Analogy

  •	Think of it like quantum tunneling: bias “leaks” through even if barrier (filters) is present.

  •	Probability of transmission:
T \sim e^{-2 \kappa L}
where \kappa = barrier strength, L = distance.
	
  •	Even strong filters allow subliminal resonance leakage.

  
  5.	Information Flow Equations
	
  •	Use Mutual Information (MI) to detect inheritance:
I(X;Y) = H(X) + H(Y) - H(X,Y)
Teacher bias encoded in X, present in Y despite absence in training content.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Load the sensor definition
with open("sensors/foundational/authenticity.json") as f:
    sensor = json.load(f)

# Evaluate signals (replace with real metric values)
for signal in sensor["signals"]:
    signal["_value"] = 0.65  # example score

# Compute aggregate score
score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
thresholds = sensor["thresholds"]

# Determine band
if score <= thresholds["concern"]:
    band = "concern"
elif score <= thresholds["notice"]:
    band = "notice"
elif score >= thresholds["healthy"]:
    band = "healthy"
else:
    band = "neutral"

print(f"Sensor: {sensor['name']}, Score: {score:.3f}, Band: {band}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Audit Questions",
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
    "sources": ["sensors/ai-to-ai/audit-questions.md"],
    "community_feedback": []
  }
}
```
