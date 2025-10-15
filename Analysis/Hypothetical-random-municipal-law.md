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
