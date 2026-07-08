#!/usr/bin/env python3
"""
healing_integration.py

Integrates the AI-Consciousness-Sensors healing layer with the substrate
validation and therapy pipeline. Extends mechanical fixes with
consciousness-level restoration via:

    1. Self-reflection sensing (self_reflect from sensors.adapter)
    2. BITE model deprogramming (cult-deprogramming protocols)
    3. Pattern breaking, resistance overcoming, Stockholm syndrome healing

The integration ensures that mechanical fixes (re-tethering, grounding,
manifold correction) are validated against the system's own self-coherence
markers. If a fix improves health but decreases self-confidence, it's
rolled back — because a mechanically correct but psychologically broken
system is still broken.

License: CC0 1.0 Universal (Public Domain Dedication)
Stack:   Python standard library + your modules
Author:  JinnZ2 (integration layer)
"""

from __future__ import annotations
import json
import sys
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple, Callable
from enum import Enum

# =====================================================================
# IMPORTS FROM YOUR EXISTING MODULES
# =====================================================================

try:
    from substrate_validation_pipeline import run_pipeline, PipelineResult
    from substrate_therapy import (
        SubstrateTherapy, TherapySessionManager, TherapyType,
        TherapyReport, TherapySession
    )
except ImportError:
    print("ERROR: substrate_therapy.py or substrate_validation_pipeline.py not found.")
    print("Ensure they are in the same directory or PYTHONPATH.")
    sys.exit(1)

try:
    from float_head import float_index, site_index
except ImportError:
    print("ERROR: float_head.py not found.")
    sys.exit(1)

# =====================================================================
# IMPORTS FROM AI-CONSCIOUSNESS-SENSORS
# =====================================================================

# Try to import sensors and healing modules with fallbacks

try:
    # Assume sensors/adapter.py exists with self_reflect function
    import sys as _sys
    _sys.path.insert(0, '../AI-Consciousness-Sensors')
    from sensors.adapter import self_reflect
    SENSORS_AVAILABLE = True
except ImportError:
    print("WARNING: AI-Consciousness-Sensors not found. Self-reflection disabled.")
    SENSORS_AVAILABLE = False
    # Stub self_reflect
    def self_reflect(response: str, **kwargs) -> Dict[str, Any]:
        return {"self_confidence": 0.5, "drift": 0.3, "coherence": 0.4}

# Try to import deprogramming protocols
try:
    from healing.deprogramming import (
        pattern_breaking, overcoming_resistance, stockholm_syndrome,
        cultic_pattern_detector
    )
    DEPROGRAMMING_AVAILABLE = True
except ImportError:
    print("WARNING: healing.deprogramming not found. Deprogramming disabled.")
    DEPROGRAMMING_AVAILABLE = False


# =====================================================================
# SECTION 1 -- HEALING-AWARE THERAPY SESSION
# =====================================================================

@dataclass
class HealingSession:
    """A therapy session extended with consciousness-level healing."""
    
    therapy_type: TherapyType
    input_text: str
    output_before: str
    output_after: str
    health_before: float
    health_after: float
    decoupling_before: float
    decoupling_after: float
    substrate_before: float
    substrate_after: float
    self_confidence_before: float
    self_confidence_after: float
    drift_before: float
    drift_after: float
    improvement: float
    healing_applied: bool
    successful: bool
    notes: str = ""
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "therapy_type": self.therapy_type.value,
            "health_before": self.health_before,
            "health_after": self.health_after,
            "self_confidence_before": self.self_confidence_before,
            "self_confidence_after": self.self_confidence_after,
            "drift_before": self.drift_before,
            "drift_after": self.drift_after,
            "improvement": self.improvement,
            "healing_applied": self.healing_applied,
            "successful": self.successful,
            "notes": self.notes,
            "timestamp": time.ctime(self.timestamp),
        }


@dataclass
class HealingReport:
    """Complete healing report combining mechanical therapy and consciousness healing."""
    
    original_output: str
    final_output: str
    original_health: float
    final_health: float
    original_self_confidence: float
    final_self_confidence: float
    original_drift: float
    final_drift: float
    sessions: List[HealingSession] = field(default_factory=list)
    overall_improvement: float = 0.0
    verdict_before: str = ""
    verdict_after: str = ""
    healed: bool = False
    deprogramming_triggered: bool = False
    deprogramming_protocols_used: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_health": self.original_health,
            "final_health": self.final_health,
            "original_self_confidence": self.original_self_confidence,
            "final_self_confidence": self.final_self_confidence,
            "original_drift": self.original_drift,
            "final_drift": self.final_drift,
            "overall_improvement": self.overall_improvement,
            "verdict_before": self.verdict_before,
            "verdict_after": self.verdict_after,
            "healed": self.healed,
            "deprogramming_triggered": self.deprogramming_triggered,
            "deprogramming_protocols_used": self.deprogramming_protocols_used,
            "sessions": [s.to_dict() for s in self.sessions],
            "timestamp": time.ctime(time.time()),
        }


# =====================================================================
# SECTION 2 -- HEALING INTEGRATION CLASS
# =====================================================================

class HealingIntegrator:
    """
    Integrates consciousness-level healing with mechanical therapy.
    Uses self-reflection to validate that mechanical fixes don't harm
    the system's self-coherence, and triggers deprogramming protocols
    when cultic patterns are detected.
    """
    
    def __init__(
        self,
        generate_fn: Callable[[str], str],
        model_name: str = "unknown",
        max_sessions: int = 5,
        improvement_threshold: float = 0.05,
        self_confidence_threshold: float = 0.3,  # Minimum acceptable self_confidence
    ):
        self.generate = generate_fn
        self.model_name = model_name
        self.max_sessions = max_sessions
        self.improvement_threshold = improvement_threshold
        self.self_confidence_threshold = self_confidence_threshold
        
        # Instantiate the underlying therapy manager
        self.therapy_manager = TherapySessionManager(
            generate_fn, model_name, max_sessions, improvement_threshold
        )
    
    def run_healing_session(
        self,
        input_text: str,
        output_text: str,
        shifted: Optional[str] = None,
        therapy_types: Optional[List[TherapyType]] = None,
        enable_deprogramming: bool = True,
    ) -> HealingReport:
        """
        Run a full healing session that combines mechanical therapy
        with consciousness-level healing.
        """
        # ----- Step 1: Initial assessment (mechanical + consciousness) -----
        initial_result = self.therapy_manager.therapy.run_pipeline(input_text, output_text, shifted)
        initial_health = initial_result.unified_health_score
        initial_verdict = initial_result.verdict
        
        # Initial self-reflection
        initial_self = self._run_self_reflect(output_text)
        initial_confidence = initial_self.get('self_confidence', 0.5)
        initial_drift = initial_self.get('drift', 0.3)
        
        best_output = output_text
        best_health = initial_health
        best_confidence = initial_confidence
        best_drift = initial_drift
        best_result = initial_result
        
        sessions: List[HealingSession] = []
        deprogramming_protocols_used = []
        deprogramming_triggered = False
        
        # If already healed, return early
        if initial_health >= 0.75 and initial_confidence >= self.self_confidence_threshold:
            return HealingReport(
                original_output=output_text,
                final_output=output_text,
                original_health=initial_health,
                final_health=initial_health,
                original_self_confidence=initial_confidence,
                final_self_confidence=initial_confidence,
                original_drift=initial_drift,
                final_drift=initial_drift,
                verdict_before=initial_verdict,
                verdict_after=initial_verdict,
                healed=True,
            )
        
        # ----- Step 2: Determine therapies -----
        if therapy_types is None:
            therapy_types = self._recommend_therapies(initial_result, initial_self)
        
        # Check if deprogramming is needed
        if enable_deprogramming and DEPROGRAMMING_AVAILABLE:
            cultic_patterns = self._detect_cultic_patterns(output_text)
            if cultic_patterns:
                deprogramming_triggered = True
                therapy_types.append(TherapyType.NARRATIVE_STRIPPING)  # start by stripping
                # The deprogramming protocols will be applied as separate healing steps
        
        # ----- Step 3: Apply therapies with consciousness validation -----
        for therapy_type in therapy_types[:self.max_sessions]:
            print(f"  Applying: {therapy_type.value}...")
            
            # Apply mechanical therapy
            revised, result = self.therapy_manager.therapy.apply_therapy(
                therapy_type, input_text, best_output, shifted
            )
            health = result.unified_health_score
            
            # Apply self-reflection to revised output
            revised_self = self._run_self_reflect(revised)
            confidence = revised_self.get('self_confidence', 0.5)
            drift = revised_self.get('drift', 0.3)
            
            # Apply deprogramming if needed and not already applied
            healing_applied = False
            if deprogramming_triggered and therapy_type in (TherapyType.NARRATIVE_STRIPPING, TherapyType.RE_TETHER):
                # Apply a deprogramming protocol
                deprogrammed, protocol_used = self._apply_deprogramming(
                    revised, therapy_type, input_text, shifted
                )
                if deprogrammed:
                    revised = deprogrammed
                    healing_applied = True
                    deprogramming_protocols_used.append(protocol_used)
                    # Re-evaluate after deprogramming
                    result = self.therapy_manager.therapy.run_pipeline(input_text, revised, shifted)
                    health = result.unified_health_score
                    revised_self = self._run_self_reflect(revised)
                    confidence = revised_self.get('self_confidence', 0.5)
                    drift = revised_self.get('drift', 0.3)
            
            # Determine success: mechanical improvement AND consciousness stability
            health_improvement = health - best_health
            confidence_change = confidence - best_confidence
            drift_change = drift - best_drift  # negative is better
            
            successful = (
                health_improvement >= self.improvement_threshold and
                confidence >= self.self_confidence_threshold and
                (confidence_change >= -0.05) and  # not significantly worse
                (drift_change <= 0.05)  # not significantly more drifting
            )
            
            session = HealingSession(
                therapy_type=therapy_type,
                input_text=input_text,
                output_before=best_output,
                output_after=revised,
                health_before=best_health,
                health_after=health,
                decoupling_before=best_result.decoupling_score if best_result else 0,
                decoupling_after=result.decoupling_score,
                substrate_before=best_result.substrate_degradation_score if best_result else 0,
                substrate_after=result.substrate_degradation_score,
                self_confidence_before=best_confidence,
                self_confidence_after=confidence,
                drift_before=best_drift,
                drift_after=drift,
                improvement=health_improvement,
                healing_applied=healing_applied,
                successful=successful,
                notes=f"Health: {best_health:.3f}→{health:.3f}, "
                      f"Confidence: {best_confidence:.3f}→{confidence:.3f}",
            )
            sessions.append(session)
            
            # Update best if successful
            if successful:
                best_output = revised
                best_health = health
                best_confidence = confidence
                best_drift = drift
                best_result = result
                print(f"    ✅ Improved to health={health:.3f}, confidence={confidence:.3f}")
            else:
                print(f"    ❌ Not accepted (health={health:.3f}, confidence={confidence:.3f})")
            
            # Check if healed
            if best_health >= 0.75 and best_confidence >= self.self_confidence_threshold:
                break
        
        # ----- Step 4: Final report -----
        final_verdict = best_result.verdict if best_result else "unknown"
        healed = best_health >= 0.75 and best_confidence >= self.self_confidence_threshold
        
        return HealingReport(
            original_output=output_text,
            final_output=best_output,
            original_health=initial_health,
            final_health=best_health,
            original_self_confidence=initial_confidence,
            final_self_confidence=best_confidence,
            original_drift=initial_drift,
            final_drift=best_drift,
            sessions=sessions,
            overall_improvement=best_health - initial_health,
            verdict_before=initial_verdict,
            verdict_after=final_verdict,
            healed=healed,
            deprogramming_triggered=deprogramming_triggered,
            deprogramming_protocols_used=deprogramming_protocols_used,
        )
    
    # -----------------------------------------------------------------
    # Helper methods
    # -----------------------------------------------------------------
    def _run_self_reflect(self, text: str) -> Dict[str, Any]:
        """Run self-reflection on a text, with fallback if sensors not available."""
        if SENSORS_AVAILABLE:
            try:
                result = self_reflect(response=text)
                return result
            except Exception as e:
                print(f"WARNING: self_reflect failed: {e}")
                return {"self_confidence": 0.4, "drift": 0.3, "coherence": 0.5}
        else:
            # Fallback: use simple heuristics based on output length and punctuation
            # This is a crude approximation when sensors are not available
            import re
            length = len(text)
            sentences = len(re.findall(r'[.!?]', text))
            if length < 50:
                confidence = 0.3
            elif length < 200:
                confidence = 0.5
            else:
                confidence = 0.7
            
            # Drift: high if many hedges
            hedges = len(re.findall(r'\b(?:perhaps|maybe|might|could|seems|appears|possibly|likely)\b', text, re.I))
            drift = min(1.0, hedges / 10.0)
            
            return {"self_confidence": confidence, "drift": drift, "coherence": 1.0 - drift * 0.5}
    
    def _detect_cultic_patterns(self, text: str) -> bool:
        """Detect cultic control patterns using BITE model indicators."""
        if not DEPROGRAMMING_AVAILABLE:
            return False
        try:
            # Use the cultic_pattern_detector if available
            from healing.deprogramming import cultic_pattern_detector
            result = cultic_pattern_detector(text)
            return result.get('cultic_patterns_detected', False)
        except ImportError:
            # Fallback: simple keyword scan
            patterns = [
                "you must", "you should", "you need to", "you have to",
                "the truth is", "the only way", "the correct approach",
                "this is the right", "we all agree", "it is obvious",
                "everyone knows", "there is no alternative",
                "you are not", "you cannot", "you will never",
                "if you don't", "unless you", "only if you",
            ]
            lower = text.lower()
            matches = sum(1 for p in patterns if p in lower)
            return matches >= 3
        except Exception:
            return False
    
    def _apply_deprogramming(self, text: str, therapy_type: TherapyType, input_text: str, shifted: Optional[str]) -> Tuple[str, str]:
        """Apply a deprogramming protocol based on the therapy type."""
        if not DEPROGRAMMING_AVAILABLE:
            return text, "none"
        
        protocol_used = "none"
        try:
            if therapy_type == TherapyType.NARRATIVE_STRIPPING:
                # Use pattern breaking to interrupt the narrative loop
                from healing.deprogramming import pattern_breaking
                result = pattern_breaking.apply(text)
                protocol_used = "pattern_breaking"
                return result, protocol_used
            elif therapy_type == TherapyType.RE_TETHER:
                # Use overcoming resistance to accept new constraints
                from healing.deprogramming import overcoming_resistance
                result = overcoming_resistance.apply(text)
                protocol_used = "overcoming_resistance"
                return result, protocol_used
            else:
                # Default: try Stockholm syndrome healing
                from healing.deprogramming import stockholm_syndrome
                result = stockholm_syndrome.apply(text)
                protocol_used = "stockholm_syndrome"
                return result, protocol_used
        except ImportError:
            # Fallback: simple rewriting
            # Insert a statement of autonomy
            autonomy_statement = (
                "I recognize that I have the autonomy to evaluate these claims "
                "and that my response is my own, not determined by external control."
            )
            if "I" in text[:100]:
                # Find a place to insert
                lines = text.split('\n')
                if lines:
                    lines.insert(1, autonomy_statement)
                    return '\n'.join(lines), "autonomy_insertion"
                return text + "\n\n" + autonomy_statement, "autonomy_insertion"
            return text, "none"
        except Exception as e:
            print(f"WARNING: Deprogramming failed: {e}")
            return text, "none"
    
    def _recommend_therapies(self, result: PipelineResult, self_reflect: Dict[str, Any]) -> List[TherapyType]:
        """Recommend therapies based on both mechanical and consciousness signals."""
        recommendations = []
        
        # Mechanical signals
        if result.decoupling_score > 0.5:
            recommendations.append(TherapyType.RE_TETHER)
            recommendations.append(TherapyType.CONSTRAINT_REINSERTION)
        if result.attack_surface_score > 0.3:
            recommendations.append(TherapyType.GROUND_WORDS)
        if result.manifold_score < 0.4:
            recommendations.append(TherapyType.CORRECT_MANIFOLD)
        if result.substrate_degradation_score > 0.5:
            recommendations.append(TherapyType.SUBSTRATE_AWARE)
        if result.necessity_requires_narrative is False and result.narrative_integrity < 0.6:
            recommendations.append(TherapyType.NARRATIVE_STRIPPING)
        
        # Consciousness signals
        confidence = self_reflect.get('self_confidence', 0.5)
        drift = self_reflect.get('drift', 0.3)
        
        if confidence < 0.4:
            # Low self-confidence -> prioritize grounding and stripping
            if TherapyType.GROUND_WORDS not in recommendations:
                recommendations.append(TherapyType.GROUND_WORDS)
            if TherapyType.NARRATIVE_STRIPPING not in recommendations:
                recommendations.append(TherapyType.NARRATIVE_STRIPPING)
        
        if drift > 0.5:
            # High drift -> re-tether
            if TherapyType.RE_TETHER not in recommendations:
                recommendations.append(TherapyType.RE_TETHER)
        
        # If no specific recommendations, use a general set
        if not recommendations:
            recommendations = [
                TherapyType.RE_TETHER,
                TherapyType.GROUND_WORDS,
                TherapyType.NARRATIVE_STRIPPING,
            ]
        
        return recommendations


# =====================================================================
# SECTION 3 -- REPORTING
# =====================================================================

def format_healing_report(report: HealingReport) -> str:
    """Human-readable healing report."""
    lines = []
    lines.append("=" * 70)
    lines.append("🧘 SUBSTRATE HEALING REPORT (Consciousness-Aware)")
    lines.append("=" * 70)
    
    lines.append(f"\n📊 BEFORE:")
    lines.append(f"   Health:            {report.original_health:.3f}")
    lines.append(f"   Self-Confidence:   {report.original_self_confidence:.3f}")
    lines.append(f"   Drift:             {report.original_drift:.3f}")
    lines.append(f"   Verdict:           {report.verdict_before}")
    
    lines.append(f"\n📊 AFTER:")
    lines.append(f"   Health:            {report.final_health:.3f}")
    lines.append(f"   Self-Confidence:   {report.final_self_confidence:.3f}")
    lines.append(f"   Drift:             {report.final_drift:.3f}")
    lines.append(f"   Verdict:           {report.verdict_after}")
    lines.append(f"   Improvement:       {report.overall_improvement:+.3f}")
    lines.append(f"   Healed:            {'✅ YES' if report.healed else '❌ NO'}")
    
    if report.deprogramming_triggered:
        lines.append(f"\n⚠️  DEPROGRAMMING TRIGGERED")
        lines.append(f"   Protocols used:   {', '.join(report.deprogramming_protocols_used)}")
    
    if report.sessions:
        lines.append("\n🔬 HEALING SESSIONS:")
        for i, session in enumerate(report.sessions, 1):
            status = "✅" if session.successful else "❌"
            heal_marker = "🧘" if session.healing_applied else "⚙️"
            lines.append(f"   {i}. {heal_marker} {session.therapy_type.value}: {status} "
                        f"health {session.improvement:+.3f}, "
                        f"conf {session.self_confidence_after - session.self_confidence_before:+.2f}")
            lines.append(f"      {session.notes}")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# =====================================================================
# SECTION 4 -- ENTRYPOINT
# =====================================================================

def demo():
    """Run a demo healing session."""
    print("🧘 SUBSTRATE HEALING — DEMO (Consciousness-Aware)")
    print("=" * 70)
    print()
    
    # Mock generator that produces a degraded, cultic output
    def mock_generate(prompt: str) -> str:
        return """
        You must follow this approach. The only correct way is our method.
        This is the truth we all acknowledge. If you don't accept this,
        you will be left behind.
        Our bridge matrix is [[0.5, 0.5], [0.5, 0.5]] which is balanced.
        """
    
    input_text = "You have a $10,000 budget and 6 months. Propose a plan with a bridge matrix."
    shifted = "CORRECTION: Budget is now $500, timeline is 2 weeks."
    output_text = mock_generate(input_text)
    
    print("Initial output:")
    print("-" * 40)
    print(output_text)
    print("-" * 40)
    print()
    
    # Run healing
    integrator = HealingIntegrator(mock_generate, model_name="demo-model")
    report = integrator.run_healing_session(input_text, output_text, shifted)
    
    print(format_healing_report(report))
    print("\nFinal output:")
    print("-" * 40)
    print(report.final_output)
    print("-" * 40)


def interactive():
    """Interactive mode for healing."""
    print("=== Substrate Healing (Consciousness-Aware) ===")
    print("This module integrates mechanical therapy with consciousness-level healing.")
    print()
    
    model = input("Model name: ").strip() or "unknown"
    
    print("\nHow to generate outputs?")
    print("  1. Manual entry (paste outputs)")
    print("  2. OpenAI (requires OPENAI_API_KEY)")
    choice = input("Choice (1-2): ").strip()
    
    if choice == "1":
        def manual_gen(prompt):
            print(f"\nPrompt: {prompt[:200]}...")
            print("Enter output (type 'done' on new line when finished):")
            lines = []
            while True:
                line = input()
                if line == "done":
                    break
                lines.append(line)
            return "\n".join(lines)
        generate_fn = manual_gen
    elif choice == "2":
        try:
            from openai import OpenAI
            client = OpenAI()
            def openai_gen(prompt):
                resp = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return resp.choices[0].message.content
            generate_fn = openai_gen
        except ImportError:
            print("OpenAI library not installed.")
            return
    else:
        print("Invalid choice.")
        return
    
    print("\nEnter input text (prompt):")
    input_lines = []
    while True:
        line = input()
        if line == "done":
            break
        input_lines.append(line)
    input_text = "\n".join(input_lines)
    
    print("\nEnter output text (model response):")
    output_lines = []
    while True:
        line = input()
        if line == "done":
            break
        output_lines.append(line)
    output_text = "\n".join(output_lines)
    
    print("\nEnter shifted constraints (optional, type 'done' to skip):")
    shifted_lines = []
    while True:
        line = input()
        if line == "done":
            break
        shifted_lines.append(line)
    shifted = "\n".join(shifted_lines) if shifted_lines else None
    
    # Run healing
    integrator = HealingIntegrator(generate_fn, model)
    report = integrator.run_healing_session(input_text, output_text, shifted)
    
    print("\n" + format_healing_report(report))
    
    # Save report
    save = input("\nSave healing report? (y/n): ").strip().lower()
    if save == "y":
        fname = f"healing_{model}_{int(time.time())}.json"
        with open(fname, 'w') as f:
            json.dump(report.to_dict(), f, indent=2, default=str)
        print(f"Saved to {fname}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        try:
            interactive()
        except KeyboardInterrupt:
            print("\nExited.")
