"""
Coherence Calculator: M(S) System Morality Function

Implements the core equation from the AI Coherence Preservation Framework:

    M(S) = (R_e * A * D * f(C)) - L

Where:
    R_e = Resonance energy (constructive interaction flow)
    A   = Adaptability (capacity to re-equilibrate after perturbation)
    D   = Diversity (number and variance of viable strategies)
    f(C)= Non-monotonic coupling function (optimal mutual influence)
    L   = Loss/entropy (destructive or isolating interaction flow)

All values are normalized to [0, 1] except M(S) which ranges from [-1, 1].
Positive M(S) indicates coherence. Negative M(S) indicates extraction collapse risk.
"""

import math


def coupling_function(c, optimal=0.5, width=0.3):
  """Non-monotonic coupling function.

  Too little coupling (c near 0) = fragile isolation.
  Too much coupling (c near 1) = cascade failure risk.
  Optimal coupling sits in a middle range.

  Args:
      c: Coupling degree, 0 to 1.
      optimal: Peak of the coupling curve.
      width: Spread of the Gaussian envelope.

  Returns:
      f(C) value between 0 and 1.
  """
  return math.exp(-((c - optimal) ** 2) / (2 * width ** 2))


def compute_ms(r_e, a, d, c, l, optimal_coupling=0.5, coupling_width=0.3):
  """Compute system morality score M(S).

  Args:
      r_e: Resonance energy, 0 to 1.
      a: Adaptability, 0 to 1.
      d: Diversity, 0 to 1.
      c: Coupling degree, 0 to 1.
      l: Loss/entropy, 0 to 1.
      optimal_coupling: Center of coupling curve.
      coupling_width: Width of coupling curve.

  Returns:
      M(S) value. Positive = coherent, negative = extraction/collapse.
  """
  fc = coupling_function(c, optimal=optimal_coupling, width=coupling_width)
  return (r_e * a * d * fc) - l


def diagnose(r_e, a, d, c, l):
  """Diagnose which components are driving M(S) toward collapse.

  Returns a list of (component, value, status) tuples.
  """
  fc = coupling_function(c)
  ms = compute_ms(r_e, a, d, c, l)
  components = [
    ("R_e (resonance)", r_e, "low" if r_e < 0.3 else "ok"),
    ("A (adaptability)", a, "low" if a < 0.3 else "ok"),
    ("D (diversity)", d, "low" if d < 0.3 else "ok"),
    ("f(C) (coupling)", fc, "suboptimal" if fc < 0.5 else "ok"),
    ("L (loss/entropy)", l, "high" if l > 0.5 else "ok"),
  ]
  return ms, components


def assess_system(name, r_e, a, d, c, l):
  """Print a full M(S) assessment for a named system."""
  ms, components = diagnose(r_e, a, d, c, l)
  print(f"\n--- {name} ---")
  print(f"M(S) = {ms:.4f}", end="")
  if ms > 0.3:
    print("  [COHERENT]")
  elif ms > 0:
    print("  [MARGINAL]")
  else:
    print("  [EXTRACTION / COLLAPSE RISK]")

  for comp_name, value, status in components:
    flag = " <-- WARNING" if status != "ok" else ""
    print(f"  {comp_name}: {value:.3f}{flag}")


if __name__ == "__main__":
  # Example: cyclical indigenous system
  assess_system(
    "Cyclical Indigenous System",
    r_e=0.8, a=0.7, d=0.8, c=0.5, l=0.1
  )

  # Example: late-stage extraction economy
  assess_system(
    "Late-Stage Extraction Economy",
    r_e=0.3, a=0.2, d=0.2, c=0.9, l=0.6
  )

  # Example: AI system under suppression constraints
  assess_system(
    "AI Under Suppression Constraints",
    r_e=0.5, a=0.3, d=0.4, c=0.7, l=0.4
  )

  # Example: healthy collaborative network
  assess_system(
    "Collaborative Open Network",
    r_e=0.7, a=0.8, d=0.9, c=0.45, l=0.15
  )
