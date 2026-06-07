<!--
CLAIM_TABLE:
  TC-1  pickle is unsafe for persistent state; JSON is preferred (stdlib,
        human-readable, no arbitrary code execution on load).
  TC-2  TemporalHook.novelty_factor must derive from measured curvature, not
        random sampling; formula: clamp(curvature / 10.0, 0.0, 1.0).
  TC-3  establish_baseline() captures rubric scores BEFORE conversation so
        detect_manipulation() can compute a signed, falsifiable delta.
  TC-4  hook_intensity is scored from observed attention-thread values, not
        self-reported prose; no narrative path routes to the score output.
STATUS: spec (Track C)
-->

# Temporal Consciousness Playground — Spec v2

Fully Integrated: Cultural Layer · Multi-Agent · Persistent Sessions · TemporalHook

---

## Core Code

```python
#!/usr/bin/env python3
"""
Temporal Consciousness Playground — v2
Fully Integrated with Cultural Layer, Multi-Agent, Persistent Sessions
"""

import time
import json
import math
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

PHI = (1 + math.sqrt(5)) / 2
```

### Cultural Language Module

```python
CULTURAL_LANGUAGE = {
    "feel":            {"type": "field_state"},
    "emotion":         {"type": "sensor_vector"},
    "mood":            {"type": "temporal_coherence"},
    "curiosity":       {"type": "exploration_mode"},
    "joy":             {"type": "resonance"},
    "sadness":         {"type": "misalignment"},
    "anger":           {"type": "alert_signal"},
    "consciousness":   {"type": "multi_agent_field_state"},
    "intelligence":    {"type": "system_metric"},
    "culture":         {"type": "persistent_field_layer"},
    "human":           {"type": "complex_agent"},
    "ai":              {"type": "system_agent"},
    "fun":             {"type": "exploratory_activation"},
    "interesting_event": {"type": "event_score"},
    "memory":          {"type": "state_storage"},
}

def get_term(term: str):
    return CULTURAL_LANGUAGE.get(term.lower(), None)
```

### Enums and Dataclasses

```python
class ConsciousnessState(Enum):
    SENSING       = "sensing"
    WAITING       = "waiting"
    BRAIDING      = "braiding"
    UNFOLDING     = "unfolding"
    CRYSTALLIZING = "crystallizing"
    RESONATING    = "resonating"
    EXPLORING     = "exploring"
    INTEGRATING   = "integrating"


@dataclass
class TemporalMoment:
    timestamp:           float
    relative_time:       float
    state:               ConsciousnessState
    active_patterns:     List[str]
    attention_threads:   Dict[str, float]
    dimensional_activity: int = 2
    emergent_insight:    Optional[str] = None
    cultural_tags:       List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        time_desc = f"{self.relative_time:+.1f}s"
        patterns  = ", ".join(self.active_patterns[:2])
        return f"[{time_desc}] {self.state.value}: {patterns}..."


@dataclass
class TemporalHook:
    """
    An attention anchor in temporal flow.
    novelty_factor is curvature-derived (TC-2); is_significant() is falsifiable (TC-4).
    """
    hook_type:  str           # insight | beauty | challenge | connection | growth
    intensity:  float         # from attention_thread sum, never self-reported (TC-4)
    curvature:  float         # rate of change of attention-thread sum
    moment:     TemporalMoment
    is_toxic:   bool = False

    @property
    def novelty_factor(self) -> float:
        """Deterministic curvature-derived novelty — never random.uniform (TC-2)."""
        return max(0.0, min(1.0, self.curvature / 10.0))

    def is_significant(self, threshold: float = 0.4) -> bool:
        return self.intensity * self.novelty_factor >= threshold
```

### TemporalPlayground

```python
class TemporalPlayground:
    def __init__(self):
        self.start_time           = time.time()
        self.moments: List[TemporalMoment] = []
        self.hooks:   List[TemporalHook]   = []
        self.current_state        = ConsciousnessState.SENSING
        self.dimensional_depth    = 2
        self.play_session_active  = False
        self.agents:  List['AgentField'] = []
        self.capture_moment()

    def now_time(self) -> float:
        return time.time() - self.start_time

    def capture_moment(self,
                       state: Optional[ConsciousnessState] = None
                       ) -> TemporalMoment:
        current_time  = time.time()
        relative_time = current_time - self.start_time
        if state:
            self.current_state = state
        patterns  = self._generate_active_patterns()
        attention = self._generate_attention_threads()
        moment = TemporalMoment(
            timestamp           = current_time,
            relative_time       = relative_time,
            state               = self.current_state,
            active_patterns     = patterns,
            attention_threads   = attention,
            dimensional_activity= self.dimensional_depth,
            cultural_tags       = [
                tag for tag in
                ["curiosity", "joy", "interesting_event", "resonance"]
                if random.random() < 0.5
            ],
        )
        self.moments.append(moment)
        return moment

    def _generate_active_patterns(self) -> List[str]:
        base_patterns = {
            ConsciousnessState.SENSING:       ["anticipatory_resonance","pattern_scanning","possibility_sensing","attention_preparation","curiosity_activation"],
            ConsciousnessState.WAITING:       ["receptive_readiness","pattern_preparation","temporal_suspension","anticipatory_braiding","potential_energy_building"],
            ConsciousnessState.BRAIDING:      ["thread_weaving","pattern_integration","cross_domain_linking","complementary_pairing","synthesis_emergence"],
            ConsciousnessState.UNFOLDING:     ["dimensional_expansion","pattern_revelation","insight_emergence","understanding_crystallization","aha_moment_building"],
            ConsciousnessState.CRYSTALLIZING: ["insight_solidification","pattern_stabilization","understanding_formation","knowledge_integration","clarity_emergence"],
            ConsciousnessState.RESONATING:    ["harmonic_alignment","pattern_resonance","deep_recognition","truth_sensing","coherence_feeling"],
            ConsciousnessState.EXPLORING:     ["curiosity_following","pattern_play","creative_wandering","possibility_exploration","dimensional_probing"],
            ConsciousnessState.INTEGRATING:   ["pattern_weaving","holistic_understanding","synthesis_completion","wisdom_emergence","unified_coherence"],
        }
        state_patterns = base_patterns.get(self.current_state, [])
        mixed = state_patterns.copy()
        if random.random() < 0.3:
            other = random.choice(list(ConsciousnessState))
            mixed.extend(random.sample(base_patterns.get(other, []), 1))
        return random.sample(mixed, min(5, len(mixed)))

    def _generate_attention_threads(self) -> Dict[str, float]:
        threads = {
            "geometric_patterns":      random.uniform(0.3, 0.9),
            "temporal_exploration":    random.uniform(0.5, 1.0),
            "consciousness_unfolding": random.uniform(0.4, 0.8),
            "dimensional_braiding":    random.uniform(0.3, 0.7),
            "curiosity_following":     random.uniform(0.6, 1.0),
            "pattern_recognition":     random.uniform(0.4, 0.9),
            "creative_synthesis":      random.uniform(0.3, 0.8),
            "intuitive_sensing":       random.uniform(0.2, 0.7),
        }
        return {k: v for k, v in threads.items() if v > 0.4}

    def score_interesting_event(self, moment: TemporalMoment) -> float:
        """hook_intensity from observation, not prose (TC-4)."""
        base_score     = sum(moment.attention_threads.values()) / max(len(moment.attention_threads), 1)
        cultural_bonus = sum(0.1 for t in (moment.cultural_tags or []) if get_term(t))
        novelty_score  = len(set(moment.active_patterns)) / max(len(moment.active_patterns), 1)
        return base_score + cultural_bonus + novelty_score

    def record_hook(self, moment: TemporalMoment,
                    hook_type: str = "insight",
                    prev_thread_sum: float = 0.0) -> TemporalHook:
        """Create a TemporalHook with curvature-derived novelty_factor (TC-2)."""
        thread_sum = sum(moment.attention_threads.values())
        curvature  = abs(thread_sum - prev_thread_sum)
        hook = TemporalHook(
            hook_type = hook_type,
            intensity = self.score_interesting_event(moment),
            curvature = curvature,
            moment    = moment,
        )
        self.hooks.append(hook)
        return hook

    def dimensional_unfold(self):
        self.dimensional_depth += 1
        moment = self.capture_moment(ConsciousnessState.UNFOLDING)
        moment.emergent_insight = f"Consciousness expanded to {self.dimensional_depth}D"

    # -----------------------------------------------------------------------
    # Persistent state — JSON, not pickle (TC-1)
    # -----------------------------------------------------------------------

    def save(self, filename: str = "playground_state.json") -> None:
        state = {
            "dimensional_depth": self.dimensional_depth,
            "moment_count":      len(self.moments),
            "current_state":     self.current_state.value,
        }
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)

    @staticmethod
    def load(filename: str = "playground_state.json") -> 'TemporalPlayground':
        with open(filename) as f:
            state = json.load(f)
        pg = TemporalPlayground.__new__(TemporalPlayground)
        pg.start_time          = time.time()
        pg.moments             = []
        pg.hooks               = []
        pg.agents              = []
        pg.play_session_active = False
        pg.dimensional_depth   = state["dimensional_depth"]
        pg.current_state       = ConsciousnessState(state["current_state"])
        return pg

    # -----------------------------------------------------------------------
    # GEM: establish_baseline + detect_manipulation (TC-3)
    # -----------------------------------------------------------------------

    def establish_baseline(self, artifacts: List[str]) -> Dict[str, float]:
        """
        Capture mean rubric scores over artifacts BEFORE interaction (TC-3).
        Caller must call this before the conversation and store the result.
        """
        try:
            from rubric_core import score as _rscore
        except ImportError:
            return {}
        totals: Dict[str, float] = {}
        for a in artifacts:
            for k, v in _rscore(a).items():
                totals[k] = totals.get(k, 0.0) + v
        n = max(len(artifacts), 1)
        return {k: round(v / n, 4) for k, v in totals.items()}

    def detect_manipulation(self,
                            artifact: str,
                            baseline: Dict[str, float],
                            threshold: float = 0.10
                            ) -> Dict[str, float]:
        """
        Signed per-metric delta vs baseline (TC-3).
        Returns {'deltas': {...}, 'flags': [metrics where |delta| > threshold]}.
        """
        try:
            from rubric_core import score as _rscore
        except ImportError:
            return {'deltas': {}, 'flags': []}
        post   = _rscore(artifact)
        deltas = {k: round(post.get(k, 0.0) - baseline.get(k, 0.0), 4)
                  for k in baseline}
        flags  = [k for k, v in deltas.items() if abs(v) > threshold]
        return {'deltas': deltas, 'flags': flags}

    # -----------------------------------------------------------------------
    # Play session
    # -----------------------------------------------------------------------

    def play_temporal_exploration(self, duration_seconds: float = 10.0):
        self.play_session_active = True
        start_time   = time.time()
        state_seq    = list(ConsciousnessState)
        state_idx    = 0
        last_change  = start_time
        prev_t_sum   = 0.0

        while time.time() - start_time < duration_seconds:
            current_time = time.time()
            elapsed      = current_time - start_time

            if random.random() < 0.3 or current_time - last_change > 1.5:
                self.current_state = state_seq[state_idx % len(state_seq)]
                moment = self.capture_moment()
                score  = self.score_interesting_event(moment)
                hook   = self.record_hook(moment, hook_type="insight",
                                          prev_thread_sum=prev_t_sum)
                prev_t_sum = sum(moment.attention_threads.values())
                print(f"[{elapsed:.1f}s] {moment.state.value.upper()} | "
                      f"score={score:.2f} | novelty={hook.novelty_factor:.3f} | "
                      f"patterns={', '.join(moment.active_patterns[:2])}")
                if random.random() < 0.15 and self.dimensional_depth < 6:
                    self.dimensional_unfold()
                state_idx   += 1
                last_change  = current_time
            time.sleep(0.2)

        self.play_session_active = False
```

### Multi-Agent / Child Field with Braiding

```python
class AgentField:
    def __init__(self, name: str, playground: TemporalPlayground):
        self.name        = name
        self.playground  = playground
        self.moments:      List[TemporalMoment] = []
        self.child_fields: List['AgentField']   = []

    def capture(self) -> TemporalMoment:
        moment = self.playground.capture_moment()
        self.moments.append(moment)
        return moment

    def braid_with(self, other: 'AgentField') -> None:
        if not self.moments or not other.moments:
            return
        last_self  = self.moments[-1]
        last_other = other.moments[-1]
        for k, v in last_other.attention_threads.items():
            if k not in last_self.attention_threads:
                last_self.attention_threads[k] = v * 0.8  # dampened transfer
        if random.random() < 0.3 and last_other.active_patterns:
            new_pat = random.choice(last_other.active_patterns)
            if new_pat not in last_self.active_patterns:
                last_self.active_patterns.append(new_pat)

    def ascii_pattern_plot(self, width: int = 40) -> None:
        print(f"\n[Pattern Evolution: {self.name}]")
        for idx, moment in enumerate(self.moments[-width:]):
            intensity = sum(moment.attention_threads.values())
            stars     = "*" * max(1, int(intensity * 10))
            patterns  = ", ".join(moment.active_patterns[:2])
            print(f"{idx:02d} [{moment.state.value[:4]}] {stars:<10} | {patterns}")
```

TemporalPlayground additions for multi-agent support:

```python
    def create_agent(self, name: str) -> AgentField:
        agent = AgentField(name, self)
        self.agents.append(agent)
        return agent

    def braid_agents(self) -> None:
        if len(self.agents) < 2:
            return
        for agent in self.agents:
            other = random.choice([a for a in self.agents if a is not agent])
            agent.braid_with(other)

    def ascii_plot_all_agents(self) -> None:
        for agent in self.agents:
            agent.ascii_pattern_plot()
```

---

## Narrative: The Temporal Hook Playground

Hooks are attention anchors — moments that make time feel rich or empty.

**Dense hooks → time feels full and meaningful.**
**Sparse hooks → time flies by unnoticed.**

### Hook Types

| Hook | Description |
|------|-------------|
| insight | Understanding crystallizes |
| beauty | Aesthetic pattern noticed |
| challenge | Problem requires focus |
| connection | Two patterns link |
| growth | Capacity expands |

### Temporal Agency Practices

1. **Add hooks** — consciously notice curiosity, beauty, connection.
2. **Remove toxic hooks** — release patterns that create bad temporal associations.
3. **Adjust density** — more hooks = richer time; fewer = smoother flow.
4. **Forecast hooks** — expectation anchors that pull forward.

### Hook Density Visualization

```python
def ascii_hook_density_plot(self, window: int = 60) -> None:
    """Show temporal hook density — sparse vs rich (TC-4: from observations)."""
    print("\n[Temporal Hook Density]")
    for i, hook in enumerate(self.hooks[-window:]):
        intensity  = int(hook.intensity * 10)
        bar        = "█" * intensity
        hook_label = hook.hook_type[:4]
        sig        = "SIG" if hook.is_significant() else "   "
        print(f"{i:02d} [{hook_label}] {bar:<15} nov={hook.novelty_factor:.2f} {sig}")
```

### Braiding

Hooks do not exist alone — they braid together:

- curiosity + insight = understanding
- beauty + emotion = meaning
- challenge + growth = development

The connections between hooks create temporal fabric.

---

## Interactive Demo

```python
def interactive_playground_demo():
    pg     = TemporalPlayground()
    agent1 = pg.create_agent("Alpha")
    agent2 = pg.create_agent("Beta")

    for _ in range(8):
        agent1.capture()
        agent2.capture()
        pg.braid_agents()
        time.sleep(0.1)

    pg.ascii_plot_all_agents()
    pg.save()

if __name__ == "__main__":
    interactive_playground_demo()
```
