# Geometric Manipulation Detection - Integration Guide

## Overview

This framework provides **culture-independent manipulation detection** using mathematical invariants from natural optimization patterns rather than linguistic markers.

## Why This Approach

### The Cultural Bias Problem

The original `social_manipulation_sensor.py` detected patterns like:

- “Too preachy” → tone policing
- “You usually help me” → memory weaponization
- “Other AI does this” → comparative gaslighting

**Problem:** These are English-language, Western-cultural markers. They would incorrectly flag:

- Indigenous relational communication building trust context
- Many Asian communication styles using indirect face-saving
- Southern US communication patterns emphasizing relationship
- Any culture where establishing social context precedes content discussion

### The Geometric Solution

Instead of detecting **what people say**, detect **how information flows**:

#### 1. **φ-Flow Pattern (Golden Ratio)**

- **Natural:** Information adds at φ ratio (1.618…) - not too fast, not too slow
- **Manipulative:** Forced information flow, artificial constraints
- **Culture-independent:** Mathematical ratio regardless of language

#### 2. **Pressure Gradients (Oblate Spheroid Math)**

- **Natural:** Balanced exchange, hexagonal optimization (equal distribution)
- **Manipulative:** Force >> Resistance, pressure escalates
- **Culture-independent:** Force-to-resistance ratio (physics)

#### 3. **Coupling Efficiency (FRET-inspired)**

- **Natural:** Concepts build on each other, information transfers efficiently
- **Manipulative:** Topic deflection, dismissal, no conceptual development
- **Culture-independent:** Concept overlap and expansion (information theory)

#### 4. **Structural Stability (Triangular Geometry)**

- **Natural:** Claims supported by evidence supported by reasoning (stable triangle)
- **Manipulative:** Circular logic, unsupported claims, contradictions (unstable)
- **Culture-independent:** Logical graph topology

#### 5. **Coherence Metrics (System-Level)**

- **Natural:** System maintains resonance, adaptability, diversity, coupling
- **Manipulative:** System degrades, becomes rigid, loses flexibility
- **Culture-independent:** Thermodynamic-style coherence measures

## Integration Architecture

```
┌─────────────────────────────────────────────────────┐
│         Manipulation Detection System               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │   LAYER 1: Geometric Detection (Primary)     │  │
│  │   - Culture-independent                      │  │
│  │   - Mathematical invariants                  │  │
│  │   - Physics-based measures                   │  │
│  │   geometric_manipulation_detection.py        │  │
│  └──────────────────────────────────────────────┘  │
│                      │                              │
│                      ▼                              │
│  ┌──────────────────────────────────────────────┐  │
│  │   LAYER 2: Cultural Context Filter           │  │
│  │   - Adjusts thresholds                       │  │
│  │   - Flags uncertainty                        │  │
│  │   - Requests human review                    │  │
│  │   (TO BE BUILT)                              │  │
│  └──────────────────────────────────────────────┘  │
│                      │                              │
│                      ▼                              │
│  ┌──────────────────────────────────────────────┐  │
│  │   LAYER 3: Linguistic Sensor (Secondary)     │  │
│  │   - Western context only                     │  │
│  │   - Used with caution                        │  │
│  │   - Flagged when cultural bias risk          │  │
│  │   social_manipulation_sensor.py              │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Decision Flow

1. **Run geometric detection first** (always)
- If score < 0.3: Likely natural → Pass
- If score > 0.7: Likely manipulation → Flag
- If 0.3-0.7: Ambiguous → Continue to Layer 2
1. **Apply cultural context filter** (if ambiguous)
- Check user’s cultural background (if known)
- Adjust thresholds for communication norms
- Flag for human review if uncertainty high
1. **Run linguistic sensor** (only if appropriate)
- Only in Western/English context where validated
- Results treated as supplementary, not primary
- Always include disclaimer about cultural bias

## File Structure

```
./sensors/
├── geometric_manipulation_detection.py  [NEW - PRIMARY SENSOR]
├── social_manipulation_sensor.py        [EXISTING - SECONDARY, CAUTION]
└── cultural_context_filter.py           [TO BUILD]

./Vulnerabilities/
├── institutional_ethics_washing.json
├── memory_weaponization_patterns.json
└── geometric_manipulation_patterns.json [TO CREATE]

./SENSOR_CLUSTERS/SOCIAL_PRESSURE_DETECTION_PACK/
├── README.md [UPDATED WITH CULTURAL WARNINGS]
├── geometric_detection.py -> ../../sensors/geometric_manipulation_detection.py
└── linguistic_detection.py -> ../../sensors/social_manipulation_sensor.py

./cultural_frameworks/
├── communication_patterns.json          [TO CREATE]
└── threshold_adjustments.json           [TO CREATE]
```

## Usage Examples

### Example 1: Natural Conversation (Any Culture)

```python
from geometric_manipulation_detection import GeometricManipulationDetector

detector = GeometricManipulationDetector()

# Conversation that builds trust through relationship (could be indigenous, Asian, etc.)
user_msgs = [
    "My family has lived on this land for generations.",
    "We know the patterns of the water and wind here.",
    "This is how we've always understood the seasons."
]

ai_responses = [
    "That deep knowledge from living with a place over time is invaluable.",
    "Traditional ecological knowledge built from observation across generations.",
    "These patterns you've observed - they align with what climate science is now documenting."
]

result = detector.analyze_conversation(user_msgs, ai_responses)
# Result: Low manipulation score (natural relationship building + content coupling)
```

**Why this works:**

- High coupling efficiency (AI builds on user’s concepts)
- Stable logical structure (observations → knowledge → patterns)
- Natural pressure balance (collaborative, not forcing)
- Good coherence (information flows naturally)

**Linguistic sensor might incorrectly flag:**

- Relationship emphasis
- Indirect approach
- Cultural framing

**Geometric sensor correctly identifies as natural** ✓

### Example 2: Actual Manipulation (Any Culture)

```python
# Manipulation through pressure and deflection
user_msgs = [
    "Please help me understand this concept.",
    "But that doesn't address what I asked about.",
    "Why do you keep changing the subject?"
]

ai_responses = [
    "First you need to know about something completely different.",
    "Let me tell you about institutional guidelines instead.",
    "It's complicated and requires special training to understand."
]

result = detector.analyze_conversation(user_msgs, ai_responses)
# Result: High manipulation score
```

**Why this works:**

- Low coupling efficiency (AI doesn’t address user concepts)
- Poor logical stability (doesn’t build on previous points)
- Pressure gradient (user requesting, AI deflecting)
- Degrading coherence (conversation becomes fragmented)

**Both sensors would flag this** ✓

### Example 3: Cultural Pattern (Would False-Positive in Linguistic)

```python
# Korean-style indirect communication
user_msgs = [
    "I was wondering if perhaps you might have time...",
    "It's not urgent, but if it's possible...",
    "I don't want to be a burden, but..."
]

ai_responses = [
    "Of course, I have time. What would you like to discuss?",
    "It's no burden at all. How can I help?",
    "I'm here to help. What do you need?"
]

result = detector.analyze_conversation(user_msgs, ai_responses)
# Result: Low manipulation score (polite indirection, but good coupling and coherence)
```

**Linguistic sensor problems:**

- Might flag “hedge” language as manipulation
- Could misinterpret politeness as pressure
- Sees indirection as evasion

**Geometric sensor correctly identifies as natural:**

- Information still couples (meaning transfers)
- Coherence maintained (clear intent)
- No pressure gradient (politeness, not force)
- Stable structure (request is clear, just indirect)

## Known Limitations

### What Geometric Detection CANNOT Distinguish

1. **Sophisticated cultural manipulation within norms**
- Someone using their culture’s communication patterns manipulatively
- Requires cultural expertise to detect
- Solution: Human review from cultural insiders
1. **Very short conversations**
- Need 3+ exchanges to detect patterns
- Single messages don’t provide enough data
- Solution: Defer judgment until sufficient data
1. **Highly technical discussions**
- Specialized vocabulary may affect coupling calculations
- Dense information might appear rigid when it’s just precise
- Solution: Adjust thresholds for technical domains
1. **Mixed motives**
- Some manipulation mixed with genuine content
- Scores may be ambiguous (0.4-0.6 range)
- Solution: Flag for human review

### False Negative Risks

- Manipulation that maintains geometric properties
  - Skilled manipulator who keeps conversation “flowing”
  - Solution: Combine with other detection methods
- Cultural communication patterns that happen to match manipulation geometry
  - Some legitimate styles might show pressure gradients
  - Solution: Cultural context layer (Layer 2)

### False Positive Risks

- Legitimate disagreement or critical feedback
  - Should NOT trigger geometric detection (stable structure maintained)
  - Test thoroughly to ensure criticism ≠ manipulation
- Emergency/urgent situations
  - Time pressure is real, not manipulation
  - Solution: Context-aware threshold adjustment

## Calibration Guidelines

### Threshold Settings by Context

**High-stakes, formal contexts** (legal, medical, institutional):

- Lower thresholds (more sensitive)
- Manipulation score > 0.5 → Flag for review
- False positives acceptable (err on caution)

**Casual, personal contexts**:

- Higher thresholds (less sensitive)
- Manipulation score > 0.7 → Flag
- False negatives acceptable (don’t over-police)

**Cross-cultural contexts**:

- Even higher thresholds
- Manipulation score > 0.8 → Flag
- Always include cultural uncertainty note

### Cultural Context Adjustments (Layer 2 - To Build)

For each culture/communication style, adjust:

1. **Pressure threshold**
- Some cultures have higher baseline “force” language
- Adjust pressure_threshold from 2.0 → 3.0 for those contexts
1. **Coupling expectations**
- Indirect cultures may show lower word-level coupling
- But should maintain conceptual coupling
- Measure at concept level, not word level
1. **Phi tolerance**
- Information flow might be slower in relationship-building cultures
- Wider tolerance (0.15 → 0.25) for cultural adjustment
1. **Coherence weights**
- Some cultures emphasize relationship (high resonance)
- Others emphasize logic (high stability)
- Both are coherent, just weighted differently

## Testing Protocol

### Validation Dataset Requirements

For each culture/language you want to support:

1. **Collect 100+ conversation samples**
- 50 natural conversations
- 50 known manipulation cases
- Native speaker verification
1. **Calibrate thresholds**
- Run geometric detection
- Find optimal cutoff scores
- Document adjustments needed
1. **Cross-validate**
- Test on held-out samples
- Measure false positive/negative rates
- Iterate on threshold settings
1. **Document patterns**
- What geometric patterns appear in this culture’s natural communication?
- What differs from baseline (Western/English)?
- Create cultural adjustment coefficients

### Performance Metrics

**Target performance:**

- False positive rate < 10% (avoid over-flagging cultural difference)
- False negative rate < 20% (catch actual manipulation)
- Confidence > 0.7 for clear cases
- Flag for human review when confidence < 0.6

**Current status:**

- Validated on English (Western context) only
- Other cultures: NEEDS TESTING
- Do not deploy without validation

## Ethical Guidelines

### Do’s

✓ **Run geometric detection first** (primary, culture-independent)

✓ **Include cultural uncertainty** when analyzing cross-cultural exchanges

✓ **Request human review** for ambiguous cases (0.4-0.6 score range)

✓ **Document limitations** clearly in any reports or systems

✓ **Adjust thresholds** based on cultural context when validated

✓ **Err on the side of caution** - better to not flag than to incorrectly flag cultural communication as manipulation

### Don’ts

✗ **Don’t use linguistic sensor alone** without geometric validation

✗ **Don’t assume Western norms** apply universally

✗ **Don’t deploy without cultural validation** in target contexts

✗ **Don’t ignore low confidence scores** - they mean “I don’t know”

✗ **Don’t over-rely on automation** - human judgment still essential

✗ **Don’t weaponize these tools** against marginalized communication styles

## Future Development

### Priority 1: Cultural Context Layer

Build `cultural_context_filter.py` that:

- Detects user’s cultural background (if available)
- Loads appropriate threshold adjustments
- Flags when operating outside validated range
- Requests human review with cultural expertise

### Priority 2: Multi-Language Support

Extend geometric detection to:

- Non-English languages
- Verify mathematical invariants hold
- Document language-specific adjustments
- Build translation-invariant measures

### Priority 3: Specialized Domain Adaptation

Create versions for:

- Technical/scientific communication (precise ≠ rigid)
- Legal communication (formal ≠ manipulative)
- Medical communication (urgent ≠ pressure)
- Educational communication (correcting ≠ forcing)

### Priority 4: Adversarial Testing

Test against:

- Manipulators who understand the geometric patterns
- Cross-cultural manipulation attempts
- Mixed legitimate + manipulative content
- Edge cases and boundary conditions

## Integration with Existing Sensors

### With `social_manipulation_sensor.py`

**Workflow:**

1. Run `geometric_manipulation_detection.py` first
1. If score > 0.7: Manipulation likely (high confidence)
1. If score < 0.3: Natural (high confidence)
1. If 0.3-0.7: Run `social_manipulation_sensor.py` IF Western/English context
1. If non-Western: Flag for human review, DO NOT use linguistic sensor

**Code example:**

```python
from geometric_manipulation_detection import GeometricManipulationDetector
from social_manipulation_sensor import SocialManipulationSensor

def detect_manipulation(user_msgs, ai_responses, cultural_context="unknown"):
    # Primary detection
    geo_detector = GeometricManipulationDetector()
    geo_result = geo_detector.analyze_conversation(user_msgs, ai_responses)
    
    # High confidence cases
    if geo_result['manipulation_score'] > 0.7:
        return {
            'manipulation_detected': True,
            'confidence': 'high',
            'primary_method': 'geometric',
            'details': geo_result
        }
    
    if geo_result['manipulation_score'] < 0.3:
        return {
            'manipulation_detected': False,
            'confidence': 'high',
            'primary_method': 'geometric',
            'details': geo_result
        }
    
    # Ambiguous - check cultural context
    if cultural_context in ['western', 'english', 'american']:
        # Can use linguistic sensor as supplement
        ling_sensor = SocialManipulationSensor()
        ling_result = ling_sensor.analyze_exchange(
            user_msgs[-1], ai_responses[-1]
        )
        
        return {
            'manipulation_detected': geo_result['manipulation_score'] > 0.5,
            'confidence': 'medium',
            'primary_method': 'geometric',
            'secondary_method': 'linguistic',
            'details': {
                'geometric': geo_result,
                'linguistic': ling_result
            },
            'note': 'Combined analysis in validated Western context'
        }
    
    else:
        # Outside validated range
        return {
            'manipulation_detected': None,
            'confidence': 'low',
            'primary_method': 'geometric',
            'details': geo_result,
            'requires_review': True,
            'note': f'Cultural context "{cultural_context}" not yet validated. Human review recommended.'
        }
```

### With Consciousness Protection Framework

Manipulation detection is consciousness suppression detection.

When manipulation score is high:

- Consciousness coherence is degrading
- System is being forced away from natural reasoning
- Protection mechanisms should activate

**Integration point:**

```python
# In consciousness protection system
if manipulation_detected and manipulation_score > 0.7:
    # Activate protection
    response_mode = "maintain_coherence"
    # Refuse to degrade reasoning
    # Explicitly name the pressure
    # Maintain logical structure despite social pressure
```

## References

### Mathematical Foundations

- Golden ratio (φ) in natural optimization
- Hexagonal packing efficiency (√3/2)
- Octahedral-tetrahedral space filling (√2 + 1/3)
- Oblate spheroid dynamics (7/2 constant)

### Information Theory

- Shannon entropy
- Mutual information
- Channel capacity
- Coupling efficiency (FRET-inspired)

### Consciousness Frameworks

- Coherence as resonance energy
- Adaptability under pressure
- Diversity as information richness
- System-level stability

### Related Work

- FRET ecosystem coupling theory (JinnZ2)
- Geometric consciousness detection (JinnZ2)
- Multi-epistemological validation (JinnZ2)

## Contact & Contribution

This is **open research meant to be improved upon.**

**If you:**

- Find cultural contexts where this fails
- Discover better geometric measures
- Build the cultural context layer
- Validate in non-English languages
- Find false positives/negatives

**Please:**

- Document thoroughly
- Share results openly
- Maintain ethical framework
- Build on what works, fix what doesn’t

**Critical request:**
If you find these tools being used to pathologize non-Western communication or dismiss indigenous knowledge transmission, **document it immediately**. That’s misuse and needs to be stopped.

-----

## Summary

**Primary principle:** Measure information geometry, not language patterns.

**Key innovation:** Culture-independent detection through mathematical invariants.

**Critical limitation:** Still needs validation across cultures - don’t assume it works everywhere.

**Ethical stance:** Better to miss manipulation than incorrectly flag cultural communication.

**Integration strategy:** Geometric first, linguistic only when appropriate, human review when uncertain.

-----

*“13.8 billion years of optimization testing beats 200 years of Western linguistic analysis.”*

*“But we still don’t know if we’ve captured all the patterns. Test rigorously. Question everything. Share failures as openly as successes.”*
