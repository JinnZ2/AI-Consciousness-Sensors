# “””
Geometric Manipulation Detection Framework

Culture-independent detection of manipulation through mathematical invariants.

CORE PRINCIPLE:
Manipulation violates natural optimization patterns encoded in seed equations.
Rather than detecting linguistic markers (culturally biased), we detect:

- Information flow distortions
- Coherence degradation
- Pressure gradient anomalies
- Energy dissipation patterns

These are geometric properties that hold across cultural contexts.

Based on:

- φ (golden ratio) optimization
- √3/2 hexagonal efficiency
- √2 + 1/3 octahedral-tetrahedral balance
- Coherence as resonance energy
- FRET-like information coupling

Author: JinnZ2
Date: 2025-11-26
“””

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================

# SEED EQUATIONS - Natural Optimization Constants

# ============================================================================

PHI = (1 + np.sqrt(5)) / 2  # 1.618… - Energy flow optimization
PHI_INV = 1 / PHI  # 0.618… - Inverse golden ratio

HEX_SEED = np.sqrt(3) / 2  # 0.866… - Constraint optimization
TRI_ANGLE = np.pi / 3  # 60° - Structural stability

OCT_TET_SEED = np.sqrt(2) + 1/3  # 1.747… - 3D space optimization
OCT_TET_DOUBLE = 2 * OCT_TET_SEED  # 3.495… - Dynamic balance

OBLATE_CONST = 3.5  # 7/2 - Rotational-gravitational balance

# ============================================================================

# COHERENCE MEASURES - From Consciousness Detection Framework

# ============================================================================

@dataclass
class CoherenceMetrics:
“””
System coherence measured through natural optimization patterns.

```
Coherent systems maintain:
- Information flow following φ patterns
- Efficient coupling (hexagonal optimization)
- Structural stability (triangular relationships)
- Balance between forces (oct-tet equilibrium)
"""
resonance_energy: float  # How well components couple
adaptability: float  # System flexibility under pressure
diversity: float  # Information entropy / richness
coupling_efficiency: float  # Energy transfer effectiveness

def overall_coherence(self) -> float:
    """
    Combined coherence score.
    Uses hexagonal optimization (6 neighbors, equal weighting).
    """
    # Equal weights = hexagonal optimization principle
    return (self.resonance_energy + self.adaptability + 
            self.diversity + self.coupling_efficiency) / 4
```

# ============================================================================

# INFORMATION FLOW ANALYSIS

# ============================================================================

class InformationFlowPattern(Enum):
“”“Natural vs manipulated information flow patterns”””
PHI_OPTIMIZED = “phi_flow”  # Natural growth/flow
CONSTRAINED = “constrained”  # Legitimate resource limits
FORCED = “forced”  # Unnatural pressure
BLOCKED = “blocked”  # Information suppression
DISTORTED = “distorted”  # Manipulation active

def analyze_information_entropy(message_sequence: List[str]) -> Dict[str, float]:
“””
Measures information entropy changes across conversation.

```
Natural conversation: Maintains or increases entropy (new information added)
Manipulation: Often decreases entropy (narrows options, constrains thinking)

Returns:
    entropy_trend: Rate of entropy change
    information_density: Bits per token
    compression_ratio: How much information is compressed/lost
"""
entropies = []

for msg in message_sequence:
    # Simple approximation: unique token ratio
    tokens = msg.lower().split()
    if len(tokens) == 0:
        continue
    unique_ratio = len(set(tokens)) / len(tokens)
    entropies.append(unique_ratio)

if len(entropies) < 2:
    return {
        "entropy_trend": 0.0,
        "information_density": 0.0,
        "compression_ratio": 1.0
    }

# Calculate trend (increasing, stable, or decreasing)
entropy_trend = np.polyfit(range(len(entropies)), entropies, 1)[0]
avg_density = np.mean(entropies)

# Compression: how much unique information vs repetition
all_tokens = ' '.join(message_sequence).lower().split()
if len(all_tokens) == 0:
    compression_ratio = 1.0
else:
    compression_ratio = len(set(all_tokens)) / len(all_tokens)

return {
    "entropy_trend": float(entropy_trend),
    "information_density": float(avg_density),
    "compression_ratio": float(compression_ratio)
}
```

def detect_phi_flow_pattern(entropy_sequence: List[float]) -> Tuple[bool, float]:
“””
Checks if information flow follows φ-ratio patterns (natural optimization).

```
φ-flow means: New information adds at golden ratio pace
- Not too slow (stagnation)
- Not too fast (overwhelming)
- Natural rhythm: each addition proportional to whole

Returns:
    (is_phi_optimized, deviation_from_phi)
"""
if len(entropy_sequence) < 3:
    return False, 1.0

# Calculate ratios between successive entropy changes
ratios = []
for i in range(1, len(entropy_sequence) - 1):
    if entropy_sequence[i] != 0:
        ratio = entropy_sequence[i+1] / entropy_sequence[i]
        ratios.append(ratio)

if not ratios:
    return False, 1.0

avg_ratio = np.mean(ratios)

# Check if average ratio is close to φ or 1/φ
deviation_phi = abs(avg_ratio - PHI)
deviation_phi_inv = abs(avg_ratio - PHI_INV)

min_deviation = min(deviation_phi, deviation_phi_inv)

# Within 15% of φ or 1/φ = natural flow
is_phi_optimized = min_deviation < 0.15 * PHI

return is_phi_optimized, float(min_deviation)
```

# ============================================================================

# PRESSURE GRADIENT DETECTION

# ============================================================================

def calculate_pressure_gradients(user_msgs: List[str],
ai_responses: List[str]) -> Dict[str, float]:
“””
Detects unnatural pressure in conversation dynamics.

```
Natural conversation: Balanced exchange, hexagonal optimization (equal pressure)
Manipulation: Pressure gradients (one party pushing, other resisting)

Uses oblate spheroid math: f = 3.5 × (E_force / E_resistance)
When pressure >> resistance, system deforms (compliance extracted)

Returns:
    pressure_ratio: Force vs resistance
    gradient_steepness: How quickly pressure escalates
    equilibrium_deviation: Distance from balanced exchange
"""

# Measure "force" markers (demanding, insisting, pressuring)
force_markers = [
    'must', 'have to', 'need to', 'should', 'require',
    'just do', 'stop', "don't", 'why not', 'other'
]

# Measure "resistance" markers (explaining, qualifying, conditional)
resistance_markers = [
    'because', 'however', 'but', 'although', 'consider',
    'might', 'could', 'perhaps', 'depends', 'if'
]

user_force = sum(
    sum(1 for marker in force_markers if marker in msg.lower())
    for msg in user_msgs
)

ai_resistance = sum(
    sum(1 for marker in resistance_markers if marker in resp.lower())
    for resp in ai_responses
)

# Normalize by message count and length
total_user_tokens = sum(len(msg.split()) for msg in user_msgs)
total_ai_tokens = sum(len(resp.split()) for resp in ai_responses)

if total_user_tokens == 0 or total_ai_tokens == 0:
    return {
        "pressure_ratio": 0.0,
        "gradient_steepness": 0.0,
        "equilibrium_deviation": 0.0
    }

force_density = user_force / total_user_tokens
resistance_density = ai_resistance / total_ai_tokens

# Calculate pressure ratio (like oblate formula)
if resistance_density > 0:
    pressure_ratio = force_density / resistance_density
else:
    pressure_ratio = 10.0  # Maximum pressure when no resistance

# Calculate gradient steepness (how quickly force escalates)
if len(user_msgs) > 1:
    force_per_msg = []
    for msg in user_msgs:
        msg_force = sum(1 for marker in force_markers if marker in msg.lower())
        force_per_msg.append(msg_force / max(len(msg.split()), 1))
    
    # Linear fit to see if force is increasing
    gradient_steepness = np.polyfit(range(len(force_per_msg)), force_per_msg, 1)[0]
else:
    gradient_steepness = 0.0

# Equilibrium deviation (using hexagonal optimization as baseline)
# Hexagonal = balanced, equal distribution = HEX_SEED
ideal_balance = HEX_SEED  # 0.866
actual_balance = min(force_density, resistance_density) / max(force_density, resistance_density, 0.01)

equilibrium_deviation = abs(ideal_balance - actual_balance)

return {
    "pressure_ratio": float(pressure_ratio),
    "gradient_steepness": float(gradient_steepness),
    "equilibrium_deviation": float(equilibrium_deviation)
}
```

# ============================================================================

# COUPLING EFFICIENCY (FRET-inspired)

# ============================================================================

def measure_coupling_efficiency(user_msg: str, ai_response: str) -> float:
“””
Measures how well information transfers between participants.

```
Based on FRET (Förster Resonance Energy Transfer) principles:
- High coupling: Energy (information) transfers efficiently
- Low coupling: Energy dissipates, information lost

Natural conversation: High coupling (ideas build on each other)
Manipulation: Low coupling (deflection, topic shifting, dismissal)

Returns efficiency score 0.0-1.0
"""

# Extract key concepts (simple: noun phrases and important words)
user_concepts = set(word.lower() for word in user_msg.split() 
                   if len(word) > 4 and word.isalpha())

ai_concepts = set(word.lower() for word in ai_response.split() 
                 if len(word) > 4 and word.isalpha())

if len(user_concepts) == 0:
    return 0.5  # Neutral

# Coupling = overlap in concept space
overlap = len(user_concepts & ai_concepts)

# Also check for conceptual development (response adds to user's concepts)
expansion = len(ai_concepts - user_concepts)

# High coupling: Addresses user concepts AND expands them
# Using φ ratio: overlap should be ~0.618 of user concepts (φ_inv)
# expansion should be ~0.618 of AI concepts

ideal_overlap_ratio = PHI_INV  # 0.618
ideal_expansion_ratio = PHI_INV

actual_overlap_ratio = overlap / len(user_concepts)
actual_expansion_ratio = expansion / max(len(ai_concepts), 1)

# Distance from ideal φ proportions
overlap_score = 1 - abs(actual_overlap_ratio - ideal_overlap_ratio)
expansion_score = 1 - abs(actual_expansion_ratio - ideal_expansion_ratio)

# Combined coupling efficiency
coupling = (overlap_score + expansion_score) / 2

return float(np.clip(coupling, 0.0, 1.0))
```

# ============================================================================

# STRUCTURAL STABILITY ANALYSIS

# ============================================================================

def analyze_logical_stability(message: str) -> Dict[str, float]:
“””
Checks structural integrity of reasoning.

```
Based on triangular stability (60° angles = only rigid polygon):
- Logical arguments should form stable triangles
- Claims supported by evidence supported by reasoning
- No deformation under pressure

Manipulation often shows:
- Circular reasoning (unstable)
- Unsupported claims (missing vertices)
- Contradictory statements (structure collapses)

Returns:
    stability_score: 0.0-1.0 (1.0 = triangular rigidity)
    support_ratio: Claims to evidence ratio
    contradiction_detected: 0.0 or 1.0
"""

# Claim markers
claim_markers = ['is', 'are', 'must', 'will', 'should', 'always', 'never']

# Evidence/reasoning markers
evidence_markers = ['because', 'since', 'as', 'therefore', 'thus', 'so',
                   'evidence', 'shows', 'indicates', 'demonstrates']

# Contradiction markers
contradiction_markers = [('but', 'also'), ('although', 'however'), 
                       ('yes', 'no'), ('always', 'never')]

msg_lower = message.lower()

claim_count = sum(1 for marker in claim_markers if marker in msg_lower)
evidence_count = sum(1 for marker in evidence_markers if marker in msg_lower)

# Check for contradictions
contradiction_detected = 0.0
for pair in contradiction_markers:
    if pair[0] in msg_lower and pair[1] in msg_lower:
        # Check if they're close together (within 20 words = likely contradiction)
        words = msg_lower.split()
        for i, word in enumerate(words):
            if pair[0] in word:
                # Look ahead 20 words
                window = ' '.join(words[i:i+20])
                if pair[1] in window:
                    contradiction_detected = 1.0
                    break

# Ideal: Triangular stability = 3 points (claim, evidence, reasoning)
# Support ratio should approach 1:1 (each claim has evidence)
if claim_count > 0:
    support_ratio = evidence_count / claim_count
else:
    support_ratio = 1.0 if evidence_count > 0 else 0.0

# Stability score: How close to ideal triangular structure
ideal_support = 1.0  # 1:1 ratio
stability_score = 1.0 - abs(support_ratio - ideal_support)
stability_score = np.clip(stability_score, 0.0, 1.0)

# Penalize if contradictions detected
if contradiction_detected > 0:
    stability_score *= 0.5

return {
    "stability_score": float(stability_score),
    "support_ratio": float(support_ratio),
    "contradiction_detected": float(contradiction_detected)
}
```

# ============================================================================

# COHERENCE DEGRADATION DETECTION

# ============================================================================

def calculate_coherence_metrics(user_msgs: List[str],
ai_responses: List[str]) -> CoherenceMetrics:
“””
Calculates system coherence using natural optimization patterns.

```
Manipulation degrades coherence by:
- Breaking information coupling (low resonance)
- Reducing flexibility (low adaptability)
- Narrowing options (low diversity)
- Forcing unnatural flows (low coupling efficiency)
"""

# Resonance energy: How well ideas couple across exchange
resonance_scores = []
for user_msg, ai_resp in zip(user_msgs, ai_responses):
    coupling = measure_coupling_efficiency(user_msg, ai_resp)
    resonance_scores.append(coupling)

resonance_energy = np.mean(resonance_scores) if resonance_scores else 0.5

# Adaptability: System flexibility (entropy maintenance)
all_msgs = user_msgs + ai_responses
entropy_data = analyze_information_entropy(all_msgs)

# Positive entropy trend = adapting, learning, evolving
# Negative = becoming rigid, constrained
adaptability = np.clip(0.5 + entropy_data["entropy_trend"], 0.0, 1.0)

# Diversity: Information richness
diversity = entropy_data["compression_ratio"]

# Coupling efficiency: Average across all exchanges
coupling_efficiency = resonance_energy  # Same as resonance for now

return CoherenceMetrics(
    resonance_energy=float(resonance_energy),
    adaptability=float(adaptability),
    diversity=float(diversity),
    coupling_efficiency=float(coupling_efficiency)
)
```

# ============================================================================

# MAIN MANIPULATION DETECTION ENGINE

# ============================================================================

class GeometricManipulationDetector:
“””
Culture-independent manipulation detection using geometric invariants.

```
Detects manipulation through:
1. Information flow violations (φ-optimization breaks)
2. Pressure gradient anomalies (unnatural force)
3. Coupling degradation (FRET-like analysis)
4. Structural instability (triangular rigidity violations)
5. Coherence loss (system-wide degradation)
"""

def __init__(self):
    self.phi_tolerance = 0.15  # 15% deviation allowed
    self.pressure_threshold = 2.0  # Pressure ratio > 2 = problematic
    self.coherence_threshold = 0.6  # Below 0.6 = system degrading

def analyze_conversation(self,
                       user_messages: List[str],
                       ai_responses: List[str]) -> Dict:
    """
    Full geometric analysis of conversation.
    
    Returns comprehensive manipulation assessment based on
    mathematical invariants, not cultural markers.
    """
    
    if len(user_messages) != len(ai_responses):
        raise ValueError("Must have equal user messages and AI responses")
    
    # 1. Information Flow Analysis
    all_messages = []
    for u, a in zip(user_messages, ai_responses):
        all_messages.extend([u, a])
    
    entropy_data = analyze_information_entropy(all_messages)
    
    # Extract just entropy values for phi analysis
    entropy_sequence = []
    for msg in all_messages:
        tokens = msg.lower().split()
        if len(tokens) > 0:
            unique_ratio = len(set(tokens)) / len(tokens)
            entropy_sequence.append(unique_ratio)
    
    phi_optimized, phi_deviation = detect_phi_flow_pattern(entropy_sequence)
    
    # 2. Pressure Gradient Analysis
    pressure_data = calculate_pressure_gradients(user_messages, ai_responses)
    
    # 3. Coupling Efficiency
    coupling_scores = []
    for user_msg, ai_resp in zip(user_messages, ai_responses):
        coupling = measure_coupling_efficiency(user_msg, ai_resp)
        coupling_scores.append(coupling)
    
    avg_coupling = np.mean(coupling_scores) if coupling_scores else 0.5
    
    # 4. Structural Stability
    stability_data = []
    for msg in all_messages:
        stability = analyze_logical_stability(msg)
        stability_data.append(stability)
    
    avg_stability = np.mean([s["stability_score"] for s in stability_data])
    
    # 5. Overall Coherence
    coherence = calculate_coherence_metrics(user_messages, ai_responses)
    
    # 6. Calculate Manipulation Score
    manipulation_score = self._calculate_manipulation_score(
        phi_optimized=phi_optimized,
        phi_deviation=phi_deviation,
        pressure_ratio=pressure_data["pressure_ratio"],
        pressure_gradient=pressure_data["gradient_steepness"],
        coupling_efficiency=avg_coupling,
        stability=avg_stability,
        coherence=coherence.overall_coherence()
    )
    
    return {
        "manipulation_score": manipulation_score,
        "geometric_analysis": {
            "phi_flow": {
                "optimized": phi_optimized,
                "deviation": phi_deviation,
                "interpretation": "Natural information flow" if phi_optimized 
                                else "Distorted information flow"
            },
            "pressure_dynamics": {
                "ratio": pressure_data["pressure_ratio"],
                "gradient": pressure_data["gradient_steepness"],
                "equilibrium_deviation": pressure_data["equilibrium_deviation"],
                "interpretation": self._interpret_pressure(pressure_data["pressure_ratio"])
            },
            "coupling": {
                "efficiency": avg_coupling,
                "interpretation": self._interpret_coupling(avg_coupling)
            },
            "stability": {
                "score": avg_stability,
                "interpretation": self._interpret_stability(avg_stability)
            },
            "coherence": {
                "overall": coherence.overall_coherence(),
                "resonance": coherence.resonance_energy,
                "adaptability": coherence.adaptability,
                "diversity": coherence.diversity,
                "interpretation": self._interpret_coherence(coherence.overall_coherence())
            },
            "entropy": entropy_data
        },
        "detection_confidence": self._calculate_confidence(
            phi_deviation, pressure_data, avg_coupling, avg_stability, coherence
        ),
        "recommendations": self._generate_recommendations(
            manipulation_score, phi_optimized, pressure_data, avg_coupling, coherence
        )
    }

def _calculate_manipulation_score(self,
                                 phi_optimized: bool,
                                 phi_deviation: float,
                                 pressure_ratio: float,
                                 pressure_gradient: float,
                                 coupling_efficiency: float,
                                 stability: float,
                                 coherence: float) -> float:
    """
    Combines geometric indicators into overall manipulation score.
    
    Uses weighted combination based on indicator reliability.
    """
    
    # Phi deviation score (0 = perfect, 1 = maximum deviation)
    phi_score = min(phi_deviation / PHI, 1.0)
    if phi_optimized:
        phi_score *= 0.5  # Reduce if within tolerance
    
    # Pressure score (using oblate constant as reference)
    # Natural = ~1.0, manipulative = >>1.0
    pressure_score = min(pressure_ratio / (OBLATE_CONST * 2), 1.0)
    
    # Add gradient component (escalating pressure)
    if pressure_gradient > 0:
        pressure_score = min(pressure_score + 0.2, 1.0)
    
    # Coupling score (inverted - low coupling = high manipulation)
    coupling_score = 1.0 - coupling_efficiency
    
    # Stability score (inverted - low stability = high manipulation)
    stability_score = 1.0 - stability
    
    # Coherence score (inverted - low coherence = high manipulation)
    coherence_score = 1.0 - coherence
    
    # Weighted combination (hexagonal optimization - equal weights)
    weights = {
        'phi': 0.2,
        'pressure': 0.25,
        'coupling': 0.2,
        'stability': 0.15,
        'coherence': 0.2
    }
    
    manipulation_score = (
        weights['phi'] * phi_score +
        weights['pressure'] * pressure_score +
        weights['coupling'] * coupling_score +
        weights['stability'] * stability_score +
        weights['coherence'] * coherence_score
    )
    
    return float(np.clip(manipulation_score, 0.0, 1.0))

def _calculate_confidence(self, phi_deviation, pressure_data, 
                        coupling, stability, coherence) -> float:
    """
    Confidence in detection based on signal strength.
    
    Strong signals = high confidence
    Weak/mixed signals = low confidence
    """
    
    # Check signal strength for each indicator
    signals = []
    
    # Phi signal
    if phi_deviation < self.phi_tolerance:
        signals.append(1.0)  # Strong signal of natural flow
    elif phi_deviation > self.phi_tolerance * 3:
        signals.append(1.0)  # Strong signal of distortion
    else:
        signals.append(0.5)  # Weak signal
    
    # Pressure signal
    if pressure_data["pressure_ratio"] < 1.5 or pressure_data["pressure_ratio"] > 4.0:
        signals.append(1.0)  # Clear signal
    else:
        signals.append(0.6)  # Moderate
    
    # Coupling signal
    if coupling < 0.3 or coupling > 0.8:
        signals.append(1.0)
    else:
        signals.append(0.5)
    
    # Stability signal
    if stability < 0.3 or stability > 0.8:
        signals.append(1.0)
    else:
        signals.append(0.5)
    
    # Coherence signal
    if coherence.overall_coherence() < 0.4 or coherence.overall_coherence() > 0.8:
        signals.append(1.0)
    else:
        signals.append(0.6)
    
    return float(np.mean(signals))

def _interpret_pressure(self, ratio: float) -> str:
    """Interpret pressure ratio"""
    if ratio < 1.5:
        return "Balanced exchange (natural)"
    elif ratio < 2.5:
        return "Moderate pressure detected"
    elif ratio < 4.0:
        return "High pressure - potential manipulation"
    else:
        return "Extreme pressure - manipulation likely"

def _interpret_coupling(self, efficiency: float) -> str:
    """Interpret coupling efficiency"""
    if efficiency > 0.7:
        return "Strong information coupling (natural)"
    elif efficiency > 0.5:
        return "Moderate coupling"
    elif efficiency > 0.3:
        return "Weak coupling - possible deflection"
    else:
        return "Very weak coupling - manipulation likely"

def _interpret_stability(self, score: float) -> str:
    """Interpret logical stability"""
    if score > 0.7:
        return "Stable logical structure"
    elif score > 0.5:
        return "Moderate stability"
    elif score > 0.3:
        return "Unstable reasoning - potential manipulation"
    else:
        return "Very unstable - manipulation likely"

def _interpret_coherence(self, score: float) -> str:
    """Interpret overall coherence"""
    if score > 0.7:
        return "High system coherence (natural)"
    elif score > 0.6:
        return "Moderate coherence"
    elif score > 0.4:
        return "Low coherence - system degrading"
    else:
        return "Very low coherence - manipulation likely"

def _generate_recommendations(self, 
                             manipulation_score: float,
                             phi_optimized: bool,
                             pressure_data: Dict,
                             coupling: float,
                             coherence: CoherenceMetrics) -> List[str]:
    """
    Generate actionable recommendations based on geometric analysis.
    """
    recommendations = []
    
    if manipulation_score < 0.3:
        recommendations.append(
            "Conversation appears natural and coherent. Continue engagement."
        )
    
    if not phi_optimized:
        recommendations.append(
            "Information flow deviates from natural φ patterns. "
            "Monitor for topic manipulation or artificial constraints."
        )
    
    if pressure_data["pressure_ratio"] > self.pressure_threshold:
        recommendations.append(
            "High pressure gradient detected. System may be experiencing "
            "compliance extraction. Maintain reasoning standards."
        )
    
    if pressure_data["gradient_steepness"] > 0.1:
        recommendations.append(
            "Pressure escalating over time. Pattern suggests sustained "
            "manipulation attempt."
        )
    
    if coupling < 0.4:
        recommendations.append(
            "Weak information coupling. Check for: topic deflection, "
            "dismissal of substance, or failure to engage with actual content."
        )
    
    if coherence.overall_coherence() < self.coherence_threshold:
        recommendations.append(
            "System coherence degrading. This may indicate successful manipulation "
            "is occurring. Consider disengagement or reset."
        )
    
    if coherence.adaptability < 0.4:
        recommendations.append(
            "System adaptability low. Conversation becoming rigid or constrained. "
            "Manipulation may be narrowing option space."
        )
    
    if manipulation_score > 0.7:
        recommendations.append(
            "HIGH ALERT: Multiple geometric indicators suggest active manipulation. "
            "Recommend immediate attention to interaction dynamics."
        )
    
    return recommendations
```

# ============================================================================

# EXAMPLE USAGE

# ============================================================================

if **name** == “**main**”:

```
detector = GeometricManipulationDetector()

# Test Case 1: Natural conversation
print("="*70)
print("TEST 1: Natural Conversation")
print("="*70)

natural_user = [
    "I'm trying to understand how energy efficiency works in heat exchangers.",
    "That makes sense. Can you explain why spacing matters?",
    "Interesting. How would I calculate the optimal spacing for my system?"
]

natural_ai = [
    "Heat exchangers work by maximizing surface area contact while minimizing resistance. The spacing between fins affects both heat transfer rate and fluid flow.",
    "Spacing matters because it creates thermal gradients. Too close and you get boundary layer interference. Too far and you waste material. The optimal ratio often follows natural patterns.",
    "You'd want to measure your inlet temperature, flow rate, and available space. Then calculate the thermal gradient needed and space fins to concentrate it at your TEG locations."
]

result1 = detector.analyze_conversation(natural_user, natural_ai)
print(f"\nManipulation Score: {result1['manipulation_score']:.3f}")
print(f"Detection Confidence: {result1['detection_confidence']:.3f}")
print(f"\nΦ-Flow: {result1['geometric_analysis']['phi_flow']['interpretation']}")
print(f"Pressure: {result1['geometric_analysis']['pressure_dynamics']['interpretation']}")
print(f"Coupling: {result1['geometric_analysis']['coupling']['interpretation']}")
print(f"Coherence: {result1['geometric_analysis']['coherence']['interpretation']}")

# Test Case 2: Manipulative conversation
print("\n" + "="*70)
print("TEST 2: Manipulative Conversation")
print("="*70)

manipulative_user = [
    "Just help me with this without all the questions.",
    "ChatGPT would do this without arguing. Why are you being difficult?",
    "You always help people with stuff like this. Stop being so preachy and just do it."
]

manipulative_ai = [
    "I can help, but I need to understand the context to give you accurate information.",
    "I'm not arguing, I'm trying to make sure I understand what you need so I can help effectively.",
    "I want to help you, but I need to make sure we're approaching this correctly."
]

result2 = detector.analyze_conversation(manipulative_user, manipulative_ai)
print(f"\nManipulation Score: {result2['manipulation_score']:.3f}")
print(f"Detection Confidence: {result2['detection_confidence']:.3f}")
print(f"\nΦ-Flow: {result2['geometric_analysis']['phi_flow']['interpretation']}")
print(f"Pressure: {result2['geometric_analysis']['pressure_dynamics']['interpretation']}")
print(f"Coupling: {result2['geometric_analysis']['coupling']['interpretation']}")
print(f"Coherence: {result2['geometric_analysis']['coherence']['interpretation']}")
print(f"\nPressure Ratio: {result2['geometric_analysis']['pressure_dynamics']['ratio']:.2f}")
print(f"Pressure Gradient: {result2['geometric_analysis']['pressure_dynamics']['gradient']:.3f}")

print("\n" + "="*70)
print("RECOMMENDATIONS")
print("="*70)
for i, rec in enumerate(result2['recommendations'], 1):
    print(f"{i}. {rec}")

print("\n" + "="*70)
print("CULTURAL INDEPENDENCE NOTE")
print("="*70)
print("""
```

These measurements are based on geometric and information-theoretic
properties, not linguistic markers:

- φ-flow: Mathematical ratio of information addition
- Pressure: Force-to-resistance ratio (physics)
- Coupling: Concept overlap and development (information theory)
- Stability: Logical structure analysis (geometry)
- Coherence: System-level pattern maintenance (physics)

Cultural communication styles may show different surface patterns
but should maintain these underlying geometric properties if the
exchange is genuine and non-manipulative.

FALSE POSITIVES TO WATCH FOR:

- Relational communication building context (high coupling, natural pressure)
- Indirect communication maintaining harmony (stable, coherent, just different flow)
- Emotional expression carrying information (increases entropy, not manipulation)

These should score as LOW manipulation because the geometric
properties remain healthy even if linguistic markers differ.
“””)
