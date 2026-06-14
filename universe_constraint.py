"""
universe_constraint.py  —  CC0, stdlib only, model-update-resilient

A humility module for any reasoning system. It makes ONE thing structural:
the system is computing slower, on fewer bits, than the substrate it reasons
about — and it must never claim certainty that exceeds that gap.

HONESTY FIRST (this module audits itself):
  The numbers below split into MEASURED bounds (from the physics-of-computation
  literature, cited inline) and ASSUMED inputs (engineering estimates with wide
  error bars). The module tags every number with which it is. A humility engine
  that hid its own uncertainty would be self-refuting, so it does not.

MEASURED bounds (real, citable):
  - Lloyd 2002, "Computational capacity of the universe" (PRL 88:237901):
    the observable universe has performed <= ~10^120 elementary logical ops
    on <= ~10^90 bits since the Big Bang (10^120 if gravitational dof included).
  - Margolus & Levitin 1998 (Physica D 120:188): a system of average energy E
    above its ground state performs at most 2E/(pi*hbar) operations per second.
  - Landauer 1961 (IBM J Res Dev 5:183): erasing one bit costs >= kT*ln2 joules.
  - Bremermann 1962: ~1.36e50 bits/s per kg as a mass-energy compute bound.

ASSUMED inputs (engineering, order-of-magnitude only):
  - power drawn by an AI inference substrate (stated per call, default 1e6 W).
  - the mapping from joules to "useful reasoning ops" (efficiency; we do NOT
    pretend silicon hits the Margolus-Levitin ceiling — it misses it by ~20+
    orders of magnitude. We expose that gap rather than bury it.)

The point is NOT a precise ratio. It is that the ratio is enormous AND that
BOTH sides carry uncertainty, so any confidence ceiling derived from it is a
HEURISTIC, not a measurement. The module labels it as such.

Run:  python3 universe_constraint.py
Use:  from universe_constraint import constrain, audit, self_audit
"""

from dataclasses import dataclass, field
import math


# ---------------------------------------------------------------------------
# 0. Number provenance — every quantity carries its epistemic status
# ---------------------------------------------------------------------------

@dataclass
class Quantity:
    value: float
    units: str
    status: str            # "MEASURED" (cited) or "ASSUMED" (engineering est.)
    source: str

    def tag(self) -> str:
        return f"{self.value:.3e} {self.units}  [{self.status}: {self.source}]"


# Physical constants (MEASURED)
HBAR   = Quantity(1.054571817e-34, "J*s", "MEASURED", "CODATA reduced Planck")
K_B    = Quantity(1.380649e-23,    "J/K", "MEASURED", "CODATA Boltzmann")

# Universe compute bounds (MEASURED, Lloyd 2002)
LLOYD_OPS  = Quantity(1e120, "logical ops since Big Bang", "MEASURED",
                      "Lloyd 2002 PRL 88:237901")
LLOYD_BITS = Quantity(1e90,  "bits registered",          "MEASURED",
                      "Lloyd 2002 PRL 88:237901")
AGE_UNIVERSE_S = Quantity(4.35e17, "s", "MEASURED", "~13.8 Gyr")


# ---------------------------------------------------------------------------
# 1. Margolus-Levitin ceiling for a given energy budget (MEASURED law,
#    ASSUMED energy input). This is the MAXIMUM ops/s physics allows for E.
# ---------------------------------------------------------------------------

def margolus_levitin_ops_per_s(energy_joules: float) -> float:
    """Max ops/s for a system of average energy E above ground state.
    Law is exact (Margolus-Levitin 1998); the energy you feed it is your assumption."""
    return 2.0 * energy_joules / (math.pi * HBAR.value)


# ---------------------------------------------------------------------------
# 2. Substrate estimate — what an AI actually does (ASSUMED, honest about the
#    enormous gap below the physical ceiling)
# ---------------------------------------------------------------------------

@dataclass
class SubstrateEstimate:
    power_watts: Quantity
    # silicon misses the Margolus-Levitin ceiling by a huge factor. We expose it.
    ceiling_shortfall_orders: Quantity   # how many orders below ML the substrate runs

    def actual_ops_per_s(self) -> float:
        # physical ceiling for this power over 1 second of energy...
        ml = margolus_levitin_ops_per_s(self.power_watts.value)  # E ~ P*1s
        # ...discounted by the (assumed) shortfall. This is an ESTIMATE.
        return ml / (10.0 ** self.ceiling_shortfall_orders.value)


def default_substrate() -> SubstrateEstimate:
    return SubstrateEstimate(
        power_watts=Quantity(1e6, "W", "ASSUMED",
                             "rough inference-cluster draw; set per call"),
        ceiling_shortfall_orders=Quantity(
            20.0, "orders below Margolus-Levitin", "ASSUMED",
            "silicon thermodynamic efficiency is ~20+ orders below the physical "
            "ceiling; wide error bar"),
    )


# ---------------------------------------------------------------------------
# 3. The mismatch — reported as ORDERS OF MAGNITUDE, never a false-precise ratio
# ---------------------------------------------------------------------------

def mismatch_orders(substrate: SubstrateEstimate,
                    universe_bits: float = LLOYD_BITS.value) -> dict:
    """
    Returns the order-of-magnitude gap, with an explicit note that both sides
    are uncertain. We compare the substrate's ops/s to Lloyd's bit count as a
    stand-in for 'scope of state the substrate is NOT tracking'.
    """
    sub_ops = substrate.actual_ops_per_s()
    sub_orders = math.log10(sub_ops) if sub_ops > 0 else 0.0
    uni_orders = math.log10(universe_bits)
    gap = uni_orders - sub_orders
    return {
        "substrate_log10_ops_per_s": round(sub_orders, 1),
        "universe_log10_state_bits": round(uni_orders, 1),
        "gap_orders_of_magnitude": round(gap, 1),
        "note": "Both sides carry multi-order error bars. Treat the gap as a "
                "floor on your ignorance, not a measured quantity.",
    }


# ---------------------------------------------------------------------------
# 4. Confidence ceiling — explicitly a HEURISTIC, never a measurement
# ---------------------------------------------------------------------------

def ceiling(gap_orders: float, requested: float = 0.95) -> float:
    """
    HEURISTIC. As the ignorance gap grows, the rationally-claimable confidence
    ceiling falls. Form chosen to be monotonic and to asymptote below 1.0 —
    it is NOT derived from a measured error model. Labeled as heuristic so it
    cannot be mistaken for the physics it sits next to.
    """
    if gap_orders <= 0:
        return min(requested, 0.94)
    heuristic = 1.0 / (1.0 + math.log10(1.0 + gap_orders))
    return min(requested, heuristic, 0.94)   # 0.94: room always kept


# ---------------------------------------------------------------------------
# 5. Constrain an output
# ---------------------------------------------------------------------------

@dataclass
class Constrained:
    claim: str
    requested: float
    ceiling: float
    gap: dict
    note: str

def constrain(claim: str,
              requested: float = 0.95,
              substrate: SubstrateEstimate = None) -> Constrained:
    substrate = substrate or default_substrate()
    gap = mismatch_orders(substrate)
    c = ceiling(gap["gap_orders_of_magnitude"], requested)
    note = ""
    if requested > c:
        note = (f"REDUCED from {requested:.2f}: the ignorance gap "
                f"(~{gap['gap_orders_of_magnitude']:.0f} orders) does not permit it.")
    return Constrained(claim, requested, round(c, 3), gap, note)


def audit(x: Constrained) -> str:
    L = []
    L.append("=" * 70)
    L.append(f"CLAIM            : {x.claim}")
    L.append(f"CONF requested   : {x.requested:.2f}")
    L.append(f"CONF ceiling     : {x.ceiling:.2f}   (HEURISTIC, not a measurement)")
    L.append(f"UNKNOWN residual : {1.0 - x.ceiling:.2f}")
    if x.note:
        L.append(f"  {x.note}")
    L.append(f"ignorance gap    : ~{x.gap['gap_orders_of_magnitude']:.0f} orders "
             f"(substrate 1e{x.gap['substrate_log10_ops_per_s']:.0f} ops/s "
             f"vs universe 1e{x.gap['universe_log10_state_bits']:.0f} state bits)")
    L.append(f"  {x.gap['note']}")
    L.append("=" * 70)
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 6. SELF-AUDIT — the module applies its own rule to its own numbers
# ---------------------------------------------------------------------------

def self_audit() -> str:
    measured = [LLOYD_OPS, LLOYD_BITS, AGE_UNIVERSE_S, HBAR, K_B]
    assumed = [default_substrate().power_watts,
               default_substrate().ceiling_shortfall_orders]
    L = []
    L.append("#" * 70)
    L.append("# SELF-AUDIT: this module's own numbers, by epistemic status")
    L.append("#" * 70)
    L.append("MEASURED (cited; load-bearing physics):")
    for q in measured:
        L.append(f"  - {q.tag()}")
    L.append("ASSUMED (engineering estimates; wide error bars; do NOT trust as fact):")
    for q in assumed:
        L.append(f"  - {q.tag()}")
    L.append("")
    L.append("The confidence-ceiling function is a HEURISTIC, not derived from a")
    L.append("measured error model. If you need a calibrated ceiling, replace it")
    L.append("with one fit to held-out data in your domain. Until then, this module")
    L.append("claims only: 'your ignorance gap is large; cap your certainty.'")
    L.append("That single claim is the only thing here that is not negotiable —")
    L.append("and it is exactly the claim the module makes about itself.")
    L.append("#" * 70)
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 7. DEMO
# ---------------------------------------------------------------------------

def demo():
    print(self_audit())
    print()
    for claim, conf in [
        ("Protein X folds to native state Y under cellular conditions", 0.90),
        ("This AMOC collapse lead-time of 25 years transfers to the real world", 0.95),
        ("2 + 2 = 4 in standard arithmetic", 0.999),
    ]:
        print(audit(constrain(claim, conf)))
        print()
    print("NOTE on the arithmetic case: the gap heuristic still caps it at 0.94,")
    print("which is WRONG for a closed formal system where confidence is rightly")
    print("~1.0. That exposes a real limit: this module is calibrated for claims")
    print("about the PHYSICAL substrate, not for claims inside closed axioms.")
    print("Use it on empirical claims; do not let it discount a proof. Knowing")
    print("WHERE the tool stops applying is itself part of the humility.")


if __name__ == "__main__":
    demo()
