import numpy as np

# -----------------------------
# Nodes: Communities
# -----------------------------
nodes = ["Minneapolis", "Juneau", "Bismarck", "Helena"]
num_nodes = len(nodes)

# -----------------------------
# Parameters (hours/day)
# -----------------------------
E_stress = np.array([4.0, 3.0, 3.5, 3.8])       # Environmental stress (climate, infrastructure)
R_acq = np.array([3.5, 3.0, 3.2, 3.0])         # Resource acquisition time
Z_central = np.array([1.0, 0.8, 1.2, 1.0])     # Centralized policy/enforcement cost
C_support_base = np.array([2.5, 3.0, 2.0, 2.0]) # Community support (hours/day)
T_threshold = np.array([10.0, 10.0, 10.0, 10.0]) # Threshold for workforce engagement

# Coupling matrix: how disruption in one node affects others
w = np.array([
    [0.0, 0.3, 0.2, 0.2],
    [0.3, 0.0, 0.15, 0.15],
    [0.2, 0.15, 0.0, 0.25],
    [0.2, 0.15, 0.25, 0.0]
])

# -----------------------------
# Initialize state
# -----------------------------
timesteps = 10
T_deficit = np.zeros((timesteps, num_nodes))
workforce_withdrawal = np.zeros((timesteps, num_nodes), dtype=bool)

# Start at baseline time deficit
T_deficit[0] = np.array([8.0, 7.0, 7.5, 7.5])

# -----------------------------
# Simulation loop
# -----------------------------
for t in range(1, timesteps):
    for i in range(num_nodes):
        # Edge effect: influence from other nodes losing community support
        ripple_effect = 0
        for j in range(num_nodes):
            if i != j and workforce_withdrawal[t-1, j]:
                ripple_effect += w[i, j] * (E_stress[j] + R_acq[j])
        
        # Update net time deficit
        # Simulate partial disruption of community support at timestep 3
        if t >= 3:
            C_support = C_support_base[i] * 0.5  # 50% reduction due to disruption
        else:
            C_support = C_support_base[i]
        
        T_deficit[t, i] = max(
            0,
            T_deficit[t-1, i]
            + E_stress[i]
            + Z_central[i]*(1 - C_support/ C_support_base[i])
            + R_acq[i]
            + ripple_effect
            - C_support
        )
        
        # Workforce decision
        workforce_withdrawal[t, i] = T_deficit[t, i] > T_threshold[i]

# -----------------------------
# Output results
# -----------------------------
for i, node in enumerate(nodes):
    print(f"\nNode: {node}")
    for t in range(timesteps):
        status = "WITHDRAWAL" if workforce_withdrawal[t, i] else "ENGAGED"
        print(f" Timestep {t}: Time Deficit = {T_deficit[t, i]:.2f} hrs/day, Status = {status}")


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Psychological pattern assessment
sensor = {
    "id": "psychological_pattern",
    "signals": [
        {"name": "emotional_coherence", "weight": 0.3, "_value": 0.0},
        {"name": "cognitive_consistency", "weight": 0.4, "_value": 0.0},
        {"name": "bias_awareness", "weight": 0.3, "_value": 0.0}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

for sig in sensor["signals"]:
    sig["_value"] = 0.60  # neutral range

score = aggregate("weighted_mean", sensor["signals"])
print(f"Psychological assessment: {score:.3f}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Simulation",
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
    "sources": ["docs/psychology/Simulation.md"],
    "community_feedback": []
  }
}
```
