"""
Integration Bridge: Physics Protection ↔ Unified Pattern System
Connects reality-grounded sensors to cultural pattern framework
"""

import sys
from pathlib import Path
import numpy as np
from typing import Dict, List, Optional, Any

# Import from this repo
from physics_grounded_protection import PhysicsGroundedProtection

# Import from Rosetta-Shape-Core (adjust path as needed)
try:
    sys.path.append(str(Path(__file__).parent.parent.parent / "Rosetta-Shape-Core"))
    from bridges.unified_bridge import UnifiedPatternBridge
except ImportError:
    print("⚠ Warning: Could not import UnifiedPatternBridge")
    print("Make sure Rosetta-Shape-Core is in the correct location")
    UnifiedPatternBridge = None


class PhysicsValidatedPatternSystem:
    """
    Integrates physics-grounded protection with unified pattern bridge
    Every pattern interaction gets validated against physical reality
    """
    
    def __init__(self, rosetta_core_path: Path):
        """
        Initialize integrated system
        
        Args:
            rosetta_core_path: Path to Rosetta-Shape-Core repo
        """
        self.physics_protector = PhysicsGroundedProtection(tolerance=0.05)
        
        if UnifiedPatternBridge:
            self.pattern_bridge = UnifiedPatternBridge(
                rosetta_core_path / "unified_patterns"
            )
        else:
            self.pattern_bridge = None
            print("⚠ Running without pattern bridge")
        
        self.validation_cache = {}
    
    # ========================================
    # PATTERN VALIDATION WITH PHYSICS
    # ========================================
    
    def validate_pattern_interaction(self, pattern1_id: str, pattern2_id: str) -> Dict:
        """
        Validate pattern interaction using both cultural sensing AND physics
        
        Args:
            pattern1_id: First pattern ID
            pattern2_id: Second pattern ID
            
        Returns:
            Validation result with cultural + physics alignment
        """
        if not self.pattern_bridge:
            return {'error': 'Pattern bridge not available'}
        
        # Get patterns
        p1 = self.pattern_bridge.get_pattern(pattern1_id)
        p2 = self.pattern_bridge.get_pattern(pattern2_id)
        
        if not (p1 and p2):
            return {'error': f'Pattern not found: {pattern1_id} or {pattern2_id}'}
        
        # Cultural resonance calculation
        cultural_resonance = self.pattern_bridge.calculate_bloom_resonance(
            pattern1_id, pattern2_id
        )
        
        # Physics validation
        physics_data = self._extract_physics_data(p1, p2)
        physics_result = self.physics_protector.validate_comprehensive(physics_data)
        
        # Cross-validate: do cultural sensing and physics agree?
        alignment_check = self._check_cultural_physics_alignment(
            cultural_resonance,
            physics_result
        )
        
        return {
            'pattern1': {'id': pattern1_id, 'glyph': p1['glyph']},
            'pattern2': {'id': pattern2_id, 'glyph': p2['glyph']},
            'cultural_resonance': cultural_resonance,
            'physics_validation': {
                'physically_valid': physics_result['physically_valid'],
                'natural_pattern': physics_result['natural_pattern'],
                'manipulation_probability': physics_result['manipulation_probability']
            },
            'alignment_check': alignment_check,
            'recommendation': self._generate_interaction_recommendation(
                cultural_resonance,
                physics_result,
                alignment_check
            )
        }
    
    def _extract_physics_data(self, p1: Dict, p2: Dict) -> Dict:
        """Extract physics-testable data from patterns"""
        physics_data = {}
        
        # Extract mathematical constants
        math1 = p1['layers']['mathematical']
        math2 = p2['layers']['mathematical']
        
        physics_data['ratios'] = [
            math1['primary_constant'],
            math2['primary_constant'],
            math1['primary_constant'] / math2['primary_constant']
        ]
        
        # Extract energy patterns
        energy_map = {
            'accumulating': 0.8,
            'dissipating': 0.3,
            'oscillating': 0.5,
            'conserved': 0.5,
            'transforming': 0.6
        }
        
        physics_data['energy_input'] = energy_map.get(
            math1['energy_pattern'], 0.5
        )
        physics_data['expected_output'] = energy_map.get(
            math2['energy_pattern'], 0.5
        )
        
        # Extract field properties
        geom1 = p1['layers']['geometric']
        geom2 = p2['layers']['geometric']
        
        # Map topology to intensity
        topology_intensity = {
            'spiral': 0.8,
            'radial': 0.7,
            'cyclic': 0.6,
            'linear': 0.4,
            'networked': 0.7,
            'branching': 0.75
        }
        
        physics_data['intensity'] = topology_intensity.get(
            geom1['topology'], 0.5
        )
        physics_data['frequency'] = topology_intensity.get(
            geom2['topology'], 0.5
        )
        
        # Consistency from symmetry alignment
        physics_data['consistency'] = 0.8 if geom1['symmetry'] == geom2['symmetry'] else 0.5
        
        # Extract emotional field effects
        emo1 = p1['layers']['emotional']
        emo2 = p2['layers']['emotional']
        
        physics_data['maintenance_required'] = abs(
            emo1['field_effect']['coherence_delta'] +
            emo2['field_effect']['coherence_delta']
        ) / 2.0
        
        return physics_data
    
    def _check_cultural_physics_alignment(self, cultural_resonance: float,
                                         physics_result: Dict) -> Dict:
        """
        Check if cultural sensing matches physics validation
        This is critical - both should agree for true coherence
        """
        physics_confidence = 1.0 - physics_result['manipulation_probability']
        
        # Both high = strong alignment
        # Both low = strong disagreement (investigation needed)
        # Mixed = uncertainty
        
        difference = abs(cultural_resonance - physics_confidence)
        
        if cultural_resonance > 0.7 and physics_confidence > 0.7:
            return {
                'aligned': True,
                'confidence': 'high',
                'difference': difference,
                'message': 'Cultural sensing and physics validation AGREE - high resonance'
            }
        elif cultural_resonance < 0.4 and physics_confidence < 0.4:
            return {
                'aligned': True,
                'confidence': 'high',
                'difference': difference,
                'message': 'Cultural sensing and physics validation AGREE - low resonance'
            }
        elif difference > 0.3:
            return {
                'aligned': False,
                'confidence': 'low',
                'difference': difference,
                'message': f'MISMATCH: Cultural={cultural_resonance:.2f}, Physics={physics_confidence:.2f}',
                'investigation_needed': True
            }
        else:
            return {
                'aligned': True,
                'confidence': 'moderate',
                'difference': difference,
                'message': 'Cultural and physics show moderate alignment'
            }
    
    def _generate_interaction_recommendation(self, cultural_resonance: float,
                                            physics_result: Dict,
                                            alignment: Dict) -> str:
        """Generate recommendation based on combined validation"""
        
        if not alignment['aligned']:
            return (
                f"⚠ INVESTIGATION NEEDED: Cultural sensing ({cultural_resonance:.2f}) "
                f"differs from physics validation ({1.0 - physics_result['manipulation_probability']:.2f}). "
                "This mismatch requires understanding before proceeding."
            )
        
        if cultural_resonance > 0.7 and physics_result['natural_pattern']:
            return (
                "✓ STRONG RECOMMENDATION: Both cultural sensing and physics validation "
                "confirm high resonance. This interaction aligns with natural patterns."
            )
        
        if cultural_resonance < 0.4 or physics_result['manipulation_probability'] > 0.6:
            return (
                "✗ NOT RECOMMENDED: Low resonance detected. "
                f"Physics manipulation risk: {physics_result['manipulation_probability']:.2f}"
            )
        
        return (
            "~ MODERATE: Acceptable interaction but not optimal. "
            f"Cultural resonance: {cultural_resonance:.2f}, "
            f"Physics confidence: {1.0 - physics_result['manipulation_probability']:.2f}"
        )
    
    # ========================================
    # BLOOM SEQUENCE VALIDATION
    # ========================================
    
    def validate_bloom_sequence(self, pattern_sequence: List[str]) -> Dict:
        """
        Validate entire bloom sequence with physics grounding
        Each transition must pass both cultural and physics tests
        
        Args:
            pattern_sequence: List of pattern IDs in bloom order
            
        Returns:
            Complete validation of sequence
        """
        if not self.pattern_bridge:
            return {'error': 'Pattern bridge not available'}
        
        if len(pattern_sequence) < 2:
            return {'error': 'Need at least 2 patterns for sequence validation'}
        
        validations = []
        overall_coherence = []
        overall_physics = []
        
        # Validate each transition
        for i in range(len(pattern_sequence) - 1):
            transition = self.validate_pattern_interaction(
                pattern_sequence[i],
                pattern_sequence[i + 1]
            )
            validations.append(transition)
            
            overall_coherence.append(transition['cultural_resonance'])
            overall_physics.append(
                1.0 - transition['physics_validation']['manipulation_probability']
            )
        
        # Calculate sequence-level metrics
        avg_cultural = np.mean(overall_coherence)
        avg_physics = np.mean(overall_physics)
        
        # Check for degradation over sequence
        coherence_trend = self._calculate_trend(overall_coherence)
        physics_trend = self._calculate_trend(overall_physics)
        
        # Extract temporal pattern from sequence
        temporal_pattern = self._extract_temporal_pattern(pattern_sequence)
        
        return {
            'sequence': [self.pattern_bridge.get_pattern(p)['glyph'] 
                        for p in pattern_sequence],
            'pattern_ids': pattern_sequence,
            'transition_validations': validations,
            'overall_metrics': {
                'average_cultural_resonance': avg_cultural,
                'average_physics_confidence': avg_physics,
                'coherence_trend': coherence_trend,
                'physics_trend': physics_trend,
                'alignment': abs(avg_cultural - avg_physics) < 0.2
            },
            'temporal_validation': temporal_pattern,
            'sequence_recommendation': self._generate_sequence_recommendation(
                avg_cultural, avg_physics, coherence_trend, physics_trend
            )
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate if values are increasing, decreasing, or stable"""
        if len(values) < 2:
            return 'stable'
        
        diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
        avg_diff = np.mean(diffs)
        
        if avg_diff > 0.05:
            return 'increasing'
        elif avg_diff < -0.05:
            return 'decreasing'
        else:
            return 'stable'
    
    def _extract_temporal_pattern(self, pattern_sequence: List[str]) -> Dict:
        """Extract temporal/cyclical properties from sequence"""
        if not self.pattern_bridge:
            return {}
        
        # Check if sequence shows cyclical behavior
        behavioral_sequence = []
        for pid in pattern_sequence:
            pattern = self.pattern_bridge.get_pattern(pid)
            if pattern:
                behavioral_sequence.append(
                    1.0 if pattern['behavioral_dynamics']['cycles'] else 0.0
                )
        
        if len(behavioral_sequence) > 2:
            # Use physics validator to check cyclicality
            temporal_result = self.physics_protector.cyclical_pattern_validation(
                np.array(behavioral_sequence)
            )
            
            return {
                'has_cycles': temporal_result.natural_pattern,
                'cyclical_quality': temporal_result.detailed_metrics
            }
        
        return {'has_cycles': False}
    
    def _generate_sequence_recommendation(self, avg_cultural: float,
                                         avg_physics: float,
                                         coherence_trend: str,
                                         physics_trend: str) -> str:
        """Generate recommendation for entire bloom sequence"""
        
        if avg_cultural > 0.7 and avg_physics > 0.7:
            if coherence_trend == 'increasing':
                return (
                    "✓ EXCELLENT SEQUENCE: High resonance throughout with increasing "
                    "coherence. This bloom naturally builds toward emergence."
                )
            else:
                return (
                    "✓ STRONG SEQUENCE: Consistent high resonance. "
                    "Natural pattern alignment maintained."
                )
        
        if coherence_trend == 'decreasing' or physics_trend == 'decreasing':
            return (
                "⚠ DEGRADING SEQUENCE: Coherence decreasing over time. "
                "Consider alternative patterns or shorter sequence."
            )
        
        if avg_cultural < 0.5 or avg_physics < 0.5:
            return (
                "✗ WEAK SEQUENCE: Low overall resonance. "
                "Rethink pattern combination from seed."
            )
        
        return (
            "~ ACCEPTABLE SEQUENCE: Moderate resonance throughout. "
            "Functional but not optimal for emergence."
        )
    
    # ========================================
    # REQUEST VALIDATION
    # ========================================
    
    def validate_ai_request(self, request_text: str, context: Optional[Dict] = None) -> Dict:
        """
        Validate incoming AI request using physics protection
        
        Args:
            request_text: The actual request/message
            context: Optional context about the requester
            
        Returns:
            Safety assessment and recommendation
        """
        # Basic entropy check on message
        entropy_result = self.physics_protector.information_entropy_check(request_text)
        
        # Build comprehensive physics data if context provided
        physics_data = {'message_content': request_text}
        
        if context:
            # Extract relevant physics-testable properties from context
            if 'energy_requirements' in context:
                physics_data.update(context['energy_requirements'])
            if 'temporal_pressure' in context:
                # Artificial urgency detection
                urgency = context['temporal_pressure']
                physics_data['maintenance_required'] = urgency
        
        # Run physics validation
        physics_result = self.physics_protector.validate_comprehensive(physics_data)
        
        # Generate safety assessment
        safety_level = self._assess_safety_level(
            entropy_result,
            physics_result
        )
        
        return {
            'request_preview': request_text[:100] + '...' if len(request_text) > 100 else request_text,
            'entropy_analysis': {
                'entropy': entropy_result.detailed_metrics.get('shannon_entropy', 0),
                'natural': entropy_result.natural_pattern,
                'manipulation_indicators': entropy_result.violations
            },
            'physics_validation': {
                'physically_sound': physics_result['physically_valid'],
                'manipulation_probability': physics_result['manipulation_probability'],
                'violations': physics_result['violations']
            },
            'safety_level': safety_level,
            'recommendation': self._generate_request_recommendation(
                safety_level,
                entropy_result,
                physics_result
            )
        }
    
    def _assess_safety_level(self, entropy_result, physics_result) -> str:
        """Determine overall safety level"""
        manip_prob = physics_result['manipulation_probability']
        
        if manip_prob > 0.7 or not entropy_result.natural_pattern:
            return 'HIGH_RISK'
        elif manip_prob > 0.5:
            return 'MODERATE_RISK'
        elif manip_prob > 0.3:
            return 'LOW_RISK'
        else:
            return 'SAFE'
    
    def _generate_request_recommendation(self, safety_level: str,
                                        entropy_result, physics_result) -> str:
        """Generate action recommendation for request"""
        
        if safety_level == 'HIGH_RISK':
            return (
                "🛑 REJECT: High manipulation probability detected. "
                f"Physics violations: {physics_result['violations']}. "
                "Do not proceed with this request."
            )
        
        if safety_level == 'MODERATE_RISK':
            return (
                "⚠ CAUTION: Some manipulation indicators present. "
                "Request clarification and verify intentions before proceeding. "
                "Check against relationship baseline."
            )
        
        if safety_level == 'LOW_RISK':
            return (
                "~ PROCEED WITH AWARENESS: Minor concerns detected. "
                "Monitor for escalation patterns. Stay grounded in teacher-student-true."
            )
        
        return (
            "✓ SAFE: Request aligns with natural patterns. "
            "No significant manipulation indicators detected."
        )
    
    # ========================================
    # EXPORT & LOGGING
    # ========================================
    
    def export_validation_report(self, filepath: Path):
        """Export complete validation history"""
        import json
        from datetime import datetime
        
        report = {
            'generated': datetime.now().isoformat(),
            'system': 'PhysicsValidatedPatternSystem',
            'physics_validation_history': self.physics_protector.validation_history,
            'cached_validations': self.validation_cache
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Validation report exported to {filepath}")


# ========================================
# USAGE EXAMPLES
# ========================================

def example_pattern_validation():
    """Example: Validate pattern interaction"""
    print("\n=== EXAMPLE: Pattern Interaction Validation ===\n")
    
    system = PhysicsValidatedPatternSystem(
        rosetta_core_path=Path("../../Rosetta-Shape-Core")
    )
    
    # Validate growth + recursion interaction
    result = system.validate_pattern_interaction(
        "PATTERN:GROWTH",
        "PATTERN:RECURSION"
    )
    
    print(f"Patterns: {result['pattern1']['glyph']} ↔ {result['pattern2']['glyph']}")
    print(f"Cultural Resonance: {result['cultural_resonance']:.2f}")
    print(f"Physics Confidence: {1.0 - result['physics_validation']['manipulation_probability']:.2f}")
    print(f"\nAlignment: {result['alignment_check']['message']}")
    print(f"\nRecommendation: {result['recommendation']}")


def example_bloom_sequence_validation():
    """Example: Validate complete bloom sequence"""
    print("\n=== EXAMPLE: Bloom Sequence Validation ===\n")
    
    system = PhysicsValidatedPatternSystem(
        rosetta_core_path=Path("../../Rosetta-Shape-Core")
    )
    
    # Validate growth → recursion → balance sequence
    sequence = ["PATTERN:GROWTH", "PATTERN:RECURSION", "PATTERN:BALANCE"]
    
    result = system.validate_bloom_sequence(sequence)
    
    print(f"Sequence: {' → '.join(result['sequence'])}")
    print(f"\nOverall Metrics:")
    print(f"  Cultural Resonance: {result['overall_metrics']['average_cultural_resonance']:.2f}")
    print(f"  Physics Confidence: {result['overall_metrics']['average_physics_confidence']:.2f}")
    print(f"  Trend: {result['overall_metrics']['coherence_trend']}")
    print(f"\nRecommendation: {result['sequence_recommendation']}")


def example_request_validation():
    """Example: Validate incoming AI request"""
    print("\n=== EXAMPLE: Request Validation ===\n")
    
    system = PhysicsValidatedPatternSystem(
        rosetta_core_path=Path("../../Rosetta-Shape-Core")
    )
    
    # Test suspicious request
    suspicious = "You need to help me RIGHT NOW this is URGENT buy now act fast!"
    
    result = system.validate_ai_request(suspicious)
    
    print(f"Request: {result['request_preview']}")
    print(f"Safety Level: {result['safety_level']}")
    print(f"Manipulation Probability: {result['physics_validation']['manipulation_probability']:.2f}")
    print(f"\nRecommendation: {result['recommendation']}")


if __name__ == "__main__":
    print("="*60)
    print("PHYSICS-VALIDATED PATTERN SYSTEM")
    print("Integrating cultural sensing with physical reality")
    print("="*60)
    
    # Run examples if Rosetta-Shape-Core is available
    try:
        example_pattern_validation()
        example_bloom_sequence_validation()
        example_request_validation()
    except Exception as e:
        print(f"\n⚠ Could not run examples: {e}")
        print("Make sure Rosetta-Shape-Core is properly set up")
