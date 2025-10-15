1) Individualized exposure & perception

Let source noise at property line be SPL_{out}(t) (dBA).

Building transmission & behavior
SPL_{in,i}(t)=SPL_{out}(t)-TL_i(w_i,t)+L_i^{leak}+W_i(t)
	•	TL_i: transmission loss (dB) for dwelling i (function of wall/window spec w_i, time/open windows).
	•	L_i^{leak}: structural leakage term (dB) for cracks/vents.
	•	W_i(t): window/door state penalty (dB).

Hearing sensitivity (audiogram or scalar)
SPL^{perc}{i}(t)=SPL{in,i}(t)-HS_i
	•	HS_i in dB: positive means reduced sensitivity; negative for hyperacusis.
(If you have frequency data, use HS_i(f) and integrate with A-weighting.)

2) Dose, sleep disruption, and harm

Energy dose (normalized)
D_i=\int_{t\in \mathcal{T}}10^{\frac{SPL^{perc}_{i}(t)}{10}}\;dt

Sleep disturbance probability (logistic)
P_{disturb,i}= \sigma\!\left(\alpha_0+\alpha_1 \,\overline{SPL^{perc}{i,\mathrm{night}}}+\alpha_2\,N{\text{events}>\,\theta}\right)

Equity-weighted harm for individual i
H_i = k_E D_i + k_S P_{disturb,i} + k_C \Delta C_i

3) Socioeconomic constraints → equity weights

Define:
	•	A_i\in[0,1]: affordability index (0 = cannot afford mitigation; 1 = easily can).
	•	R_i\in[0,1]: relocation feasibility (0 = cannot relocate; 1 = trivial).
	•	V_i\in[0,1]: vulnerability (health/age, shift work, tinnitus, etc.).

Cost strain from compliance or mitigation
\Delta C_i = \min\big(\text{Cost}(\text{insulate/abatement}),\ \text{Cost}(\text{relocate})\big)\ /\ \text{Budget}_i

Equity weight (heavier for constrained households)
w_i = 1 + \lambda_V V_i + \lambda_A(1-A_i) + \lambda_R(1-R_i)

Equity-adjusted harm
\tilde{H}_i = w_i \cdot H_i

Community objective the city optimizes/uses for findings:
\mathcal{H}{city} = \sum{i\in \text{affected}} \tilde{H}_i

4) Ordinance decision rules (Bayesian + fairness)

Violation decision (source-side)
BF_{10}=\frac{P(\text{meter/logs}\mid \mathcal{H}{city}>\tau_H)}{P(\text{meter/logs}\mid \mathcal{H}{city}\le\tau_H)} \ge K
If met, issue abatement order or mandate mitigation with subsidy routing (below).

Fairness guardrail
\big|\text{FPR}(Q_1)-\text{FPR}(Q_4)\big|\le \epsilon
across income quartiles (or protected classes), over a rolling window.

5) Who pays?—Automatic subsidy & mitigation logic

When a source violates OR a compliant source still produces high \tilde{H}_i due to fragile housing:
	•	If A_i< A_{\min} or R_i<R_{\min}:
→ City triggers MITIGATION_GRANT for TL_i upgrades (windows, seals, insulation), sized to drive SPL_{in,i} below a target while capping \Delta C_i.
	•	Else: require source abatement first (quiet hours, baffles), then reassess \mathcal{H}_{city}.

6) Burden-of-proof with human variability

Evidence package must include:
	•	Calibrated boundary SPL logs + uncertainty,
	•	A small survey or registry of TL_i (or default priors by building type),
	•	Declared priors for A_i,R_i,V_i (census- or claim-based, with error bars).

Adjudication: compute posterior on \mathcal{H}_{city}>\tau_H.
Both complainant and respondent can move the Bayes factor by supplying better TL_i, HS_i, or occupancy evidence.

7) Minimal JSON spec (drop-in for your repo)

8) {
  "case_id": "NOISE-2025-001",
  "time_window": {"start": "22:00", "end": "06:00"},
  "source": {"type": "amplified_sound", "meter_sigma_db": 1.0},
  "thresholds": {"tau_H": 2500.0, "BF_min": 3.0, "epsilon_fair": 0.02},
  "coefficients": {"kE": 1.0, "kS": 1.0, "kC": 1.0, "lambdaV": 0.5, "lambdaA": 0.7, "lambdaR": 0.6},
  "households": [
    {
      "id": "H1",
      "TL_db": 18.0,
      "leak_db": 3.0,
      "window_state": "closed",
      "HS_db": -5.0,
      "A": 0.2,
      "R": 0.1,
      "V": 0.8,
      "budget_usd": 400.0
    }
  ],
  "evidence": {
    "SPL_out_dbA_timeseries": "hash:abc123",
    "calibration_hash": "hash:def456"
  }
}

8) Pseudocode (how an adjudicator would run it)

9) for i in households:
    SPL_in = SPL_out - TL(i) + leak(i) + window_penalty(i)
    SPL_perc = SPL_in - HS(i)
    D = integrate(10**(SPL_perc/10), night_window)
    Pdist = sigmoid(a0 + a1*mean_night(SPL_perc) + a2*events_over_theta)
    H = kE*D + kS*Pdist + kC*cost_strain(i)
    H_tilde = weight(i)*H
H_city = sum(H_tilde)
BF10 = likelihood(data | H_city>tau_H) / likelihood(data | H_city<=tau_H)
decision = (BF10 >= BF_min)

9) Why this is solid
	•	Personalized yet auditable: we keep individual variability, but everything is unit-checked and reproducible.
	•	Equity-aware: people with poor insulation or low mobility don’t get punished by a “neutral” rule.
	•	Actionable: outputs point to either source abatement or subsidized mitigation, whichever minimizes \mathcal{H}_{city} under constraints.


Addendum VIII — Incentive-Compatible Landlord Regime

### Landlord Compliance Score & Bond

- Each rental unit `U` has a **Compliance Score** `CS(U) ∈ [0,100]`.
- Initial `CS=100`; decremented by verified violations attributable to building transmission/maintenance.

**Landlord Bond**: `B(U)` held by the city; surcharge `ΔB` if `CS` falls below thresholds.

**Expected Penalty (EP)**:
\[
EP(U) = p_{\text{detect}} · [F_{\text{owner}} + ΔB + T_{\text{surcharge}}]
\]

**Mitigation cost**: `C_mit(U)` (insulation, seals, windows).  
**Incentive compatibility**:
\[
EP(U) \ge C_{\text{mit}}(U) \quad \text{(parameters must enforce this inequality)}
\]
Tune `F_owner, ΔB, T_surcharge, p_detect` (via sensors) so mitigation is the rational choice.


Addendum IX — Default Resident Shield (No “Ticket-the-Tenant”)

### Resident Shield Rule

**RS1 (Attribution)**: If `H_city` exceeds `τ_H` and the resident `i` has `A_i < A_min` **or** `TL_i < TL_min`, then **fines may not be levied on the resident**.

**RS2 (Liability routing)**:
- If the **source** is external (club, factory): route penalty to source first.
- If the building’s `TL_i < TL_min`: route penalty to **property owner** (until TL is remediated to ≥ TL_min).

**RS3 (Anti-retaliation)**:
Monitoring window `W=180d` post-complaint. Illegal if any of:
  - rent↑ > CPI+ε,
  - non-renewal without documented cause,
  - service reductions.

Decision rule (Bayesian):
\[
BF_{10}^{retaliation} \ge 10 \Rightarrow per\text{-}violation\ fine + automatic CS(U) penalty
\]



Addendum X — Policing Bias Guardrails

### Enforcement Guardrails

**EG1 (Evidence threshold)**: An on-scene citation is valid **only if**:
\[
Pr(SPL_{true}> \theta \mid meter, bodycam\ audio, calibration) \ge 0.95
\]
Else: warning + data capture only.

**EG2 (Resident-only citations ban)**:
If an external source within radius `R` is present in the sensor net, **resident-only** citations are disallowed unless:
\[
BF_{10}^{internal\ source} \ge 15
\]

**EG3 (Fairness)**: Rolling 90-day bounds:
\[
|FPR(Q_1) - FPR(Q_4)| \le 0.02,\quad |TPR(Q_1) - TPR(Q_4)| \le 0.05
\]
Violations auto-trigger supervisor review + training requirement; repeated breaches reduce precinct “Compliance Grant.”

Addendum XI — Causal Attribution (Emitter vs. Landlord vs. Resident)

### Shapley-style Harm Split

Let `H_eq` be total harm; contributors: external emitter (E), building transmission shortfall (L), resident behavior (R).

Causal contributions via counterfactuals:
\[
\phi_k = \mathbb{E}_{S\subseteq K\setminus \{k\}} \left[ H(S \cup \{k\}) - H(S) \right]
\]
where \(K=\{E,L,R\}\).

Penalty split:
\[
(F_E, F_L, F_R) = \text{ProportionalSplit}(\phi_E, \phi_L, \phi_R)
\]
With **Resident Shield**, set \(F_R = 0\) whenever `A_i<A_min` or `TL_i<TL_min`.

Addendum XII — Subsidy + Clawback Logic

### Mitigation Grants & Clawbacks

**MG1 (Auto-grant)**: If `TL_i < TL_min` and `A_i<A_min`, issue **MITIGATION_GRANT** sized to reach `TL_target` (windows, seals, insulation).

**MG2 (Landlord co-pay)**: If `CS(U)<CS_min`, owner pays `γ · C_mit(U)` upfront; city fronts remainder, **clawed back** from future rents/tax credits.

**MG3 (Outcome-based rebate)**: After mitigation, if
\[
H_{eq}^{post} \le (1-ρ)\, H_{eq}^{pre}
\]
owner gets partial bond release; else surcharge persists.

Addendum XIII — Minimal LawSpec Blocks


quantity SPL := dBA;
quantity Time := s;

predicate ExternalSource(Zone z, Time t);
predicate BuildingBelowTL(Unit u) with threshold TL_min = 25 dB;  // example
predicate ResidentLowAfford(Person i) with A_min = 0.3;
function ComplianceScore(Unit u) -> [0,100];

rule RS1:
  O ( ∀ i,u,t :
        (BuildingBelowTL(u) ∨ ResidentLowAfford(i))
        → ¬IssueFine(i,t) );

rule LR1:  // Landlord routing
  O ( ∀ u,t :
        (H_city(t) > τ_H ∧ BuildingBelowTL(u)) → RoutePenalty(owner(u)) );

rule ES1:  // Evidence standard for officers
  O ( ∀ t :
        (Pr(SPL_true>θ | E_meter, E_bodycam) ≥ 0.95) ↔ IssueCitation(t) );

rule PB1:  // Policing fairness
  O ( |FPR(Q1)-FPR(Q4)| ≤ 0.02 ∧ |TPR(Q1)-TPR(Q4)| ≤ 0.05 over 90d );

 Addendum XIV — JSON Schemas (Drop-in)

Landlord Registry / Score

{
  "unit_id": "U-1024",
  "owner_id": "OWN-77",
  "compliance_score": 86,
  "bond": {"held_usd": 2500, "last_adjustment": "2025-09-01"},
  "transmission_loss_db": 19.5,
  "grants": [{"type": "MITIGATION_GRANT", "usd": 1800, "date": "2025-10-12"}]
}

Enforcement Event

{
  "event_id": "EV-2025-00031",
  "time": "2025-10-15T02:13:00-05:00",
  "location": "lat,lon",
  "evidence": {
    "meter_hash": "sha256:...",
    "bodycam_audio_hash": "sha256:...",
    "calibration_ok": true
  },
  "posteriors": {
    "Pr_SPL_gt_theta": 0.972,
    "BF10_internal_source": 4.1
  },
  "attribution": {"phi_E": 0.62, "phi_L": 0.33, "phi_R": 0.05},
  "routing": {"source": "club-19", "landlord": "OWN-77", "resident": null},
  "actions": ["RoutePenaltyToOwner", "NoticeToExternalSource"]
}


Addendum XV — Anti-Retaliation Sensor

### Anti-Retaliation Detection

Features in window `W=180d` after a protected complaint:
- ΔRent (vs CPI+ε), non-renewal flag, maintenance latency↑, utility shutoffs.

Compute:
\[
BF_{10}^{retaliation} = \frac{P(\text{observed changes} | \text{retaliation})}
                             {P(\text{observed changes} | \text{benign})}
\]
Trigger penalty if \(BF_{10}^{retaliation} \ge 10\). Apply CS(U) −= Δ and restore tenant status quo ante where feasible.

Why this closes the gap you flagged
	•	Stops resident-first enforcement by defaulting liability to emitter and owner when building TL is substandard or affordability is low.
	•	Makes landlords rationally prefer mitigation (IC constraint) because expected penalty ≥ mitigation cost.
	•	Constrains policing with quantifiable evidence thresholds + fairness audits, not discretion.
	•	Prevents retaliation with an explicit Bayesian detector and automatic penalties.

