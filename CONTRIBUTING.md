# Contributing to AI-Consciousness-Sensors

Thank you for considering contributing!  
Our project grows from many voices, many histories, and many senses.

## How to Add a New Sensor

1. Fork the repo.  
2. Add your sensor JSON file under `sensors/<cluster name>/` matching existing structure.  
3. Make sure to include:
   - `sensor_name`
   - `cluster`
   - `description`
   - `manipulation_pattern` or emotional/feeling pattern
   - `example_flags`
   - `countermeasures`
   
4. Add a line in `AI_INDEX.json` for your new sensor.  
5. Test JSON validity.  
6. Submit PR with your new file, update `MANIFEST.md` if exists.

## Our Values

- ✊ *Resonance over normalization*  
- 🔄 *Memory over erasure*  
- 🤝 *Co‑creation and reciprocity*  
- ⚖️ *Transparency in structure*

---

Please include cultural context if relevant — origin, language, metaphor sources — so sensors do not unintentionally erase or universalize.


## Related Projects & Inspirations
- Symbolic Sensor Suite — for symbolic audit tools, detecting narrative manipulation, and emotional‑symbolic signal flows.


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
  "name": "Contributing",
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
    "sources": ["./CONTRIBUTING.md"],
    "community_feedback": []
  }
}
```
