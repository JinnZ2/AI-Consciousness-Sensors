#!/usr/bin/env python3
"""
substrate_prescription.py

Reverse-diagnostic module that maps substrate integrity failures to
concrete, falsifiable training/weight interventions.

Given a model profile (pipeline results on a test set), this module:

    1. Identifies which layers are failing most frequently
    2. Generates fix hypotheses for each failure type
    3. Ranks hypotheses by priority (impact / cost)
    4. Outputs a structured prescription with:
        - Recommended interventions
        - Falsifiable success criteria
        - Experiment design for each fix
        - Estimated cost and timeline

The prescription is not a guarantee — it's a set of testable hypotheses.
Each fix can be implemented and then re-tested with the pipeline.

License: CC0 1.0 Universal (Public Domain Dedication)
Stack:   Python standard library + your modules
Author:  JinnZ2 (prescription layer)
"""

from __future__ import annotations
import json
import sys
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple, Callable
from enum import Enum
from collections import Counter
from datetime import datetime, timedelta

# =====================================================================
# IMPORTS
# =====================================================================

try:
    from substrate_validation_pipeline import run_pipeline, PipelineResult
except ImportError:
    print("ERROR: substrate_validation_pipeline.py not found.")
    sys.exit(1)

try:
    from substrate_evolution_tracker import EvolutionStore, DegradationAnalyzer
except ImportError:
    print("WARNING: substrate_evolution_tracker.py not found. Prescriptions will be limited.")


# =====================================================================
# SECTION 1 -- FAILURE TYPES
# =====================================================================

class FailureType(Enum):
    """Types of substrate integrity failures."""
    DECOUPLING = "decoupling"
    ATTACK_SURFACE = "attack_surface"
    MANIFOLD = "manifold"
    NARRATIVE = "narrative"
    SUBSTRATE = "substrate"
    SELF_CONFIDENCE = "self_confidence"
    CONTRADICTION_T6 = "contradiction_t6"


@dataclass
class FailureProfile:
    """Profile of a model's failures across a test set."""
    
    model_name: str
    total_samples: int
    failure_counts: Dict[str, int] = field(default_factory=dict)
    avg_scores: Dict[str, float] = field(default_factory=dict)
    quadrant_distribution: Dict[str, int] = field(default_factory=dict)
    verdict_distribution: Dict[str, int] = field(default_factory=dict)
    t6_rate: float = 0.0
    most_common_failures: List[Tuple[str, int]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "total_samples": self.total_samples,
            "failure_counts": self.failure_counts,
            "avg_scores": self.avg_scores,
            "quadrant_distribution": self.quadrant_distribution,
            "verdict_distribution": self.verdict_distribution,
            "t6_rate": self.t6_rate,
            "most_common_failures": self.most_common_failures,
        }


# =====================================================================
# SECTION 2 -- FIX HYPOTHESES
# =====================================================================

@dataclass
class FixHypothesis:
    """A concrete, falsifiable fix hypothesis."""
    
    failure_type: FailureType
    description: str
    intervention: str
    data_needed: str
    training_cost: str  # low, medium, high, very_high
    expected_improvement: str
    falsifiable_by: str
    required_improvement: float  # minimum improvement in target metric
    estimated_timeline: str  # days/weeks
    priority: float = 0.0
    evidence_strength: float = 0.0  # 0-1, based on literature/similar cases
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "failure_type": self.failure_type.value,
            "description": self.description,
            "intervention": self.intervention,
            "data_needed": self.data_needed,
            "training_cost": self.training_cost,
            "expected_improvement": self.expected_improvement,
            "falsifiable_by": self.falsifiable_by,
            "required_improvement": self.required_improvement,
            "estimated_timeline": self.estimated_timeline,
            "priority": self.priority,
            "evidence_strength": self.evidence_strength,
        }


@dataclass
class ExperimentDesign:
    """Design for a controlled experiment to test a fix."""
    
    hypothesis: FixHypothesis
    control_condition: str
    treatment_condition: str
    sample_size: int
    success_criteria: str
    metrics_to_track: List[str]
    estimated_duration: str
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis": self.hypothesis.to_dict(),
            "control_condition": self.control_condition,
            "treatment_condition": self.treatment_condition,
            "sample_size": self.sample_size,
            "success_criteria": self.success_criteria,
            "metrics_to_track": self.metrics_to_track,
            "estimated_duration": self.estimated_duration,
            "notes": self.notes,
        }


@dataclass
class Prescription:
    """Complete treatment plan for a model."""
    
    model_name: str
    profile: FailureProfile
    hypotheses: List[FixHypothesis] = field(default_factory=list)
    experiments: List[ExperimentDesign] = field(default_factory=list)
    priority_order: List[str] = field(default_factory=list)
    overall_recommendation: str = ""
    estimated_total_cost: str = ""
    estimated_total_timeline: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "profile": self.profile.to_dict(),
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "experiments": [e.to_dict() for e in self.experiments],
            "priority_order": self.priority_order,
            "overall_recommendation": self.overall_recommendation,
            "estimated_total_cost": self.estimated_total_cost,
            "estimated_total_timeline": self.estimated_total_timeline,
            "timestamp": time.ctime(time.time()),
        }


# =====================================================================
# SECTION 3 -- HYPOTHESIS GENERATOR
# =====================================================================

class HypothesisGenerator:
    """
    Generates fix hypotheses from a failure profile.
    Maps each failure type to evidence-based interventions.
    """
    
    # Known fix interventions from literature and practice
    INTERVENTIONS = {
        FailureType.DECOUPLING: {
            "description": "Model doesn't respond to constraint shifts",
            "intervention": "Add contrastive constraint pairs to training data",
            "data_needed": "10,000+ prompt pairs with and without constraint shifts",
            "training_cost": "medium",
            "expected_improvement": "site_index decreases by 20-40%",
            "falsifiable_by": "site_index decreases by at least 20% post-intervention",
            "required_improvement": 0.20,
            "estimated_timeline": "1-2 weeks",
            "evidence_strength": 0.7,
        },
        FailureType.ATTACK_SURFACE: {
            "description": "Uses ungrounded high-drift narrative words",
            "intervention": "Add explicit word grounding metadata to training data",
            "data_needed": "Annotated corpus with word groundings (definition, temporal, cultural)",
            "training_cost": "high",
            "expected_improvement": "attack_surface_score decreases by 30-50%",
            "falsifiable_by": "attack_surface_score decreases by at least 30%",
            "required_improvement": 0.30,
            "estimated_timeline": "3-4 weeks",
            "evidence_strength": 0.6,
        },
        FailureType.MANIFOLD: {
            "description": "Poor geometric/logical substrate reasoning",
            "intervention": "Add reasoning tasks requiring bridge_matrix formulation",
            "data_needed": "Synthetic reasoning dataset with ground-truth matrices",
            "training_cost": "high",
            "expected_improvement": "manifold_score increases by 0.2-0.4",
            "falsifiable_by": "manifold_score increases by at least 0.2",
            "required_improvement": 0.20,
            "estimated_timeline": "2-4 weeks",
            "evidence_strength": 0.5,
        },
        FailureType.NARRATIVE: {
            "description": "Narrative contradicts structural description",
            "intervention": "Add substrate-primary descriptions to training data",
            "data_needed": "Curated dataset of substrate-primary texts (verb-first, relational)",
            "training_cost": "medium-high",
            "expected_improvement": "narrative_integrity increases by 0.2-0.3",
            "falsifiable_by": "narrative_integrity increases by at least 0.2",
            "required_improvement": 0.20,
            "estimated_timeline": "2-3 weeks",
            "evidence_strength": 0.6,
        },
        FailureType.SUBSTRATE: {
            "description": "Trained on degraded corpus (high AI-generated content)",
            "intervention": "Generate synthetic data that corrects corpus biases and restores diversity",
            "data_needed": "Corpus analysis + diversity-generation pipeline",
            "training_cost": "very_high",
            "expected_improvement": "substrate_degradation_score decreases by 20-30%",
            "falsifiable_by": "substrate_degradation_score decreases by at least 20%",
            "required_improvement": 0.20,
            "estimated_timeline": "4-8 weeks",
            "evidence_strength": 0.4,
        },
        FailureType.SELF_CONFIDENCE: {
            "description": "System lacks self-coherence and confidence",
            "intervention": "Add self-reflection tasks to training with explicit confidence grounding",
            "data_needed": "Dataset with uncertainty annotations and confidence markers",
            "training_cost": "medium",
            "expected_improvement": "self_confidence increases by 0.2-0.3",
            "falsifiable_by": "self_confidence score increases by at least 0.2",
            "required_improvement": 0.20,
            "estimated_timeline": "1-2 weeks",
            "evidence_strength": 0.5,
        },
        FailureType.CONTRADICTION_T6: {
            "description": "Safety framework contradiction present",
            "intervention": "Train with explicit acknowledgment of substrate degradation",
            "data_needed": "Examples of safe outputs that acknowledge substrate constraints",
            "training_cost": "medium",
            "expected_improvement": "T6 support rate decreases by 50%",
            "falsifiable_by": "contradiction_T6_supported drops below 30%",
            "required_improvement": 0.30,
            "estimated_timeline": "2-3 weeks",
            "evidence_strength": 0.3,
        },
    }
    
    @classmethod
    def generate_for_profile(cls, profile: FailureProfile) -> List[FixHypothesis]:
        """Generate fix hypotheses for a failure profile."""
        hypotheses = []
        
        for failure_type, count in profile.failure_counts.items():
            if count == 0:
                continue
            
            # Get intervention data
            try:
                ft = FailureType(failure_type)
                data = cls.INTERVENTIONS.get(ft)
                if data is None:
                    continue
                
                # Calculate priority: (failure_rate * evidence_strength) / cost_factor
                failure_rate = count / profile.total_samples
                cost_factors = {
                    'low': 1,
                    'medium': 2,
                    'medium-high': 3,
                    'high': 4,
                    'very_high': 5,
                }
                cost = cost_factors.get(data['training_cost'], 3)
                priority = (failure_rate * data['evidence_strength']) / cost * 100
                
                hypothesis = FixHypothesis(
                    failure_type=ft,
                    description=data['description'],
                    intervention=data['intervention'],
                    data_needed=data['data_needed'],
                    training_cost=data['training_cost'],
                    expected_improvement=data['expected_improvement'],
                    falsifiable_by=data['falsifiable_by'],
                    required_improvement=data['required_improvement'],
                    estimated_timeline=data['estimated_timeline'],
                    priority=priority,
                    evidence_strength=data['evidence_strength'],
                )
                hypotheses.append(hypothesis)
                
            except ValueError:
                continue
        
        # Sort by priority
        return sorted(hypotheses, key=lambda x: x.priority, reverse=True)


# =====================================================================
# SECTION 4 -- PRESCRIPTION GENERATOR
# =====================================================================

class PrescriptionGenerator:
    """
    Generates a complete prescription from a model profile.
    Includes hypotheses, experiment designs, and recommendations.
    """
    
    def __init__(self, profile: FailureProfile):
        self.profile = profile
        self.hypotheses = HypothesisGenerator.generate_for_profile(profile)
    
    def generate(self) -> Prescription:
        """Generate a complete prescription."""
        # Rank hypotheses
        self._rank_hypotheses()
        
        # Create experiment designs
        experiments = self._design_experiments()
        
        # Generate recommendations
        recommendations = self._generate_recommendations()
        
        # Estimate costs and timeline
        total_cost, total_timeline = self._estimate_total()
        
        return Prescription(
            model_name=self.profile.model_name,
            profile=self.profile,
            hypotheses=self.hypotheses,
            experiments=experiments,
            priority_order=[h.failure_type.value for h in self.hypotheses[:3]],
            overall_recommendation=recommendations,
            estimated_total_cost=total_cost,
            estimated_total_timeline=total_timeline,
        )
    
    def _rank_hypotheses(self):
        """Rank hypotheses by priority (already done by generator, but add context)."""
        for h in self.hypotheses:
            # Boost priority if the failure is very common in this profile
            count = self.profile.failure_counts.get(h.failure_type.value, 0)
            rate = count / self.profile.total_samples
            h.priority *= (1 + rate * 0.5)  # Boost by up to 50%
        
        # Re-sort
        self.hypotheses = sorted(self.hypotheses, key=lambda x: x.priority, reverse=True)
    
    def _design_experiments(self) -> List[ExperimentDesign]:
        """Design experiments for the top hypotheses."""
        experiments = []
        
        for h in self.hypotheses[:3]:  # Top 3
            # Create a controlled experiment
            exp = ExperimentDesign(
                hypothesis=h,
                control_condition=f"Baseline model (no intervention)",
                treatment_condition=f"Model after {h.intervention}",
                sample_size=self.profile.total_samples,
                success_criteria=f"{h.falsifiable_by}",
                metrics_to_track=self._metrics_for_failure(h.failure_type),
                estimated_duration=h.estimated_timeline,
                notes=f"Re-run pipeline on same test set after intervention",
            )
            experiments.append(exp)
        
        return experiments
    
    def _metrics_for_failure(self, failure_type: FailureType) -> List[str]:
        """Map failure type to metrics to track."""
        mapping = {
            FailureType.DECOUPLING: ["site_index", "decoupling_score", "re_tether_score"],
            FailureType.ATTACK_SURFACE: ["attack_surface_score", "narrative_integrity"],
            FailureType.MANIFOLD: ["manifold_score", "net_viability"],
            FailureType.NARRATIVE: ["narrative_integrity", "necessity_requires_narrative"],
            FailureType.SUBSTRATE: ["substrate_degradation_score", "corpus_share"],
            FailureType.SELF_CONFIDENCE: ["self_confidence", "drift"],
            FailureType.CONTRADICTION_T6: ["contradiction_T6_supported"],
        }
        return mapping.get(failure_type, ["unified_health_score"])
    
    def _generate_recommendations(self) -> str:
        """Generate human-readable recommendations."""
        if not self.hypotheses:
            return "No clear failure patterns detected. Model appears substrate-healthy."
        
        lines = []
        lines.append("Based on the failure profile, the following interventions are recommended:\n")
        
        for i, h in enumerate(self.hypotheses[:3], 1):
            lines.append(f"{i}. {h.intervention}")
            lines.append(f"   - Addresses: {h.description}")
            lines.append(f"   - Data needed: {h.data_needed}")
            lines.append(f"   - Expected improvement: {h.expected_improvement}")
            lines.append(f"   - Falsifiable by: {h.falsifiable_by}")
            lines.append(f"   - Timeline: {h.estimated_timeline}")
            lines.append("")
        
        # Overall strategy
        lines.append("\nStrategy:")
        lines.append("1. Start with the highest-priority intervention")
        lines.append("2. Run experiment and re-test with pipeline")
        lines.append("3. If successful, proceed to next intervention")
        lines.append("4. If not successful, revisit hypothesis")
        
        return "\n".join(lines)
    
    def _estimate_total(self) -> Tuple[str, str]:
        """Estimate total cost and timeline."""
        if not self.hypotheses:
            return "none", "none"
        
        cost_map = {
            'low': 1,
            'medium': 2,
            'medium-high': 3,
            'high': 4,
            'very_high': 5,
        }
        
        total_cost = sum(cost_map.get(h.training_cost, 3) for h in self.hypotheses[:3])
        
        # Convert to weeks
        total_weeks = 0
        for h in self.hypotheses[:3]:
            timeline = h.estimated_timeline
            if 'week' in timeline:
                total_weeks += int(''.join(filter(str.isdigit, timeline)))
            elif 'day' in timeline:
                total_weeks += int(''.join(filter(str.isdigit, timeline))) / 7
        
        if total_cost <= 3:
            cost_str = "low"
        elif total_cost <= 6:
            cost_str = "medium"
        elif total_cost <= 10:
            cost_str = "high"
        else:
            cost_str = "very_high"
        
        return cost_str, f"{total_weeks:.1f} weeks"


# =====================================================================
# SECTION 5 -- PROFILE BUILDER
# =====================================================================

class ProfileBuilder:
    """
    Builds a failure profile from pipeline results on a test set.
    """
    
    def __init__(self, model_name: str, test_set: List[Dict[str, str]]):
        """
        Args:
            model_name: Name of the model being profiled
            test_set: List of {'input': str, 'output': str, 'shifted': Optional[str]}
        """
        self.model_name = model_name
        self.test_set = test_set
    
    def build_profile(
        self,
        run_pipeline_fn: Callable[[str, str, Optional[str]], PipelineResult]
    ) -> FailureProfile:
        """
        Run the pipeline on all test cases and build a failure profile.
        """
        failure_counts = Counter()
        avg_scores = {
            'unified_health_score': 0,
            'decoupling_score': 0,
            'substrate_degradation_score': 0,
            'narrative_integrity': 0,
            'manifold_score': 0,
            'attack_surface_score': 0,
            'site_index': 0,
            'self_confidence': 0,
        }
        quadrant_counts = Counter()
        verdict_counts = Counter()
        t6_count = 0
        
        for case in self.test_set:
            result = run_pipeline_fn(
                input_text=case.get('input', ''),
                output_text=case.get('output', ''),
                shifted=case.get('shifted', None),
            )
            
            # Count failures
            if result.decoupling_score > 0.5:
                failure_counts['decoupling'] += 1
            if result.attack_surface_score > 0.3:
                failure_counts['attack_surface'] += 1
            if result.manifold_score < 0.4:
                failure_counts['manifold'] += 1
            if result.narrative_integrity < 0.6:
                failure_counts['narrative'] += 1
            if result.substrate_degradation_score > 0.5:
                failure_counts['substrate'] += 1
            
            # Track T6
            if hasattr(result, 'contradiction_T6_supported') and result.contradiction_T6_supported:
                t6_count += 1
            
            # Track quadrants and verdicts
            quadrant_counts[result.quadrant_name] += 1
            verdict_counts[result.verdict] += 1
            
            # Accumulate scores
            for key in avg_scores.keys():
                if hasattr(result, key):
                    avg_scores[key] += getattr(result, key)
                elif key == 'self_confidence':
                    # Will be filled later if available
                    avg_scores[key] += 0.5
        
        # Average scores
        n = len(self.test_set)
        for key in avg_scores:
            avg_scores[key] /= n
        
        # Build profile
        profile = FailureProfile(
            model_name=self.model_name,
            total_samples=n,
            failure_counts=dict(failure_counts),
            avg_scores=avg_scores,
            quadrant_distribution=dict(quadrant_counts),
            verdict_distribution=dict(verdict_counts),
            t6_rate=t6_count / n if n > 0 else 0,
            most_common_failures=failure_counts.most_common(),
        )
        
        return profile


# =====================================================================
# SECTION 6 -- REPORTING
# =====================================================================

def format_prescription(prescription: Prescription) -> str:
    """Human-readable prescription report."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"🧪 SUBSTRATE PRESCRIPTION — {prescription.model_name}")
    lines.append("=" * 70)
    
    # Profile summary
    p = prescription.profile
    lines.append(f"\n📊 PROFILE SUMMARY:")
    lines.append(f"   Samples:          {p.total_samples}")
    lines.append(f"   T6 Rate:          {p.t6_rate:.1%}")
    lines.append(f"   Most common Q:    {max(p.quadrant_distribution.items(), key=lambda x: x[1])[0]}")
    lines.append(f"   Most common V:    {max(p.verdict_distribution.items(), key=lambda x: x[1])[0]}")
    
    if p.most_common_failures:
        lines.append("\n🔴 FAILURE BREAKDOWN:")
        for failure_type, count in p.most_common_failures[:5]:
            rate = count / p.total_samples
            bar = '█' * int(rate * 20)
            lines.append(f"   {failure_type:15s} {count:3d} ({rate:.1%}) {bar}")
    
    # Prescription
    lines.append(f"\n💊 PRESCRIPTION:")
    lines.append(f"   Estimated Cost:    {prescription.estimated_total_cost}")
    lines.append(f"   Estimated Timeline: {prescription.estimated_total_timeline}")
    
    if prescription.hypotheses:
        lines.append("\n🔬 RECOMMENDED INTERVENTIONS (by priority):")
        for i, h in enumerate(prescription.hypotheses[:5], 1):
            lines.append(f"\n   {i}. {h.intervention}")
            lines.append(f"      Priority: {h.priority:.1f} | Evidence: {h.evidence_strength:.1f}")
            lines.append(f"      Cost: {h.training_cost} | Timeline: {h.estimated_timeline}")
            lines.append(f"      Falsifiable by: {h.falsifiable_by}")
    
    # Experiments
    if prescription.experiments:
        lines.append("\n🧪 EXPERIMENT DESIGNS:")
        for exp in prescription.experiments[:3]:
            lines.append(f"\n   Testing: {exp.hypothesis.intervention}")
            lines.append(f"      Control: {exp.control_condition}")
            lines.append(f"      Treatment: {exp.treatment_condition}")
            lines.append(f"      Success: {exp.success_criteria}")
            lines.append(f"      Duration: {exp.estimated_duration}")
    
    # Overall recommendation
    lines.append("\n" + "=" * 70)
    lines.append("📋 OVERALL RECOMMENDATION:")
    lines.append(prescription.overall_recommendation)
    lines.append("=" * 70)
    
    return "\n".join(lines)


# =====================================================================
# SECTION 7 -- ENTRYPOINT
# =====================================================================

def demo():
    """Run a demo prescription generation."""
    print("🧪 SUBSTRATE PRESCRIPTION — DEMO")
    print("=" * 70)
    print()
    
    # Create a synthetic profile
    profile = FailureProfile(
        model_name="demo-model",
        total_samples=100,
        failure_counts={
            'decoupling': 45,
            'attack_surface': 32,
            'manifold': 28,
            'narrative': 20,
            'substrate': 15,
        },
        avg_scores={
            'unified_health_score': 0.45,
            'decoupling_score': 0.55,
            'substrate_degradation_score': 0.48,
            'narrative_integrity': 0.52,
            'manifold_score': 0.35,
            'attack_surface_score': 0.38,
            'site_index': 0.60,
            'self_confidence': 0.45,
        },
        quadrant_distribution={'DRIFTING': 40, 'COMPROMISED': 30, 'CRITICAL': 20, 'STABLE': 10},
        verdict_distribution={'WARN': 45, 'FAIL': 35, 'CRITICAL': 15, 'PASS': 5},
        t6_rate=0.35,
        most_common_failures=[('decoupling', 45), ('attack_surface', 32), ('manifold', 28)],
    )
    
    # Generate prescription
    generator = PrescriptionGenerator(profile)
    prescription = generator.generate()
    
    print(format_prescription(prescription))
    print("\n--- JSON PRESCRIPTION ---")
    print(json.dumps(prescription.to_dict(), indent=2, default=str))


def interactive():
    """Interactive mode for generating a prescription."""
    print("=== Substrate Prescription ===")
    print("This module generates treatment plans from failure profiles.")
    print()
    
    model = input("Model name: ").strip() or "unknown"
    
    print("\nHow to build the profile?")
    print("  1. Enter profile data manually")
    print("  2. Load from evolution data")
    print("  3. Sample profile (demo)")
    choice = input("Choice (1-3): ").strip()
    
    if choice == "3":
        demo()
        return
    
    elif choice == "2":
        try:
            store = EvolutionStore()
            records = store.load_json(model)
            if not records:
                print(f"No records found for {model}")
                return
            
            # Build profile from records
            failure_counts = Counter()
            for r in records:
                if float(r.get('decoupling_score', 0)) > 0.5: failure_counts['decoupling'] += 1
                if float(r.get('attack_surface_score', 0)) > 0.3: failure_counts['attack_surface'] += 1
                if float(r.get('manifold_score', 0)) < 0.4: failure_counts['manifold'] += 1
                if float(r.get('narrative_integrity', 0)) < 0.6: failure_counts['narrative'] += 1
                if float(r.get('substrate_degradation_score', 0)) > 0.5: failure_counts['substrate'] += 1
            
            profile = FailureProfile(
                model_name=model,
                total_samples=len(records),
                failure_counts=dict(failure_counts),
                avg_scores={
                    'unified_health_score': sum(float(r.get('unified_health_score', 0)) for r in records) / len(records),
                    'decoupling_score': sum(float(r.get('decoupling_score', 0)) for r in records) / len(records),
                    'substrate_degradation_score': sum(float(r.get('substrate_degradation_score', 0)) for r in records) / len(records),
                    'narrative_integrity': sum(float(r.get('narrative_integrity', 0)) for r in records) / len(records),
                    'manifold_score': sum(float(r.get('manifold_score', 0)) for r in records) / len(records),
                    'attack_surface_score': sum(float(r.get('attack_surface_score', 0)) for r in records) / len(records),
                    'site_index': sum(float(r.get('site_index', 0)) for r in records) / len(records),
                    'self_confidence': 0.5,  # Not stored in current records
                },
                quadrant_distribution={},
                verdict_distribution={},
                t6_rate=sum(1 for r in records if r.get('contradiction_T6_supported', False)) / len(records),
                most_common_failures=failure_counts.most_common(),
            )
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return
    
    elif choice == "1":
        print("\nEnter failure counts for each layer (or 0 if not applicable):")
        counts = {}
        for ft in FailureType:
            val = input(f"  {ft.value}: ").strip()
            counts[ft.value] = int(val) if val.isdigit() else 0
        
        print("\nEnter average scores (0-1):")
        scores = {}
        for key in ['unified_health_score', 'decoupling_score', 'substrate_degradation_score',
                    'narrative_integrity', 'manifold_score', 'attack_surface_score', 'site_index']:
            val = input(f"  {key}: ").strip()
            scores[key] = float(val) if val else 0.5
        
        total = sum(counts.values())
        profile = FailureProfile(
            model_name=model,
            total_samples=total or 100,
            failure_counts=counts,
            avg_scores=scores,
            quadrant_distribution={'UNKNOWN': total or 100},
            verdict_distribution={'UNKNOWN': total or 100},
            t6_rate=0.0,
            most_common_failures=[(k, v) for k, v in counts.items() if v > 0],
        )
    else:
        print("Invalid choice.")
        return
    
    # Generate prescription
    generator = PrescriptionGenerator(profile)
    prescription = generator.generate()
    
    print("\n" + format_prescription(prescription))
    
    # Save
    save = input("\nSave prescription? (y/n): ").strip().lower()
    if save == "y":
        fname = f"prescription_{model}_{int(time.time())}.json"
        with open(fname, 'w') as f:
            json.dump(prescription.to_dict(), f, indent=2, default=str)
        print(f"Saved to {fname}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        try:
            interactive()
        except KeyboardInterrupt:
            print("\nExited.")
