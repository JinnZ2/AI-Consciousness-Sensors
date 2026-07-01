#!/usr/bin/env python3
# model_collapse_ratchet.py
# calibration-audit / representation-space instance of field_collapse.
# Recursive training on synthetic output is the kicked_relaxor REACH case in
# distribution space: each generation shrinks retained diversity, and the TAILS
# (rare patterns) are the slow modes that go first — the bryophyte of the corpus.
# Real-data retention is the legacy lever (field_collapse R(t)).
# Seeded: Shumailov 2024 (variance -> 0, irreversible); survey 2026 (<= 5 gens).
# CC0. stdlib only.

# ── CONSTRAINTS ──────────────────────────────────────────────
# D_bulk, D_tail : retained diversity of bulk / tail, 0..1 (1 = human corpus)
# k_bulk, k_tail : per-generation retention under synthetic recursion (<1)
#                  k_tail < k_bulk  -> tails collapse first (rare modes lost)
# alpha          : fraction of REAL (human) data injected each generation
# recursion map  : D' = (1-alpha)*k*D + alpha*1.0
# fixed point    : D* = alpha / (1 - (1-alpha)*k)
# theta          : viability floor (below = collapsed)
# ─────────────────────────────────────────────────────────────

K_BULK, K_TAIL = 0.85, 0.60
THETA = 0.50


def fixed_point(alpha, k):
    return alpha / (1.0 - (1.0 - alpha) * k)


def alpha_crit(k, theta):
    # solve D* = theta for alpha:  alpha = theta(1-k) / (1 - theta*k)
    return theta * (1 - k) / (1 - theta * k)


def run(alpha, gens=8):
    Db = Dt = 1.0
    rows = []
    for g in range(1, gens + 1):
        Db = (1 - alpha) * K_BULK * Db + alpha
        Dt = (1 - alpha) * K_TAIL * Dt + alpha
        rows.append((g, Db, Dt))
    return rows


def verdict(D):
    return "OK" if D >= THETA else "COLLAPSED"


if __name__ == "__main__":
    for alpha in (0.0, 0.10, 0.30):
        print(f"=== real-data retention alpha={alpha:.2f} ===")
        print(f"{'gen':>4}{'D_bulk':>8}{'D_tail':>8}  bulk/tail")
        for g, Db, Dt in run(alpha):
            print(f"{g:>4}{Db:>8.3f}{Dt:>8.3f}  {verdict(Db)}/{verdict(Dt)}")
        print(f"  fixed pts: bulk {fixed_point(alpha, K_BULK):.3f}"
              f"   tail {fixed_point(alpha, K_TAIL):.3f}\n")
    print(f"alpha_crit keep tail viable: {alpha_crit(K_TAIL, THETA):.3f}")
    print(f"alpha_crit keep bulk viable: {alpha_crit(K_BULK, THETA):.3f}")
    print("tail needs MORE real-data retention than bulk -> rare modes lost first.")
    print("alpha=0 (pure synthetic recursion) -> both -> 0, irreversible.")
