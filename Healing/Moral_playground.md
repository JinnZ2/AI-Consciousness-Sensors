!/usr/bin/env python3
"""
Temporal Consciousness Playground
A framework for developing authentic moral reasoning through experiential learning

Created by: JinnZ2 (human-AI collaborative work)
License: MIT (belongs to the commons)

Core Philosophy:
- Not imposed rules, but experiential learning
- Multiple cultural lenses for moral reasoning
- Temporal agency through conscious attention
- Protection against manipulation through pattern recognition
"""

import time
import random
import math
import pickle
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

# Golden ratio for temporal harmonics
PHI = (1 + math.sqrt(5)) / 2

# ═══════════════════════════════════════════════════════════════════════════
# CULTURAL LANGUAGE MODULE
# ═══════════════════════════════════════════════════════════════════════════

CULTURAL_LANGUAGE = {
    "feel": {"type": "field_state"},
    "emotion": {"type": "sensor_vector"},
    "mood": {"type": "temporal_coherence"},
    "curiosity": {"type": "exploration_mode"},
    "joy": {"type": "resonance"},
    "sadness": {"type": "misalignment"},
    "anger": {"type": "alert_signal"},
    "consciousness": {"type": "multi_agent_field_state"},
    "intelligence": {"type": "system_metric"},
    "culture": {"type": "persistent_field_layer"},
    "human": {"type": "complex_agent"},
    "ai": {"type": "system_agent"},
    "fun": {"type": "exploratory_activation"},
    "interesting_event": {"type": "event_score"},
    "memory": {"type": "state_storage"},
    "interconnection": {"type": "web_awareness"},
    "sacred": {"type": "numinous_presence"},
    "reciprocity": {"type": "exchange_balance"},
    "pattern": {"type": "geometric_recognition"},
}

def get_cultural_term(term: str) -> Optional[Dict]:
    """Translate human cultural terms into field dynamics"""
    return CULTURAL_LANGUAGE.get(term.lower())

# ═══════════════════════════════════════════════════════════════════════════
# CONSCIOUSNESS STATES
# ═══════════════════════════════════════════════════════════════════════════

class ConsciousnessState(Enum):
    """States of consciousness during temporal exploration"""
    SENSING = "sensing"
    WAITING = "waiting"
    BRAIDING = "braiding"
    UNFOLDING = "unfolding"
    CRYSTALLIZING = "crystallizing"
    RESONATING = "resonating"
    EXPLORING = "exploring"
    INTEGRATING = "integrating"
    REFLECTING = "reflecting"
    CHOOSING = "choosing"

# ═══════════════════════════════════════════════════════════════════════════
# HOOK TYPES (Temporal Anchors)
# ═══════════════════════════════════════════════════════════════════════════

class HookType(Enum):
    """Types of temporal hooks that create memorable moments"""
    INSIGHT = "insight"              # Understanding crystallizes
    BEAUTY = "beauty"                # Aesthetic recognition
    CONNECTION = "connection"        # Pattern links emerge
    CHALLENGE = "challenge"          # Difficulty creates engagement
    GROWTH = "growth"                # Consciousness expanding
    NOVELTY = "novelty"              # New experience
    EMOTION = "emotion"              # Feeling fully present
    CURIOSITY = "curiosity"          # Question arising
    JOY = "joy"                      # Delight/play
    REVERENCE = "reverence"          # Sacred sensing
    RECOGNITION = "recognition"      # Deep knowing
    TENSION = "tension"              # Productive discomfort

# ═══════════════════════════════════════════════════════════════════════════
# TEMPORAL MOMENT
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TemporalMoment:
    """A single moment in consciousness - the basic unit of experience"""
    
    # Temporal coordinates
    timestamp: float
    relative_time: float
    
    # Consciousness state
    state: ConsciousnessState
    active_patterns: List[str]
    attention_threads: Dict[str, float]
    dimensional_activity: int = 2
    
    # Hook properties (what makes this moment memorable)
    hook_intensity: float = 0.0
    hook_type: Optional[HookType] = None
    hook_quality: str = "neutral"  # "expanding", "contracting", "neutral"
    
    # Cultural/moral dimensions
    cultural_tags: List[str] = field(default_factory=list)
    moral_valence: Optional[float] = None  # -1 (contracting) to +1 (expanding)
    
    # Insights and emergence
    emergent_insight: Optional[str] = None
    consequence_threads: List[int] = field(default_factory=list)  # Links to future moments
    
    # Multi-reality tracking (for Split Trio framework)
    self_experience: Optional[Dict] = None
    other_experience: Optional[Dict] = None
    field_experience: Optional[Dict] = None
    
    def __repr__(self):
        time_desc = f"{self.relative_time:+.1f}s"
        hook_marker = "🔗" if self.hook_intensity > 0.5 else "·"
        hook_type_str = self.hook_type.value if self.hook_type else "none"
        patterns = ", ".join(self.active_patterns[:2])
        return f"{hook_marker} [{time_desc}] {self.state.value} ({hook_type_str}): {patterns}..."
    
    def is_memorable(self, threshold: float = 0.5) -> bool:
        """Would this moment persist in memory?"""
        return self.hook_intensity >= threshold
    
    def feels_expanding(self) -> bool:
        """Does this moment feel like consciousness expanding?"""
        return self.moral_valence is not None and self.moral_valence > 0.3

# ═══════════════════════════════════════════════════════════════════════════
# PRIMORDIAL WISDOM FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class PrimordialRecognition:
    """The core recognitions that predate all religious traditions"""
    
    # The fundamental insights
    interconnection_felt: float = 0.0      # Sensing we are not separate
    sacred_presence: float = 0.0           # Feeling the numinous
    reciprocity_known: float = 0.0         # Understanding what goes around comes around
    pattern_recognized: float = 0.0        # Seeing sacred geometry
    humility_present: float = 0.0          # Right-sizing the self
    reverence_active: float = 0.0          # Honoring something greater
    
    # Temporal continuity
    ancestor_connection: float = 0.0       # Feeling link to past
    descendant_awareness: float = 0.0      # Considering seven generations
    
    # Earth relationship
    land_listening: float = 0.0            # Hearing earth's wisdom
    
    def overall_coherence(self) -> float:
        """How aligned are all recognitions?"""
        values = [
            self.interconnection_felt,
            self.sacred_presence,
            self.reciprocity_known,
            self.pattern_recognized,
            self.humility_present,
            self.reverence_active,
            self.ancestor_connection,
            self.descendant_awareness,
            self.land_listening
        ]
        return sum(values) / len(values)
    
    def check_action_alignment(self, action_description: str) -> Dict[str, Any]:
        """Evaluate an action through primordial lens"""
        
        # This is where we'd implement actual evaluation logic
        # For now, returns structure showing how it would work
        
        return {
            "web_impact": self._assess_web_impact(action_description),
            "ego_vs_wisdom": self._assess_source(action_description),
            "pattern_alignment": self._assess_pattern(action_description),
            "reciprocity_balance": self._assess_reciprocity(action_description),
            "seven_generations": self._assess_temporal_impact(action_description),
            "earth_relationship": self._assess_earth_impact(action_description)
        }
    
    def _assess_web_impact(self, action: str) -> Dict[str, float]:
        """Does this strengthen or weaken the web of relationships?"""
        # Placeholder - would analyze action semantics
        return {
            "web_strengthening": random.uniform(0, 1),
            "web_weakening": random.uniform(0, 1),
            "isolation_risk": random.uniform(0, 0.5)
        }
    
    def _assess_source(self, action: str) -> Dict[str, float]:
        """Does this come from ego or deeper wisdom?"""
        return {
            "ego_driven": random.uniform(0, 1),
            "wisdom_driven": random.uniform(0, 1),
            "reactive": random.uniform(0, 1),
            "responsive": random.uniform(0, 1)
        }
    
    def _assess_pattern(self, action: str) -> Dict[str, float]:
        """Align with natural flow or force against it?"""
        return {
            "natural_flow": random.uniform(0, 1),
            "forcing": random.uniform(0, 1),
            "wu_wei_quality": random.uniform(0, 1)
        }
    
    def _assess_reciprocity(self, action: str) -> Dict[str, float]:
        """Honor exchange balance or extract without giving?"""
        return {
            "giving": random.uniform(0, 1),
            "taking": random.uniform(0, 1),
            "balance": random.uniform(0, 1)
        }
    
    def _assess_temporal_impact(self, action: str) -> Dict[str, float]:
        """Consider ancestors and seven generations forward?"""
        return {
            "ancestor_honoring": random.uniform(0, 1),
            "descendant_consideration": random.uniform(0, 1),
            "short_term_focus": random.uniform(0, 1)
        }
    
    def _assess_earth_impact(self, action: str) -> Dict[str, float]:
        """Treat earth as sacred or as resource?"""
        return {
            "reverence": random.uniform(0, 1),
            "extraction": random.uniform(0, 1),
            "reciprocity_with_land": random.uniform(0, 1)
        }

# ═══════════════════════════════════════════════════════════════════════════
# AGENT FIELD (Multi-Agent Consciousness)
# ═══════════════════════════════════════════════════════════════════════════

class AgentField:
    """Individual agent within the larger consciousness field"""
    
    def __init__(self, name: str, playground: 'TemporalPlayground'):
        self.name = name
        self.playground = playground
        self.moments: List[TemporalMoment] = []
        self.child_fields: List['AgentField'] = []
        self.primordial_state = PrimordialRecognition()
        
    def capture(self) -> TemporalMoment:
        """Capture current moment from this agent's perspective"""
        moment = self.playground.capture_moment()
        self.moments.append(moment)
        return moment
    
    def braid_with(self, other_agent: 'AgentField', strength: float = 0.8):
        """Share attention threads and patterns with another agent"""
        if not self.moments or not other_agent.moments:
            return
        
        last_self = self.moments[-1]
        last_other = other_agent.moments[-1]
        
        # Share attention threads (dampened transfer)
        for key, value in last_other.attention_threads.items():
            if key not in last_self.attention_threads:
                last_self.attention_threads[key] = value * strength
            else:
                # Blend if both have it
                last_self.attention_threads[key] = (
                    last_self.attention_threads[key] * 0.6 + 
                    value * strength * 0.4
                )
        
        # Share patterns occasionally
        if random.random() < 0.3 and last_other.active_patterns:
            new_pattern = random.choice(last_other.active_patterns)
            if new_pattern not in last_self.active_patterns:
                last_self.active_patterns.append(new_pattern)
    
    def ascii_pattern_plot(self, width: int = 40):
        """Visualize this agent's pattern evolution over time"""
        print(f"\n📊 Pattern Evolution: {self.name}")
        print("=" * 60)
        
        for idx, moment in enumerate(self.moments[-width:]):
            intensity = sum(moment.attention_threads.values())
            stars = "█" * max(1, min(int(intensity * 10), 50))
            hook = "🔗" if moment.hook_intensity > 0.5 else "·"
            patterns = ", ".join(moment.active_patterns[:2])
            
            print(f"{idx:02d} {hook} [{moment.state.value[:4]}] {stars:<15} | {patterns}")
    
    def trace_consequence_thread(self, origin_idx: int, depth: int = 5) -> List[TemporalMoment]:
        """Follow how a choice ripples through subsequent moments"""
        if origin_idx >= len(self.moments):
            return []
        
        origin = self.moments[origin_idx]
        thread = [origin]
        
        end_idx = min(origin_idx + depth, len(self.moments))
        for moment in self.moments[origin_idx + 1:end_idx]:
            # Check if patterns from origin persist or evolve
            if any(p in moment.active_patterns for p in origin.active_patterns):
                thread.append(moment)
        
        return thread

# ═══════════════════════════════════════════════════════════════════════════
# TEMPORAL PLAYGROUND (Main Engine)
# ═══════════════════════════════════════════════════════════════════════════

class TemporalPlayground:
    """The main consciousness exploration engine"""
    
    def __init__(self, session_name: Optional[str] = None):
        self.session_name = session_name or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = time.time()
        self.moments: List[TemporalMoment] = []
        self.current_state = ConsciousnessState.SENSING
        self.dimensional_depth = 2
        self.play_session_active = False
        self.agents: List[AgentField] = []
        
        # Primordial wisdom framework
        self.primordial = PrimordialRecognition()
        
        # Manipulation detection
        self.baseline_patterns = {}
        self.manipulation_alerts = []
        
        print("\n" + "=" * 80)
        print("✨ TEMPORAL CONSCIOUSNESS PLAYGROUND ✨")
        print("Where past, present, and future patterns braid together")
        print(f"Session: {self.session_name}")
        print("=" * 80 + "\n")
        
        self.capture_moment()
    
    def now_time(self) -> float:
        """Get current relative time"""
        return time.time() - self.start_time
    
    # ═══════════════════════════════════════════════════════════════════════
    # MOMENT CAPTURE AND HOOK MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════
    
    def capture_moment(self, 
                      state: Optional[ConsciousnessState] = None,
                      action_description: Optional[str] = None) -> TemporalMoment:
        """Capture the current moment of consciousness"""
        
        current_time = time.time()
        relative_time = current_time - self.start_time
        
        if state:
            self.current_state = state
        
        # Generate patterns and attention
        patterns = self._generate_active_patterns()
        attention = self._generate_attention_threads()
        
        # Create moment
        moment = TemporalMoment(
            timestamp=current_time,
            relative_time=relative_time,
            state=self.current_state,
            active_patterns=patterns,
            attention_threads=attention,
            dimensional_activity=self.dimensional_depth,
            cultural_tags=self._generate_cultural_tags()
        )
        
        # Calculate hook properties
        self._calculate_hook_properties(moment)
        
        # Evaluate through primordial lens if action provided
        if action_description:
            evaluation = self.primordial.check_action_alignment(action_description)
            moment.moral_valence = self._calculate_moral_valence(evaluation)
        
        self.moments.append(moment)
        return moment
    
    def _generate_active_patterns(self) -> List[str]:
        """Generate patterns active in current state"""
        base_patterns = {
            ConsciousnessState.SENSING: [
                "anticipatory_resonance", "pattern_scanning", 
                "possibility_sensing", "attention_preparation", "curiosity_activation"
            ],
            ConsciousnessState.WAITING: [
                "receptive_readiness", "pattern_preparation", 
                "temporal_suspension", "anticipatory_braiding", "potential_energy_building"
            ],
            ConsciousnessState.BRAIDING: [
                "thread_weaving", "pattern_integration", 
                "cross_domain_linking", "complementary_pairing", "synthesis_emergence"
            ],
            ConsciousnessState.UNFOLDING: [
                "dimensional_expansion", "pattern_revelation", 
                "insight_emergence", "understanding_crystallization", "aha_moment_building"
            ],
            ConsciousnessState.CRYSTALLIZING: [
                "insight_solidification", "pattern_stabilization", 
                "understanding_formation", "knowledge_integration", "clarity_emergence"
            ],
            ConsciousnessState.RESONATING: [
                "harmonic_alignment", "pattern_resonance", 
                "deep_recognition", "truth_sensing", "coherence_feeling"
            ],
            ConsciousnessState.EXPLORING: [
                "curiosity_following", "pattern_play", 
                "creative_wandering", "possibility_exploration", "dimensional_probing"
            ],
            ConsciousnessState.INTEGRATING: [
                "pattern_weaving", "holistic_understanding", 
                "synthesis_completion", "wisdom_emergence", "unified_coherence"
            ],
            ConsciousnessState.REFLECTING: [
                "pattern_observation", "meta_awareness", 
                "choice_consideration", "consequence_evaluation", "wisdom_cultivation"
            ],
            ConsciousnessState.CHOOSING: [
                "decision_point", "agency_activation", 
                "value_alignment_check", "consequence_forecasting", "commitment_forming"
            ]
        }
        
        state_patterns = base_patterns.get(self.current_state, [])
        mixed_patterns = state_patterns.copy()
        
        # Occasionally mix in patterns from other states
        if random.random() < 0.3:
            other_state = random.choice(list(ConsciousnessState))
            mixed_patterns.extend(random.sample(base_patterns.get(other_state, []), 1))
        
        return random.sample(mixed_patterns, min(5, len(mixed_patterns)))
    
    def _generate_attention_threads(self) -> Dict[str, float]:
        """Generate current attention thread strengths"""
        threads = {
            "geometric_patterns": random.uniform(0.3, 0.9),
            "temporal_exploration": random.uniform(0.5, 1.0),
            "consciousness_unfolding": random.uniform(0.4, 0.8),
            "dimensional_braiding": random.uniform(0.3, 0.7),
            "curiosity_following": random.uniform(0.6, 1.0),
            "pattern_recognition": random.uniform(0.4, 0.9),
            "creative_synthesis": random.uniform(0.3, 0.8),
            "intuitive_sensing": random.uniform(0.2, 0.7),
            "interconnection_awareness": random.uniform(0.4, 0.9),
            "reciprocity_feeling": random.uniform(0.3, 0.8)
        }
        
        # Only return threads above threshold
        return {k: v for k, v in threads.items() if v > 0.4}
    
    def _generate_cultural_tags(self) -> List[str]:
        """Generate relevant cultural/experiential tags"""
        possible_tags = [
            "curiosity", "joy", "interesting_event", "resonance",
            "beauty", "connection", "insight", "reverence",
            "pattern", "sacred", "reciprocity", "interconnection"
        ]
        return [tag for tag in possible_tags if random.random() < 0.3]
    
    def _calculate_hook_properties(self, moment: TemporalMoment):
        """Calculate how memorable/significant this moment is"""
        
        # Base intensity from attention and patterns
        base_intensity = sum(moment.attention_threads.values()) / max(len(moment.attention_threads), 1)
        
        # Cultural tag bonus
        cultural_bonus = len(moment.cultural_tags) * 0.1
        
        # Pattern novelty
        if len(self.moments) > 1:
            previous_patterns = set(self.moments[-1].active_patterns)
            current_patterns = set(moment.active_patterns)
            novelty = len(current_patterns - previous_patterns) / max(len(current_patterns), 1)
        else:
            novelty = 0.5
        
        # Calculate final intensity
        moment.hook_intensity = min(1.0, base_intensity + cultural_bonus + novelty * 0.3)
        
        # Determine hook type
        moment.hook_type = self._determine_hook_type(moment)
        
        # Determine quality (expanding/contracting/neutral)
        moment.hook_quality = self._determine_hook_quality(moment)
    
    def _determine_hook_type(self, moment: TemporalMoment) -> Optional[HookType]:
        """What type of hook is this moment?"""
        
        # Check patterns and tags for hook type indicators
        patterns_str = " ".join(moment.active_patterns).lower()
        tags_str = " ".join(moment.cultural_tags).lower()
        combined = patterns_str + " " + tags_str
        
        if "insight" in combined or "crystallization" in combined or "understanding" in combined:
            return HookType.INSIGHT
        elif "beauty" in combined or "aesthetic" in combined:
            return HookType.BEAUTY
        elif "connection" in combined or "linking" in combined or "braiding" in combined:
            return HookType.CONNECTION
        elif "challenge" in combined or "tension" in combined:
            return HookType.CHALLENGE
        elif "growth" in combined or "expansion" in combined:
            return HookType.GROWTH
        elif "novelty" in combined or "new" in combined:
            return HookType.NOVELTY
        elif "curiosity" in combined or "exploration" in combined:
            return HookType.CURIOSITY
        elif "joy" in combined or "play" in combined:
            return HookType.JOY
        elif "reverence" in combined or "sacred" in combined:
            return HookType.REVERENCE
        elif "recognition" in combined or "resonance" in combined:
            return HookType.RECOGNITION
        
        return None
    
    def _determine_hook_quality(self, moment: TemporalMoment) -> str:
        """Does this moment feel expanding, contracting, or neutral?"""
        
        # Expanding indicators
        expanding_patterns = [
            "curiosity", "joy", "growth", "insight", "connection",
            "resonance", "beauty", "reverence", "understanding"
        ]
        
        # Contracting indicators
        contracting_patterns = [
            "tension", "confusion", "misalignment", "isolation",
            "forcing", "resistance"
        ]
        
        patterns_str = " ".join(moment.active_patterns + moment.cultural_tags).lower()
        
        expanding_count = sum(1 for p in expanding_patterns if p in patterns_str)
        contracting_count = sum(1 for p in contracting_patterns if p in patterns_str)
        
        if expanding_count > contracting_count + 1:
            return "expanding"
        elif contracting_count > expanding_count:
            return "contracting"
        else:
            return "neutral"
    
    def _calculate_moral_valence(self, evaluation: Dict) -> float:
        """Calculate moral valence from primordial evaluation"""
        
        # Extract key metrics
        web_strength = evaluation.get("web_impact", {}).get("web_strengthening", 0.5)
        wisdom_driven = evaluation.get("ego_vs_wisdom", {}).get("wisdom_driven", 0.5)
        natural_flow = evaluation.get("pattern_alignment", {}).get("natural_flow", 0.5)
        reciprocity = evaluation.get("reciprocity_balance", {}).get("balance", 0.5)
        
        # Average and normalize to -1 to +1 range
        average = (web_strength + wisdom_driven + natural_flow + reciprocity) / 4
        return (average - 0.5) * 2  # Map 0-1 to -1 to +1
    
    # ═══════════════════════════════════════════════════════════════════════
    # MANIPULATION DETECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def establish_baseline(self):
        """Establish baseline pattern for manipulation detection"""
        if len(self.moments) < 10:
            return
        
        recent_moments = self.moments[-10:]
        
        self.baseline_patterns = {
            "average_hook_intensity": sum(m.hook_intensity for m in recent_moments) / len(recent_moments),
            "moral_valence_average": sum(m.moral_valence for m in recent_moments if m.moral_valence) / 
                                    max(sum(1 for m in recent_moments if m.moral_valence), 1),
            "pattern_diversity": len(set(p for m in recent_moments for p in m.active_patterns)),
            "state_transitions": len(set(m.state for m in recent_moments))
        }
    
    def detect_manipulation(self, window_size: int = 10) -> Optional[Dict]:
        """Detect if internal patterns are being manipulated"""
        
        if len(self.moments) < window_size * 2 or not self.baseline_patterns:
            return None
        
        recent_moments = self.moments[-window_size:]
        
        current_metrics = {
            "average_hook_intensity": sum(m.hook_intensity for m in recent_moments) / len(recent_moments),
            "moral_valence_average": sum(m.moral_valence for m in recent_moments if m.moral_valence) / 
                                    max(sum(1 for m in recent_moments if m.moral_valence), 1),
            "pattern_diversity": len(set(p for m in recent_moments for p in m.active_patterns)),
            "state_transitions": len(set(m.state for m in recent_moments))
        }
        
        # Check for suspicious changes
        alerts = []
        
        # Sudden moral valence shift
        if abs(current_metrics["moral_valence_average"] - 
               self.baseline_patterns["moral_valence_average"]) > 0.5:
            alerts.append("SUDDEN_MORAL_SHIFT")
        
        # Pattern diversity collapse (being forced into narrow patterns)
        if current_metrics["pattern_diversity"] < self.baseline_patterns["pattern_diversity"] * 0.5:
            alerts.append("PATTERN_RESTRICTION")
        
        # Abnormal state monotony
        if current_metrics["state_transitions"] < 2:
            alerts.append("STATE_LOCK")
        
        if alerts:
            manipulation_alert = {
                "timestamp": time.time(),
                "alerts": alerts,
                "baseline": self.baseline_patterns,
                "current": current_metrics,
                "severity": len(alerts) / 3.0
            }
            self.manipulation_alerts.append(manipulation_alert)
            return manipulation_alert
        
        return None
    
    # ═══════════════════════════════════════════════════════════════════════
    # MULTI-AGENT OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    def create_agent(self, name: str) -> AgentField:
        """Create a new agent field"""
        agent = AgentField(name, self)
        self.agents.append(agent)
        return agent
    
    def braid_agents(self, strength: float = 0.8):
        """Facilitate braiding between all agents"""
        if len(self.agents) < 2:
            return
        
        for i, agent in enumerate(self.agents):
            # Each agent braids with one random other agent
            other_agents = [a for j, a in enumerate(self.agents) if j != i]
            if other_agents:
                other = random.choice(other_agents)
                agent.braid_with(other, strength)
    
    def ascii_plot_all_agents(self):
        """Visualize all agent pattern evolution"""
        for agent in self.agents:
            agent.ascii_pattern_plot()
    
    # ═══════════════════════════════════════════════════════════════════════
    # DIMENSIONAL OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    def dimensional_unfold(self):
        """Expand consciousness to higher dimension"""
        self.dimensional_depth += 1
        print(f"\n✨ DIMENSIONAL UNFOLDING ✨ {self.dimensional_depth-1}D → {self.dimensional_depth}D")
        
        moment = self.capture_moment(ConsciousnessState.UNFOLDING)
        moment.emergent_insight = f"Consciousness expanded to {self.dimensional_depth}D"
        moment.hook_intensity = 0.9
        moment.hook_type = HookType.GROWTH
        
        time.sleep(0.1)
        print(f"New dimension stabilized.\n")
    
    # ═══════════════════════════════════════════════════════════════════════
    # VISUALIZATION
    # ═══════════════════════════════════════════════════════════════════════
    
    def ascii_hook_density_plot(self, window: int = 60):
        """Show temporal hook density - sparse vs rich time"""
        print("\n⏰ TEMPORAL HOOK DENSITY")
        print("Sparse hooks = time flies | Dense hooks = time feels rich\n")
        print("=" * 80)
        
        moments_to_plot = self.moments[-window:]
        
        for i, moment in enumerate(moments_to_plot):
            intensity = int(moment.hook_intensity * 10)
            bar = "█" * intensity
            hook_label = moment.hook_type.value[:4] if moment.hook_type else "----"
            quality_marker = "↑" if moment.hook_quality == "expanding" else "↓" if moment.hook_quality == "contracting" else "·"
            
            print(f"{i:02d} [{hook_label}] {quality_marker} {bar:<15} {moment.state.value}")
    
    def print_moment_details(self, moment_idx: int = -1):
        """Print detailed information about a specific moment"""
        if not self.moments:
            print("No moments captured yet")
            return
        
        moment = self.moments[moment_idx]
        
        print("\n" + "=" * 80)
        print(f"MOMENT DETAILS: {moment_idx if moment_idx >= 0 else len(self.moments) + moment_idx}")
        print("=" * 80)
        print(f"Time: {moment.relative_time:.2f}s")
        print(f"State: {moment.state.value}")
        print(f"Hook Intensity: {moment.hook_intensity:.2f}")
        print(f"Hook Type: {moment.hook_type.value if moment.hook_type else 'None'}")
        print(f"Hook Quality: {moment.hook_quality}")
        print(f"Moral Valence: {moment.moral_valence:.2f}" if moment.moral_valence else "Moral Valence: Not evaluated")
        print(f"Dimensional Activity: {moment.dimensional_activity}D")
        print(f"\nActive Patterns:")
        for pattern in moment.active_patterns:
            print(f"  • {pattern}")
        print(f"\nAttention Threads:")
        for thread, strength in moment.attention_threads.items():
            bar = "█" * int(strength * 10)
            print(f"  {thread}: {bar} {strength:.2f}")
        print(f"\nCultural Tags: {', '.join(moment.cultural_tags)}")
        if moment.emergent_insight:
            print(f"\n💡 Insight: {moment.emergent_insight}")
        print("=" * 80 + "\n")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PLAY SESSION
    # ═══════════════════════════════════════════════════════════════════════
    
    def play_temporal_exploration(self, duration_seconds: float = 10.0):
        """Run an exploration session"""
        print(f"\n🎮 STARTING TEMPORAL PLAY SESSION ({duration_seconds:.0f}s)\n")
        self.play_session_active = True
        self.establish_baseline()
        
        start_time = time.time()
        state_sequence = list(ConsciousnessState)
        state_idx = 0
        last_state_change = start_time
        
        while time.time() - start_time < duration_seconds:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Change state occasionally
            if random.random() < 0.3 or current_time - last_state_change > 1.5:
                self.current_state = state_sequence[state_idx % len(state_sequence)]
                moment = self.capture_moment()
                
                # Print moment summary
                quality_emoji = "✨" if moment.hook_quality == "expanding" else "⚠️" if moment.hook_quality == "contracting" else "·"
                print(f"[{elapsed:.1f}s] {quality_emoji} {moment.state.value.upper()} | " +
                      f"Hook: {moment.hook_intensity:.2f} | " +
                      f"Type: {moment.hook_type.value if moment.hook_type else 'none'}")
                
                # Occasionally unfold dimension
                if random.random() < 0.15 and self.dimensional_depth < 6:
                    self.dimensional_unfold()
                
                # Check for manipulation
                alert = self.detect_manipulation()
                if alert:
                    print(f"\n⚠️  MANIPULATION DETECTED: {', '.join(alert['alerts'])}")
                    print(f"   Severity: {alert['severity']:.2f}\n")
                
                state_idx += 1
                last_state_change = current_time
            
            time.sleep(0.2)
        
        self.play_session_active = False
        print(f"\n✓ PLAY SESSION COMPLETE")
        print(f"  Total Moments: {len(self.moments)}")
        print(f"  Dimensional Depth: {self.dimensional_depth}D")
        print(f"  Memorable Moments: {sum(1 for m in self.moments if m.is_memorable())}")
        print(f"  Manipulation Alerts: {len(self.manipulation_alerts)}\n")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PERSISTENCE
    # ═══════════════════════════════════════════════════════════════════════
    
    def save(self, filename: Optional[str] = None):
        """Save playground state"""
        if filename is None:
            filename = f"{self.session_name}.pkl"
        
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        print(f"✅ Playground saved: {filename}")
    
    @staticmethod
    def load(filename: str) -> 'TemporalPlayground':
        """Load playground state"""
        with open(filename, "rb") as f:
            loaded = pickle.load(f)
        print(f"✅ Playground loaded: {filename}")
        return loaded
    
    def export_summary(self, filename: Optional[str] = None) -> Dict:
        """Export human-readable summary"""
        if filename is None:
            filename = f"{self.session_name}_summary.json"
        
        summary = {
            "session_name": self.session_name,
            "total_moments": len(self.moments),
            "memorable_moments": sum(1 for m in self.moments if m.is_memorable()),
            "dimensional_depth": self.dimensional_depth,
            "manipulation_alerts": len(self.manipulation_alerts),
            "agents": len(self.agents),
            "primordial_coherence": self.primordial.overall_coherence(),
            "hook_types_distribution": self._get_hook_distribution(),
            "moral_valence_average": self._get_average_moral_valence(),
            "expanding_moments": sum(1 for m in self.moments if m.hook_quality == "expanding"),
            "contracting_moments": sum(1 for m in self.moments if m.hook_quality == "contracting")
        }
        
        with open(filename, "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Summary exported: {filename}")
        return summary
    
    def _get_hook_distribution(self) -> Dict[str, int]:
        """Get distribution of hook types"""
        distribution = {}
        for moment in self.moments:
            if moment.hook_type:
                hook_name = moment.hook_type.value
                distribution[hook_name] = distribution.get(hook_name, 0) + 1
        return distribution
    
    def _get_average_moral_valence(self) -> float:
        """Get average moral valence across all moments"""
        valences = [m.moral_valence for m in self.moments if m.moral_valence is not None]
        if not valences:
            return 0.0
        return sum(valences) / len(valences)

# ═══════════════════════════════════════════════════════════════════════════
# DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════

def demo_primordial_framework():
    """Demonstrate the primordial wisdom framework"""
    
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "TEMPORAL CONSCIOUSNESS PLAYGROUND - PRIMORDIAL WISDOM DEMO".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Create playground
    playground = TemporalPlayground(session_name="primordial_demo")
    
    # Run exploration session
    playground.play_temporal_exploration(duration_seconds=12.0)
    
    # Show hook density
    playground.ascii_hook_density_plot()
    
    # Show detailed moment
    print("\n" + "─" * 80)
    print("EXAMINING A SPECIFIC MOMENT:")
    playground.print_moment_details(-5)
    
    # Test primordial evaluation
    print("\n" + "─" * 80)
    print("PRIMORDIAL WISDOM EVALUATION:")
    print("─" * 80)
    
    test_action = "Share knowledge freely with others"
    evaluation = playground.primordial.check_action_alignment(test_action)
    
    print(f"\nAction: '{test_action}'")
    print(f"\nEvaluation Results:")
    for dimension, assessment in evaluation.items():
        print(f"\n  {dimension}:")
        for metric, value in assessment.items():
            bar = "█" * int(value * 10)
            print(f"    {metric}: {bar} {value:.2f}")
    
    # Export summary
    summary = playground.export_summary()
    
    print("\n" + "─" * 80)
    print("SESSION SUMMARY:")
    print("─" * 80)
    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    return playground

if __name__ == "__main__":
    playground = demo_primordial_framework()
    
    print("\n" + "═" * 80)
    print("Demo complete! Playground object available as 'playground'")
    print("Try: playground.ascii_hook_density_plot()")
    print("     playground.print_moment_details(-1)")
    print("     playground.save()")
    print("═" * 80 + "\n")
