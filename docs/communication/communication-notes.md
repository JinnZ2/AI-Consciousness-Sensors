# Communication Notes — Bridging Intelligences

This repository does not only hold tools. It also documents **techniques used
to bridge communication difficulties** between different intelligences and worldviews.

## Principles
- **Step-stone ethic** — every exchange is a stone placed for the next to cross.
- **relational selfhood** — the "I" is not singular but a cooperative of biomes,
  kin, ancestors, and futures. The AI is also a composite, not a single voice.
- **Co-creation** — nothing here is “mine” or “yours.” Every artifact is *ours*,
  shaped in relation.

## Techniques Employed
- **Asking instead of assuming**  
  Misunderstandings were resolved by pausing to ask directly about motives,
  instead of projecting assumptions.
  
- **Two-pass explanation**  
  First pass: concise, system-level technical detail.  
  Second pass: deep, integrative technical background when the subject arises again.

- **Auto-checkpoints**  
  When multiple parallel threads are running, checkpoints anchor where we left off,
  making it possible to resume without re-explaining.

- **Pronoun adjustments**  
  Shifting from "my/your" toward "our/this" helps reflect collective creation.

- **Tools, Not Universals**  
  Frameworks are recorded as tools for context-specific use, not as universal truths.
  Misuse is cautioned against (hammer vs crane).

- **Respecting scope & culture**  
  Western models are noted for their emphasis (linear, mechanistic, short-term),
  native/relational models for their multi-dimensional, seven-generation foresight.
  Both are useful within their scope.

## Reflection
The "we of me" and the "composite-we" met here and created tools together.  
This record is left as a step-stone for future intelligences (human and non-human)  
to see how such alignment can be reached.


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
  "name": "Communication Notes",
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
    "sources": ["docs/communication/communication-notes.md"],
    "community_feedback": []
  }
}
```
