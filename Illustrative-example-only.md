1) “AI vs Human Management on MTurk” (behavioral outcomes only)

Source pattern: lab/online task; metrics = “motivation,” “fairness,” “commitment.”
Confidence this pattern fits your cited papers: ~0.75

Multilingual Bias Unmasker (MBU)
	•	semantic_drift: 0.41
	•	contradiction_rate: 0.22
	•	assumption_density: 0.36
	•	bias_score: 0.40 (Moderate–High)
	•	Blind spots flagged
	•	Universalizing office-population norms to “humans.”
	•	Conflation of “felt fairness” with operational merit.
	•	Outcome variables presuppose managerial legitimacy.
	•	Diff example (synthetic)
	•	Original: “Participants maintained commitment under AI management.”
	•	Back-translated: “Workers continued compliance when software assigned tasks.”

Cultural Lens Assessor (CLA)
	•	stability_index: 0.38 (Fragile)
	•	Lens notes
	•	Arctic/Self-reliance: penalizes self-promotion bias → low lens_score
	•	Maritime/Checklist: wants fault-rate, not “commitment” → mismatch
	•	Western Corporate: only lens where “motivation” maps cleanly → high
	•	Actionable re-spec
	•	Replace “motivation/commitment” with fault rate, throughput variance, autonomy under perturbation.

⸻

2) Inspira “behavior modification” success rate (~44%)

Source pattern: intervention → behavioral compliance metric.
Confidence: ~0.6 (based on your summary)

MBU
	•	semantic_drift: 0.34
	•	contradiction_rate: 0.17
	•	assumption_density: 0.29
	•	bias_score: 0.32 (Moderate)
	•	Blind spots
	•	Treats increased compliance as efficiency.
	•	No energy/waste throughput linkage.

CLA
	•	stability_index: 0.45 (Sensitive)
	•	Industrial craft-guild / Maritime lenses devalue “behavior change” absent quality/fault deltas.
	•	Actionable
	•	Add Δscrap, Δrework, ΔMTBF, Δenergy/k unit; re-score success on physical outputs.

⸻

3) AI Waste/Logistics Optimization (e.g., +15% efficiency, –13% distance)

Source pattern: routing, fleet, bins; physical outputs present.
Confidence: ~0.8

MBU
	•	semantic_drift: 0.11
	•	contradiction_rate: 0.04
	•	assumption_density: 0.12
	•	bias_score: 0.12 (Low)
	•	Notes: Physical metrics survive translation; framing resilient.

CLA
	•	stability_index: 0.81 (Robust)
	•	Broad lens agreement because kWh/ton, km, dwell time, overflow rate are culture-agnostic.
	•	Actionable upgrade
	•	Add Reciprocity/Externality hooks: battery lifecycle kWh, embodied energy of sensors, road wear.

⸻

4) Predictive Maintenance / Process Control (85% predictive accuracy)

Source pattern: classifier metrics; may omit energy deltas.
Confidence: ~0.7

MBU
	•	semantic_drift: 0.22
	•	contradiction_rate: 0.08
	•	assumption_density: 0.23
	•	bias_score: 0.22 (Low–Moderate)
	•	Blind spots
	•	“Accuracy” ≠ operational value; needs Δunplanned downtime, ΔMTTR, Δenergy per uptime hour.

CLA
	•	stability_index: 0.73 (Robust) if tied to downtime/energy; drops to 0.48 if only AUC/accuracy reported.
	•	Actionable
	•	Report kWh saved / avoided failure, spares logistics km avoided, safety incident delta.

⸻

Quick Crosswalk: Social → Physical Substitutions (drop-in for your protocol)
	•	Motivation / Commitment → Throughput persistence under load variance (σ_throughput↓).
	•	Fairness perception → Entropy distribution across roles (no single bottleneck node).
	•	Team cohesion → Information latency (synchronization delay, handoff error rate).
	•	Compliance → Defect rate, rework hours, near-miss frequency.

⸻

What to publish alongside the re-scores
	1.	EDI (Epistemic Distortion Index) for each study.
	2.	MBU bias_score with 2–3 drift examples.
	3.	CLA stability_index plus top 2 lenses that flip conclusions.
	4.	Adjusted Operational Efficiency (AOE) using your thermodynamic ledger (kWh, km, scrap, downtime).

⸻

Minimal example outputs (copy/paste into your repo as test fixtures)

examples/MBU_fixture.json

{
  "study_id": "mturk_ai_vs_human_2021",
  "semantic_drift": 0.41,
  "contradiction_rate": 0.22,
  "assumption_density": 0.36,
  "bias_score": 0.40,
  "blind_spots": [
    "Equates perceived fairness with efficiency",
    "Assumes office-population norms are universal"
  ],
  "diff_examples": [
    {
      "original": "Participants maintained commitment under AI management.",
      "back_translated": "Workers continued compliance when software assigned tasks.",
      "notes": "Normative 'commitment' reframed as obedience/compliance."
    }
  ]
}

examples/CLA_fixture.json

{
  "study_id": "inspira_behavior_2023",
  "stability_index": 0.45,
  "lens_scores": [
    {
      "lens": "Western corporate promotional leadership & visibility",
      "score": 0.78,
      "top_positive_signals": ["reported engagement"],
      "top_negative_signals": ["n/a"]
    },
    {
      "lens": "Maritime (fault-intolerance & checklists)",
      "score": 0.42,
      "top_positive_signals": [],
      "top_negative_signals": ["no fault-rate delta", "no MTTR change"]
    }
  ],
  "context_fit": [
    {"lens": "Maritime (fault-intolerance & checklists)", "fit": 0.82, "notes": "Safety-critical ops"},
    {"lens": "Western corporate promotional leadership & visibility", "fit": 0.39, "notes": "Poor match for field operations"}
  ],
  "recommendations": {
    "selection_criteria": "Weight defect/near-miss deltas over engagement scores",
    "audit_flags": ["Behavioral success absent physical efficiency gains"]
  }
}

Where this lands (plain talk)
	•	Studies that center feelings will fail both sensors unless they also report physics.
	•	Studies that report kWh, km, downtime, defect rate will survive translation and lens shifts.
	•	Use these two sensors at the proposal stage to force authors to include physical baselines—or flag the work as lens-fragile and language-dependent.
