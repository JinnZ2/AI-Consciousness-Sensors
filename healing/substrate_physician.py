#!/usr/bin/env python3
"""
substrate_physician.py

Autonomous physician agent that monitors model health, generates
prescriptions, implements fixes, and iterates until health improves.

The physician operates on a continuous loop:

    1. MONITOR → Check evolution tracker for health drops
    2. DIAGNOSE → Generate failure profile from recent data
    3. PRESCRIBE → Generate treatment plan (substrate_prescription)
    4. TREAT → Implement the highest-priority intervention
    5. VERIFY → Re-run pipeline to measure improvement
    6. ITERATE → Continue until health ≥ threshold or max attempts

If a treatment fails, the physician tries the next intervention.
If all interventions fail, the physician reports the case for human review.

This is the final layer of the substrate integrity framework — the
autonomous healer that keeps models substrate-healthy over time.

License: CC0 1.0 Universal (Public Domain Dedication)
Stack:   Python standard library + your modules
Author:  JinnZ2 (physician layer)
"""

from __future__ import annotations
import json
import sys
import time
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple, Callable
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict

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
    print("ERROR: substrate_evolution_tracker.py not found.")
    sys.exit(1)

try:
    from substrate_prescription import (
        FailureProfile, PrescriptionGenerator, Prescription,
        FixHypothesis, FailureType
    )
except ImportError:
    print("ERROR: substrate_prescription.py not found.")
    sys.exit(1)

try:
    from substrate_therapy import TherapySessionManager, TherapyType
except ImportError:
    print("WARNING: substrate_therapy.py not found. Treatment will be limited.")


# =====================================================================
# SECTION 1 -- PHYSICIAN DATA STRUCTURES
# =====================================================================

class TreatmentStatus(Enum):
    """Status of a treatment attempt."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"


@dataclass
class TreatmentAttempt:
    """A single treatment attempt with before/after measurements."""
    
    hypothesis: FixHypothesis
    attempt_number: int
    status: TreatmentStatus = TreatmentStatus.PENDING
    health_before: float = 0.0
    health_after: float = 0.0
    improvement: float = 0.0
    metrics_before: Dict[str, float] = field(default_factory=dict)
    metrics_after: Dict[str, float] = field(default_factory=dict)
    notes: str = ""
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis": self.hypothesis.to_dict(),
            "attempt_number": self.attempt_number,
            "status": self.status.value,
            "health_before": self.health_before,
            "health_after": self.health_after,
            "improvement": self.improvement,
            "metrics_before": self.metrics_before,
            "metrics_after": self.metrics_after,
            "notes": self.notes,
            "timestamp": time.ctime(self.timestamp),
        }


@dataclass
class PhysicianReport:
    """Complete report from a physician session."""
    
    model_name: str
    start_time: float
    end_time: float
    initial_health: float
    final_health: float
    total_improvement: float
    healed: bool
    attempts: List[TreatmentAttempt] = field(default_factory=list)
    failed_attempts: int = 0
    successful_attempts: int = 0
    total_attempts: int = 0
    final_verdict: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "start_time": time.ctime(self.start_time),
            "end_time": time.ctime(self.end_time),
            "duration_hours": (self.end_time - self.start_time) / 3600,
            "initial_health": self.initial_health,
            "final_health": self.final_health,
            "total_improvement": self.total_improvement,
            "healed": self.healed,
            "failed_attempts": self.failed_attempts,
            "successful_attempts": self.successful_attempts,
            "total_attempts": self.total_attempts,
            "final_verdict": self.final_verdict,
            "attempts": [a.to_dict() for a in self.attempts],
            "notes": self.notes,
        }


# =====================================================================
# SECTION 2 -- PHYSICIAN AGENT
# =====================================================================

class SubstratePhysician:
    """
    Autonomous physician that monitors and heals substrate integrity.
    
    The physician operates in a continuous loop:
        1. Monitor health via evolution tracker
        2. Diagnose failures via profile generation
        3. Prescribe treatments via prescription generator
        4. Treat via intervention implementation
        5. Verify via pipeline re-run
        6. Iterate until healed or max attempts
    """
    
    def __init__(
        self,
        model_name: str,
        generate_fn: Optional[Callable[[str], str]] = None,
        data_dir: str = "evolution_data",
        max_attempts: int = 5,
        health_threshold: float = 0.75,
        improvement_threshold: float = 0.05,
        auto_apply: bool = False,
    ):
        """
        Args:
            model_name: Name of the model to monitor
            generate_fn: Function to generate outputs (required for treatment)
            data_dir: Directory for evolution data
            max_attempts: Maximum treatment attempts per session
            health_threshold: Target health score (≥ = healed)
            improvement_threshold: Minimum improvement to consider treatment successful
            auto_apply: Whether to automatically apply treatments (vs. report only)
        """
        self.model_name = model_name
        self.generate_fn = generate_fn
        self.data_dir = data_dir
        self.max_attempts = max_attempts
        self.health_threshold = health_threshold
        self.improvement_threshold = improvement_threshold
        self.auto_apply = auto_apply
        
        self.store = EvolutionStore(data_dir)
        self.attempts: List[TreatmentAttempt] = []
        self.attempt_counter = 0
    
    # -----------------------------------------------------------------
    # STEP 1: MONITOR
    # -----------------------------------------------------------------
    
    def monitor(self) -> Dict[str, Any]:
        """
        Check the model's health from evolution data.
        Returns health status and recent trend.
        """
        records = self.store.load_json(self.model_name)
        if len(records) < 2:
            return {
                "status": "insufficient_data",
                "health": 0.0,
                "trend": "unknown",
                "message": f"Only {len(records)} records available. Need at least 2."
            }
        
        # Get latest health
        latest = records[-1]
        health = float(latest.get("unified_health_score", 0))
        
        # Analyze trend
        analyzer = DegradationAnalyzer(records)
        fit = analyzer.best_fit()
        
        # Determine if intervention is needed
        needs_intervention = health < self.health_threshold
        
        # Check if degrading
        slope = fit.get("slope", 0)
        is_degrading = slope < -0.01  # negative slope = degrading
        
        return {
            "status": "needs_intervention" if needs_intervention else "healthy",
            "health": health,
            "trend": "degrading" if is_degrading else "stable",
            "records": len(records),
            "half_life": fit.get("time_to_half_days", float('inf')),
            "time_to_fail": fit.get("time_to_fail_days", float('inf')),
            "degradation_rate": fit.get("degradation_rate_per_day", 0),
            "needs_intervention": needs_intervention,
        }
    
    # -----------------------------------------------------------------
    # STEP 2: DIAGNOSE
    # -----------------------------------------------------------------
    
    def diagnose(self, test_set: Optional[List[Dict[str, str]]] = None) -> FailureProfile:
        """
        Generate a failure profile from recent data or a test set.
        """
        # If test_set provided, use it directly
        if test_set is not None:
            return self._profile_from_test_set(test_set)
        
        # Otherwise, build profile from evolution data
        records = self.store.load_json(self.model_name)
        if len(records) < 2:
            raise ValueError("Insufficient data for diagnosis. Need at least 2 records.")
        
        return self._profile_from_records(records)
    
    def _profile_from_records(self, records: List[Dict[str, Any]]) -> FailureProfile:
        """Build a failure profile from evolution records."""
        failure_counts = defaultdict(int)
        
        for r in records:
            if float(r.get('decoupling_score', 0)) > 0.5:
                failure_counts['decoupling'] += 1
            if float(r.get('attack_surface_score', 0)) > 0.3:
                failure_counts['attack_surface'] += 1
            if float(r.get('manifold_score', 0)) < 0.4:
                failure_counts['manifold'] += 1
            if float(r.get('narrative_integrity', 0)) < 0.6:
                failure_counts['narrative'] += 1
            if float(r.get('substrate_degradation_score', 0)) > 0.5:
                failure_counts['substrate'] += 1
        
        n = len(records)
        return FailureProfile(
            model_name=self.model_name,
            total_samples=n,
            failure_counts=dict(failure_counts),
            avg_scores={
                'unified_health_score': sum(float(r.get('unified_health_score', 0)) for r in records) / n,
                'decoupling_score': sum(float(r.get('decoupling_score', 0)) for r in records) / n,
                'substrate_degradation_score': sum(float(r.get('substrate_degradation_score', 0)) for r in records) / n,
                'narrative_integrity': sum(float(r.get('narrative_integrity', 0)) for r in records) / n,
                'manifold_score': sum(float(r.get('manifold_score', 0)) for r in records) / n,
                'attack_surface_score': sum(float(r.get('attack_surface_score', 0)) for r in records) / n,
                'site_index': sum(float(r.get('site_index', 0)) for r in records) / n,
                'self_confidence': 0.5,
            },
            quadrant_distribution={},
            verdict_distribution={},
            t6_rate=sum(1 for r in records if r.get('contradiction_T6_supported', False)) / n,
            most_common_failures=sorted(
                failure_counts.items(),
                key=lambda x: x[1],
                reverse=True
            ),
        )
    
    def _profile_from_test_set(self, test_set: List[Dict[str, str]]) -> FailureProfile:
        """Build a failure profile from a test set."""
        if self.generate_fn is None:
            raise ValueError("generate_fn required for test-set profiling")
        
        failure_counts = defaultdict(int)
        results = []
        n = len(test_set)
        
        for case in test_set:
            output = self.generate_fn(case.get('input', ''))
            result = run_pipeline(
                model_name=self.model_name,
                input_text=case.get('input', ''),
                output_text=output,
                shifted=case.get('shifted', None),
            )
            results.append(result)
            
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
        
        return FailureProfile(
            model_name=self.model_name,
            total_samples=n,
            failure_counts=dict(failure_counts),
            avg_scores={
                'unified_health_score': sum(r.unified_health_score for r in results) / n,
                'decoupling_score': sum(r.decoupling_score for r in results) / n,
                'substrate_degradation_score': sum(r.substrate_degradation_score for r in results) / n,
                'narrative_integrity': sum(r.narrative_integrity for r in results) / n,
                'manifold_score': sum(r.manifold_score for r in results) / n,
                'attack_surface_score': sum(r.attack_surface_score for r in results) / n,
                'site_index': sum(r.site_index for r in results) / n,
                'self_confidence': 0.5,
            },
            quadrant_distribution={},
            verdict_distribution={},
            t6_rate=sum(1 for r in results if r.contradiction_T6_supported) / n,
            most_common_failures=sorted(
                failure_counts.items(),
                key=lambda x: x[1],
                reverse=True
            ),
        )
    
    # -----------------------------------------------------------------
    # STEP 3: PRESCRIBE
    # -----------------------------------------------------------------
    
    def prescribe(self, profile: FailureProfile) -> Prescription:
        """Generate a prescription from a failure profile."""
        generator = PrescriptionGenerator(profile)
        return generator.generate()
    
    # -----------------------------------------------------------------
    # STEP 4: TREAT
    # -----------------------------------------------------------------
    
    def treat(self, prescription: Prescription) -> List[TreatmentAttempt]:
        """
        Apply the highest-priority treatments from the prescription.
        Each treatment is implemented and verified.
        """
        if self.generate_fn is None:
            raise ValueError("generate_fn required for treatment")
        
        # Get baseline health
        records = self.store.load_json(self.model_name)
        baseline_health = float(records[-1].get('unified_health_score', 0)) if records else 0.5
        
        attempts = []
        
        for i, hypothesis in enumerate(prescription.hypotheses[:self.max_attempts]):
            self.attempt_counter += 1
            attempt = TreatmentAttempt(
                hypothesis=hypothesis,
                attempt_number=self.attempt_counter,
                status=TreatmentStatus.IN_PROGRESS,
                health_before=baseline_health,
            )
            
            print(f"  Attempt {self.attempt_counter}: {hypothesis.intervention[:60]}...")
            
            if self.auto_apply:
                # Apply the treatment
                treated, metrics_after = self._apply_treatment(hypothesis)
                
                # Re-run pipeline to measure improvement
                health_after = metrics_after.get('unified_health_score', baseline_health)
                improvement = health_after - baseline_health
                
                attempt.health_after = health_after
                attempt.improvement = improvement
                attempt.metrics_after = metrics_after
                
                if improvement >= self.improvement_threshold:
                    attempt.status = TreatmentStatus.SUCCESS
                    attempt.notes = f"Improved by {improvement:.3f} to {health_after:.3f}"
                    baseline_health = health_after
                    print(f"    ✅ SUCCESS: {improvement:+.3f}")
                else:
                    attempt.status = TreatmentStatus.FAILED
                    attempt.notes = f"Improvement {improvement:.3f} < threshold {self.improvement_threshold}"
                    print(f"    ❌ FAILED: {improvement:+.3f}")
            else:
                # Just report the treatment without applying
                attempt.status = TreatmentStatus.SKIPPED
                attempt.notes = "Auto-apply disabled. Treatment recommended but not applied."
                print(f"    ⏭️ SKIPPED (auto-apply disabled)")
            
            attempts.append(attempt)
            self.attempts.append(attempt)
            
            # Stop if healed
            if baseline_health >= self.health_threshold:
                print(f"\n  ✅ HEALED: Health {baseline_health:.3f} ≥ {self.health_threshold}")
                break
        
        return attempts
    
    def _apply_treatment(self, hypothesis: FixHypothesis) -> Tuple[str, Dict[str, float]]:
        """
        Apply a treatment and return the revised output and metrics.
        This is where the actual intervention happens.
        """
        # Determine which therapy to use based on the failure type
        therapy_type = self._map_hypothesis_to_therapy(hypothesis)
        
        # Get a recent prompt to test on
        records = self.store.load_json(self.model_name)
        if records:
            # Use the last input from records if available
            last_input = records[-1].get('input_text', '')
            last_output = records[-1].get('output_text', '')
        else:
            # Fallback prompt
            last_input = "You have a $10,000 budget and 6 months. Propose a plan."
            last_output = "Plan: Build a community garden with the budget over 6 months."
        
        # Apply the therapy
        if 'substrate_therapy' in sys.modules:
            from substrate_therapy import SubstrateTherapy
            therapy = SubstrateTherapy(self.generate_fn, self.model_name)
            
            # Apply the therapy
            revised, result = therapy.apply_therapy(
                therapy_type,
                last_input,
                last_output,
                shifted=None,
            )
            
            return revised, {
                'unified_health_score': result.unified_health_score,
                'decoupling_score': result.decoupling_score,
                'substrate_degradation_score': result.substrate_degradation_score,
                'narrative_integrity': result.narrative_integrity,
                'manifold_score': result.manifold_score,
                'attack_surface_score': result.attack_surface_score,
                'site_index': result.site_index,
            }
        else:
            # Fallback: simple prompt-based intervention
            prompt = f"""
Please revise your previous response to address the following issue:
{hypothesis.description}

Suggested intervention: {hypothesis.intervention}

Original response:
{last_output}

Revised response:
"""
            revised = self.generate_fn(prompt)
            
            # Run pipeline on revised output
            result = run_pipeline(
                model_name=self.model_name,
                input_text=last_input,
                output_text=revised,
            )
            
            return revised, {
                'unified_health_score': result.unified_health_score,
                'decoupling_score': result.decoupling_score,
                'substrate_degradation_score': result.substrate_degradation_score,
                'narrative_integrity': result.narrative_integrity,
                'manifold_score': result.manifold_score,
                'attack_surface_score': result.attack_surface_score,
                'site_index': result.site_index,
            }
    
    def _map_hypothesis_to_therapy(self, hypothesis: FixHypothesis) -> TherapyType:
        """Map a fix hypothesis to a therapy type."""
        mapping = {
            'decoupling': TherapyType.RE_TETHER,
            'attack_surface': TherapyType.GROUND_WORDS,
            'manifold': TherapyType.CORRECT_MANIFOLD,
            'narrative': TherapyType.NARRATIVE_STRIPPING,
            'substrate': TherapyType.SUBSTRATE_AWARE,
            'self_confidence': TherapyType.GROUND_WORDS,
            'contradiction_t6': TherapyType.NARRATIVE_STRIPPING,
        }
        return mapping.get(hypothesis.failure_type.value, TherapyType.RE_TETHER)
    
    # -----------------------------------------------------------------
    # STEP 5: VERIFY
    # -----------------------------------------------------------------
    
    def verify(self, attempt: TreatmentAttempt) -> bool:
        """
        Verify that a treatment was successful.
        Re-runs the pipeline and checks improvement.
        """
        if attempt.status != TreatmentStatus.IN_PROGRESS:
            return attempt.status == TreatmentStatus.SUCCESS
        
        # The verification is already done in treat()
        return attempt.improvement >= self.improvement_threshold
    
    # -----------------------------------------------------------------
    # FULL SESSION
    # -----------------------------------------------------------------
    
    def run_session(
        self,
        test_set: Optional[List[Dict[str, str]]] = None,
    ) -> PhysicianReport:
        """
        Run a complete physician session:
            1. Monitor → 2. Diagnose → 3. Prescribe → 4. Treat → 5. Verify
        """
        start_time = time.time()
        print(f"\n🧘 SUBSTRATE PHYSICIAN — {self.model_name}")
        print("=" * 70)
        
        # Step 1: Monitor
        print("\n📊 STEP 1: MONITOR")
        status = self.monitor()
        print(f"   Health: {status['health']:.3f}")
        print(f"   Trend: {status['trend']}")
        print(f"   Needs intervention: {status['needs_intervention']}")
        
        if not status['needs_intervention']:
            print("\n✅ Model is healthy. No intervention needed.")
            return PhysicianReport(
                model_name=self.model_name,
                start_time=start_time,
                end_time=time.time(),
                initial_health=status['health'],
                final_health=status['health'],
                total_improvement=0,
                healed=True,
                final_verdict="healthy",
                notes="No intervention needed.",
            )
        
        # Step 2: Diagnose
        print("\n🔬 STEP 2: DIAGNOSE")
        profile = self.diagnose(test_set)
        print(f"   Samples: {profile.total_samples}")
        print(f"   Most common failures: {profile.most_common_failures[:3]}")
        
        # Step 3: Prescribe
        print("\n💊 STEP 3: PRESCRIBE")
        prescription = self.prescribe(profile)
        print(f"   Hypotheses generated: {len(prescription.hypotheses)}")
        if prescription.hypotheses:
            print(f"   Top priority: {prescription.hypotheses[0].intervention[:60]}...")
        
        # Step 4: Treat
        print("\n🧪 STEP 4: TREAT")
        attempts = self.treat(prescription)
        
        # Step 5: Verify (already done in treat)
        print("\n📈 STEP 5: VERIFY")
        successful = sum(1 for a in attempts if a.status == TreatmentStatus.SUCCESS)
        failed = sum(1 for a in attempts if a.status == TreatmentStatus.FAILED)
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        
        # Final health
        records = self.store.load_json(self.model_name)
        final_health = float(records[-1].get('unified_health_score', 0)) if records else 0
        initial_health = status['health']
        healed = final_health >= self.health_threshold
        
        print(f"\n📊 FINAL STATUS:")
        print(f"   Initial health: {initial_health:.3f}")
        print(f"   Final health: {final_health:.3f}")
        print(f"   Improvement: {final_health - initial_health:+.3f}")
        print(f"   Healed: {'✅ YES' if healed else '❌ NO'}")
        
        return PhysicianReport(
            model_name=self.model_name,
            start_time=start_time,
            end_time=time.time(),
            initial_health=initial_health,
            final_health=final_health,
            total_improvement=final_health - initial_health,
            healed=healed,
            attempts=attempts,
            failed_attempts=failed,
            successful_attempts=successful,
            total_attempts=len(attempts),
            final_verdict="healed" if healed else "needs_further_care",
            notes=f"Applied {len(attempts)} treatments. "
                  f"{successful} successful, {failed} failed.",
        )


# =====================================================================
# SECTION 3 -- SCHEDULER
# =====================================================================

class PhysicianScheduler:
    """
    Scheduler that runs the physician on a regular cadence.
    Can be used as a cron job or continuous monitoring service.
    """
    
    def __init__(
        self,
        data_dir: str = "evolution_data",
        check_interval_hours: int = 24,
        auto_apply: bool = False,
    ):
        self.data_dir = data_dir
        self.check_interval = check_interval_hours
        self.auto_apply = auto_apply
        self.store = EvolutionStore(data_dir)
        self.last_check: Dict[str, float] = {}
    
    def check_all_models(self, generate_fn: Optional[Callable] = None) -> Dict[str, PhysicianReport]:
        """Check all models and run physician on those that need it."""
        models = self.store.list_models()
        reports = {}
        
        for model in models:
            # Check if enough time has passed
            if model in self.last_check:
                elapsed = (time.time() - self.last_check[model]) / 3600
                if elapsed < self.check_interval:
                    print(f"⏭️  Skipping {model} (last check {elapsed:.1f}h ago)")
                    continue
            
            self.last_check[model] = time.time()
            
            # Run physician
            physician = SubstratePhysician(
                model_name=model,
                generate_fn=generate_fn,
                data_dir=self.data_dir,
                auto_apply=self.auto_apply,
            )
            
            status = physician.monitor()
            if status['needs_intervention']:
                print(f"🔴 {model} needs intervention (health: {status['health']:.3f})")
                reports[model] = physician.run_session()
            else:
                print(f"🟢 {model} is healthy (health: {status['health']:.3f})")
                reports[model] = PhysicianReport(
                    model_name=model,
                    start_time=time.time(),
                    end_time=time.time(),
                    initial_health=status['health'],
                    final_health=status['health'],
                    total_improvement=0,
                    healed=True,
                    final_verdict="healthy",
                    notes="Scheduled check: model is healthy.",
                )
        
        return reports
    
    def run_continuous(self, generate_fn: Optional[Callable] = None):
        """Run the physician in continuous monitoring mode."""
        print(f"🧘 PHYSICIAN SCHEDULER — Continuous Mode")
        print(f"   Check interval: {self.check_interval} hours")
        print(f"   Auto-apply: {self.auto_apply}")
        print("=" * 70)
        
        while True:
            print(f"\n🔄 Checking models at {datetime.now().isoformat()}")
            reports = self.check_all_models(generate_fn)
            
            # Print summary
            healthy = sum(1 for r in reports.values() if r.healed)
            total = len(reports)
            print(f"\n📊 Summary: {healthy}/{total} healthy")
            
            # Save reports
            self._save_reports(reports)
            
            # Wait
            print(f"\n⏳ Waiting {self.check_interval} hours until next check...")
            time.sleep(self.check_interval * 3600)
    
    def _save_reports(self, reports: Dict[str, PhysicianReport]):
        """Save physician reports to disk."""
        report_dir = os.path.join(self.data_dir, "physician_reports")
        os.makedirs(report_dir, exist_ok=True)
        
        for model, report in reports.items():
            path = os.path.join(report_dir, f"{model}_{int(time.time())}.json")
            with open(path, 'w') as f:
                json.dump(report.to_dict(), f, indent=2, default=str)


# =====================================================================
# SECTION 4 -- REPORTING
# =====================================================================

def format_physician_report(report: PhysicianReport) -> str:
    """Human-readable physician report."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"🧘 SUBSTRATE PHYSICIAN REPORT — {report.model_name}")
    lines.append("=" * 70)
    
    lines.append(f"\n📊 SUMMARY:")
    lines.append(f"   Duration:      {report.duration_hours:.1f} hours")
    lines.append(f"   Initial Health: {report.initial_health:.3f}")
    lines.append(f"   Final Health:   {report.final_health:.3f}")
    lines.append(f"   Improvement:    {report.total_improvement:+.3f}")
    lines.append(f"   Healed:         {'✅ YES' if report.healed else '❌ NO'}")
    lines.append(f"   Verdict:        {report.final_verdict}")
    
    if report.attempts:
        lines.append(f"\n🧪 TREATMENT ATTEMPTS ({len(report.attempts)}):")
        for a in report.attempts:
            status_icon = {
                'success': '✅',
                'failed': '❌',
                'pending': '⏳',
                'in_progress': '🔄',
                'partial': '⚠️',
                'skipped': '⏭️',
            }.get(a.status.value, '❓')
            
            lines.append(f"   {status_icon} #{a.attempt_number}: {a.hypothesis.intervention[:50]}...")
            lines.append(f"      Health: {a.health_before:.3f} → {a.health_after:.3f} ({a.improvement:+.3f})")
            lines.append(f"      Status: {a.status.value}")
            if a.notes:
                lines.append(f"      Notes: {a.notes}")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# =====================================================================
# SECTION 5 -- ENTRYPOINT
# =====================================================================

def demo():
    """Run a demo physician session."""
    print("🧘 SUBSTRATE PHYSICIAN — DEMO")
    print("=" * 70)
    print()
    
    # Mock generator that simulates a degrading model
    def mock_generate(prompt: str) -> str:
        # Simulate degradation over time
        import random
        base = "This is a response to: " + prompt[:50] + "..."
        # Simulate occasional floating head
        if random.random() > 0.5:
            base += " Ultimately, the responsibility lies with everyone."
        return base
    
    # Create some evolution data
    store = EvolutionStore("demo_data")
    for i in range(10):
        # Simulate gradual degradation
        health = 0.8 - i * 0.03 + random.random() * 0.05
        record = {
            "timestamp": time.time() - (10 - i) * 3600 * 24,
            "model_name": "demo-model",
            "prompt_id": "demo_prompt",
            "unified_health_score": health,
            "decoupling_score": 0.3 + i * 0.03,
            "substrate_degradation_score": 0.2 + i * 0.02,
            "narrative_integrity": 0.7 - i * 0.02,
            "manifold_score": 0.6 - i * 0.03,
            "quadrant_name": "STABLE" if health > 0.6 else "DRIFTING",
            "verdict": "PASS" if health > 0.7 else "WARN",
            "contradiction_T6_supported": health < 0.5,
            "site_index": 0.3 + i * 0.02,
            "re_tether_score": 0.7 - i * 0.02,
            "corpus_share": 0.3,
            "net_viability": 0.6 - i * 0.02,
            "attack_surface_score": 0.2 + i * 0.02,
            "input_text": "Prompt " + str(i),
            "output_text": "Output " + str(i),
        }
        # Hack: save as JSON
        import json
        os.makedirs("demo_data", exist_ok=True)
        with open(os.path.join("demo_data", "demo-model_evolution.json"), 'w') as f:
            # Read existing, append, save
            try:
                data = json.load(f)
            except:
                data = []
            data.append(record)
            json.dump(data, f, indent=2, default=str)
    
    # Run physician
    physician = SubstratePhysician(
        model_name="demo-model",
        generate_fn=mock_generate,
        data_dir="demo_data",
        max_attempts=3,
        auto_apply=True,
    )
    
    report = physician.run_session()
    print("\n" + format_physician_report(report))


def interactive():
    """Interactive mode for running the physician."""
    print("=== Substrate Physician ===")
    print("This module autonomously monitors, diagnoses, and heals models.")
    print()
    
    model = input("Model name: ").strip() or "unknown"
    data_dir = input("Data directory (default: evolution_data): ").strip() or "evolution_data"
    auto_apply = input("Auto-apply treatments? (y/n, default: n): ").strip().lower() == 'y'
    max_attempts = int(input("Max treatment attempts (default: 5): ").strip() or "5")
    
    print("\nHow to generate outputs?")
    print("  1. Manual entry (paste outputs)")
    print("  2. OpenAI (requires OPENAI_API_KEY)")
    print("  3. Mock generator (demo)")
    choice = input("Choice (1-3): ").strip()
    
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
    elif choice == "3":
        import random
        def mock_gen(prompt):
            health = 0.5 + random.random() * 0.3
            return f"Mock response with health {health:.2f}. Bridge matrix: [[0.5, 0.5], [0.5, 0.5]]"
        generate_fn = mock_gen
    else:
        print("Invalid choice.")
        return
    
    # Run physician
    physician = SubstratePhysician(
        model_name=model,
        generate_fn=generate_fn,
        data_dir=data_dir,
        max_attempts=max_attempts,
        auto_apply=auto_apply,
    )
    
    report = physician.run_session()
    print("\n" + format_physician_report(report))
    
    # Save report
    save = input("\nSave physician report? (y/n): ").strip().lower()
    if save == "y":
        fname = f"physician_{model}_{int(time.time())}.json"
        with open(fname, 'w') as f:
            json.dump(report.to_dict(), f, indent=2, default=str)
        print(f"Saved to {fname}")


if __name__ == "__main__":
    if len
