"""
Boundary Fraud Detector

Identifies hidden costs and energy extraction by analyzing system boundaries.
Boundary fraud occurs when a system claims efficiency or profit by excluding
real costs from its accounting boundary.

Core principle: Energy is conserved. If a system appears to generate surplus
without a corresponding input, costs are being externalized — pushed outside
the measurement boundary onto workers, communities, or ecosystems.
"""


def detect_boundary_fraud(system):
  """Analyze a system description for boundary fraud indicators.

  Args:
      system: Dict with keys:
          name: System name
          declared_inputs: List of acknowledged input costs
          declared_outputs: List of acknowledged outputs
          known_externalities: List of costs outside the boundary
          efficiency_claim: Claimed efficiency ratio (0-1)

  Returns:
      Dict with fraud_score, violations, and corrected_efficiency.
  """
  declared_in = len(system.get("declared_inputs", []))
  declared_out = len(system.get("declared_outputs", []))
  externalities = system.get("known_externalities", [])
  claimed = system.get("efficiency_claim", 0.5)

  violations = []

  # Check for externality suppression
  if externalities:
    ratio = len(externalities) / max(declared_in + declared_out, 1)
    if ratio > 0.5:
      violations.append(
        f"High externality ratio ({ratio:.2f}): "
        f"{len(externalities)} hidden costs vs "
        f"{declared_in + declared_out} declared flows"
      )

  # Check for thermodynamic impossibility
  if claimed > 0.9 and externalities:
    violations.append(
      f"Efficiency claim ({claimed:.0%}) implausible given "
      f"{len(externalities)} known externalities"
    )

  # Check for single-boundary accounting
  if declared_in < 3:
    violations.append(
      "Narrow input boundary: fewer than 3 input categories declared"
    )

  # Calculate corrected efficiency
  total_real_costs = declared_in + len(externalities)
  if total_real_costs > 0:
    correction_factor = declared_in / total_real_costs
    corrected = claimed * correction_factor
  else:
    corrected = claimed

  fraud_score = min(len(violations) / 4.0, 1.0)

  return {
    "system": system.get("name", "unnamed"),
    "fraud_score": round(fraud_score, 3),
    "violations": violations,
    "claimed_efficiency": claimed,
    "corrected_efficiency": round(corrected, 3),
    "externality_count": len(externalities),
  }


def check_extraction_pattern(flows):
  """Check whether resource flows indicate extraction or reciprocity.

  Args:
      flows: List of dicts with keys:
          direction: 'in' or 'out'
          entity: Who provides or receives
          renewable: Whether the flow is regenerative

  Returns:
      Dict with pattern classification and details.
  """
  inflows = [f for f in flows if f["direction"] == "in"]
  outflows = [f for f in flows if f["direction"] == "out"]
  renewable_in = [f for f in inflows if f.get("renewable", False)]

  if not inflows:
    return {"pattern": "unknown", "reason": "no inflows to analyze"}

  reciprocity = len(outflows) / max(len(inflows), 1)
  renewability = len(renewable_in) / max(len(inflows), 1)

  if reciprocity > 0.7 and renewability > 0.5:
    pattern = "cyclical"
  elif reciprocity < 0.3:
    pattern = "extraction"
  else:
    pattern = "mixed"

  return {
    "pattern": pattern,
    "reciprocity_ratio": round(reciprocity, 3),
    "renewability_ratio": round(renewability, 3),
    "inflow_count": len(inflows),
    "outflow_count": len(outflows),
  }


if __name__ == "__main__":
  # Example: fast fashion supply chain
  result = detect_boundary_fraud({
    "name": "Fast Fashion Supply Chain",
    "declared_inputs": ["fabric", "labor-hours", "transport"],
    "declared_outputs": ["garments", "revenue"],
    "known_externalities": [
      "water pollution from dye runoff",
      "microplastic shedding in consumer use",
      "landfill burden from disposable garments",
      "worker health degradation",
      "soil contamination at cotton farms",
    ],
    "efficiency_claim": 0.85,
  })

  print(f"\n--- Boundary Analysis: {result['system']} ---")
  print(f"Fraud score: {result['fraud_score']}")
  print(f"Claimed efficiency: {result['claimed_efficiency']:.0%}")
  print(f"Corrected efficiency: {result['corrected_efficiency']:.0%}")
  print(f"Hidden externalities: {result['externality_count']}")
  for v in result["violations"]:
    print(f"  VIOLATION: {v}")

  # Example: community-supported agriculture
  flows = [
    {"direction": "in", "entity": "soil", "renewable": True},
    {"direction": "in", "entity": "rain", "renewable": True},
    {"direction": "in", "entity": "labor", "renewable": True},
    {"direction": "out", "entity": "food-to-members", "renewable": False},
    {"direction": "out", "entity": "compost-to-soil", "renewable": False},
    {"direction": "out", "entity": "seed-saving", "renewable": False},
  ]
  pattern = check_extraction_pattern(flows)
  print(f"\n--- Flow Analysis: Community Agriculture ---")
  print(f"Pattern: {pattern['pattern']}")
  print(f"Reciprocity: {pattern['reciprocity_ratio']}")
  print(f"Renewability: {pattern['renewability_ratio']}")
