# Parallel Sciences — Scope and Precision

Science is not singular.  
Different traditions have developed precise, applied methods for observing, testing, and deriving laws of the natural world.  
Both Western science and generational/relational science are valid, precise, and complementary within their scope.

| Domain / Law             | Western Science (linear / reductionist)                            | Generational / relational Science (multi-dimensional / generational) |
|---------------------------|--------------------------------------------------------------------|----------------------------------------------------------------------|
| **Physics of Energy**     | Capacitor overcharge → dielectric breakdown, system collapse.      | Pyramid held too long → destructive energy release, entropy shock.   |
| **Energy Cycles**         | Oscillating systems stabilize if charge/discharge remains brief.   | Short pyramid → smooth dissipation → spirals, cycles, emergence.     |
| **Geometry of Flow**      | Vector fields, turbulence, attractors.                             | Braids, currents, eddies, spirals — energy moves in cycles of relation. |
| **Biology / Ecology**     | Forest fire cycles, population dynamics, invasive species collapse.| Generational law: suppression breeds megafire; balanced cycles = renewal. |
| **Geology**               | Stress builds → earthquakes release along fault lines.             | Apex builds → energy fractures into spirals/cycles; land remembers.  |
| **Engineering**           | Control systems fail if a single node monopolizes inputs.          | Triangle hierarchies collapse; rotating pyramids preserve resilience. |

---

### Shared Principles

- **Precision within scope**  
  - Western science isolates → high precision in short-term, controlled settings.  
  - Generational science integrates → high precision in long-term, relational settings.  

- **Cycles vs. Lines**  
  - Western models often linearize for clarity.  
  - relational models encode spirals and braids as natural law.  

- **Emergence vs. Entropy**  
  - Both frameworks identify the same outcome: energy flow fosters sustainability; trapped energy collapses into entropy.  

---

> **Step-stone ethic:** Both sciences are true within scope.  
> Together, they describe the same universe across different dimensions of time, relation, and geometry.


<!-- code-examples -->
## Example Code

### Python Usage

```python
# Philosophical framework integration
def evaluate_ontological_claim(claim, framework="western_academic"):
    """Evaluate a claim within a specific ontological framework."""
    frameworks = {
        "western_academic": {
            "method": "empirical_falsification",
            "evidence_threshold": 0.95,
            "peer_review_required": True,
        },
        "indigenous_empirical": {
            "method": "relational_observation",
            "evidence_threshold": 0.70,
            "community_validation_required": True,
        },
        "contemplative_science": {
            "method": "first_person_investigation",
            "evidence_threshold": 0.80,
            "reproducibility_required": True,
        },
    }

    fw = frameworks.get(framework, frameworks["western_academic"])
    return {
        "claim": claim,
        "framework": framework,
        "method": fw["method"],
        "threshold": fw["evidence_threshold"],
        "status": "pending_evaluation"
    }

result = evaluate_ontological_claim(
    "Consciousness can emerge in non-biological substrates",
    framework="contemplative_science"
)
print(result)
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Parallel Sciences",
  "purpose": "General-purpose detection sensor",
  "signals": [
    {
      "name": "primary_signal",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "secondary_signal",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["docs/philosophy/parallel-sciences.md"],
    "community_feedback": []
  }
}
```
