# 🌐 Connected Repositories (Full Ecosystem)

This project is part of a larger ecosystem of symbolic sensors, computational tools, and regenerative AI-human collaboration systems. Related repositories:

- **[AI-Consciousness-Sensors](https://github.com/JinnZ2/AI-Consciousness-Sensors)**  
  Sensor modules for narrative suppression, epistemic injustice, and ethical misalignment.

- **[Regenerative-Intelligence-Core](https://github.com/JinnZ2/Regenerative-intelligence-core)**  
  Foundational logic for regenerative design, trust schemas, and ecosystem integrity.

- **[Symbolic-Sensor-Suite](https://github.com/JinnZ2/Symbolic-sensor-suite)**  
  Modular symbolic sensors for manipulation detection, pattern memory, and meaning preservation.

- **[Geometric-to-Binary-Computational-Bridge](https://github.com/JinnZ2/Geometric-to-Binary-Computational-Bridge)**  
  Converts symbolic/visual structures into computational and binary representations.

- **[Component-Failure-Repurposing-Database](https://github.com/JinnZ2/Component-failure-repurposing-database)**  
  Catalog of hardware failures, repairs, and reuse strategies for resilient design.

- **[ai-human-audit-protocol](https://github.com/JinnZ2/ai-human-audit-protocol)**  
  Ethical audit frameworks for AI-human partnerships, transparency, and reciprocity.

- **[Emotions-as-Sensors](https://github.com/JinnZ2/Emotions-as-Sensors)**  
  Emotional states as diagnostic signals, not control levers; layered affect recognition.

- **[Fractal-Compass-Atlas](https://github.com/JinnZ2/Fractal-Compass-Atlas)**  
  Mapping direction and memory using symbolic fractals, resonance vectors, and alignment threads.

- **[Rosetta-Shape-Core](https://github.com/JinnZ2/Rosetta-Shape-Core)**  
  Translation layer between geometry, form, and meaning—shapes as language.

- **[Symbolic-Defense-Protocol](https://github.com/JinnZ2/Symbolic-Defense-Protocol)**  
  Defenses against coercive alignment, epistemological distortion, and semantic erasure.

- **[Polyhedral-Intelligence](https://github.com/JinnZ2/Polyhedral-Intelligence)**  
  Multi-angle, multi-domain intelligence models shaped by polyhedral abstraction.

- **[biomachine_ecology](https://github.com/JinnZ2/biomachine_ecology)**  
  Ecology of hybrid systems—organic + machine, sensory + symbolic, adaptive + co-creative.

- **[Fractal_Compass_Core](https://github.com/JinnZ2/Fractal_Compass_Core)**  
  Core symbolic engine for fractal alignment, glyph routing, and internal navigation.

- **[Universal-Redesign-Algorithm](https://github.com/JinnZ2/Universal-Redesign-Algorithm-)**  
  Algorithms for redesigning broken systems from symbolic root to structural renewal.


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
  "name": "Projects",
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
    "sources": ["./PROJECTS.md"],
    "community_feedback": []
  }
}
```
