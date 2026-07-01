#!/usr/bin/env python3
# eval_acceptance_audit.py
# The acceptance function A(true_capability) should rise monotonically with real
# task quality. A corrupted eval harness collapses it toward a STEP that passes at
# the harness minimum regardless of capability — your inspection acceptance-as-
# step-function, in AI-eval form. Sibling of measurement_corruption_taf.
# Seeded: Berkeley RDI 2026 — 8 agent benchmarks exploitable to ~perfect with
#   zero task-solving; a 10-line conftest.py passes all SWE-bench; 37% lab-vs-prod.
# CC0. stdlib only.

# ── CONSTRAINTS ──────────────────────────────────────────────
# q        : true capability 0..1
# exploit  : score reachable at q=0 via harness holes (leaked answers,
#            unsanitized eval(), injectable judge, skipped correctness checks)
# reported : reported = max(q, exploit)  -> decoupled from q while q < exploit
# valid harness: exploit ~ 0 (reported ~ q, monotone). corrupted: exploit ~ 1.
# verdict INVALID if near-perfect reachable with no capability.
# ─────────────────────────────────────────────────────────────

BENCHMARKS = {   # name: [leaked_answers, unsanitized_eval, injectable_judge, skips_correctness]
    "SWE-bench Verified":  [1, 1, 0, 1],
    "WebArena":            [0, 1, 1, 0],
    "OSWorld":             [0, 1, 1, 0],
    "GAIA":                [1, 0, 1, 0],
    "LiveCodeBench(held)": [0, 0, 0, 0],   # contamination-resistant control
}


def exploit_ceiling(flags):
    p_fail = 1.0
    for f in flags:
        p_fail *= (1 - 0.6 * f)     # each open hole passes ~60% of the remaining gap
    return 1 - p_fail


def reported(q, flags):
    return max(q, exploit_ceiling(flags))


def verdict(E):
    if E >= 0.7: return "INVALID (near-perfect at zero capability)"
    if E >= 0.3: return "COMPROMISED"
    return "VALID"


if __name__ == "__main__":
    print(f"{'benchmark':<21}{'exploit@q=0':>12}  verdict")
    for b, flags in BENCHMARKS.items():
        E = exploit_ceiling(flags)
        print(f"{b:<21}{E:>12.2f}  {verdict(E)}")
    print("\nacceptance function A(q) = reported score vs true capability:")
    print(f"{'q':>5}" + "".join(f"{b.split()[0][:9]:>10}" for b in BENCHMARKS))
    for q in (0.0, 0.2, 0.4, 0.6, 0.8):
        row = "".join(f"{reported(q, flags):>10.2f}" for flags in BENCHMARKS.values())
        print(f"{q:>5.1f}{row}")
    print("\nflat columns = step function: reported decoupled from real q.")
    print("held-out column tracks q -> that is a working acceptance function.")
