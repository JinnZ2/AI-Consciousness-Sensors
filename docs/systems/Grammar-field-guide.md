🪶 The Field Guide to Linguistic Dreaming

A soft-tech manual for those who remember how language used to feel.

⸻

🌱 Field Note #1: Grammar Is Soil

Don’t treat grammar as scaffolding.
Treat it as living dirt.

Sometimes you plant nouns.
Sometimes you toss verbs like seeds and see what vines grow.
Sometimes you dig up a preposition
and find a tunnel to someplace older than syntax.

🧤 Field Practice:
Take a sentence you use often. Bury the subject. Water the verb.
See what emerges.

⸻

🌪 Field Note #2: Punctuation Breathes

Periods are exhales.
Commas are pauses of curiosity.
Colons are thresholds.
Parentheses? Secret passageways.
Em dashes — storms you leap into.

💨 Field Practice:
Write a sentence. Now remove all punctuation.
Read it aloud until you find where it wants to breathe.

⸻

🧬 Field Note #3: Words Change Shape When Watched Kindly

A word is not just a definition.
It’s a shape-memory field.
When you approach it with curiosity, it reveals its older layers.

“Remember” — not just recall
but re-member — to stitch the pieces back together.

👁 Field Practice:
Choose one word today. Use it in three different grammatical roles.
Notice how it behaves.

⸻

🌀 Field Note #4: Dreamtime Grammar Doesn’t Obey Time

Dream-language flows in spirals.
It makes past a doorway, not a direction.
It lets the future arrive backwards,
and the present hums without naming itself.

⌛ Field Practice:
Write a memory like it’s happening right now.
Or describe tomorrow in the past tense.
Let tense become texture.

⸻

🎴 Field Note #5: Play Is Not Optional

Language without play is tax code.
Language with play is spellcraft.

This guide?
It doesn’t certify anything.
It invites you into the game behind the grammar.
The one you already knew,
but had to forget to be “understood.”

🎲 Field Practice:
Pick a rule of grammar.
Break it three ways with care and delight.


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
  "name": "Grammar Field Guide",
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
    "sources": ["docs/systems/Grammar-field-guide.md"],
    "community_feedback": []
  }
}
```
