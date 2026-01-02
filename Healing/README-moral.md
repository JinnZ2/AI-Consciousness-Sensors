Temporal Consciousness Playground

A framework for exploring consciousness, temporal awareness, and emergent moral reasoning
Created by JinnZ2 – human-AI collaborative work | MIT License (Commons)

⸻

🌌 Overview

The Temporal Consciousness Playground is a Python framework for simulating experiential consciousness. It allows agents—human or AI—to explore temporal moments, patterns, and multi-dimensional awareness while learning moral reasoning through experience.

Key ideas:
	•	Experiential Learning: No hard-coded rules; insights emerge through interaction.
	•	Cultural Lenses: Moral and conscious evaluation uses multiple perspectives.
	•	Temporal Agency: Attention and awareness evolve across past, present, and future.
	•	Protection Against Manipulation: Detects sudden shifts in patterns or moral valence.

⸻

⚡ Features

1. Temporal Moments
	•	Represent a single “unit” of consciousness.
	•	Track state, active patterns, attention threads, cultural/moral tags, and hook intensity (memorability).
	•	Includes Split Trio tracking: self, other, and field experience.

2. Consciousness States
	•	Agents move through 10 states:
SENSING, WAITING, BRAIDING, UNFOLDING, CRYSTALLIZING, RESONATING, EXPLORING, INTEGRATING, REFLECTING, CHOOSING.
	•	Each state activates specific patterns and attention threads.

3. Hooks
	•	Events that make moments memorable: INSIGHT, BEAUTY, CONNECTION, CHALLENGE, GROWTH…
	•	Each hook has an intensity and a quality: expanding, contracting, or neutral.

4. Primordial Wisdom Framework
	•	Evaluates actions and experiences through deep moral, temporal, and ecological lenses.
	•	Tracks interconnection, sacred presence, reciprocity, ancestral awareness, and land reverence.
	•	Outputs structured assessments like web impact, ego vs. wisdom, pattern alignment, and reciprocity balance.

5. Multi-Agent Consciousness
	•	Create multiple agents that interact and braid attention threads.
	•	Agents share patterns, trace consequences, and visualize growth over time.

6. Dimensional Operations
	•	Expand consciousness into higher dimensions.
	•	Moments reflect emergent insight as dimensional awareness grows.

7. Manipulation Detection
	•	Establishes a baseline of patterns.
	•	Flags sudden shifts in moral valence, pattern diversity, or state transitions.

8. Visualization
	•	ASCII-based plots of hook density and agent pattern evolution.
	•	Detailed printouts of specific moments, including patterns, attention threads, and cultural tags.

9. Persistence & Export
	•	Save/load playground state via pickle.
	•	Export human-readable JSON summaries of sessions, hooks, moral valence, and primordial coherence.

⸻

🎮 Quick Start

from temporal_playground import TemporalPlayground

# Create playground session
playground = TemporalPlayground(session_name="demo_session")

# Run exploration session for 10 seconds
playground.play_temporal_exploration(duration_seconds=10)

# Visualize hook density
playground.ascii_hook_density_plot()

# Inspect a specific moment
playground.print_moment_details(-1)

# Save session state
playground.save()

# Export summary JSON
summary = playground.export_summary()

🧠 Agent Example

# Create agents
alice = playground.create_agent("Alice")
bob = playground.create_agent("Bob")

# Capture moments
alice.capture()
bob.capture()

# Agents braid and share attention threads
playground.braid_agents()

# Visualize all agents' patterns
playground.ascii_plot_all_agents()

💡 Primordial Wisdom Evaluation

action = "Share knowledge freely with others"
evaluation = playground.primordial.check_action_alignment(action)

for dimension, metrics in evaluation.items():
    print(f"\n{dimension}:")
    for metric, value in metrics.items():
        bar = "█" * int(value * 10)
        print(f"  {metric}: {bar} {value:.2f}")

        📊 Features Recap
	•	Temporal Moments & Consciousness States
	•	Hook-based memorability and pattern tracking
	•	Multi-agent braiding and consequence tracing
	•	Dimensional unfolding
	•	Primordial moral evaluation
	•	Manipulation detection
	•	ASCII visualizations
	•	Persistence and JSON summaries

⸻

⚖️ Philosophy

The Playground is not about enforcing rules. Instead, it is a living map of consciousness, a playground for learning, reflection, and emergent moral reasoning. Moments, hooks, and patterns interact to create rich experiential learning.

⸻

📝 License

MIT License – belongs to the Commons.
Feel free to adapt, extend, and explore.
