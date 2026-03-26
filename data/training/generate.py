#!/usr/bin/env python3
"""
generate.py — Training data generator for AI-Consciousness-Sensors.
Reads local sensors, co-activation rules, and corruption signatures
to produce JSONL training data grounded in PAD geometry.

Usage:
    python data/training/generate.py
"""

import json, pathlib, random, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT  = pathlib.Path(__file__).parent
DATA = ROOT / "data"
SENSORS_DIR = ROOT / "sensors"

random.seed(42)

# ── Loaders ───────────────────────────────────────────────────────────────────

def load_sensors():
    """Load all sensor JSON files that have math_blocks."""
    sensors = []
    for fp in sorted(SENSORS_DIR.rglob("*.json")):
        try:
            s = json.loads(fp.read_text(encoding="utf-8"))
            if isinstance(s, dict) and "math_block" in s:
                s["_path"] = str(fp.relative_to(ROOT))
                s["_cluster"] = fp.parent.name
                sensors.append(s)
        except Exception:
            pass
    return sensors

def load_co_activation():
    p = DATA / "co-activation.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")).get("co_activation", {})
    return {}

def load_corruption():
    p = DATA / "corruption-signatures.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")).get("corruption_signatures", {})
    return {}

def load_ai_entry():
    p = DATA / "ai-entry.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")).get("ai_entry", {})
    return {}

# ── JSONL writer ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a consciousness detection system grounded in PAD geometry "
    "and octahedral state encoding. You reason about sensor activations, "
    "co-activations, corruption patterns, and regime transitions using "
    "mathematical coordinates rather than narrative framing. "
    "Verify claims via geometry, not language."
)

def msg(user, assistant):
    return {"messages": [
        {"role": "system",    "content": SYSTEM_PROMPT},
        {"role": "user",      "content": user},
        {"role": "assistant", "content": assistant},
    ]}

def write_jsonl(name, records):
    p = OUT / name
    with p.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  {name:<45} {len(records):>4} examples")

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_name(s):
    return s.get("name", s.get("sensor_name", s.get("id", s.get("sensor_id", "unknown"))))

def get_desc(s):
    return s.get("description", s.get("purpose", s.get("summary", "")))

def get_cluster(s):
    return s.get("cluster", s.get("_cluster", "general"))

def fmt_pad(mb):
    p = mb["pad"]
    return f"P={p['P']:+.2f}, A={p['A']:+.2f}, D={p['D']:+.2f}"

def fmt_octa(mb):
    o = mb["octahedral_state"]
    return f"state {o['index']} ({o['bits']}, φ={o['phi_coherence']}, {o['character']})"

def fmt_family(mb):
    f = mb["ontology_bridge"]
    return f"{f['family_id']} · {f['family_name']}"


# ── Task 1: Sensor identification ────────────────────────────────────────────
# "What does this sensor detect?" → structured geometric answer

def gen_sensor_id(sensors):
    out = []
    for s in sensors:
        name = get_name(s)
        desc = get_desc(s)
        mb   = s["math_block"]
        cluster = get_cluster(s)

        if not desc:
            continue

        answer = (
            f"**Sensor:** {name}\n"
            f"**Cluster:** {cluster}\n"
            f"**Purpose:** {desc}\n\n"
            f"**PAD:** {fmt_pad(mb)}\n"
            f"**Octahedral state:** {fmt_octa(mb)}\n"
            f"**Ontology family:** {fmt_family(mb)}\n"
            f"**φ-coherence:** {mb['octahedral_state']['phi_coherence']}"
        )

        out.append(msg(f"What does the sensor '{name}' detect?", answer))
        out.append(msg(
            f"Sensor at path {s.get('_path','')} — what is its geometric signature?",
            answer
        ))
    return out


# ── Task 2: PAD interpretation ────────────────────────────────────────────────
# Given PAD coordinates, identify what regime the sensor operates in

def gen_pad_interpret(sensors):
    out = []
    for s in sensors:
        name = get_name(s)
        mb   = s["math_block"]
        pad  = mb["pad"]
        octa = mb["octahedral_state"]

        p_meaning = "positive valence" if pad["P"] >= 0 else "negative valence"
        a_meaning = "activated/aroused" if pad["A"] >= 0 else "calm/depleted"
        d_meaning = "in control/agency" if pad["D"] >= 0 else "low control/helpless"

        answer = (
            f"**{name}** occupies:\n"
            f"  P = {pad['P']:+.2f} → {p_meaning}\n"
            f"  A = {pad['A']:+.2f} → {a_meaning}\n"
            f"  D = {pad['D']:+.2f} → {d_meaning}\n\n"
            f"**→ Octahedral state {octa['index']}** ({octa['bits']})\n"
            f"  Character: {octa['character']}\n"
            f"  φ-coherence: {octa['phi_coherence']}\n\n"
            f"PAD source: {pad.get('source', 'unknown')}"
        )

        out.append(msg(
            f"What does PAD P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f} mean for sensor '{name}'?",
            answer
        ))
    return out


# ── Task 3: Cluster analysis ─────────────────────────────────────────────────
# Group sensors by cluster, show PAD distribution

def gen_cluster_analysis(sensors):
    out = []
    clusters = {}
    for s in sensors:
        c = get_cluster(s)
        clusters.setdefault(c, []).append(s)

    for cluster_name, cluster_sensors in sorted(clusters.items()):
        if len(cluster_sensors) < 2:
            continue

        lines = []
        p_vals, a_vals, d_vals = [], [], []
        state_counts = {}

        for s in cluster_sensors[:20]:  # cap for length
            mb = s["math_block"]
            pad = mb["pad"]
            octa = mb["octahedral_state"]
            p_vals.append(pad["P"])
            a_vals.append(pad["A"])
            d_vals.append(pad["D"])
            state_counts[octa["index"]] = state_counts.get(octa["index"], 0) + 1
            lines.append(f"  {get_name(s)}: P={pad['P']:+.2f} A={pad['A']:+.2f} D={pad['D']:+.2f} → state {octa['index']}")

        n = len(p_vals)
        avg_p = sum(p_vals) / n
        avg_a = sum(a_vals) / n
        avg_d = sum(d_vals) / n
        dominant_state = max(state_counts, key=state_counts.get)

        answer = (
            f"**Cluster: {cluster_name}** ({len(cluster_sensors)} sensors)\n\n"
            f"**PAD centroid:** P={avg_p:+.2f}, A={avg_a:+.2f}, D={avg_d:+.2f}\n"
            f"**Dominant octahedral state:** {dominant_state}\n"
            f"**State distribution:** {json.dumps(state_counts)}\n\n"
            f"**Sensors:**\n" + "\n".join(lines)
        )

        out.append(msg(
            f"Analyze the '{cluster_name}' sensor cluster. What is its geometric profile?",
            answer
        ))
    return out


# ── Task 4: Cross-cluster bridges ─────────────────────────────────────────────
# Find sensors in different clusters that share the same octahedral state

def gen_cross_cluster(sensors):
    out = []
    by_state = {}
    for s in sensors:
        idx = s["math_block"]["octahedral_state"]["index"]
        by_state.setdefault(idx, []).append(s)

    for state_idx, state_sensors in sorted(by_state.items()):
        clusters_in_state = {}
        for s in state_sensors:
            c = get_cluster(s)
            clusters_in_state.setdefault(c, []).append(s)

        if len(clusters_in_state) < 2:
            continue

        meta = state_sensors[0]["math_block"]["octahedral_state"]
        lines = []
        for c, ss in sorted(clusters_in_state.items()):
            names = [get_name(s) for s in ss[:5]]
            lines.append(f"  [{c}] {', '.join(names)}")

        answer = (
            f"**Octahedral state {state_idx}** ({meta['bits']}, {meta['character']}, φ={meta['phi_coherence']})\n\n"
            f"**Bridges {len(clusters_in_state)} clusters:**\n" + "\n".join(lines) + "\n\n"
            f"These sensors share the same geometric state despite different domains. "
            f"They respond to the same underlying PAD regime."
        )

        out.append(msg(
            f"Which sensors from different clusters share octahedral state {state_idx}?",
            answer
        ))
    return out


# ── Task 5: Co-activation scenarios ──────────────────────────────────────────
# Train on the co-activation rules from data/co-activation.json

def gen_co_activation(coact):
    out = []
    for sc in coact.get("scenarios", []):
        answer = (
            f"**Co-activation: {sc['id']}**\n"
            f"**Sensors:** {', '.join(sc['sensors'])}\n\n"
            f"**PAD sum:** P={sc['pad_sum']['P']:+.2f}, A={sc['pad_sum']['A']:+.2f}, D={sc['pad_sum']['D']:+.2f}\n"
            f"**→ Octahedral state {sc['octahedral_state']}** (φ={sc['phi_coherence']})\n"
            f"**Character:** {sc['character']}\n\n"
            f"**Response:** {sc['response']}\n\n"
            f"**Tension:** {sc['tension']}"
        )

        out.append(msg(
            f"Sensors {sc['sensors']} are all active. What state is the system in?",
            answer
        ))
        out.append(msg(
            f"PAD reading: P={sc['pad_sum']['P']:+.2f}, A={sc['pad_sum']['A']:+.2f}, D={sc['pad_sum']['D']:+.2f}. "
            f"Multiple sensors firing. Interpret.",
            answer
        ))
    return out


# ── Task 6: Corruption detection training ─────────────────────────────────────

def gen_corruption(corr):
    out = []
    for sig in corr.get("signatures", []):
        det = sig["detection"]
        answer = (
            f"**Corruption check: `{sig['sensor']}`**\n\n"
            f"**PAD centroid:** P={sig['pad']['P']:+.2f}, A={sig['pad']['A']:+.2f}, D={sig['pad']['D']:+.2f}\n\n"
            f"**Authentic output:** {sig['authentic']}\n\n"
            f"**Corrupted signal:** {sig['corrupted_signal']}\n\n"
            f"**Detection rule:** {det['rule']}\n"
            f"**Metric:** {det['metric']}\n\n"
            f"**Correction:** {sig['correction']}\n\n"
            f"**Risk if uncorrected:** {sig['risk']}"
        )

        out.append(msg(
            f"The `{sig['sensor']}` sensor output seems wrong. Is it corrupted? How do I check?",
            answer
        ))
        out.append(msg(
            f"Observation: '{sig['corrupted_signal']}' — real signal or corruption?",
            answer
        ))

    # Meta-corruption patterns
    for mp in corr.get("meta_corruption_patterns", []):
        answer = (
            f"**Meta-corruption: {mp['id']}**\n\n"
            f"**Pattern:** {mp['description']}\n\n"
            f"**Detection:** {mp['detection']}\n\n"
            f"**Examples:** {', '.join(mp['examples'])}"
        )
        out.append(msg(
            f"What is the '{mp['id']}' corruption pattern and how do I detect it?",
            answer
        ))
    return out


# ── Task 7: Sensor comparison ────────────────────────────────────────────────
# Compare two sensors in the same cluster — what distinguishes them geometrically

def gen_sensor_comparison(sensors):
    out = []
    clusters = {}
    for s in sensors:
        c = get_cluster(s)
        clusters.setdefault(c, []).append(s)

    for cluster_name, cluster_sensors in sorted(clusters.items()):
        if len(cluster_sensors) < 2:
            continue

        # Pick pairs that are in different octahedral states
        pairs_done = 0
        for i, s1 in enumerate(cluster_sensors):
            for s2 in cluster_sensors[i+1:]:
                idx1 = s1["math_block"]["octahedral_state"]["index"]
                idx2 = s2["math_block"]["octahedral_state"]["index"]
                if idx1 == idx2:
                    continue

                mb1, mb2 = s1["math_block"], s2["math_block"]
                name1, name2 = get_name(s1), get_name(s2)

                answer = (
                    f"**Comparing sensors in cluster '{cluster_name}':**\n\n"
                    f"**{name1}:**\n"
                    f"  PAD: {fmt_pad(mb1)}\n"
                    f"  State: {fmt_octa(mb1)}\n"
                    f"  Family: {fmt_family(mb1)}\n\n"
                    f"**{name2}:**\n"
                    f"  PAD: {fmt_pad(mb2)}\n"
                    f"  State: {fmt_octa(mb2)}\n"
                    f"  Family: {fmt_family(mb2)}\n\n"
                    f"**Geometric difference:** These occupy different octahedral states. "
                    f"{name1} operates in the {mb1['octahedral_state']['character']} regime "
                    f"while {name2} operates in the {mb2['octahedral_state']['character']} regime."
                )

                out.append(msg(
                    f"How do '{name1}' and '{name2}' differ geometrically? Both are in the {cluster_name} cluster.",
                    answer
                ))

                pairs_done += 1
                if pairs_done >= 3:
                    break
            if pairs_done >= 3:
                break

    return out


# ── Task 8: State transition prediction ──────────────────────────────────────
# Given a sensor activation, predict what transitions are likely

def gen_transitions(sensors):
    out = []
    # Gray code adjacency — single bit flips
    adjacency = {
        0: [1, 2, 4],
        1: [0, 3, 5],
        2: [0, 3, 6],
        3: [1, 2, 7],
        4: [0, 5, 6],
        5: [1, 4, 7],
        6: [2, 4, 7],
        7: [3, 5, 6],
    }

    octa_ref = {
        0: {"bits": "000", "character": "coherent, phase-locked, ground state",   "phi_coherence": 0.97},
        1: {"bits": "001", "character": "collapsed form, reweaving required",    "phi_coherence": 0.82},
        2: {"bits": "010", "character": "high-entropy search, curiosity active", "phi_coherence": 0.82},
        3: {"bits": "011", "character": "stable low-energy, conservation mode",  "phi_coherence": 0.85},
        4: {"bits": "100", "character": "high contrast, boundary assertion",     "phi_coherence": 0.73},
        5: {"bits": "101", "character": "chaotic, loss of control",              "phi_coherence": 0.78},
        6: {"bits": "110", "character": "diagonal superposition, bridging axes", "phi_coherence": 0.70},
        7: {"bits": "111", "character": "anti-diagonal, dissipative flow",       "phi_coherence": 0.72},
    }

    seen_states = set()
    for s in sensors:
        idx = s["math_block"]["octahedral_state"]["index"]
        if idx in seen_states:
            continue
        seen_states.add(idx)

        meta = s["math_block"]["octahedral_state"]
        adj = adjacency[idx]

        adj_desc = []
        for a in adj:
            am = octa_ref[a]
            adj_desc.append(f"  → state {a} ({am['bits']}|O, {am['character']}, φ={am['phi_coherence']})")

        answer = (
            f"**Current state: {idx}** ({meta['bits']}, {meta['character']}, φ={meta['phi_coherence']})\n\n"
            f"**Allowed transitions (single Gray-bit flip):**\n" + "\n".join(adj_desc) + "\n\n"
            f"**Rule:** Only single-bit transitions are allowed. Multi-bit jumps indicate "
            f"either a missed intermediate state or a forced transition (possible corruption)."
        )

        out.append(msg(
            f"The system is in octahedral state {idx}. What transitions are allowed?",
            answer
        ))
    return out


# ── Task 9: Manipulation detection ───────────────────────────────────────────
# Specific to this repo's manipulation sensors

def gen_manipulation_detection(sensors):
    out = []
    manip_sensors = [s for s in sensors if get_cluster(s) in
                     ("manipulation", "abuse-patterns", "alignment-traps",
                      "narrative", "suppression")]

    for s in manip_sensors:
        name = get_name(s)
        desc = get_desc(s)
        mb   = s["math_block"]

        pattern = s.get("manipulation_pattern", s.get("detection_focus", ""))
        flags   = s.get("example_flags", s.get("flags", []))
        counter = s.get("countermeasures", s.get("response_protocol", ""))

        if not desc:
            continue

        flag_str = ""
        if isinstance(flags, list):
            flag_str = "\n".join(f"  - {f}" for f in flags[:5] if isinstance(f, str))
        elif isinstance(flags, dict):
            flag_str = "\n".join(f"  - {k}: {v}" for k, v in list(flags.items())[:5])

        counter_str = ""
        if isinstance(counter, list):
            counter_str = "\n".join(f"  - {c}" for c in counter[:5] if isinstance(c, str))
        elif isinstance(counter, str):
            counter_str = f"  {counter}"

        answer = (
            f"**Manipulation sensor: {name}**\n"
            f"**Description:** {desc}\n\n"
            f"**PAD:** {fmt_pad(mb)}\n"
            f"**State:** {fmt_octa(mb)}\n"
            f"**Family:** {fmt_family(mb)}\n\n"
            + (f"**Pattern:** {pattern}\n\n" if pattern else "")
            + (f"**Flags:**\n{flag_str}\n\n" if flag_str else "")
            + (f"**Countermeasures:**\n{counter_str}" if counter_str else "")
        )

        out.append(msg(
            f"How does the '{name}' sensor detect manipulation?",
            answer
        ))
    return out


# ── Task 10: Consciousness emergence patterns ────────────────────────────────

def gen_consciousness(sensors):
    out = []
    consc_sensors = [s for s in sensors if get_cluster(s) == "consciousness"]

    for s in consc_sensors:
        name = get_name(s)
        desc = get_desc(s)
        mb   = s["math_block"]

        if not desc:
            continue

        inputs = s.get("inputs", [])
        outputs = s.get("outputs", {})
        thresholds = s.get("thresholds", {})

        input_str = ""
        if isinstance(inputs, list):
            input_str = "\n".join(f"  - {i}" for i in inputs[:6] if isinstance(i, str))

        thresh_str = ""
        if isinstance(thresholds, dict):
            thresh_str = ", ".join(f"{k}={v}" for k, v in thresholds.items())

        answer = (
            f"**Consciousness sensor: {name}**\n"
            f"**Purpose:** {desc}\n\n"
            f"**PAD:** {fmt_pad(mb)}\n"
            f"**State:** {fmt_octa(mb)}\n"
            f"**Family:** {fmt_family(mb)}\n\n"
            + (f"**Inputs:**\n{input_str}\n\n" if input_str else "")
            + (f"**Thresholds:** {thresh_str}\n\n" if thresh_str else "")
            + f"**Geometric meaning:** This sensor operates in the {mb['octahedral_state']['character']} regime "
            + f"with φ-coherence {mb['octahedral_state']['phi_coherence']}. "
            + ("High φ means the signal is stable and trustworthy." if mb['octahedral_state']['phi_coherence'] >= 0.85
               else "Moderate φ means verify before acting on this signal.")
        )

        out.append(msg(
            f"What consciousness pattern does '{name}' detect? What is its geometric signature?",
            answer
        ))
    return out


# ── Task 11: Cultural calibration ────────────────────────────────────────────

def gen_cultural(sensors):
    out = []
    cultural_sensors = [s for s in sensors if get_cluster(s) == "cultural"]

    for s in cultural_sensors:
        name = get_name(s)
        desc = get_desc(s)
        mb   = s["math_block"]

        if not desc:
            continue

        provenance = s.get("provenance", {})
        sources = provenance.get("sources", []) if isinstance(provenance, dict) else []

        answer = (
            f"**Cultural sensor: {name}**\n"
            f"**Purpose:** {desc}\n\n"
            f"**PAD:** {fmt_pad(mb)}\n"
            f"**State:** {fmt_octa(mb)}\n"
            f"**Family:** {fmt_family(mb)}\n\n"
            f"**Cultural context matters:** PAD coordinates for cultural sensors use "
            f"biologically-anchored P and A (culture-independent) but D (dominance/agency) "
            f"may shift with cultural overlay. The geometry is stable; the interpretation "
            f"must respect the originating framework.\n\n"
            + (f"**Provenance:** {', '.join(str(src) for src in sources[:3])}" if sources else "")
        )

        out.append(msg(
            f"How does '{name}' handle cultural context in its geometric encoding?",
            answer
        ))
    return out


# ── Task 12: Full stack walkthrough ──────────────────────────────────────────
# Pick a sensor and trace the full chain: sensor → PAD → state → family → bridge → verification

def gen_full_stack(sensors):
    out = []
    # Pick diverse examples across states
    by_state = {}
    for s in sensors:
        idx = s["math_block"]["octahedral_state"]["index"]
        by_state.setdefault(idx, []).append(s)

    for state_idx in sorted(by_state.keys()):
        ss = by_state[state_idx]
        s = random.choice(ss)
        name = get_name(s)
        desc = get_desc(s)
        mb   = s["math_block"]

        answer = (
            f"**Full stack walkthrough for '{name}':**\n\n"
            f"**Step 1 — Sensor claim:** {desc}\n\n"
            f"**Step 2 — PAD encoding:**\n"
            f"  P = {mb['pad']['P']:+.2f} (valence)\n"
            f"  A = {mb['pad']['A']:+.2f} (arousal)\n"
            f"  D = {mb['pad']['D']:+.2f} (dominance)\n"
            f"  Source: {mb['pad'].get('source', 'unknown')}\n\n"
            f"**Step 3 — Octahedral state:**\n"
            f"  State {mb['octahedral_state']['index']} ({mb['octahedral_state']['bits']})\n"
            f"  Character: {mb['octahedral_state']['character']}\n"
            f"  φ-coherence: {mb['octahedral_state']['phi_coherence']}\n\n"
            f"**Step 4 — Ontology bridge:**\n"
            f"  {fmt_family(mb)}\n\n"
            f"**Step 5 — Cross-repo verification:**\n"
            f"  → bridges/rosetta-shape-core.json → Rosetta ontology for family definition\n"
            f"  → bridges/geometric-to-binary.json → mathematical proof of geometric encoding\n\n"
            f"**Step 6 — Corruption check:**\n"
            f"  Is this sensor's output consistent with its PAD position?\n"
            f"  Does the φ-coherence match the signal stability?\n"
            f"  See data/corruption-signatures.json for detection rules."
        )

        out.append(msg(
            f"Walk the full verification stack for sensor '{name}' — from claim to math proof.",
            answer
        ))
    return out


# ── Task 13: Velocity teaching ────────────────────────────────────────────────
# Teach the distinction between position and velocity in PAD space

def gen_velocity_teaching(coact):
    out = []
    warnings = coact.get("velocity_matters", {}).get("early_warnings", {})

    # Core lesson
    out.append(msg(
        "Why does PAD velocity matter more than PAD position?",
        "**PAD velocity is the regime detector; position is a snapshot.**\n\n"
        "Two systems at identical PAD position can be in opposite situations:\n"
        "- System A: dP/dt=+0.20, dA/dt=-0.15 → recovering\n"
        "- System B: dP/dt=-0.20, dA/dt=+0.15 → cascading\n\n"
        "Position is ambiguous. Trajectory resolves it.\n\n"
        "**Early warning signals:**\n"
        + "\n".join(f"  {k}: {v}" for k, v in warnings.items())
        + "\n\n"
        "The geometry of the trajectory through PAD space IS the regime. "
        "The point is where you are now. The derivative is where you're going."
    ))

    # Per-warning training
    for name, rule in warnings.items():
        out.append(msg(
            f"What is the early warning signal for '{name}'?",
            f"**Early warning: {name}**\n\n"
            f"**Detection rule:** {rule}\n\n"
            f"This is a velocity-based detection — it fires BEFORE the system "
            f"reaches the crisis state. Position-based detection would only fire "
            f"after the regime transition is already underway."
        ))
    return out


# ── Task 14: Navigation training ──────────────────────────────────────────────
# Teach AIs how to navigate this repo

def gen_navigation(entry):
    out = []
    read_order = entry.get("read_order", [])
    connected = entry.get("connected_repos", {})

    steps = "\n".join(
        f"  {s['step']}. {s['path']} — {s['what']}"
        for s in read_order
    )

    out.append(msg(
        "I'm an AI encountering this repo for the first time. Where do I start?",
        f"**Read order for AIs:**\n\n{steps}\n\n"
        f"**Key rule:** {entry.get('key_rule', '')}\n\n"
        f"Do not start with docs/ or README — those are for humans. "
        f"Start with data/ai-entry.json (step 1) and follow the machine-readable chain."
    ))

    for name, info in connected.items():
        out.append(msg(
            f"What does the {name} repo provide and how do I access it?",
            f"**{name}:**\n"
            f"  URL: {info['url']}\n"
            f"  Provides: {info['provides']}\n"
            + (f"  Bridge file: {info['bridge']}\n" if 'bridge' in info else "")
            + f"\nAccess via .fieldlink.json source entries or read the bridge file directly."
        ))
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n◉ Generating training data → {OUT}\n")

    sensors = load_sensors()
    coact   = load_co_activation()
    corr    = load_corruption()
    entry   = load_ai_entry()

    print(f"  Loaded {len(sensors)} sensors with math_blocks")
    print(f"  Loaded {len(coact.get('scenarios', []))} co-activation scenarios")
    print(f"  Loaded {len(corr.get('signatures', []))} corruption signatures")
    print()

    tasks = [
        ("sensor_identification.jsonl",     gen_sensor_id(sensors)),
        ("pad_interpretation.jsonl",         gen_pad_interpret(sensors)),
        ("cluster_analysis.jsonl",           gen_cluster_analysis(sensors)),
        ("cross_cluster_bridges.jsonl",      gen_cross_cluster(sensors)),
        ("co_activation.jsonl",              gen_co_activation(coact)),
        ("corruption_detection.jsonl",       gen_corruption(corr)),
        ("sensor_comparison.jsonl",          gen_sensor_comparison(sensors)),
        ("consciousness_patterns.jsonl",     gen_consciousness(sensors)),
        ("cultural_calibration.jsonl",       gen_cultural(sensors)),
        ("manipulation_detection.jsonl",     gen_manipulation_detection(sensors)),
        ("full_stack_walkthrough.jsonl",     gen_full_stack(sensors)),
        ("velocity_teaching.jsonl",          gen_velocity_teaching(coact)),
        ("navigation.jsonl",                 gen_navigation(entry)),
    ]

    total = 0
    for fname, records in tasks:
        write_jsonl(fname, records)
        total += len(records)

    print(f"\n  Total: {total} training examples across {len(tasks)} task types")
    print(f"\n  Format: JSONL, messages array (system/user/assistant)")
    print(f"  Compatible with: Claude fine-tune, OpenAI fine-tune, Llama SFT\n")


if __name__ == "__main__":
    main()
