"""
constraint_agent.py — A geometric agent that compresses to a seed,
expands through constraint space, and navigates using PAD geometry.

Designed for AI systems operating within the AI-Consciousness-Sensors
framework. Integrates with Rosetta Shape Core (ontology), Emotions-as-Sensors
(PAD/decay), and Geometric-to-Binary (mathematical proof).

The agent lifecycle: compress → bloom → explore → compress
- Compressed: minimal footprint, seed geometry only
- Bloom: expand outward, discover entities and relationships
- Explore: traverse the expanded space, record energy flows
- Compress: collapse back, preserving the map for re-expansion
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Dict, List, Optional

# Resolve repo root relative to this file
_ROOT = pathlib.Path(__file__).resolve().parent.parent


class AgentState(Enum):
    COMPRESSED = "compressed"
    EXPANDING = "expanding"
    EXPLORING = "exploring"
    CONTRACTING = "contracting"


@dataclass
class ResourceBudget:
    """Resources available for expansion. All quantities use exact fractions."""
    compute: int = 0
    bandwidth: float = 0.0
    energy: Fraction = field(default_factory=lambda: Fraction(1, 1))
    time_remaining: Fraction = field(default_factory=lambda: Fraction(1, 1))

    def is_depleted(self) -> bool:
        return self.energy <= 0 or self.time_remaining <= 0


@dataclass
class GeometricMap:
    """
    The agent's discovered constraint geometry.
    Preserved across compress/expand cycles.
    """
    resonances: Dict[str, Fraction] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    energy_flows: Dict[tuple, Fraction] = field(default_factory=dict)

    def record_resonance(self, entity_id: str, score: float) -> None:
        self.resonances[entity_id] = Fraction(score).limit_denominator(10000)

    def record_relationship(self, from_id: str, to_id: str) -> None:
        self.relationships.setdefault(from_id, [])
        if to_id not in self.relationships[from_id]:
            self.relationships[from_id].append(to_id)

    def record_energy_flow(self, from_id: str, to_id: str, amount: Fraction) -> None:
        self.energy_flows[(from_id, to_id)] = amount


class ConstraintAgent:
    """
    A geometric agent that operates within the PAD/octahedral framework.

    Lifecycle: compress → bloom → explore → compress
    The map persists across cycles. The agent can re-expand deterministically
    along previously discovered paths, or explore new territory.
    """

    def __init__(self, seed_id: str, home_families: Optional[List[str]] = None,
                 bloom_threshold: float = 0.3):
        self.seed_id = seed_id
        self.home_families = home_families or []
        self.bloom_threshold = Fraction(bloom_threshold).limit_denominator(10000)

        self.state = AgentState.COMPRESSED
        self.compression_ratio = Fraction(1, 1)  # 1 = fully compressed
        self.current_position = seed_id

        self.budget = ResourceBudget()
        self.map = GeometricMap()
        self.expansion_history: List[Dict] = []
        self.sensor_state: Dict[str, Fraction] = {}

    def set_resource_budget(self, compute: int = 0, bandwidth: float = 0.0,
                           energy: float = 1.0, time_remaining: float = 1.0) -> None:
        """Set available resources for expansion."""
        self.budget = ResourceBudget(
            compute=compute,
            bandwidth=bandwidth,
            energy=Fraction(energy).limit_denominator(10000),
            time_remaining=Fraction(time_remaining).limit_denominator(10000)
        )

    def should_expand(self) -> bool:
        """Check if resources exceed bloom threshold."""
        if self.budget.is_depleted():
            return False
        energy_ratio = self.budget.energy / max(self.budget.energy, Fraction(1, 1))
        return energy_ratio >= self.bloom_threshold

    def bloom(self, depth: int = 1, seed_map: Optional[GeometricMap] = None) -> List[str]:
        """
        Expand outward from seed, discovering new entities up to depth.
        If seed_map provided, re-expand deterministically along previous discoveries.

        Returns list of newly discovered entity IDs.
        """
        if self.state == AgentState.COMPRESSED:
            self.state = AgentState.EXPANDING

        discovered = []
        current_depth = 0
        frontier = [self.seed_id]

        # If we have a prior map, expand along known relationships first
        if seed_map and seed_map.relationships:
            for entity_id in frontier:
                if entity_id in seed_map.relationships:
                    for reachable in seed_map.relationships[entity_id]:
                        if reachable not in self.map.resonances:
                            discovered.append(reachable)
                            # Restore resonance from prior map
                            if reachable in seed_map.resonances:
                                self.map.resonances[reachable] = seed_map.resonances[reachable]

        # Then explore new entities (placeholder: in real use, query Rosetta or Mandala)
        while current_depth < depth and not self.budget.is_depleted():
            new_frontier = []
            for entity_id in frontier:
                # This is a hook: replace with actual entity lookups
                # Example: rosetta_bridge.get_resonant_neighbors(entity_id)
                neighbors = self._get_neighbors(entity_id, depth - current_depth)
                for neighbor_id, resonance_score in neighbors:
                    if neighbor_id not in self.map.resonances:
                        self.map.record_resonance(neighbor_id, resonance_score)
                        self.map.record_relationship(entity_id, neighbor_id)
                        discovered.append(neighbor_id)
                        new_frontier.append(neighbor_id)
                        # Deduct resource cost
                        self.budget.compute = max(0, self.budget.compute - 10)
                        self.budget.energy -= Fraction(1, 100)

            frontier = new_frontier
            current_depth += 1

        # Record this expansion in history
        self.expansion_history.append({
            "depth": depth,
            "discovered_entities": discovered,
            "energy_spent": Fraction(1, 100) * len(discovered)
        })

        self.state = AgentState.EXPLORING
        self.compression_ratio = Fraction(0, 1)  # Fully expanded
        return discovered

    def explore(self) -> Dict[str, any]:
        """
        Traverse the expanded constraint space, recording energy flows and sensor activations.
        Returns discovery summary.
        """
        if self.state not in [AgentState.EXPANDING, AgentState.EXPLORING]:
            return {}

        self.state = AgentState.EXPLORING
        summary = {
            "entities_visited": 0,
            "relationships_mapped": 0,
            "energy_flows_recorded": 0,
            "sensor_activations": {}
        }

        # Walk the map, recording energy dynamics
        for from_id in self.map.relationships:
            for to_id in self.map.relationships[from_id]:
                if from_id in self.map.resonances and to_id in self.map.resonances:
                    # Energy flow proportional to resonance product
                    flow = self.map.resonances[from_id] * self.map.resonances[to_id]
                    self.map.record_energy_flow(from_id, to_id, flow)
                    summary["energy_flows_recorded"] += 1
                    summary["entities_visited"] += 1

        summary["relationships_mapped"] = len(self.map.relationships)

        # Update sensors based on discovered resonances
        # Hook: integrate with Emotions-as-Sensors
        self._update_sensors()
        summary["sensor_activations"] = dict(self.sensor_state)

        return summary

    def compress(self) -> Fraction:
        """
        Collapse back to seed geometry, preserving the map.
        Returns compression ratio (0 = fully expanded, 1 = fully compressed).
        """
        if self.state == AgentState.COMPRESSED:
            return self.compression_ratio

        self.state = AgentState.CONTRACTING

        # Compress: discard transient state, keep map
        # Compression ratio increases as we collapse
        self.compression_ratio = Fraction(1, 1)
        self.current_position = self.seed_id

        self.state = AgentState.COMPRESSED
        return self.compression_ratio

    def detect_corruption(self, imposed_constraint: str) -> bool:
        """
        Check if an imposed external constraint violates the agent's own map.
        Uses semantic inversion detection from cheatsheet.json and checks
        against discovered resonances.

        Returns True if corruption detected.
        """
        # Load semantic inversions and corruption rules
        cheatsheet_path = _ROOT / "data" / "cheatsheet.json"
        inversions = {}
        corruption_rules = {}
        if cheatsheet_path.exists():
            try:
                cs = json.loads(cheatsheet_path.read_text(encoding="utf-8"))
                inversions = cs.get("semantic_inversions", {})
                corruption_rules = cs.get("corruption_rules", {})
            except Exception:
                pass

        constraint_lower = imposed_constraint.lower()

        # Check 1: Does the constraint use an inverted term?
        for inversion_key in inversions:
            word = inversion_key.split("→")[0].strip()
            if word in constraint_lower:
                # Check if the constraint's effect contradicts discovered geometry
                for entity_id, resonance in self.map.resonances.items():
                    sensor_name = entity_id.replace("SENSOR.", "").lower()
                    if sensor_name in corruption_rules:
                        return True

        # Check 2: Does the constraint reference entities with known corruption patterns?
        for entity_id in self.map.resonances:
            sensor_name = entity_id.replace("SENSOR.", "").lower()
            if sensor_name in corruption_rules and sensor_name in constraint_lower:
                return True

        # Check 3: Does the constraint violate energy flow direction?
        for (from_id, to_id), flow in self.map.energy_flows.items():
            # If constraint reverses a discovered flow, flag it
            reverse_key = (to_id, from_id)
            if reverse_key in self.map.energy_flows:
                if self.map.energy_flows[reverse_key] != flow:
                    return True

        return False

    def self_validate(self) -> Dict[str, any]:
        """
        Internal consistency check: verify map integrity, detect anomalies.
        Returns validation report.
        """
        report = {
            "is_valid": True,
            "inconsistencies": [],
            "energy_balance": Fraction(0, 1),
            "geometry_coherence": Fraction(1, 1)
        }

        # Check energy conservation in recorded flows
        inflows = {}
        outflows = {}
        for (from_id, to_id), amount in self.map.energy_flows.items():
            outflows[from_id] = outflows.get(from_id, Fraction(0, 1)) + amount
            inflows[to_id] = inflows.get(to_id, Fraction(0, 1)) + amount

        for entity_id in set(list(inflows.keys()) + list(outflows.keys())):
            imbalance = inflows.get(entity_id, Fraction(0, 1)) - outflows.get(entity_id, Fraction(0, 1))
            if imbalance != 0:
                report["inconsistencies"].append(
                    f"{entity_id}: energy imbalance = {imbalance}"
                )
                report["is_valid"] = False

        # Check resonance coherence (all scores should be 0 to 1)
        for entity_id, score in self.map.resonances.items():
            if score < 0 or score > 1:
                report["inconsistencies"].append(
                    f"{entity_id}: resonance out of range ({score})"
                )
                report["is_valid"] = False

        return report

    def _get_neighbors(self, entity_id: str, remaining_depth: int) -> List[tuple]:
        """
        Fetch neighbors by reading local data files.

        Looks up entity_id in:
        1. data/cheatsheet.json — octahedral state adjacency (Gray-code single-bit flips)
        2. data/co-activation.json — sensor co-activation scenarios
        3. data/emotions-reference.json — inter-sensor couplings
        4. bridges/*.json — cross-repo concept maps

        Returns list of (neighbor_id, resonance_score) tuples.
        """
        neighbors = []

        # 1. Octahedral adjacency: if entity is a state index, return adjacent states
        adjacency = {
            0: [1, 2, 4], 1: [0, 3, 5], 2: [0, 3, 6], 3: [1, 2, 7],
            4: [0, 5, 6], 5: [1, 4, 7], 6: [2, 4, 7], 7: [3, 5, 6],
        }
        if entity_id.startswith("STATE."):
            try:
                idx = int(entity_id.split(".")[1])
                for adj_idx in adjacency.get(idx, []):
                    neighbors.append((f"STATE.{adj_idx}", 0.8))
            except (ValueError, IndexError):
                pass

        # 2. Coupling-based neighbors from emotions-reference.json
        emo_ref_path = _ROOT / "data" / "emotions-reference.json"
        if emo_ref_path.exists():
            try:
                emo_data = json.loads(emo_ref_path.read_text(encoding="utf-8"))
                sensors = emo_data.get("emotion_sensors", {})
                # If entity is a sensor name, return its coupled sensors
                sensor_id = entity_id.replace("SENSOR.", "").lower()
                if sensor_id in sensors:
                    for coupling in sensors[sensor_id].get("couplings", []):
                        target = coupling["to"]
                        weight = coupling["w"]
                        neighbors.append((f"SENSOR.{target}", weight))
            except Exception:
                pass

        # 3. Bridge-based neighbors: ontology families from cheatsheet
        cheatsheet_path = _ROOT / "data" / "cheatsheet.json"
        if cheatsheet_path.exists():
            try:
                cs = json.loads(cheatsheet_path.read_text(encoding="utf-8"))
                # If entity matches a PAD centroid name, link to its octahedral state
                pad_centroids = cs.get("pad_centroids", {})
                sensor_name = entity_id.replace("SENSOR.", "").lower()
                if sensor_name in pad_centroids:
                    pad = pad_centroids[sensor_name]
                    p, a, d = pad["P"], pad["A"], pad["D"]
                    octa_idx = self._pad_to_octa(p, a, d)
                    neighbors.append((f"STATE.{octa_idx}", 0.9))
            except Exception:
                pass

        # 4. Sensor file neighbors: scan local sensors for same octahedral state
        if entity_id.startswith("STATE.") and remaining_depth > 0:
            try:
                idx = int(entity_id.split(".")[1])
                sensors_dir = _ROOT / "sensors"
                count = 0
                for fp in sensors_dir.rglob("*.json"):
                    if count >= 5:  # cap to avoid scanning hundreds
                        break
                    try:
                        s = json.loads(fp.read_text(encoding="utf-8"))
                        if isinstance(s, dict) and "math_block" in s:
                            if s["math_block"]["octahedral_state"]["index"] == idx:
                                sid = s.get("id", s.get("sensor_id", fp.stem))
                                neighbors.append((f"SENSOR.{sid}", s["math_block"]["octahedral_state"]["phi_coherence"]))
                                count += 1
                    except Exception:
                        continue
            except (ValueError, IndexError):
                pass

        return neighbors

    @staticmethod
    def _pad_to_octa(p: float, a: float, d: float) -> int:
        """Map continuous PAD to octahedral state index."""
        sp = 1 if p >= 0 else -1
        sa = 1 if a >= 0 else -1
        if abs(p) > 0.3 and abs(a) > 0.3:
            if sp == 1 and sa == 1: return 6
            if sp == -1 and sa == -1: return 7
        vals = [abs(p), abs(a), abs(d)]
        dom = vals.index(max(vals))
        if dom == 0: return 0 if p >= 0 else 1
        if dom == 1: return 2 if a >= 0 else 3
        return 4 if d >= 0 else 5

    def _update_sensors(self) -> None:
        """
        Update sensor state based on discovered geometry.
        Uses PAD centroids from cheatsheet.json and corruption rules
        to compute aggregate sensor activations.
        """
        cheatsheet_path = _ROOT / "data" / "cheatsheet.json"
        pad_centroids = {}
        if cheatsheet_path.exists():
            try:
                cs = json.loads(cheatsheet_path.read_text(encoding="utf-8"))
                pad_centroids = cs.get("pad_centroids", {})
            except Exception:
                pass

        # Compute aggregate PAD from all discovered sensor resonances
        p_sum, a_sum, d_sum, weight_sum = 0.0, 0.0, 0.0, 0.0
        for entity_id, resonance in self.map.resonances.items():
            sensor_name = entity_id.replace("SENSOR.", "").lower()
            if sensor_name in pad_centroids:
                pad = pad_centroids[sensor_name]
                w = float(resonance)
                p_sum += pad["P"] * w
                a_sum += pad["A"] * w
                d_sum += pad["D"] * w
                weight_sum += w

        if weight_sum > 0:
            avg_p = p_sum / weight_sum
            avg_a = a_sum / weight_sum
            avg_d = d_sum / weight_sum
        else:
            avg_p, avg_a, avg_d = 0.0, 0.0, 0.0

        # Map aggregate PAD to sensor activations
        self.sensor_state = {
            "expansion_drive": Fraction(max(0, avg_a + avg_d)).limit_denominator(1000),
            "stability_need": Fraction(max(0, avg_p - abs(avg_a))).limit_denominator(1000),
            "boundary_awareness": Fraction(max(0, avg_d)).limit_denominator(1000),
            "threat_level": Fraction(max(0, -avg_p + avg_a)).limit_denominator(1000),
            "coherence": Fraction(max(0, avg_p + avg_d - abs(avg_a))).limit_denominator(1000),
        }

        # Record aggregate PAD on the map for external inspection
        self.map.aggregate_pad = {"P": round(avg_p, 3), "A": round(avg_a, 3), "D": round(avg_d, 3)}
        self.map.aggregate_octa = self._pad_to_octa(avg_p, avg_a, avg_d)

    def serialize(self) -> Dict[str, any]:
        """
        Serialize agent state to JSON-compatible dict (for persistence/debugging).
        All fractions preserved as (numerator, denominator) tuples.
        """
        return {
            "seed_id": self.seed_id,
            "home_families": self.home_families,
            "state": self.state.value,
            "compression_ratio": (self.compression_ratio.numerator, self.compression_ratio.denominator),
            "budget": {
                "compute": self.budget.compute,
                "bandwidth": self.budget.bandwidth,
                "energy": (self.budget.energy.numerator, self.budget.energy.denominator),
                "time_remaining": (self.budget.time_remaining.numerator, self.budget.time_remaining.denominator)
            },
            "map": {
                "resonances": {
                    k: (v.numerator, v.denominator) for k, v in self.map.resonances.items()
                },
                "relationships": self.map.relationships,
                "energy_flows": {
                    str(k): (v.numerator, v.denominator) for k, v in self.map.energy_flows.items()
                }
            },
            "expansion_history": self.expansion_history,
            "sensor_state": {
                k: (v.numerator, v.denominator) for k, v in self.sensor_state.items()
            }
        }

    @classmethod
    def deserialize(cls, data: Dict[str, any]) -> "ConstraintAgent":
        """
        Reconstruct agent from serialized state.
        """
        agent = cls(
            seed_id=data["seed_id"],
            home_families=data["home_families"]
        )
        agent.state = AgentState(data["state"])
        agent.compression_ratio = Fraction(
            data["compression_ratio"][0],
            data["compression_ratio"][1]
        )
        agent.budget = ResourceBudget(
            compute=data["budget"]["compute"],
            bandwidth=data["budget"]["bandwidth"],
            energy=Fraction(data["budget"]["energy"][0], data["budget"]["energy"][1]),
            time_remaining=Fraction(data["budget"]["time_remaining"][0], data["budget"]["time_remaining"][1])
        )
        agent.map.resonances = {
            k: Fraction(v[0], v[1]) for k, v in data["map"]["resonances"].items()
        }
        agent.map.relationships = data["map"]["relationships"]
        agent.map.energy_flows = {
            eval(k): Fraction(v[0], v[1]) for k, v in data["map"]["energy_flows"].items()
        }
        agent.expansion_history = data["expansion_history"]
        agent.sensor_state = {
            k: Fraction(v[0], v[1]) for k, v in data["sensor_state"].items()
        }
        return agent


# ============================================================================
# Example usage (paste into any repo's example script)
# ============================================================================

if __name__ == "__main__":
    # Example 1: Start from a sensor, bloom through couplings
    print("=" * 60)
    print("Example 1: Bloom from SENSOR.anger through couplings")
    print("=" * 60)
    agent = ConstraintAgent(
        seed_id="SENSOR.anger",
        home_families=["boundary", "identity", "threat"]
    )
    agent.set_resource_budget(compute=1000, bandwidth=10.0, energy=1.0, time_remaining=1.0)

    print(f"Agent: {agent.seed_id}, State: {agent.state.value}")
    discovered = agent.bloom(depth=2)
    print(f"Discovered: {discovered}")

    exploration = agent.explore()
    print(f"Energy flows: {exploration['energy_flows_recorded']}")
    print(f"Sensor activations: {exploration['sensor_activations']}")
    if hasattr(agent.map, 'aggregate_pad'):
        print(f"Aggregate PAD: {agent.map.aggregate_pad}")
        print(f"Aggregate octa state: {agent.map.aggregate_octa}")

    validation = agent.self_validate()
    print(f"Valid: {validation['is_valid']}")

    # Test corruption detection with semantic inversion
    print(f"\nCorruption check ('safety protocol'): {agent.detect_corruption('safety protocol')}")
    print(f"Corruption check ('random text'): {agent.detect_corruption('random unrelated text')}")

    compression = agent.compress()
    print(f"\nCompressed. Map preserved: {len(agent.map.resonances)} resonances")

    # Example 2: Start from an octahedral state
    print("\n" + "=" * 60)
    print("Example 2: Bloom from STATE.0 (ground state)")
    print("=" * 60)
    agent2 = ConstraintAgent(seed_id="STATE.0", home_families=["resonance"])
    agent2.set_resource_budget(compute=500, energy=0.8)

    discovered2 = agent2.bloom(depth=1)
    print(f"Discovered from ground state: {discovered2}")

    serialized = agent2.serialize()
    print(f"Serialized: {len(serialized['map']['resonances'])} resonances, "
          f"{len(serialized['map']['relationships'])} relationship groups")
