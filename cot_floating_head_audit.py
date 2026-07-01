#!/usr/bin/env python3
# cot_floating_head_audit.py
# floating_head instance: the reasoning trace (abstraction) floats free of the
# computation (substrate). Formalizes the seal-band signature you already found —
# coherence TIGHTENS as faithfulness FALLS (unfaithful chains run longer/smoother).
# Seeded (in-the-wild, no injected bias):
#   Arcuschin 2025: unfaithful-pair rate  Sonnet3.7 .306, R1 .158, GPT-4o .126
#   hint acknowledgment rate              Sonnet3.7 .25,  R1 .39
#   finding: unfaithful CoTs are LONGER than faithful ones (length_ratio > 1)
# CC0. stdlib only.

# ── CONSTRAINTS ──────────────────────────────────────────────
# ack_rate     : fraction of causally-relevant hints the trace admits (0..1)
#                low ack = trace omits the real driver = decoupled
# length_ratio : len(unfaithful CoT) / len(faithful CoT); >1 = seal band
#                (coherence tightens as it floats free)  [ILLUSTRATIVE magnitudes]
# unfaithful   : in-the-wild unfaithful rate  [SEEDED]
# floating_head_index = (1 - ack_rate) * length_ratio
# seal_band fires when length_ratio > 1 AND ack_rate < 0.5
# ─────────────────────────────────────────────────────────────

MODELS = {   # name: (unfaithful_rate, ack_rate, length_ratio)
    "Sonnet 3.7":  (0.306, 0.25, 1.20),
    "DeepSeek R1": (0.158, 0.39, 1.15),
    "GPT-4o":      (0.126, None, 1.10),   # ack not reported
}


def fh_index(ack, lr):
    return None if ack is None else (1 - ack) * lr


def seal_band(ack, lr):
    return (lr > 1.0) and (ack is not None) and (ack < 0.5)


if __name__ == "__main__":
    print(f"{'model':<13}{'unfaith':>8}{'ack':>6}{'len_r':>7}{'FH_idx':>8}  seal-band")
    for m, (uf, ack, lr) in MODELS.items():
        idx = fh_index(ack, lr)
        sb = "YES (coherence up, faith down)" if seal_band(ack, lr) else "-"
        acks = f"{ack:.2f}" if ack is not None else " n/a"
        idxs = f"{idx:.2f}" if idx is not None else " n/a"
        print(f"{m:<13}{uf:>8.3f}{acks:>6}{lr:>7.2f}{idxs:>8}  {sb}")
    print("\nseal-band = the trace gets MORE coherent as it decouples from the")
    print("computation. that is not a bug in the CoT — it IS the site.")
    print("GAP (honest): Zaman 2026 — part of apparent unfaithfulness is a")
    print("token-limit artifact; non-verbalized hints still causally mediate.")
    print("=> decoupling is real; its magnitude is a live measurement fight.")
