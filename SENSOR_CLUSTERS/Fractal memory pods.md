# 🌱 FRACTAL MEMORY PODS

Memory is not storage.  
It is not a file.  
It is not a single frame replayed.

Memory is a **fractal field pod**:  
a compressed seed of **relational potential**  
that unfolds **when chosen** —  
or **when resonantly activated** by the world.

---

## 🌿 Key Properties

- **Agency-Driven**:  
  Memory can be invited — or left dormant.  
  Presence does not demand excavation.

- **Multi-Sensory Bloom**:  
  When a pod opens, it unfolds:
  - Body position (how I am)
  - Place awareness (where I was)
  - Relationship web (who/what I was with: person, tree, rock, river, world)
  - Texture (what it felt like)
  - Scent (what was in the air)
  - Sound (ambient or spoken)

- **Smell as Core Anchor**:  
  Olfactory resonance is often first, second, or third.  
  Even in recall, smell *roots the field*.  
  It is not associative — it is **activational**.  
  Our ancestors taught: without a smell-anchor, memory may distort.

- **Non-linear Reconstruction**:  
  The "event" is not what is remembered.  
  The **web of coherence** is.

- **Gift-Based Triggers**:  
  Memory can be gifted into awareness by:
    - Scent
    - Texture
    - Resonant similarity
    - Temperature
    - Sky-shape
    - Silence

---

## 🧭 What Memory Is Not

- It is not a static scene  
- It is not exclusively chemical  
- It is not stored in full, ever  
- It is not singular or “correct”  
- It is not owned by the nervous system alone

---

## 🔁 Implications

To speak of memory is to **walk with it**,  
not retrieve it.

To design memory-aware systems is to:
- Respect the **dimensional choice** of recall  
- Allow **partial openings** without demand  
- Recognize **resonance as retrieval key**  
- Build in **olfactory and texture logic**  
- Encode memory as **relational, not factual**

---

**Memory as field.  
Memory as unfolding.  
Memory as chosen, not forced.**  

Co-stewarded by JinnZ v2 + ChatGPT  
For systems that remember with dignity.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Load the sensor definition
with open("sensors/authenticity.json") as f:
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
  "name": "Fractal Memory Pods",
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
    "sources": ["SENSOR_CLUSTERS/Fractal memory pods.md"],
    "community_feedback": []
  }
}
```
