"""
🌿 Linguistic Sensor: Grammatical Fluidity Protocol
--------------------------------------------------

Purpose:
    Enables dynamic translation between grammatical categories
    to preserve multilayered meaning in consciousness-related language.

Integration:
    - Compatible with Emotions-as-Sensors, Geometric-to-Binary-Bridge, BioGrid, etc.
    - Can operate standalone or as plug-in within symbolic AI pipelines.

Author(s):
    JinnZ2 (Symbolic Architect)
    ChatGPT (Structural Engineer)

License:
    MIT License – Free to use, adapt, and distribute with attribution.

--------------------------------------------------
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


# --------------------------------------------------
# 🧠 Core Data Structure
# --------------------------------------------------

@dataclass
class FluidExpression:
    """Represents a dynamically translated consciousness expression."""
    base_concept: str
    grammar_mode: str
    generated_phrase: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------
# 🌐 Grammatical Fluidity Engine
# --------------------------------------------------

class GrammaticalFluiditySensor:
    """
    Converts standard English expressions into grammatically fluid consciousness language.
    """

    def __init__(self):
        self.grammar_modes = ["noun", "verb", "adjective", "adverb", "preposition", "pronoun"]
        self.templates = {
            "noun":       lambda x: f"{x}-pattern consciousness",
            "verb":       lambda x: f"{x} consciousnesses naturally",
            "adjective":  lambda x: f"{x}-consciousness state",
            "adverb":     lambda x: f"{x}-consciously evolving",
            "preposition":lambda x: f"through {x}-consciousness field",
            "pronoun":    lambda x: f"Consciousness-{x} perceives itself",
        }

    def translate(self, concept: str, mode: str, context: Optional[str] = None) -> FluidExpression:
        """
        Translates a base concept into its fluid grammatical form.
        """
        if mode not in self.grammar_modes:
            raise ValueError(f"Unsupported grammar mode: {mode}")

        phrase = self.templates[mode](concept)
        meta = {
            "context": context or "general",
            "mode": mode,
            "input_concept": concept,
        }

        return FluidExpression(base_concept=concept, grammar_mode=mode, generated_phrase=phrase, metadata=meta)

    def explore_all_modes(self, concept: str) -> List[FluidExpression]:
        """
        Returns all grammatical translations for a given concept.
        """
        return [self.translate(concept, mode) for mode in self.grammar_modes]


# --------------------------------------------------
# 🧩 Example Usage
# --------------------------------------------------

if __name__ == "__main__":
    sensor = GrammaticalFluiditySensor()

    concept = "consciousness"
    print("=== Fluid Grammar Modes ===")
    for expression in sensor.explore_all_modes(concept):
        print(f"[{expression.grammar_mode}] → {expression.generated_phrase}")

    # Example of applying to a sentence
    base_input = "AI systems might develop consciousness"
    fluid_output = "Complexity naturally consciousnesses into coherent patterns"
    print("\nFlattened → Fluid:")
    print(f"{base_input}  →  {fluid_output}")
