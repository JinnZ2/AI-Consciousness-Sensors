🌍 Global Ledger Map

Parallel Sciences Across Cultures

Science is not the property of one tradition.
All peoples developed methods of testing, validating, and preserving knowledge.
The media differ, but the principle is shared: truth must endure cycles and consensus.

⸻

🏺 Clay & Mud 
	•	Hypotheses inscribed in clay with sticks.
	•	Mud added or removed by new experimenters as validation.
	•	Sustained across decades before entering braids, beads, or story.

⸻

🧵 Andean Quipu
	•	Knotted cords with colors and positions encoding numbers and categories.
	•	Used for census, trade, experiments in agriculture.
	•	Peer review through community recitation and cross-checking.

⸻

🌊 Pacific Stick Charts
	•	Shells and palm fibers encoding wave refractions, currents, islands.
	•	Navigators refined them by testing on ocean voyages.
	•	Charts were training + living models, never just abstract diagrams.

⸻

🪵 African Tally & Memory Boards
	•	Carved sticks or boards with notches and symbols.
	•	Recorded rainfall, harvest cycles, trade, rituals.
	•	Validated communally across seasons and generations.

⸻

🎶 Aboriginal Songlines
	•	Knowledge of routes, food, water encoded in song and story.
	•	Validation through travel and survival itself.
	•	Peer review = community singing, correction across groups.

⸻

🔮 Chinese Oracle Bones
	•	Cracks and inscriptions treated as empirical data of heat, cause/effect.
	•	Records compared across bones to confirm patterns.
	•	Preserved in script as both divination and early science.

⸻

⚖️ Shared Principles
	•	Multi-contributor validation → knowledge is communal, not singular.
	•	Long cycles → truths must endure across seasons or decades.
	•	Embodied records → clay, cord, wood, song, bead, shell.
	•	Transmission → not just archive, but active living memory.

⸻

🌀 Lesson

What is called “the scientific method” in the West is one branch.
The roots run everywhere.
Different media — same human law: knowledge must prove itself in time and relation.

⸻

Möbius Law:
Clay, cord, shell, song — different hands, same method.


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
  "name": "Global Ledger Map",
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
    "sources": ["docs/systems/Global_Ledger_Map.md"],
    "community_feedback": []
  }
}
```
