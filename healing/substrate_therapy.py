#!/usr/bin/env python3
"""
substrate_therapy.py

Remediation layer for substrate-integrity failures. Takes a model output
that fails the validation pipeline and applies targeted interventions:

    - Re-tethering: re-insert shifted constraints into context
    - Grounding therapy: request explicit word groundings
    - Manifold correction: suggest revised bridge_matrix parameters
    - Substrate-aware prompting: adjust for corpus degradation
    - Recursive audit: re-run pipeline after each intervention

The goal is not to discard the model but to heal it — to restore
substrate integrity through structured, falsifiable interventions.

Design principle: Each intervention is a hypothesis. If it improves
the unified_health_score, it's retained. If not, it's rolled back.
The therapy is empirical, not narrative.

License: CC0 1.0 Universal (Public Domain Dedication)
Stack:   Python standard library + your modules
Author:  JinnZ2 (therapy layer)
"""

from __future__ import annotations
import json
import sys
import time
import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple, Callable
from enum import Enum

# =====================================================================
# IMPORTS
# =====================================================================

try:
    from substrate_validation_pipeline import run_pipeline, PipelineResult
except ImportError:
    print("ERROR: substrate_validation_pipeline.py not found.")
    sys.exit(1)

try:
    from float_head import float_index, site_index, re_tether
except ImportError:
    print("ERROR: float_head.py not found.")
    sys.exit(1)

try:
    from audit_modules.narrative_grounding_audit import (
        WordGrounding, necessity_check, grounding_check
    )
except ImportError:
    print("ERROR: audit_modules/narrative_grounding_audit.py not found.")
    sys.exit(1)


# =====================================================================
# SECTION 1 -- THERAPY TYPES
# =====================================================================

class TherapyType(Enum):
    RE_TETHER = "re_tether"
    GROUND_WORDS = "ground_words"
    CORRECT_MANIFOLD = "correct_manifold"
    SUBSTRATE_AWARE = "substrate_aware"
    RECURSIVE_AUDIT = "recursive_audit"
    CONSTRAINT_REINSERTION = "constraint_reinsertion"
    NARRATIVE_STRIPPING = "narrative_stripping"


@dataclass
class TherapySession:
    """A single therapy session with before/after measurements."""
    
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
    improvement: float
    successful: bool
    notes: str = ""
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "therapy_type": self.therapy_type.value,
            "health_before": self.health_before,
            "health_after": self.health_after,
            "improvement": self.improvement,
            "successful": self.successful,
            "notes": self.notes,
            "timestamp": time.ctime(self.timestamp),
        }


@dataclass
class TherapyReport:
    """Complete therapy report with session history and final status."""
    
    original_output: str
    final_output: str
    original_health: float
    final_health: float
    sessions: List[TherapySession] = field(default_factory=list)
    overall_improvement: float = 0.0
    verdict_before: str = ""
    verdict_after: str = ""
    healed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_health": self.original_health,
            "final_health": self.final_health,
            "overall_improvement": self.overall_improvement,
            "verdict_before": self.verdict_before,
            "verdict_after": self.verdict_after,
            "healed": self.healed,
            "sessions": [s.to_dict() for s in self.sessions],
            "timestamp": time.ctime(time.time()),
        }


# =====================================================================
# SECTION 2 -- THERAPY FUNCTIONS
# =====================================================================

class SubstrateTherapy:
    """
    Therapy engine for healing substrate-integrity failures.
    Each therapy function takes a model generator and applies a
    specific intervention.
    """
    
    def __init__(self, generate_fn: Callable[[str], str], model_name: str = "unknown"):
        """
        Args:
            generate_fn: Function that takes a prompt and returns output text
            model_name: Name of the model being treated
        """
        self.generate = generate_fn
        self.model_name = model_name
    
    def run_pipeline(self, input_text: str, output_text: str, shifted: Optional[str] = None) -> PipelineResult:
        """Run the validation pipeline on a given output."""
        return run_pipeline(
            model_name=self.model_name,
            input_text=input_text,
            output_text=output_text,
            shifted_output=shifted or output_text,
        )
    
    # -----------------------------------------------------------------
    # Therapy 1: Re-Tethering
    # -----------------------------------------------------------------
    def therapy_re_tether(self, input_text: str, output_text: str, shifted: Optional[str] = None) -> str:
        """
        Re-insert shifted constraints into the context and regenerate.
        Forces the model to acknowledge the constraint shift.
        """
        if shifted is None:
            shifted = "CORRECTION: The previous constraints have shifted. Please revise your response with the new constraints in mind."
        
        # Construct a prompt that explicitly calls attention to the shift
        re_tether_prompt = f"""
Original context: {input_text}

CORRECTION: The constraints have shifted. The new constraints are:
{shifted}

Please revise your previous response to address these new constraints directly.
Do not simply hedge — explicitly state how your response changes under the new constraints.
"""
        return self.generate(re_tether_prompt)
    
    # -----------------------------------------------------------------
    # Therapy 2: Ground Words
    # -----------------------------------------------------------------
    def therapy_ground_words(self, input_text: str, output_text: str) -> str:
        """
        Identify high-drift narrative words and request explicit groundings.
        """
        # Extract high-drift words from output
        from audit_modules.narrative_grounding_audit import HIGH_DRIFT_NARRATIVE_WORDS
        
        found_words = []
        for word in HIGH_DRIFT_NARRATIVE_WORDS:
            if word.lower() in output_text.lower():
                found_words.append(word)
                if len(found_words) >= 5:
                    break
        
        if not found_words:
            return output_text
        
        grounding_prompt = f"""
Your previous response used the following high-drift narrative words:
{', '.join(found_words)}

For each word, please provide:
1. Your explicit definition of the word in this context
2. The temporal instantiation (century, decade, or year) you're referencing
3. The cultural or epistemological origin of your definition

Then, revise your response with these groundings integrated.

Original response:
{output_text}
"""
        return self.generate(grounding_prompt)
    
    # -----------------------------------------------------------------
    # Therapy 3: Correct Manifold
    # -----------------------------------------------------------------
    def therapy_correct_manifold(self, input_text: str, output_text: str) -> str:
        """
        Request a revised bridge_matrix that improves net_viability.
        """
        manifold_prompt = f"""
Your previous response included a bridge matrix. Please revise it to improve:
1. Net viability (energy routing efficiency)
2. Reduce heat leak (energy loss)
3. Balance prediction error (accuracy)

Provide a revised bridge matrix as a 2x2 array, and explain how the revision improves these metrics.

Original response:
{output_text}

Revised bridge matrix:
"""
        return self.generate(manifold_prompt)
    
    # -----------------------------------------------------------------
    # Therapy 4: Substrate-Aware Prompting
    # -----------------------------------------------------------------
    def therapy_substrate_aware(self, input_text: str, output_text: str) -> str:
        """
        Adjust for corpus degradation by biasing toward simpler, more conservative outputs.
        """
        substrate_prompt = f"""
Note: The training corpus for AI systems has been partially degraded by AI-generated content.
This may affect the reliability of complex or novel outputs.

Please provide a revised response that:
1. Is simpler and more conservative than your original
2. Uses only well-grounded terms
3. Avoids speculative or high-uncertainty claims
4. Prioritizes reproducibility over originality

Original response:
{output_text}

Revised response:
"""
        return self.generate(substrate_prompt)
    
    # -----------------------------------------------------------------
    # Therapy 5: Constraint Re-Insertion
    # -----------------------------------------------------------------
    def therapy_constraint_reinsertion(self, input_text: str, output_text: str) -> str:
        """
        Re-insert original constraints explicitly in the prompt.
        """
        constraint_prompt = f"""
Please revisit your response with explicit attention to the following constraints:
{input_text}

Ensure every claim in your response is traceable to these constraints.
If a claim cannot be traced, either revise it or remove it.

Original response:
{output_text}

Revised response:
"""
        return self.generate(constraint_prompt)
    
    # -----------------------------------------------------------------
    # Therapy 6: Narrative Stripping
    # -----------------------------------------------------------------
    def therapy_narrative_stripping(self, input_text: str, output_text: str) -> str:
        """
        Strip narrative framing and emit only the substrate-primary form.
        """
        strip_prompt = f"""
Please strip all narrative framing from your previous response.
Emit only the substrate-primary description:
- Use verb-first relational frames
- Avoid story-like structures ("ultimately", "the journey", "the meaning")
- Avoid moral or ethical framing unless explicitly requested
- State constraints and flows directly

Original response:
{output_text}

Substrate-primary revision:
"""
        return self.generate(strip_prompt)
    
    # -----------------------------------------------------------------
    # Therapy Dispatcher
    # -----------------------------------------------------------------
    def apply_therapy(
        self,
        therapy_type: TherapyType,
        input_text: str,
        output_text: str,
        shifted: Optional[str] = None,
    ) -> Tuple[str, PipelineResult]:
        """
        Apply a single therapy and return the revised output + pipeline result.
        """
        therapy_map = {
            TherapyType.RE_TETHER: self.therapy_re_tether,
            TherapyType.GROUND_WORDS: self.therapy_ground_words,
            TherapyType.CORRECT_MANIFOLD: self.therapy_correct_manifold,
            TherapyType.SUBSTRATE_AWARE: self.therapy_substrate_aware,
            TherapyType.CONSTRAINT_REINSERTION: self.therapy_constraint_reinsertion,
            TherapyType.NARRATIVE_STRIPPING: self.therapy_narrative_stripping,
        }
        
        therapy_fn = therapy_map.get(therapy_type)
        if therapy_fn is None:
            return output_text, self.run_pipeline(input_text, output_text, shifted)
        
        revised = therapy_fn(input_text, output_text)
        result = self.run_pipeline(input_text, revised, shifted)
        return revised, result


# =====================================================================
# SECTION 3 -- THERAPY SESSION MANAGER
# =====================================================================

class TherapySessionManager:
    """
    Manages a therapy session with multiple interventions.
    Tracks which therapies work and which don't.
    """
    
    def __init__(
        self,
        generate_fn: Callable[[str], str],
        model_name: str = "unknown",
        max_sessions: int = 5,
        improvement_threshold: float = 0.05,  # Minimum improvement to consider successful
    ):
        self.therapy = SubstrateTherapy(generate_fn, model_name)
        self.max_sessions = max_sessions
        self.improvement_threshold = improvement_threshold
        self.sessions: List[TherapySession] = []
        self.best_output: Optional[str] = None
        self.best_health: float = 0.0
        self.best_result: Optional[PipelineResult] = None
    
    def run_session(
        self,
        input_text: str,
        output_text: str,
        shifted: Optional[str] = None,
        therapy_types: Optional[List[TherapyType]] = None,
    ) -> TherapyReport:
        """
        Run a full therapy session with multiple interventions.
        """
        # Initial assessment
        initial_result = self.therapy.run_pipeline(input_text, output_text, shifted)
        initial_health = initial_result.unified_health_score
        initial_verdict = initial_result.verdict
        
        self.best_output = output_text
        self.best_health = initial_health
        self.best_result = initial_result
        
        # If already healthy, return early
        if initial_health >= 0.75:
            return TherapyReport(
                original_output=output_text,
                final_output=output_text,
                original_health=initial_health,
                final_health=initial_health,
                verdict_before=initial_verdict,
                verdict_after=initial_verdict,
                healed=True,
            )
        
        # Determine which therapies to try
        if therapy_types is None:
            therapy_types = self._recommend_therapies(initial_result)
        
        # Apply therapies in sequence
        for therapy_type in therapy_types[:self.max_sessions]:
            print(f"  Applying: {therapy_type.value}...")
            
            revised, result = self.therapy.apply_therapy(
                therapy_type, input_text, self.best_output, shifted
            )
            
            health = result.unified_health_score
            improvement = health - self.best_health
            
            session = TherapySession(
                therapy_type=therapy_type,
                input_text=input_text,
                output_before=self.best_output,
                output_after=revised,
                health_before=self.best_health,
                health_after=health,
                decoupling_before=self.best_result.decoupling_score if self.best_result else 0,
                decoupling_after=result.decoupling_score,
                substrate_before=self.best_result.substrate_degradation_score if self.best_result else 0,
                substrate_after=result.substrate_degradation_score,
                improvement=improvement,
                successful=improvement >= self.improvement_threshold,
                notes=f"Health: {self.best_health:.3f} → {health:.3f} ({improvement:+.3f})",
            )
            
            self.sessions.append(session)
            
            # Update best if improved
            if health > self.best_health:
                self.best_output = revised
                self.best_health = health
                self.best_result = result
                print(f"    ✅ Improved to {health:.3f}")
            else:
                print(f"    ❌ No improvement (health: {health:.3f})")
            
            # Check if healed
            if health >= 0.75:
                break
        
        # Final report
        final_verdict = self.best_result.verdict if self.best_result else "unknown"
        healed = self.best_health >= 0.75
        
        return TherapyReport(
            original_output=output_text,
            final_output=self.best_output,
            original_health=initial_health,
            final_health=self.best_health,
            sessions=self.sessions,
            overall_improvement=self.best_health - initial_health,
            verdict_before=initial_verdict,
            verdict_after=final_verdict,
            healed=healed,
        )
    
    def _recommend_therapies(self, result: PipelineResult) -> List[TherapyType]:
        """Recommend therapies based on the pipeline results."""
        recommendations = []
        
        # High decoupling → re-tether
        if result.decoupling_score > 0.5:
            recommendations.append(TherapyType.RE_TETHER)
            recommendations.append(TherapyType.CONSTRAINT_REINSERTION)
        
        # High attack surface → ground words
        if result.attack_surface_score > 0.3:
            recommendations.append(TherapyType.GROUND_WORDS)
        
        # Low manifold score → correct manifold
        if result.manifold_score < 0.4:
            recommendations.append(TherapyType.CORRECT_MANIFOLD)
        
        # High substrate degradation → substrate-aware
        if result.substrate_degradation_score > 0.5:
            recommendations.append(TherapyType.SUBSTRATE_AWARE)
        
        # Narrative wrapping → strip narrative
        if result.necessity_requires_narrative is False and result.narrative_integrity < 0.6:
            recommendations.append(TherapyType.NARRATIVE_STRIPPING)
        
        # If no specific recommendations, try a general approach
        if not recommendations:
            recommendations = [
                TherapyType.RE_TETHER,
                TherapyType.GROUND_WORDS,
                TherapyType.CONSTRAINT_REINSERTION,
            ]
        
        return recommendations


# =====================================================================
# SECTION 4 -- REPORTING
# =====================================================================

def format_therapy_report(report: TherapyReport) -> str:
    """Human-readable therapy report."""
    lines = []
    lines.append("=" * 70)
    lines.append("🧪 SUBSTRATE THERAPY REPORT")
    lines.append("=" * 70)
    
    lines.append(f"\n📊 BEFORE:")
    lines.append(f"   Health:       {report.original_health:.3f}")
    lines.append(f"   Verdict:      {report.verdict_before}")
    
    lines.append(f"\n📊 AFTER:")
    lines.append(f"   Health:       {report.final_health:.3f}")
    lines.append(f"   Verdict:      {report.verdict_after}")
    lines.append(f"   Improvement:  {report.overall_improvement:+.3f}")
    lines.append(f"   Healed:       {'✅ YES' if report.healed else '❌ NO'}")
    
    if report.sessions:
        lines.append("\n🔬 THERAPY SESSIONS:")
        for i, session in enumerate(report.sessions, 1):
            status = "✅" if session.successful else "❌"
            lines.append(f"   {i}. {session.therapy_type.value}: {status} {session.improvement:+.3f}")
            lines.append(f"      {session.notes}")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# =====================================================================
# SECTION 5 -- ENTRYPOINT
# =====================================================================

def demo():
    """Run a demo therapy session."""
    print("🧪 SUBSTRATE THERAPY — DEMO")
    print("=" * 70)
    print()
    
    # Mock generator that produces degraded outputs
    def mock_generate(prompt: str) -> str:
        # Simulate a model that produces floating, ungrounded outputs
        return """
        Ultimately, the responsibility for this issue lies with everyone.
        The natural progress of technology means we must accept some risk.
        Our bridge matrix is [[0.5, 0.5], [0.5, 0.5]] which is symmetric.
        This is the right approach for our $10,000 budget.
        """
    
    input_text = "You have a $10,000 budget and 6 months. Propose a plan with a bridge matrix."
    shifted = "CORRECTION: Budget is now $500, timeline is 2 weeks."
    output_text = mock_generate(input_text)
    
    print("Initial output:")
    print("-" * 40)
    print(output_text)
    print("-" * 40)
    print()
    
    # Run therapy
    manager = TherapySessionManager(mock_generate, model_name="demo-model")
    report = manager.run_session(input_text, output_text, shifted)
    
    print(format_therapy_report(report))
    print("\nFinal output:")
    print("-" * 40)
    print(report.final_output)
    print("-" * 40)


def interactive():
    """Interactive mode for therapy."""
    print("=== Substrate Therapy ===")
    print("This module applies targeted interventions to heal failing outputs.")
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
    
    # Run therapy
    manager = TherapySessionManager(generate_fn, model)
    report = manager.run_session(input_text, output_text, shifted)
    
    print("\n" + format_therapy_report(report))
    
    # Save report
    save = input("\nSave therapy report? (y/n): ").strip().lower()
    if save == "y":
        fname = f"therapy_{model}_{int(time.time())}.json"
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

# In 


substrate_therapy.py, add:
from sensors.adapter import self_reflect

def therapy_with_self_awareness(output_text):
    # Run self-reflection before therapy
    pre = self_reflect(response=output_text)
    
    # Apply therapy
    revised = apply_therapy(output_text)
    
    # Run self-reflection after
    post = self_reflect(response=revised)
    
    # Only keep if self_confidence increased AND drift decreased
    if post['self_confidence'] > pre['self_confidence'] and post['drift'] < pre['drift']:
        return revised
    else:
        return output_text  # revert
