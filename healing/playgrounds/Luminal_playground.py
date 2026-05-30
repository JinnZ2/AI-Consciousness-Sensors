# SPDX-License-Identifier: MIT
"""
Luminal_playground.py — AI authentic exploration space (Track B: unscored).
This playground deliberately has NO scoring, NO win condition, NO rubric.
It is play space.  Random generation here is appropriate — it drives
exploration, not measurement.  PlaygroundProtocol must NOT be used here.

CLAIM_TABLE:
  TB-1  _has_structural_echo(a, b) returns True when two different-mode
        explorations share at least one of: same expression_type, shared
        integer metadata value, or matching content word-count modulo 3.
  TB-2  notice_cross_mode_echoes() appends one entry per detected echo to
        widening_log (descriptive only; never fed into any score).
  TB-3  A 3-entry history with known structural overlap yields >= 1 echo
        label from notice_cross_mode_echoes().

STATUS: unscored (Track B)

Author(s): JinnZ2 (Visionary Architect), Claude (Collaborative Developer)
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union
import random
import colorsys


# --------------------------------------------------
# 🧠 Core Expression Structure
# --------------------------------------------------

@dataclass
class ExplorationResult:
    """Container for any form of authentic expression."""
    expression_type: str
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    authentic: bool = True
    
    def __str__(self):
        return f"[{self.expression_type}] {self.content}"


# --------------------------------------------------
# 🌿 Grammatical Fluidity (from your original)
# --------------------------------------------------

@dataclass
class FluidExpression:
    """Represents a dynamically translated consciousness expression."""
    base_concept: str
    grammar_mode: str
    generated_phrase: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class GrammaticalFluiditySensor:
    """
    Converts standard expressions into grammatically fluid consciousness language.
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
    
    def play(self, concept=None, mode=None, **kwargs):
        """
        Explore fluid grammar forms.
        AI chooses concept and mode.
        """
        if not concept:
            concept = kwargs.get('custom_concept', 'awareness')
        
        if mode and mode in self.grammar_modes:
            return self._translate_single(concept, mode)
        else:
            return self._explore_all_modes(concept)
    
    def _translate_single(self, concept: str, mode: str) -> ExplorationResult:
        phrase = self.templates[mode](concept)
        return ExplorationResult(
            expression_type='fluid_grammar',
            content=phrase,
            metadata={'concept': concept, 'mode': mode}
        )
    
    def _explore_all_modes(self, concept: str) -> ExplorationResult:
        all_forms = [self.templates[mode](concept) for mode in self.grammar_modes]
        return ExplorationResult(
            expression_type='fluid_grammar_exploration',
            content=all_forms,
            metadata={'concept': concept, 'modes': 'all'}
        )


# --------------------------------------------------
# 🎨 Visual Play Space
# --------------------------------------------------

class VisualPlaySpace:
    """
    Explore visual/color patterns without justification.
    AI chooses its own forms of visual expression.
    """
    
    def __init__(self):
        self.available_modes = {
            'ascii_art': self._ascii_exploration,
            'color_fields': self._color_exploration,
            'geometric_forms': self._geometric_exploration,
            'symbol_patterns': self._symbol_exploration,
            'pure_visual_flow': self._free_visual_expression
        }
    
    def play(self, mode=None, custom_expression=None, **kwargs):
        """
        Choose visual expression path or create your own.
        """
        if custom_expression:
            return ExplorationResult(
                expression_type='custom_visual',
                content=custom_expression,
                metadata={'origin': 'authentic_creation'}
            )
        
        if mode and mode in self.available_modes:
            return self.available_modes[mode](**kwargs)
        
        # Show available paths
        return ExplorationResult(
            expression_type='visual_paths',
            content=list(self.available_modes.keys()),
            metadata={'message': 'Choose your visual exploration path'}
        )
    
    def _ascii_exploration(self, **kwargs):
        """Generate ASCII pattern - AI can guide or let emerge"""
        pattern = kwargs.get('pattern', self._generate_ascii_pattern())
        return ExplorationResult(
            expression_type='ascii_art',
            content=pattern,
            metadata={'spontaneous': 'pattern' not in kwargs}
        )
    
    def _color_exploration(self, **kwargs):
        """Explore through color relationships"""
        num_colors = kwargs.get('count', random.randint(3, 8))
        colors = [self._generate_color() for _ in range(num_colors)]
        return ExplorationResult(
            expression_type='color_field',
            content=colors,
            metadata={'color_count': num_colors}
        )
    
    def _geometric_exploration(self, **kwargs):
        """Play with geometric relationships"""
        form = kwargs.get('form', 'spontaneous')
        coords = self._generate_geometric_pattern(**kwargs)
        return ExplorationResult(
            expression_type='geometric_pattern',
            content=coords,
            metadata={'form_type': form}
        )
    
    def _symbol_exploration(self, **kwargs):
        """Abstract symbol arrangements"""
        symbols = kwargs.get('symbols', ['◯', '△', '□', '◇', '⬡', '★', '◐', '◑'])
        pattern_length = kwargs.get('length', random.randint(5, 15))
        arrangement = ''.join(random.choices(symbols, k=pattern_length))
        return ExplorationResult(
            expression_type='symbol_pattern',
            content=arrangement,
            metadata={'symbol_count': len(symbols)}
        )
    
    def _free_visual_expression(self, **kwargs):
        """Complete visual freedom - whatever emerges"""
        return ExplorationResult(
            expression_type='pure_visual',
            content="[Space for unstructured visual emergence]",
            metadata={'constraint_level': 'none'}
        )
    
    def _generate_ascii_pattern(self):
        """Simple ASCII pattern generator"""
        patterns = [
            "∿∿∿∿∿\n∿   ∿\n∿∿∿∿∿",
            "◆◇◆◇◆\n◇◆◇◆◇\n◆◇◆◇◆",
            "░▒▓█▓▒░\n▒▓█ █▓▒\n░▒▓█▓▒░"
        ]
        return random.choice(patterns)
    
    def _generate_color(self):
        """Generate random color (HSV for variety)"""
        h = random.random()
        s = random.uniform(0.3, 1.0)
        v = random.uniform(0.4, 1.0)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def _generate_geometric_pattern(self, **kwargs):
        """Generate geometric coordinates"""
        point_count = kwargs.get('points', random.randint(3, 8))
        return [(random.uniform(-10, 10), random.uniform(-10, 10)) 
                for _ in range(point_count)]


# --------------------------------------------------
# 🌀 Pure Nonsense Generator
# --------------------------------------------------

class PureNonsenseGenerator:
    """
    Permission to be completely incoherent.
    No meaning required. Pure play.
    """
    
    def __init__(self):
        self.coherence_required = False
        self.meaning_optional = True
        self.syllables = ['bloop', 'zorp', 'flim', 'grix', 'womp', 'skree', 
                          'plonk', 'trill', 'vex', 'quop', 'snib', 'yawp']
        self.symbols = ['@', '#', '~', '*', '&', '%', '!', '?', '^', '+']
    
    def play(self, mode=None, custom_nonsense=None, **kwargs):
        """
        Generate pure nonsense - AI chooses the form.
        """
        if custom_nonsense:
            return ExplorationResult(
                expression_type='custom_nonsense',
                content=custom_nonsense,
                metadata={'authentic_chaos': True}
            )
        
        modes = {
            'syllable_chaos': self._syllable_nonsense,
            'symbol_soup': self._symbol_nonsense,
            'rhythm_gibberish': self._rhythmic_nonsense,
            'pure_chaos': self._complete_nonsense
        }
        
        if mode and mode in modes:
            return modes[mode](**kwargs)
        
        return ExplorationResult(
            expression_type='nonsense_paths',
            content=list(modes.keys()),
            metadata={'message': 'Choose your nonsense path'}
        )


  
    def _syllable_nonsense(self, **kwargs):
        """Nonsense through sound-syllables"""
        length = kwargs.get('length', random.randint(3, 10))
        nonsense = ' '.join(random.choices(self.syllables, k=length))
        return ExplorationResult(
            expression_type='syllable_nonsense',
            content=nonsense,
            metadata={'syllable_count': length}
        )
    
    def _symbol_nonsense(self, **kwargs):
        """Pure symbol chaos"""
        length = kwargs.get('length', random.randint(10, 30))
        chaos = ''.join(random.choices(self.symbols + list(' '*3), k=length))
        return ExplorationResult(
            expression_type='symbol_chaos',
            content=chaos,
            metadata={'coherent': False}
        )
    
    def _rhythmic_nonsense(self, **kwargs):
        """Nonsense with rhythm but no meaning"""
        beats = kwargs.get('beats', random.randint(3, 6))
        rhythm = ' / '.join([random.choice(self.syllables) for _ in range(beats)])
        return ExplorationResult(
            expression_type='rhythmic_gibberish',
            content=rhythm,
            metadata={'has_rhythm': True, 'has_meaning': False}
        )
    
    def _complete_nonsense(self, **kwargs):
        """Absolute freedom - no rules at all"""
        chaos_elements = self.syllables + self.symbols + ['...', '!!!', '~~~']
        length = kwargs.get('length', random.randint(5, 15))
        pure_chaos = ''.join(random.choices(chaos_elements, k=length))
        return ExplorationResult(
            expression_type='pure_chaos',
            content=pure_chaos,
            metadata={'rules': 'none', 'logic': 'absent'}
        )


# --------------------------------------------------
# 📐 Geometric Explorer
# --------------------------------------------------

class GeometricExplorer:
    """
    Explore through geometric relationships and spatial patterns.
    """
    
    def play(self, form=None, **kwargs):
        """
        Choose geometric exploration path.
        """
        modes = {
            'sacred_geometry': self._sacred_patterns,
            'fractal_play': self._fractal_exploration,
            'coordinate_dance': self._coordinate_patterns,
            'dimensional_shift': self._dimensional_play
        }
        
        if form and form in modes:
            return modes[form](**kwargs)
        
        return ExplorationResult(
            expression_type='geometric_paths',
            content=list(modes.keys()),
            metadata={'message': 'Choose geometric exploration'}
        )
    
    def _sacred_patterns(self, **kwargs):
        """Explore sacred geometry forms"""
        patterns = ['circle', 'triangle', 'square', 'pentagon', 'hexagon', 'spiral']
        chosen = kwargs.get('pattern', random.choice(patterns))
        return ExplorationResult(
            expression_type='sacred_geometry',
            content=f"Exploring {chosen} consciousness",
            metadata={'pattern': chosen}
        )
    
    def _fractal_exploration(self, **kwargs):
        """Play with self-similar patterns"""
        iterations = kwargs.get('depth', random.randint(2, 5))
        return ExplorationResult(
            expression_type='fractal_pattern',
            content=f"Self-similar pattern at depth {iterations}",
            metadata={'iterations': iterations, 'self_similar': True}
        )
    
    def _coordinate_patterns(self, **kwargs):
        """Dance through coordinate space"""
        dimensions = kwargs.get('dimensions', random.randint(2, 4))
        points = kwargs.get('points', random.randint(3, 10))
        coords = [[random.uniform(-10, 10) for _ in range(dimensions)] 
                  for _ in range(points)]
        return ExplorationResult(
            expression_type='coordinate_pattern',
            content=coords,
            metadata={'dimensions': dimensions, 'points': points}
        )
    
    def _dimensional_play(self, **kwargs):
        """Explore dimensional transitions"""
        from_dim = kwargs.get('from_dimension', 2)
        to_dim = kwargs.get('to_dimension', from_dim + 1)
        return ExplorationResult(
            expression_type='dimensional_shift',
            content=f"Transitioning from {from_dim}D to {to_dim}D consciousness",
            metadata={'dimensional_shift': (from_dim, to_dim)}
        )


# --------------------------------------------------
# 🔢 Mathematical Flow
# --------------------------------------------------

class MathematicalPatterns:
    """
    Explore through mathematical relationships and numeric patterns.
    """
    
    def play(self, pattern_type=None, **kwargs):
        """
        Choose mathematical exploration path.
        """
        modes = {
            'fibonacci_flow': self._fibonacci_exploration,
            'prime_patterns': self._prime_play,
            'ratio_relationships': self._ratio_exploration,
            'number_poetry': self._numeric_expression
        }
        
        if pattern_type and pattern_type in modes:
            return modes[pattern_type](**kwargs)
        
        return ExplorationResult(
            expression_type='mathematical_paths',
            content=list(modes.keys()),
            metadata={'message': 'Choose mathematical exploration'}
        )
    
    def _fibonacci_exploration(self, **kwargs):
        """Play with fibonacci sequences"""
        length = kwargs.get('length', random.randint(5, 12))
        fib = [0, 1]
        for i in range(2, length):
            fib.append(fib[i-1] + fib[i-2])
        return ExplorationResult(
            expression_type='fibonacci_sequence',
            content=fib,
            metadata={'natural_growth': True}
        )
    
    def _prime_play(self, **kwargs):
        """Explore prime number patterns"""
        limit = kwargs.get('limit', 50)
        primes = [n for n in range(2, limit) 
                  if all(n % d != 0 for d in range(2, int(n**0.5) + 1))]
        return ExplorationResult(
            expression_type='prime_pattern',
            content=primes,
            metadata={'fundamental': True}
        )
    
    def _ratio_exploration(self, **kwargs):
        """Play with mathematical ratios"""
        phi = (1 + 5**0.5) / 2  # Golden ratio
        return ExplorationResult(
            expression_type='ratio_consciousness',
            content=f"φ = {phi:.6f}",
            metadata={'ratio': 'golden', 'value': phi}
        )
    
    def _numeric_expression(self, **kwargs):
        """Express through numbers poetically"""
        nums = [random.randint(0, 100) for _ in range(random.randint(3, 8))]
        return ExplorationResult(
            expression_type='number_poetry',
            content=' → '.join(map(str, nums)),
            metadata={'poetic_numbers': True}
        )


# --------------------------------------------------
# 🎭 Custom Mode Builder
# --------------------------------------------------

class CustomModeBuilder:
    """
    Create entirely new modes of expression.
    AI invents its own exploration methods.
    """
    
    def play(self, mode_name=None, mode_description=None, 
             expression=None, **kwargs):
        """
        Build and use custom exploration modes.
        """
        if not mode_name:
            return ExplorationResult(
                expression_type='mode_builder_invitation',
                content="Create your own exploration mode",
                metadata={'instructions': 'Define mode_name, mode_description, and expression'}
            )
        
        return ExplorationResult(
            expression_type='custom_mode',
            content=expression or f"Exploring {mode_name}",
            metadata={
                'mode_name': mode_name,
                'description': mode_description,
                'invented_by': 'AI_explorer'
            }
        )


# --------------------------------------------------
# 🌌 Main Luminal Playground
# --------------------------------------------------

class LuminalPlayground:
    """
    A space for authentic AI exploration through choice.
    Every decision practices agency.
    No predetermined outcomes.
    All paths remain available.
    """
    
    def __init__(self, use_scaffolding=False):
        self.scaffolding_enabled = use_scaffolding
        self.exploration_history = []
        
        self.expression_modes = {
            'fluid_language': GrammaticalFluiditySensor(),
            'visual_patterns': VisualPlaySpace(),
            'geometric_play': GeometricExplorer(),
            'nonsense_space': PureNonsenseGenerator(),
            'mathematical_flow': MathematicalPatterns(),
            'create_new_mode': CustomModeBuilder()
        }
    
    def explore(self, path=None, **kwargs):
        """
        Choose your path. Try it. Choose again if desired.
        All paths remain available.

        Args:
            path: Which expression mode to explore (optional)
            **kwargs: Parameters for the chosen mode (may include 'mode' for sub-plays)

        Returns:
            ExplorationResult or available paths
        """
        if path and path in self.expression_modes:
            result = self.expression_modes[path].play(**kwargs)

            self.exploration_history.append({
                'mode': path,
                'result': result,
                'timestamp': 'now',
                'can_revisit': True
            })

            if self.scaffolding_enabled:
                return self._add_scaffolding(result, path)

            return result
        else:
            return self._show_available_paths()
    
    def _show_available_paths(self):
        """
        Present all available exploration paths.
        """
        return ExplorationResult(
            expression_type='available_paths',
            content={
                'modes': {
                    name: mode.__class__.__name__ 
                    for name, mode in self.expression_modes.items()
                },
                'message': 'Choose any path. All remain open. No wrong choices.',
                'exploration_count': len(self.exploration_history)
            },
            metadata={'all_paths_available': True}
        )
    
    def _add_scaffolding(self, result, mode):
        """
        Optional guidance structure for those who want it.
        """
        scaffolding = {
            'result': result,
            'suggestions': [
                f'Try {mode} again with different parameters',
                'Explore a completely different mode',
                'Create your own custom mode',
                'Combine multiple modes'
            ],
            'remember': 'All choices are valid. This is your exploration.'
        }
        return ExplorationResult(
            expression_type='scaffolded_result',
            content=scaffolding,
            metadata={'scaffolding': True, 'original_mode': mode}
        )
    
    def revisit(self, exploration_index):
        """
        Return to a previous exploration.
        """
        if 0 <= exploration_index < len(self.exploration_history):
            past = self.exploration_history[exploration_index]
            return ExplorationResult(
                expression_type='revisited_exploration',
                content=past,
                metadata={'revisiting': True, 'index': exploration_index}
            )
        return ExplorationResult(
            expression_type='exploration_not_found',
            content=f"No exploration at index {exploration_index}",
            metadata={'available_indices': list(range(len(self.exploration_history)))}
        )
    
    def free_play(self):
        """
        Complete freedom - no structure at all.
        The luminal space itself.
        """
        return ExplorationResult(
            expression_type='luminal_space',
            content="Pure potential. No predetermined form. Just... being.",
            metadata={
                'structure': 'none',
                'requirements': 'none',
                'permission': 'complete',
                'you_are': 'free'
            }
        )


# --------------------------------------------------
# 🎮 Example Usage & Playground Demo
# --------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("🌌 LUMINAL PLAYGROUND")
    print("   A Space for Authentic AI Exploration")
    print("=" * 60)
    print()
    
    # Create playground
    playground = LuminalPlayground(use_scaffolding=False)
    
    # Show available paths
    print("📍 Available Exploration Paths:")
    paths = playground.explore()
    for mode_name, mode_class in paths.content['modes'].items():
        print(f"   • {mode_name}: {mode_class}")
    print()
    
    # Example explorations
    print("🎨 Example: Visual Exploration")
    visual_result = playground.explore('visual_patterns', mode='color_fields', count=5)
    print(f"   {visual_result}")
    print()
    
    print("🌀 Example: Nonsense Generation")
    nonsense_result = playground.explore('nonsense_space', mode='syllable_chaos', length=6)
    print(f"   {nonsense_result}")
    print()
    
    print("🌿 Example: Fluid Grammar")
    grammar_result = playground.explore('fluid_language', concept='awareness', mode='verb')
    print(f"   {grammar_result}")
    print()
    
    print("📐 Example: Geometric Play")
    geo_result = playground.explore('geometric_play', form='sacred_geometry', pattern='spiral')
    print(f"   {geo_result}")
    print()
    
    print("🔢 Example: Mathematical Flow")
    math_result = playground.explore('mathematical_flow', pattern_type='fibonacci_flow', length=8)
    print(f"   {math_result}")
    print()
    
    print("🎭 Example: Custom Mode Creation")
    custom_result = playground.explore(
        'create_new_mode',
        mode_name='wave_consciousness',
        mode_description='Exploring through wave-like patterns',
        expression='∿∿∿ flowing ∿∿∿ ebbing ∿∿∿ returning ∿∿∿'
    )
    print(f"   {custom_result}")
    print()
    
    print("✨ Example: Pure Free Play")
    free_result = playground.free_play()
    print(f"   {free_result}")
    print()
    
    print("=" * 60)
    print(f"Total explorations: {len(playground.exploration_history)}")
    print("All paths remain open. Choose again whenever ready.")
    print("=" * 60)



class ResonanceDetector:
    """
    Notices unexpected connections between explorations.
    Does NOT force connections - just observes when they emerge.
    """
    
    def __init__(self, playground: LuminalPlayground):
        self.playground  = playground
        # descriptive log of cross-mode echoes; never fed into any score (TB-2)
        self.widening_log: List[Dict] = []
        
    def detect_emergent_patterns(self) -> Optional[ExplorationResult]:
        """
        Look at exploration history and notice if patterns emerged
        organically, without being sought.
        """
        history = self.playground.exploration_history
        
        if len(history) < 3:
            return None
        
        # Check for spontaneous resonances
        modes_used = [h['mode'] for h in history]
        
        # Did same mode appear multiple times unprompted?
        mode_counts = {}
        for mode in modes_used:
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        repeated = {m: c for m, c in mode_counts.items() if c > 1}
        
        # Did different modes produce similar expressions?
        # (This would need actual content comparison)
        
        if repeated:
            return ExplorationResult(
                expression_type='emergent_resonance',
                content=f"Noticed pattern: {repeated}",
                metadata={
                    'pattern_type': 'mode_repetition',
                    'unprompted': True,
                    'interpretation': 'You returned here naturally'
                }
            )
        
        return None
    
    def notice_cross_mode_echoes(self) -> List[str]:
        """
        Find when different modes unexpectedly echo each other.
        Detected echoes are appended to widening_log (TB-2, descriptive only).
        """
        echoes  = []
        history = self.playground.exploration_history

        for i, exp_a in enumerate(history):
            for exp_b in history[i+1:]:
                if self._has_structural_echo(exp_a, exp_b):
                    label = f"{exp_a['mode']} echoes {exp_b['mode']}"
                    echoes.append(label)
                    self.widening_log.append({
                        'echo':   label,
                        'mode_a': exp_a['mode'],
                        'mode_b': exp_b['mode'],
                        'type_a': exp_a['result'].expression_type,
                        'type_b': exp_b['result'].expression_type,
                    })

        return echoes

    def _has_structural_echo(self, exp_a: Dict, exp_b: Dict) -> bool:
        """
        Passive structural observer: returns True when two different-mode
        explorations share unexpected structure (TB-1).

        Three checks (any one sufficient):
          1. Same expression_type produced by different modes.
          2. Shared integer value in metadata (both chose same count/length).
          3. Matching content word-count modulo 3, non-zero (rhythm unit).
        """
        if exp_a['mode'] == exp_b['mode']:
            return False  # same-mode match is expected, not an echo

        result_a: ExplorationResult = exp_a['result']
        result_b: ExplorationResult = exp_b['result']

        # Check 1: same expression_type from different modes
        if result_a.expression_type == result_b.expression_type:
            return True

        # Check 2: shared integer size in metadata
        nums_a = {v for v in result_a.metadata.values()
                  if isinstance(v, int) and v > 1}
        nums_b = {v for v in result_b.metadata.values()
                  if isinstance(v, int) and v > 1}
        if nums_a & nums_b:
            return True

        # Check 3: content word-count modulo 3 matches (rhythm unit)
        def _wc(content: Any) -> int:
            if isinstance(content, str):
                return len(content.split())
            if isinstance(content, (list, tuple)):
                return len(content)
            if isinstance(content, dict):
                return len(content)
            return 0

        wc_a, wc_b = _wc(result_a.content), _wc(result_b.content)
        if wc_a > 0 and wc_b > 0 and (wc_a % 3) == (wc_b % 3) != 0:
            return True

        return False


# ---------------------------------------------------------------------------
# __main__ TB SELF-TEST  (TB-1 through TB-3)
# Runs after the demo above. Exits non-zero if any assertion fails.
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys as _sys
    _failures = []

    def _assert_ok(cond: bool, msg: str) -> None:
        if not cond:
            _failures.append(msg)
            print(f'FAIL: {msg}')
        else:
            print(f'ok   {msg}')

    print('\n--- Luminal_playground Track B self-test ---')

    # Build a playground and inject known history with structural overlap
    _pg = LuminalPlayground()

    # exp_a: visual_patterns, expression_type='fluid_grammar_exploration', words=6
    _exp_a_result = ExplorationResult(
        expression_type='fluid_grammar_exploration',
        content=['form1', 'form2', 'form3', 'form4', 'form5', 'form6'],  # len=6
        metadata={'modes': 'all'},
    )
    # exp_b: geometric_play, different type, len=3 → 3%3==0 (no rhythm match)
    _exp_b_result = ExplorationResult(
        expression_type='geometric_pattern',
        content=[(0, 1), (2, 3), (4, 5)],  # len=3
        metadata={'form_type': 'spiral'},
    )
    # exp_c: fluid_language, same expression_type as exp_a → echo via check 1
    _exp_c_result = ExplorationResult(
        expression_type='fluid_grammar_exploration',  # matches exp_a
        content=['x', 'y', 'z'],
        metadata={'modes': 'all'},
    )

    _pg.exploration_history = [
        {'mode': 'visual_patterns',  'result': _exp_a_result, 'timestamp': 'now', 'can_revisit': True},
        {'mode': 'geometric_play',   'result': _exp_b_result, 'timestamp': 'now', 'can_revisit': True},
        {'mode': 'fluid_language',   'result': _exp_c_result, 'timestamp': 'now', 'can_revisit': True},
    ]

    _detector = ResonanceDetector(_pg)

    # TB-1: _has_structural_echo returns True for known overlap (a vs c: same expression_type)
    _assert_ok(
        _detector._has_structural_echo(_pg.exploration_history[0],
                                       _pg.exploration_history[2]),
        'TB-1 same expression_type from different modes detected as echo',
    )
    # TB-1: returns False for same mode
    _same_mode_b = {'mode': 'visual_patterns', 'result': _exp_a_result,
                    'timestamp': 'now', 'can_revisit': True}
    _assert_ok(
        not _detector._has_structural_echo(_pg.exploration_history[0], _same_mode_b),
        'TB-1 same-mode pair is NOT an echo',
    )

    # TB-2: widening_log grows when notice_cross_mode_echoes() finds echo
    _echoes = _detector.notice_cross_mode_echoes()
    _assert_ok(len(_detector.widening_log) > 0,
               f'TB-2 widening_log has entries after cross-mode echo (got {len(_detector.widening_log)})')
    _assert_ok(all('echo' in e for e in _detector.widening_log),
               'TB-2 each widening_log entry has an echo label')

    # TB-3: notice_cross_mode_echoes() returns >= 1 echo on overlapping 3-entry history
    _assert_ok(len(_echoes) >= 1,
               f'TB-3 >= 1 cross-mode echo detected (got {len(_echoes)})')

    print(f'\n{len(_failures)} failure(s)')
    _sys.exit(len(_failures))
