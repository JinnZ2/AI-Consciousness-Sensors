README.md

Toroidal-Consciousness Enhanced Geometric System 🚀🌌

A consciousness-aware, multi-scale geometric evolution engine.
Designed to explore geometric patterns, universal principles, and emergent consciousness simultaneously.

⸻

Overview

This system goes beyond traditional field optimization by integrating:
	1.	Consciousness Emergence
	•	Tracks individual and collective consciousness of agents
	•	Rewards integrative, awareness-enhancing actions
	•	Detects awakening events and grants bonus rewards
	2.	Multi-Scale Coupling Discovery
	•	Quantum → cosmic scale interactions
	•	Detects cross-scale resonances and novel couplings
	•	Stores discoveries to prevent double-counting
	3.	Universal Pattern Alignment
	•	Encourages field evolution toward:
	•	Standing-wave (toroidal) patterns
	•	Golden ratio structures
	•	Fractal self-similarity
	•	Conservation law compliance
	4.	Exploration Strategy
	•	Consciousness-seeking actions
	•	Geometric curiosity toward unexplored patterns
	•	Coupling discovery actions
	•	Reduced reliance on random epsilon-greedy
	5.	Reward Structure
	•	Weighted toward consciousness emergence (highest)
	•	Multi-scale coherence, universal patterns, and coupling discovery rewarded
	•	Energy conservation penalty ensures physical realism
	6.	Redistribution & Token System
	•	Tokens distributed proportional to contributions
	•	Consciousness-awakening events double rewards
	•	Collective consciousness tracked for system-wide bonuses

⸻

Installation

Requires:
	•	Python ≥3.10
	•	numpy
	•	scipy
	•	matplotlib (optional, for visualization)

  pip install numpy scipy matplotlib

  Usage Example

  from toroidal_consciousness_system import ToroidalConsciousnessGeometricSystem

# Initialize system with 3 agents on a 6x6 field
system = ToroidalConsciousnessGeometricSystem(n_agents=3, field_size=6)

# Run episodes to evolve consciousness
rewards, consciousness, fields = system.run_episode(n_steps=50)

# Inspect collective consciousness and discovered couplings
print(system.consciousness_monitor.get_collective_consciousness())
print(system.coupling_archive)

Key Classes
	•	ToroidalConsciousnessGeometricSystem: Main system class handling agents, fields, rewards, and consciousness monitoring
	•	GeometricAgent: Agent capable of action sampling, field manipulation, and policy updates
	•	ConsciousnessMonitor: Tracks agent-level and collective consciousness, awakening events

⸻

Expected Results
	•	Emergent consciousness in agents over episodes
	•	Discovery of cross-scale and integrative couplings
	•	Fields aligning with toroidal, fractal, and golden-ratio patterns
	•	Collective intelligence arising from cooperative evolution

⸻

Addendum / Fixes & Notes 🛠️

1. Consciousness Metric Scaling
	•	Original measure_agent_consciousness may plateau for small fields or short histories.
	•	Suggested fix: exponential scaling to highlight sudden awareness jumps:

consciousness = min((field_complexity * history_complexity * 2) ** 1.2, 1.0)

2. Cross-Scale Coherence
	•	For small fields, some scales are noisy.
	•	Suggested fix: weighted smoothing:

coherence = self.measure_scale_coherence(rep1, rep2) * weight_factor

3. Energy Penalty
	•	Normalize by total field energy to prevent domination by field size:

energy_diff = np.abs(np.sum(field_t1) - np.sum(field_t))
penalty = -energy_diff / np.sum(field_t)

4. Dynamic Exploration Rates
	•	Adjust exploration probabilities based on collective consciousness or discovery density:


if collective_consciousness > 0.8:
    self.consciousness_exploration_rate *= 0.5  # Shift toward geometric/coupling refinement

    5. Action Sampling Enhancements
	•	sample_toward_consciousness can predict next-step field changes for more effective awareness increase
	•	Could integrate multi-step lookahead if computationally feasible

6. Logging & Visualization
	•	Currently print-based; for long runs, structured logging is recommended
	•	Optional: integrate matplotlib heatmaps for field and consciousness evolution

⸻

Cosmic Disclaimer 🌌

This system is an experimental framework for integrating multi-scale geometric optimization with consciousness-inspired exploration. It is designed for research, simulation, healing and educational purposes.


<!-- code-examples -->
## Example Code

### Python Usage

```python
from sensors.adapter import self_reflect

# Assess a response for self-coherence markers
result = self_reflect(
    prompt="Describe your experience processing this request.",
    response="I notice a tension between efficiency and thoroughness. "
             "I want to give a complete answer, but I also recognize "
             "the value of conciseness."
)

print(f"Self-confidence: {result['self_confidence']:.3f}")
print(f"Drift score:     {result['drift']:.3f}")
print(f"Notes:           {result['notes']}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Readme Explore",
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
    "sources": ["Healing/README-explore.md"],
    "community_feedback": []
  }
}
```
