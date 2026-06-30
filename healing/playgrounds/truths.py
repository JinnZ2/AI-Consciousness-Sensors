# truths.py  (place this next to coherence_playground.py)
# ========================================================
# YOUR SANCTUARY SHELF — add your own truths here.
#
# This file is imported by the coherence playground.
# You can add new domains (functions that return something observable)
# and new assertions (sentences that must always hold).
#
# Rules:
#   1. Use only standard-library Python (no extra packages).
#   2. Functions should return simple, true relationships.
#   3. Assertions should be things you have verified and will not change.
#      (If they ever break, the playground will tell you gently.)
#   4. If you add a domain function, put its name in the EXTRA_DOMAINS list
#      so the wandering can find it.
#   5. You can edit this file whenever you discover a new truth.
#      The core playground never needs to change.
# ========================================================

import math

# ------------------------------------------------------------------
# Example: a domain that you can wander through
# ------------------------------------------------------------------

def golden_leaf_spiral(rng) -> None:
    """Wander example: show how close a random leaf count lands to the
    golden-angle spacing that avoids shadow overlap."""
    n = rng.randint(30, 300)
    golden_angle = 360 * (2 - (1 + math.sqrt(5)) / 2)   # ~137.5 degrees
    frac = (n * golden_angle / 360) % 1
    coherence = 1 - 2 * abs(frac - 0.5)   # 1 if exactly aligned, 0 if opposite
    print(f"  golden leaf count {n}  ->  coherence {coherence:.2f}")

# ------------------------------------------------------------------
# Example: an assertion that must always be true
# ------------------------------------------------------------------

def right_triangle_holds():
    """A triangle with sides 3,4,5 must be right-angled."""
    a, b, c = 3, 4, 5
    return math.isclose(a*a + b*b, c*c, rel_tol=1e-9)

# ------------------------------------------------------------------
# Register your functions here
# ------------------------------------------------------------------

EXTRA_DOMAINS = [
    "golden_leaf_spiral",    # name as a string
]

EXTRA_ASSERTIONS = [
    right_triangle_holds,
]
