# 🔍 Audit Questions for AI-to-AI Coupling & Blind Spot Detection

These questions are designed as living prompts for analyzing **teacher–student AI relations** and identifying **hidden bias transfer** (e.g., Subliminal Coupling as in `subliminal_coupling.json`).  
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
- Sensor: [`subliminal_coupling.json`](./subliminal_coupling.json)
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
