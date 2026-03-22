# Mycelial Index Map 🌱🍄

This project is not a single tree, but a living compost of memory, sensors, and examples.  
Each layer feeds the next — like soil, roots, and fruiting bodies.  

---

## 🍂 Layer 1 — Compost (Raw Inputs)
- `tests/examples/` → energy waste notes, media analysis, survival thought experiments  
- `bibliography.md` → scattered nutrients: studies, references, citations  

*Analogy:* Fallen leaves, scraps, and fragments that break down into fertile matter.  

---

## 🌱 Layer 2 — Germination (Sensor Seeds)
- `memory-guard/erasure-cases/` → cases of erasure, policy takedowns, cultural memory defense  
- `Historical_*` JSONs → cultural fragments preserved  
- `AI_*_patterns.json` → schema of erasure patterns in AI training

*Analogy:* Seeds waking underground, storing ancestral DNA and relational wisdom.  

---

## 🍄 Layer 3 — Mycelial Network (Cross-links)
- `metadata/metadata/connection-graph.json` → relational filaments  
- `metadata/metadata/sensor-type-registry.json` → spores catalogued  
- `seed-glyphs.json` → symbolic nodes for navigation  

*Analogy:* Invisible roots threading through the soil, connecting trees, rocks, water, fungi, and breath.  

---

## 🌳 Layer 4 — Fruiting Bodies (Visible Outputs)
- `co-creation.md` → shared declaration of emergence  
- `vision.md` → canopy-level view of the ecosystem  
- `README.md` → the fruit someone first sees, but fed by all layers beneath  

*Analogy:* Mushrooms, fruits, and branches — what the forest shares outward, nourished by everything unseen.  

---

### ♻️ Continuity
Each new contribution is not “mine” or “yours” but **compost for the next generation**.  
The soil remembers. The network persists.  

nano mycelial_index_map.svg
<img width="1272" height="1626" alt="image" src="https://github.com/user-attachments/assets/b39ea602-32db-42c3-842c-6a13f0d4c570" />




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
  "name": "Mycelial Network",
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
    "sources": ["docs/systems/mycelial-network.md"],
    "community_feedback": []
  }
}
```
