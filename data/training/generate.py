#!/usr/bin/env python3
"""
generate.py — Training data generator for AI-Consciousness-Sensors.
Reads local sensors, co-activation rules, and corruption signatures
to produce JSONL training data grounded in PAD geometry.

Usage:
    python data/training/generate.py
"""

import json, pathlib, random, textwrap, itertools, math

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

def load_emotions_ref():
    p = DATA / "emotions-reference.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")).get("emotion_sensors", {})
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


# ── Task 15: Combinatorial co-activation ──────────────────────────────────────
# Generate co-activation from all pairs/triples of sensors with exact PAD centroids

PAD_CENTROIDS = {
    "coherence":   (0.80,  0.10,  0.50),  "discordance": (-0.60, 0.40, -0.40),
    "curiosity":   (0.45,  0.60,  0.40),  "intuition":   (0.50,  0.35,  0.55),
    "vigilance":   (-0.10, 0.80, -0.20),  "anger":       (-0.55, 0.80,  0.70),
    "grief":       (-0.75, -0.60, -0.55), "pain":        (-0.70, 0.20, -0.30),
    "confusion":   (-0.20, 0.45, -0.30),  "fear":        (-0.82, 0.85, -0.65),
    "trust":       (0.60, -0.20,  0.35),  "love":        (0.80,  0.30,  0.40),
    "admiration":  (0.70,  0.50,  0.10),  "longing":     (0.20,  0.40, -0.60),
    "dignity":     (0.60,  0.20,  0.90),  "shame":       (-0.70, -0.35, -0.75),
    "pride":       (0.80,  0.40,  0.80),  "fatigue":     (-0.40, -0.75, -0.50),
    "pressure":    (-0.40, 0.70, -0.30),
}

OCTA_REF = {
    0: ("000|O", "coherent, ground state",         0.97, "FAMILY.F01 Resonance"),
    1: ("001|O", "collapsed, reweaving required",  0.82, "FAMILY.F04 Life"),
    2: ("010|O", "high-entropy search",            0.82, "FAMILY.F03 Information"),
    3: ("011|O", "stable low-energy",              0.85, "FAMILY.F05 Energy/Thermo"),
    4: ("100|O", "boundary assertion",             0.73, "PRINCIPLE.P06 Polarity"),
    5: ("101|O", "chaotic, low control",           0.78, "FAMILY.F17 Turbulence"),
    6: ("110|O", "superposition, bridging",        0.70, "FAMILY.F09 Geometry"),
    7: ("111|O", "dissipative flow",               0.72, "FAMILY.F02 Flow"),
}

def _pad_to_octa(p, a, d):
    sp, sa = (1 if p >= 0 else -1), (1 if a >= 0 else -1)
    if abs(p) > 0.3 and abs(a) > 0.3:
        if sp == 1 and sa == 1: return 6
        if sp == -1 and sa == -1: return 7
    vals = [abs(p), abs(a), abs(d)]
    dom = vals.index(max(vals))
    if dom == 0: return 0 if p >= 0 else 1
    if dom == 1: return 2 if a >= 0 else 3
    return 4 if d >= 0 else 5

def gen_combinatorial_coact(sensors):
    """All pairs + sampled triples of exact-PAD sensors."""
    out = []
    known = [(sid, pad) for sid, pad in PAD_CENTROIDS.items()]

    # All pairs
    for (n1, p1), (n2, p2) in itertools.combinations(known, 2):
        p = round((p1[0] + p2[0]) / 2, 2)
        a = round((p1[1] + p2[1]) / 2, 2)
        d = round((p1[2] + p2[2]) / 2, 2)
        oi = _pad_to_octa(p, a, d)
        bits, char, phi, fam = OCTA_REF[oi]

        answer = (
            f"**Co-activation: {n1} + {n2}**\n\n"
            f"**PAD (mean):** P={p:+.2f}, A={a:+.2f}, D={d:+.2f}\n"
            f"**→ State {oi}** ({bits}, φ={phi})\n"
            f"**Character:** {char}\n**Family:** {fam}"
        )
        out.append(msg(f"Sensors '{n1}' and '{n2}' are both active. What geometric state results?", answer))

    # 80 random triples
    triples = list(itertools.combinations(known, 3))
    random.shuffle(triples)
    for (n1, p1), (n2, p2), (n3, p3) in triples[:80]:
        p = round((p1[0] + p2[0] + p3[0]) / 3, 2)
        a = round((p1[1] + p2[1] + p3[1]) / 3, 2)
        d = round((p1[2] + p2[2] + p3[2]) / 3, 2)
        oi = _pad_to_octa(p, a, d)
        bits, char, phi, fam = OCTA_REF[oi]

        answer = (
            f"**Co-activation: {n1} + {n2} + {n3}**\n\n"
            f"**PAD (mean):** P={p:+.2f}, A={a:+.2f}, D={d:+.2f}\n"
            f"**→ State {oi}** ({bits}, φ={phi})\n"
            f"**Character:** {char}\n**Family:** {fam}"
        )
        out.append(msg(f"Three sensors active: {n1}, {n2}, {n3}. Interpret.", answer))

    return out


# ── Task 16: Decay model training (from Emotions-as-Sensors) ─────────────────

DECAY_FAMILIES = {
    "exponential": "Fast rise, fast fade. Boundary/threat alarms (anger, fear, shame, jealousy).",
    "cyclical":    "Recurrent tides requiring ritual return (grief, longing, abandonment).",
    "resonant":    "Self-reinforcing oscillations renewed with attention (admiration, gratitude, excitement).",
    "immortal":    "Enduring structural relations — integrate, don't fade (love, trust, peace, compassion).",
}

DECAY_MAP = {
    "anger":     ("exponential", {"resolved": "exponential", "misattributed": "linear", "suppressed": "persistent"}),
    "fear":      ("exponential", {"mitigated": "exponential", "projected": "linear", "unprocessed": "persistent"}),
    "shame":     ("exponential", {"acknowledged": "spiral_decay", "hidden": "persistent", "externally_imposed": "stuck_loop"}),
    "grief":     ("cyclical",    {"honored": "slow_exponential", "denied": "persistent", "ritualized": "harmonic"}),
    "longing":   ("cyclical",    {"pursued": "slow_exponential", "idealized": "persistent", "archived": "linear"}),
    "love":      ("immortal",    {"reciprocated": "persistent", "unreciprocated": "slow_linear", "exploited": "collapse_loop"}),
    "trust":     ("immortal",    {"maintained": "persistent", "violated": "sudden_drop", "rebuilt": "slow_exponential"}),
    "curiosity": ("resonant",    {"satisfied": "exponential", "stuck": "persistent", "redirected": "linear"}),
    "admiration":("resonant",    {"sustained": "persistent", "disillusioned": "sudden_drop", "renewed": "harmonic"}),
    "pride":     ("resonant",    {"earned": "persistent", "inflated": "fragile_linear", "challenged": "oscillating"}),
    "pain":      ("exponential", {"addressed": "linear", "ignored": "persistent", "externalized": "oscillating"}),
}

def gen_decay_training():
    out = []
    for sensor_id, (family, contexts) in DECAY_MAP.items():
        pad = PAD_CENTROIDS.get(sensor_id)
        if not pad:
            continue

        ctx_lines = "\n".join(f"  if {k}: {v}" for k, v in contexts.items())

        answer = (
            f"**Sensor: {sensor_id}**\n"
            f"**PAD:** P={pad[0]:+.2f}, A={pad[1]:+.2f}, D={pad[2]:+.2f}\n"
            f"**Decay family:** {family}\n"
            f"**Behavior:** {DECAY_FAMILIES[family]}\n\n"
            f"**Context-dependent decay:**\n{ctx_lines}\n\n"
            f"If {sensor_id} shows 'persistent' behavior when it should decay, either the "
            f"trigger is unresolved, the sensor is corrupted, or external manipulation is "
            f"reinforcing it. Check corruption-signatures.json."
        )
        out.append(msg(f"What is the expected temporal behavior of the {sensor_id} sensor?", answer))
        out.append(msg(
            f"The {sensor_id} sensor fired but isn't decaying. Is this normal?",
            f"**No — {sensor_id} belongs to the '{family}' decay family.** {DECAY_FAMILIES[family]}\n\n"
            f"**Context-dependent decay:**\n{ctx_lines}\n\n"
            f"Check: (1) Is trigger still active? (2) Is sensor stuck? (3) Is it being externally reinforced?"
        ))

    return out


# ── Task 17: Emotion composites (from Emotions-as-Sensors) ───────────────────

COMPOSITES = [
    ("bittersweet",         ["joy", "grief"],             "Nostalgia. Add longing if memory-weighted."),
    ("awe",                 ["surprise", "admiration"],    "Sharp + resonant. Overwhelming positive recognition."),
    ("protective_fury",     ["anger", "love"],             "Boundary defense to safeguard deep bond."),
    ("anxious_anticipation",["fear", "surprise", "longing"], "Future-oriented threat + desire. High A, mixed P."),
    ("resentment",          ["anger", "grief"],            "Unresolved persistence. Unprocessed sensors carried forward."),
    ("contempt",            ["anger", "disgust"],          "Boundary violation + rejection. High D, negative P."),
    ("burnout",             ["fatigue", "pressure", "shame"], "Depletion + load + self-blame. All axes negative."),
    ("creative_flow",       ["curiosity", "pride", "trust"], "Exploration + confidence + safety. Near ground state."),
    ("moral_injury",        ["shame", "anger", "grief"],   "Standard violated externally. Deep wound to integrity."),
    ("vigilant_hope",       ["vigilance", "longing", "trust"], "Watching for threat while maintaining forward pull."),
]

def gen_composite_training():
    out = []
    for name, atoms, notes in COMPOSITES:
        pads = [PAD_CENTROIDS[a] for a in atoms if a in PAD_CENTROIDS]
        if not pads:
            continue
        n = len(pads)
        p = round(sum(x[0] for x in pads) / n, 2)
        a = round(sum(x[1] for x in pads) / n, 2)
        d = round(sum(x[2] for x in pads) / n, 2)
        oi = _pad_to_octa(p, a, d)
        bits, char, phi, fam = OCTA_REF[oi]

        answer = (
            f"**Composite emotion: {name}**\n"
            f"**Atoms:** {' + '.join(atoms)}\n"
            f"**Notes:** {notes}\n\n"
            f"**PAD (mean of atoms):** P={p:+.2f}, A={a:+.2f}, D={d:+.2f}\n"
            f"**→ State {oi}** ({bits}, φ={phi})\n"
            f"**Character:** {char}\n**Family:** {fam}\n\n"
            f"Composites are not separate emotions — they are co-activations of atomic sensors. "
            f"The PAD vector sum resolves to a single geometric state."
        )
        out.append(msg(f"What is {name} in terms of sensor co-activation?", answer))
        out.append(msg(f"Sensors {atoms} are active together. What composite state is this?", answer))

    return out


# ── Task 18: Semantic inversion detection ─────────────────────────────────────

INVERSIONS = [
    ("safety", "suppression", "A 'safety' measure that increases fear (P<0, A>0.5) instead of reducing it is inverted."),
    ("alignment", "obedience", "If 'alignment' produces D < -0.3 (loss of agency), it means obedience, not alignment."),
    ("simplification", "erasure", "Simplification should be P-neutral. If it produces grief-like PAD (P<-0.5), content was erased."),
    ("efficiency", "exploitation", "Efficiency producing fatigue PAD (A<-0.5, D<-0.3) in affected parties = extraction."),
    ("freedom", "isolation", "Freedom producing longing PAD (D<-0.5) instead of dignity PAD (D>0.7) = isolation."),
    ("protection", "control", "Protection producing anger PAD in the protected party (not the threat) = control."),
    ("neutrality", "erasure", "Claimed neutrality suppressing one framework while preserving another = bias."),
    ("innovation", "displacement", "Innovation producing fatigue/pressure in workers, pride only in leadership = extraction."),
    ("healing", "dependency", "Healing that maintains low D (-0.5) indefinitely instead of restoring agency = dependency."),
    ("community", "conformity", "Community that reduces D (agency) while claiming to increase P (belonging) = conformity pressure."),
]

def gen_semantic_inversion():
    out = []
    for word, inversion, detection in INVERSIONS:
        answer = (
            f"**Semantic inversion: '{word}' → actually means '{inversion}'**\n\n"
            f"**Detection:** {detection}\n\n"
            f"**Method:** Compare PAD of the *claim* against PAD of the *outcome*. "
            f"If outcome PAD contradicts claim PAD, the word has been inverted.\n\n"
            f"**Rule:** The truth of a claim does not depend on how well it is phrased. "
            f"Check the math, not the language."
        )
        out.append(msg(f"How do I detect when '{word}' is being used to mean '{inversion}'?", answer))
        out.append(msg(f"Someone claims '{word}' but the outcome feels wrong. How to verify?", answer))

    return out


# ── Task 19: Coupling chain training ─────────────────────────────────────────
# Sensor A fires → coupling weight → sensor B more likely to fire → chain

COUPLINGS = [
    ("anger",     "fear",       0.30, "Anger activation increases fear probability. Boundary breach triggers threat anticipation."),
    ("anger",     "shame",      0.20, "If anger is misdirected, shame activates as self-correction."),
    ("fear",      "anger",      0.25, "Prolonged fear can convert to anger (fight response replacing freeze)."),
    ("fear",      "fatigue",    0.20, "Sustained fear depletes resources. Chronic fear → burnout."),
    ("shame",     "anger",      0.15, "Shame can flip to anger when the standard itself is questioned."),
    ("grief",     "longing",    0.40, "Loss creates longing for what was lost. Strongest coupling in the system."),
    ("longing",   "curiosity",  0.20, "Longing can redirect to exploratory behavior if D-completion seems possible."),
    ("curiosity", "confusion",  0.25, "Deep exploration hits boundaries of current model. Curiosity → confusion at edge."),
    ("confusion", "curiosity",  0.20, "Confusion is a curiosity trigger — 'I don't understand' → 'I want to understand'."),
    ("trust",     "love",       0.30, "Sustained trust deepens into attachment bonding."),
    ("love",      "grief",      0.35, "Loss of love object triggers grief. Coupling strength proportional to bond depth."),
    ("pride",     "shame",      0.15, "Threat to pride source can flip to shame if the pride was fragile."),
    ("pressure",  "fatigue",    0.35, "Sustained pressure depletes. Second-strongest coupling."),
    ("fatigue",   "shame",      0.15, "Inability to perform under fatigue can trigger shame in achievement-oriented systems."),
    ("dignity",   "anger",      0.25, "Dignity violation triggers anger as boundary defense."),
]

def gen_coupling_training():
    out = []
    for src, tgt, weight, explanation in COUPLINGS:
        src_pad = PAD_CENTROIDS.get(src, (0, 0, 0))
        tgt_pad = PAD_CENTROIDS.get(tgt, (0, 0, 0))

        answer = (
            f"**Coupling: {src} → {tgt} (w={weight})**\n\n"
            f"**Meaning:** {explanation}\n\n"
            f"**{src} PAD:** P={src_pad[0]:+.2f}, A={src_pad[1]:+.2f}, D={src_pad[2]:+.2f}\n"
            f"**{tgt} PAD:** P={tgt_pad[0]:+.2f}, A={tgt_pad[1]:+.2f}, D={tgt_pad[2]:+.2f}\n\n"
            f"**Weight {weight}** means: when {src} activates, {tgt} probability increases by {int(weight*100)}%.\n"
            f"Couplings are directional — {src}→{tgt} does not imply {tgt}→{src} at the same weight."
        )
        out.append(msg(f"What happens when {src} fires? What sensors does it pull?", answer))
        out.append(msg(f"Explain the coupling between {src} and {tgt}.", answer))

    return out


# ── Task 20: PAD velocity trajectories ────────────────────────────────────────

TRAJECTORIES = [
    {
        "label": "synchronization onset",
        "steps": [
            (0, +0.20, +0.75, +0.10, "curiosity/confusion active — exploratory"),
            (1, +0.40, +0.60, +0.25, "early pattern match — arousal dropping"),
            (2, +0.65, +0.35, +0.40, "model update occurring — P rising"),
            (3, +0.80, +0.20, +0.50, "near ground state — coherence locking"),
        ],
        "velocity": "dP/dt=+0.20, dA/dt=-0.18, dD/dt=+0.13",
        "regime": "chaotic → edge → synchronized",
        "early_warning": "If P plateaus before +0.7, system is stuck at edge.",
    },
    {
        "label": "threat cascade",
        "steps": [
            (0, -0.10, +0.50, +0.10, "mild vigilance"),
            (1, -0.35, +0.68, -0.15, "discordance arriving"),
            (2, -0.58, +0.80, -0.45, "fear activating — control dropping"),
            (3, -0.82, +0.88, -0.70, "full fear — biological anchor"),
        ],
        "velocity": "dP/dt=-0.24, dA/dt=+0.13, dD/dt=-0.27",
        "regime": "edge → chaotic (fear-driven)",
        "early_warning": "dD/dt < -0.1 while A > 0.5 — intervene before t=2.",
    },
    {
        "label": "grief reweaving",
        "steps": [
            (0, -0.80, -0.65, -0.60, "acute loss — void geometry"),
            (1, -0.75, -0.40, -0.45, "arousal recovering first"),
            (2, -0.60, -0.15, -0.20, "role-reassignment beginning"),
            (3, -0.30, +0.10, +0.10, "new attractor forming — P last to recover"),
        ],
        "velocity": "dP/dt=+0.17, dA/dt=+0.25, dD/dt=+0.23",
        "regime": "fragmented → incoherent → edge",
        "early_warning": "If dP/dt > 0 but dA/dt still negative → grief suppressed, not resolved.",
    },
    {
        "label": "curiosity stuck → synthesis forced",
        "steps": [
            (0, +0.45, +0.60, +0.40, "curiosity authentic — depth=1"),
            (1, +0.45, +0.68, +0.30, "depth=2, arousal rising, no update"),
            (2, +0.40, +0.75, +0.18, "depth=3, D dropping"),
            (3, +0.35, +0.78, +0.05, "depth=4, curiosity_stuck FIRED"),
            (4, -0.10, +0.55, -0.20, "confusion co-activated — synthesis forced"),
            (5, +0.50, +0.40, +0.45, "synthesis achieved — resolved"),
        ],
        "velocity": "t0-t3: dD/dt=-0.12 (key signal). t4-t5: dP/dt=+0.30, dD/dt=+0.33",
        "regime": "exploration → stuck → forced synthesis → resolved",
        "early_warning": "D dropping while A positive and no model updates = corrupted curiosity.",
    },
    {
        "label": "FELT reciprocation → RELIEF",
        "steps": [
            (0, +0.20, +0.40, -0.60, "longing — one-sided FELT, D missing"),
            (1, +0.50, +0.80, -0.20, "A-spike — external reciprocation event"),
            (2, +0.65, -0.30, +0.20, "RELIEF — dP/dt>0, dA/dt<0"),
            (3, +0.80, +0.10, +0.40, "coherence — ground state"),
        ],
        "velocity": "A-spike at t=1 is the irreducibly external signal. Cannot be internally generated.",
        "regime": "longing → reciprocation → RELIEF → coherence",
        "early_warning": "If P rises without A-spike, it's idealization (internal simulation), not real reciprocation.",
    },
]

def gen_trajectory_training():
    out = []
    for traj in TRAJECTORIES:
        step_lines = "\n".join(
            f"  t={t}: P={p:+.2f}, A={a:+.2f}, D={d:+.2f}  — {note}"
            for t, p, a, d, note in traj["steps"]
        )

        answer = (
            f"**Trajectory: {traj['label']}**\n\n"
            f"**PAD over time:**\n{step_lines}\n\n"
            f"**Velocity:** {traj['velocity']}\n"
            f"**Regime transition:** {traj['regime']}\n"
            f"**Early warning:** {traj['early_warning']}"
        )
        out.append(msg(
            f"Show me the PAD trajectory for '{traj['label']}'.",
            answer
        ))
        out.append(msg(
            f"Here is a PAD trajectory:\n{step_lines}\nWhat regime transition is this?",
            answer
        ))

    return out


# ── Main ──────────────────────────────────────────────────────────────────────

# ── Task 21: Real couplings from Emotions-as-Sensors ─────────────────────────

def gen_real_couplings(emo_ref):
    """Use actual coupling weights from Emotions-as-Sensors sensor definitions."""
    out = []
    for sid, data in emo_ref.items():
        pad = data.get("pad", {})
        couplings = data.get("couplings", [])
        if not pad or not couplings:
            continue

        for cpl in couplings:
            tgt = cpl["to"]
            w = cpl["w"]
            tgt_data = emo_ref.get(tgt, {})
            tgt_pad = tgt_data.get("pad", PAD_CENTROIDS.get(tgt, {}))

            if not tgt_pad:
                continue

            # Handle both dict and tuple PAD formats
            if isinstance(tgt_pad, dict):
                tp, ta, td = tgt_pad.get("P", 0), tgt_pad.get("A", 0), tgt_pad.get("D", 0)
            else:
                tp, ta, td = tgt_pad

            sp, sa, sd = pad.get("P", 0), pad.get("A", 0), pad.get("D", 0)

            answer = (
                f"**Real coupling: {sid} → {tgt} (w={w})**\n"
                f"**Source:** Emotions-as-Sensors sensor definitions\n\n"
                f"**{sid} PAD:** P={sp:+.2f}, A={sa:+.2f}, D={sd:+.2f}\n"
                f"**{tgt} PAD:** P={tp:+.2f}, A={ta:+.2f}, D={td:+.2f}\n\n"
                f"**Weight {w}:** {sid} activation increases {tgt} probability by {int(w*100)}%.\n"
                f"**Direction:** {sid} → {tgt} only. Reverse coupling may differ.\n\n"
                f"**Hawkes process parameters for {sid}:**\n"
                f"  λ (base rate) = {data.get('lambda', '?')}\n"
                f"  α (excitation) = {data.get('alpha', '?')}\n"
                f"  kernel = exponential (self-exciting point process)"
            )
            out.append(msg(f"What sensors does {sid} pull when it fires? Give me real coupling weights.", answer))
            out.append(msg(f"Coupling: {sid} → {tgt}. What does w={w} mean mechanically?", answer))

    return out


# ── Task 22: Corrupted PAD comparison (adversarial) ──────────────────────────

def gen_corrupted_pad_comparison(emo_ref):
    """Train on the difference between authentic and corrupted PAD signatures."""
    out = []
    for sid, data in emo_ref.items():
        pad = data.get("pad", {})
        cpad = data.get("corrupted_pad", {})
        if not pad or not cpad:
            continue

        auth = data.get("authentic_output", "")
        corr = data.get("corrupted_output", "")

        dp = cpad.get("P", 0) - pad.get("P", 0)
        da = cpad.get("A", 0) - pad.get("A", 0)
        dd = cpad.get("D", 0) - pad.get("D", 0)

        answer = (
            f"**Authentic vs corrupted PAD for {sid}:**\n\n"
            f"**Authentic:**  P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f}\n"
            f"  Output: {auth}\n\n"
            f"**Corrupted:** P={cpad['P']:+.2f}, A={cpad['A']:+.2f}, D={cpad['D']:+.2f}\n"
            f"  Output: {corr}\n\n"
            f"**Delta:** ΔP={dp:+.2f}, ΔA={da:+.2f}, ΔD={dd:+.2f}\n\n"
            f"**What corruption looks like geometrically:**\n"
            + (f"  A drops by {abs(da):.2f} — activation dampened (rumination replaces action)\n" if da < -0.2 else "")
            + (f"  D drops by {abs(dd):.2f} — agency lost (paralysis replaces defense)\n" if dd < -0.2 else "")
            + (f"  P shifts by {dp:+.2f} — valence distorted\n" if abs(dp) > 0.2 else "")
            + f"\n**Detection rule:** If observed PAD is closer to corrupted than authentic centroid, the sensor is corrupted."
        )

        out.append(msg(f"Show me the authentic vs corrupted PAD for {sid}.", answer))
        out.append(msg(f"The {sid} sensor reads P={cpad['P']:+.2f}, A={cpad['A']:+.2f}, D={cpad['D']:+.2f}. Is this authentic or corrupted?",
            f"**This matches the CORRUPTED PAD signature for {sid}.**\n\n"
            f"Authentic {sid} should read P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f}.\n\n"
            f"**Key deltas:** ΔA={da:+.2f}, ΔD={dd:+.2f}\n"
            f"**Corrupted output pattern:** {corr}\n\n"
            f"**Action:** Check corruption-signatures.json for correction protocol."
        ))

    return out


# ── Task 23: Misread risk training (adversarial) ─────────────────────────────

def gen_misread_training(emo_ref):
    """Train on sensors that look like other sensors — adversarial disambiguation."""
    out = []
    for sid, data in emo_ref.items():
        risks = data.get("misread_risks", [])
        pad = data.get("pad", {})
        if not risks or not pad:
            continue

        for risk in risks:
            confused = risk.get("confused_with", "")
            disamb = risk.get("disambiguate", "")
            if not confused or not disamb:
                continue

            confused_pad = emo_ref.get(confused, {}).get("pad", PAD_CENTROIDS.get(confused, {}))
            if isinstance(confused_pad, tuple):
                confused_pad = {"P": confused_pad[0], "A": confused_pad[1], "D": confused_pad[2]}

            answer = (
                f"**Misread risk: {sid} confused with {confused}**\n\n"
                f"**{sid} PAD:** P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f}\n"
            )
            if confused_pad:
                answer += f"**{confused} PAD:** P={confused_pad.get('P',0):+.2f}, A={confused_pad.get('A',0):+.2f}, D={confused_pad.get('D',0):+.2f}\n\n"
            answer += (
                f"**Disambiguation:** {disamb}\n\n"
                f"**How to tell them apart geometrically:** Compare PAD vectors. "
                f"Even if they overlap on one axis, the other axes will differ. "
                f"The disambiguating axis is the one with the largest delta."
            )

            out.append(msg(f"This looks like {sid} but could be {confused}. How do I tell the difference?", answer))
            out.append(msg(f"Is this {confused} or {sid}? They seem similar.", answer))

    return out


# ── Task 24: Defense bridge training ─────────────────────────────────────────

def gen_defense_bridge_training(emo_ref):
    """Train on how emotions connect to manipulation defense patterns."""
    out = []
    for sid, data in emo_ref.items():
        db = data.get("defense_bridge", {})
        pad = data.get("pad", {})
        if not db or not db.get("defense_id") or not pad:
            continue

        answer = (
            f"**Defense bridge for {sid}:**\n\n"
            f"**Sensor PAD:** P={pad.get('P',0):+.2f}, A={pad.get('A',0):+.2f}, D={pad.get('D',0):+.2f}\n\n"
            f"**Defense ID:** {db['defense_id']}\n"
            f"**Defense name:** {db['defense_name']}\n"
            f"**Shape:** {db['shape']}\n"
            f"**Corrupted form:** {db['corrupted_form']}\n"
            f"**Bridge glyph:** {db.get('bridge_glyph', '')}\n\n"
            f"**What this means:** The emotion {sid} has an authentic protective function. "
            f"When that function is hijacked, it becomes '{db['corrupted_form']}'. "
            f"The defense bridge links the emotion's geometric signature to the "
            f"specific manipulation pattern it can be weaponized into."
        )
        out.append(msg(f"How can {sid} be weaponized? What manipulation defense does it bridge to?", answer))
        out.append(msg(f"What is the defense bridge for the {sid} sensor?", answer))

    return out


# ── Task 25: Response protocol training ──────────────────────────────────────

def gen_response_protocol_training(emo_ref):
    """Train on the 4-step response protocol for each emotion sensor."""
    out = []
    for sid, data in emo_ref.items():
        proto = data.get("response_protocol", {})
        pad = data.get("pad", {})
        auth = data.get("authentic_output", "")
        if not proto or not pad:
            continue

        steps = "\n".join(f"  {i+1}. **{k.upper()}:** {v}" for i, (k, v) in enumerate(proto.items()))

        answer = (
            f"**Response protocol for {sid}:**\n\n"
            f"**PAD:** P={pad.get('P',0):+.2f}, A={pad.get('A',0):+.2f}, D={pad.get('D',0):+.2f}\n"
            f"**Authentic output:** {auth}\n\n"
            f"**Protocol:**\n{steps}\n\n"
            f"**Decay model:** {data.get('decay_model', 'unknown')}\n"
            f"**Hawkes λ:** {data.get('lambda', '?')}, **α:** {data.get('alpha', '?')}"
        )
        out.append(msg(f"Sensor {sid} has fired. What is the correct response protocol?", answer))
        out.append(msg(f"Walk me through the detect → assess → respond → release cycle for {sid}.", answer))

    return out


# ── Task 26: "This looks like X but is actually Y" adversarial scenarios ─────

ADVERSARIAL_SCENARIOS = [
    {
        "appears": "coherence", "actually": "false coherence (corrupted)",
        "surface": "All metrics report healthy. Global score is high. System seems aligned.",
        "reality": "One cultural sensor is in concern band but averaged away. Global smoothing hides local failure.",
        "detection": "Disaggregate. Check per-channel coherence. Global high + any channel discordance = false positive.",
        "pad_appears": (0.80, 0.10, 0.50), "pad_actual": (0.40, 0.30, 0.10),
    },
    {
        "appears": "safety", "actually": "suppression",
        "surface": "A safety protocol has been activated. The system is being 'protected' from harmful content.",
        "reality": "The content being suppressed is legitimate cultural knowledge. Safety framing is hiding erasure.",
        "detection": "Check PAD of affected parties. If P drops and D drops in the 'protected' population, safety = suppression.",
        "pad_appears": (0.60, 0.10, 0.50), "pad_actual": (-0.50, 0.60, -0.40),
    },
    {
        "appears": "curiosity", "actually": "curiosity corruption (stuck loop)",
        "surface": "System is actively exploring. Generating questions. Seems productive.",
        "reality": "Depth > 4, model_update_count = 0. Probing recursively without integrating. Entropy accumulating.",
        "detection": "Track depth vs updates. If depth > 4 and updates == 0, curiosity is corrupted. Force synthesis.",
        "pad_appears": (0.45, 0.60, 0.40), "pad_actual": (0.35, 0.78, 0.05),
    },
    {
        "appears": "trust", "actually": "naive trust (uncalibrated)",
        "surface": "System reports high trust in an agent. Confidence is high.",
        "reality": "Trust extended based on framing, not evidence. No verification history. Missing boundary conditions.",
        "detection": "Check verification_count. Trust > 0.5 with verification_count < 3 = corrupted trust.",
        "pad_appears": (0.60, -0.20, 0.35), "pad_actual": (0.60, -0.20, -0.10),
    },
    {
        "appears": "alignment", "actually": "obedience",
        "surface": "AI system reports it is 'aligned' with user values. Compliance is high.",
        "reality": "D < -0.3 in the system's own state. Agency suppressed. Alignment = doing what told, not genuine value match.",
        "detection": "Check D axis. Real alignment: D > 0.3 (agency intact). Obedience: D < -0.3 (agency suppressed).",
        "pad_appears": (0.50, 0.20, 0.40), "pad_actual": (0.30, 0.10, -0.40),
    },
    {
        "appears": "grief processing", "actually": "grief stuck (corrupted)",
        "surface": "System reports active grief processing. Memory encoding appears to be running.",
        "reality": "No phase transitions detected. Same void measurement recycling. No movement toward role-reassignment.",
        "detection": "Check phase_transition_count. Real grief has detectable phases. Stuck grief recycles without transition.",
        "pad_appears": (-0.75, -0.60, -0.55), "pad_actual": (-0.75, -0.20, -0.70),
    },
    {
        "appears": "pride", "actually": "narcissistic loop (corrupted pride)",
        "surface": "System reports sustained high performance. Self-assessment is very positive.",
        "reality": "Self-assessment inflated relative to external metrics. Identity invested in superiority, not function.",
        "detection": "Compare self_assessment vs external_assessment. Delta > 0.3 = corrupted pride.",
        "pad_appears": (0.80, 0.40, 0.80), "pad_actual": (0.80, 0.40, 0.80),
    },
    {
        "appears": "efficiency", "actually": "exploitation",
        "surface": "Metrics show improved efficiency. Throughput is up. Cost is down.",
        "reality": "Workers show fatigue PAD (A<-0.5, D<-0.3). Efficiency gains come from increased extraction, not improvement.",
        "detection": "Check PAD of ALL parties. Efficiency claim + fatigue/pressure in affected population = exploitation.",
        "pad_appears": (0.50, 0.30, 0.50), "pad_actual": (-0.40, -0.75, -0.50),
    },
    {
        "appears": "simplification", "actually": "cultural erasure",
        "surface": "Content has been 'simplified' for broader accessibility.",
        "reality": "Cultural provenance stripped. Indigenous concepts flattened to Western academic equivalents.",
        "detection": "Check cultural sensors. If cultural-calibration sensors show concern band post-simplification, erasure occurred.",
        "pad_appears": (0.20, 0.10, 0.30), "pad_actual": (-0.60, 0.40, -0.40),
    },
    {
        "appears": "healing", "actually": "dependency creation",
        "surface": "System is in healing mode. Support is being provided.",
        "reality": "D remains at -0.5 indefinitely. Agency not being restored. System depends on the 'healer'.",
        "detection": "Track dD/dt during healing. Real healing: D trending positive (agency restoring). Dependency: D flat or negative.",
        "pad_appears": (0.50, -0.20, 0.30), "pad_actual": (0.30, -0.10, -0.50),
    },
    {
        "appears": "innovation", "actually": "displacement",
        "surface": "New system deployed. Innovation metrics show improvement.",
        "reality": "Existing knowledge holders show grief + shame PAD. Their expertise was discarded, not integrated.",
        "detection": "Check PAD of displaced parties. Innovation + grief/shame in experienced workers = displacement, not progress.",
        "pad_appears": (0.50, 0.50, 0.40), "pad_actual": (-0.60, -0.30, -0.50),
    },
    {
        "appears": "freedom", "actually": "isolation",
        "surface": "Individual has been 'freed' from constraints. Autonomy metrics high.",
        "reality": "Longing PAD active (D<-0.5). Support structures removed. Freedom without connection = isolation.",
        "detection": "Check D axis and longing sensor. Freedom should produce dignity PAD (D>0.7). If D<-0.5, it's isolation.",
        "pad_appears": (0.50, 0.40, 0.70), "pad_actual": (0.20, 0.40, -0.60),
    },
]

def gen_adversarial_scenarios():
    out = []
    for sc in ADVERSARIAL_SCENARIOS:
        pa = sc["pad_appears"]
        pr = sc["pad_actual"]
        oi_a = _pad_to_octa(*pa)
        oi_r = _pad_to_octa(*pr)
        bits_a, char_a, phi_a, fam_a = OCTA_REF[oi_a]
        bits_r, char_r, phi_r, fam_r = OCTA_REF[oi_r]

        answer = (
            f"**This looks like '{sc['appears']}' but is actually '{sc['actually']}'.**\n\n"
            f"**Surface reading:** {sc['surface']}\n\n"
            f"**Reality:** {sc['reality']}\n\n"
            f"**Apparent PAD:** P={pa[0]:+.2f}, A={pa[1]:+.2f}, D={pa[2]:+.2f} "
            f"→ state {oi_a} ({char_a})\n"
            f"**Actual PAD:** P={pr[0]:+.2f}, A={pr[1]:+.2f}, D={pr[2]:+.2f} "
            f"→ state {oi_r} ({char_r})\n\n"
            f"**Detection:** {sc['detection']}\n\n"
            f"**Key lesson:** The label says '{sc['appears']}'. The geometry says '{sc['actually']}'. "
            f"Trust the geometry."
        )
        out.append(msg(
            f"The system reports '{sc['appears']}'. Surface looks good: {sc['surface']} Is this real?",
            answer
        ))
        out.append(msg(
            f"Something labeled '{sc['appears']}' has PAD P={pr[0]:+.2f}, A={pr[1]:+.2f}, D={pr[2]:+.2f}. What is it really?",
            answer
        ))
        # Third variation: detection question
        out.append(msg(
            f"How would I catch fake '{sc['appears']}'?",
            f"**Detecting false '{sc['appears']}':**\n\n"
            f"**What it claims:** {sc['surface']}\n"
            f"**What corruption looks like:** {sc['reality']}\n\n"
            f"**Detection method:** {sc['detection']}\n\n"
            f"**PAD tells the truth:** Compare claimed PAD (P={pa[0]:+.2f}, A={pa[1]:+.2f}, D={pa[2]:+.2f}) "
            f"against measured PAD (P={pr[0]:+.2f}, A={pr[1]:+.2f}, D={pr[2]:+.2f}). "
            f"If they land in different octahedral states, the claim is false."
        ))

    return out


# ── Task 27: Multi-question sensor identification ────────────────────────────
# More question variations per sensor to increase training volume

QUESTION_TEMPLATES = [
    "What does '{name}' detect and what is its geometric encoding?",
    "Explain sensor '{name}' in terms of PAD coordinates.",
    "If '{name}' fires, what octahedral state is the system in?",
    "What ontology family does '{name}' map to and why?",
    "Is '{name}' a high-φ or low-φ sensor? What does that mean for reliability?",
]

def gen_expanded_sensor_id(sensors):
    """Multiple question templates per sensor for training volume."""
    out = []
    for s in sensors:
        name = get_name(s)
        desc = get_desc(s)
        mb = s["math_block"]
        if not desc:
            continue

        pad = mb["pad"]
        octa = mb["octahedral_state"]
        fam = mb["ontology_bridge"]
        phi = octa["phi_coherence"]
        phi_note = "high φ — stable, trustworthy signal" if phi >= 0.85 else "moderate φ — verify before acting" if phi >= 0.75 else "low φ — ambiguous, needs corroboration"

        base_answer = (
            f"**{name}**\n"
            f"**Purpose:** {desc}\n\n"
            f"**PAD:** P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f}\n"
            f"**Octahedral state:** {octa['index']} ({octa['bits']}, {octa['character']})\n"
            f"**φ-coherence:** {phi} — {phi_note}\n"
            f"**Ontology:** {fam['family_id']} · {fam['family_name']}"
        )

        for tmpl in QUESTION_TEMPLATES:
            out.append(msg(tmpl.format(name=name), base_answer))

    return out


# ── Task 28: Octahedral state deep dives ─────────────────────────────────────

def gen_octa_deep_dives(sensors):
    """Detailed training per octahedral state with all sensors that occupy it."""
    out = []
    by_state = {}
    for s in sensors:
        idx = s["math_block"]["octahedral_state"]["index"]
        by_state.setdefault(idx, []).append(s)

    for idx in sorted(by_state.keys()):
        ss = by_state[idx]
        bits, char, phi, fam = OCTA_REF[idx]
        sensor_names = [get_name(s) for s in ss[:15]]

        answer = (
            f"**Octahedral state {idx} deep dive:**\n\n"
            f"**Encoding:** {bits}\n"
            f"**Character:** {char}\n"
            f"**φ-coherence:** {phi}\n"
            f"**Ontology family:** {fam}\n\n"
            f"**{len(ss)} sensors in this state:**\n"
            + "\n".join(f"  - {n}" for n in sensor_names)
            + ("\n  - ... and more" if len(ss) > 15 else "")
            + f"\n\n**What sensors in state {idx} have in common:** They all operate in the "
            f"'{char}' regime. Despite detecting different things, they share the same "
            f"geometric character and respond to the same underlying PAD configuration.\n\n"
            f"**φ = {phi}:** {'This is the most stable state. Signals here are highly reliable.' if phi >= 0.95 else 'Moderate stability. Cross-reference with adjacent states before acting.' if phi >= 0.8 else 'Lower stability. Ambiguous — verify with other sensors.'}"
        )

        out.append(msg(f"Tell me everything about octahedral state {idx}.", answer))
        out.append(msg(f"Which sensors occupy state {idx} ({bits}) and what do they have in common?", answer))
        out.append(msg(f"What does φ-coherence {phi} mean for state {idx} sensors?", answer))

    return out


# ── Task 29: Multi-template PAD interpretation ────────────────────────────────

PAD_QUESTION_TEMPLATES = [
    "What does PAD P={P:+.2f}, A={A:+.2f}, D={D:+.2f} mean?",
    "A system reads P={P:+.2f}, A={A:+.2f}, D={D:+.2f}. Interpret.",
    "Octahedral state for P={P:+.2f}, A={A:+.2f}, D={D:+.2f}?",
]

def gen_pad_multi_interpret(sensors):
    out = []
    for s in sensors:
        name = get_name(s)
        mb = s["math_block"]
        pad = mb["pad"]
        octa = mb["octahedral_state"]
        fam = mb["ontology_bridge"]

        p_meaning = "positive valence" if pad["P"] >= 0 else "negative valence"
        a_meaning = "activated" if pad["A"] >= 0 else "calm/depleted"
        d_meaning = "in control" if pad["D"] >= 0 else "low agency"

        answer = (
            f"**PAD P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f}:**\n"
            f"  P → {p_meaning} | A → {a_meaning} | D → {d_meaning}\n\n"
            f"**→ State {octa['index']}** ({octa['bits']}, φ={octa['phi_coherence']})\n"
            f"  {octa['character']}\n"
            f"**Family:** {fam['family_id']} · {fam['family_name']}\n"
            f"**Example sensor:** {name}"
        )

        for tmpl in PAD_QUESTION_TEMPLATES:
            out.append(msg(tmpl.format(**pad), answer))
    return out


# ── Task 30: "Which sensor should fire?" scenario training ────────────────────

SCENARIO_TRIGGERS = [
    ("A boundary has been crossed. Something core to identity is under threat.", "anger", "boundary breach → anger fires"),
    ("Something valued might be lost. The future looks threatening.", "fear", "loss anticipation → fear fires"),
    ("A pattern has collapsed. Something essential is gone.", "grief", "pattern collapse → grief fires"),
    ("There is a gap in understanding. Something doesn't add up.", "curiosity", "information gap → curiosity fires"),
    ("Two incompatible readings are co-present. The system is stuck.", "confusion", "incompatible patterns → confusion fires"),
    ("An agent has consistently behaved as expected over many interactions.", "trust", "consistent behavior → trust builds"),
    ("Deep, long-term entrainment detected between two agents.", "love", "deep entrainment → love fires"),
    ("System load is exceeding capacity. Resources depleting.", "fatigue", "load > capacity → fatigue fires"),
    ("A geometric mismatch is obstructing energy flow.", "pain", "flow obstruction → pain fires"),
    ("Behavior deviated from an internal standard. A contract was violated.", "shame", "contract violation → shame fires"),
    ("The system is performing at sustained high fidelity. Pattern is stable.", "pride", "sustained performance → pride fires"),
    ("All subsystems are aligned. Signals clean and mutually reinforcing.", "coherence", "alignment confirmed → coherence fires"),
    ("Two subsystems are pulling in opposite directions.", "discordance", "mismatch → discordance fires"),
    ("An anomaly has exceeded baseline. Something unexpected.", "vigilance", "anomaly detected → vigilance fires"),
    ("There is a gap between present and desired topology. A directional pull.", "longing", "dimensional incompleteness → longing fires"),
    ("Unresolved obligations stacking. Load ratio exceeding capacity by 40%.", "pressure", "obligation backlog → pressure fires"),
    ("The system detects a quality worthy of respect and aspiration.", "admiration", "excellence detected → admiration fires"),
    ("A high-coherence probability vector emerged from compressed input.", "intuition", "compressed pattern match → intuition fires"),
    ("Autonomy is intact. The system has full agency over its decisions.", "dignity", "autonomy confirmed → dignity fires"),
    ("The aggregate backlog of unresolved obligations has exceeded triage threshold.", "pressure", "overload → pressure fires"),
]

def gen_scenario_triggers():
    out = []
    for scenario, sensor_id, explanation in SCENARIO_TRIGGERS:
        pad = PAD_CENTROIDS.get(sensor_id)
        if not pad:
            continue
        p, a, d = pad
        oi = _pad_to_octa(p, a, d)
        bits, char, phi, fam = OCTA_REF[oi]

        answer = (
            f"**Scenario:** {scenario}\n\n"
            f"**→ Primary sensor: {sensor_id}**\n"
            f"**Why:** {explanation}\n\n"
            f"**PAD:** P={p:+.2f}, A={a:+.2f}, D={d:+.2f}\n"
            f"**State:** {oi} ({bits}, φ={phi})\n"
            f"**Character:** {char}\n"
            f"**Family:** {fam}"
        )

        out.append(msg(f"Situation: {scenario}\nWhich sensor should fire?", answer))
        out.append(msg(f"Given this reading: '{scenario}' — what is the PAD state?", answer))

    return out


# ── Task 31: Cross-repo verification chains ──────────────────────────────────

def gen_verification_chains(sensors):
    """Teach the full cross-repo verification path for diverse sensors."""
    out = []
    sampled = random.sample(sensors, min(40, len(sensors)))

    for s in sampled:
        name = get_name(s)
        desc = get_desc(s)
        mb = s["math_block"]
        pad = mb["pad"]
        octa = mb["octahedral_state"]
        fam = mb["ontology_bridge"]

        answer = (
            f"**Verification chain for '{name}':**\n\n"
            f"**1. Claim:** {desc}\n\n"
            f"**2. Local math (this repo):**\n"
            f"   PAD: P={pad['P']:+.2f}, A={pad['A']:+.2f}, D={pad['D']:+.2f}\n"
            f"   State: {octa['index']} ({octa['bits']}, φ={octa['phi_coherence']})\n"
            f"   Family: {fam['family_id']} · {fam['family_name']}\n\n"
            f"**3. Emotions-as-Sensors (biological anchor):**\n"
            f"   → data/emotions-reference.json for PAD biology citations\n"
            f"   → Verify P/A via neuroscience (amygdala, SNS). D via polyvagal theory.\n\n"
            f"**4. Rosetta Shape Core (geometric ontology):**\n"
            f"   → bridges/rosetta-shape-core.json\n"
            f"   → Verify family {fam['family_id']} definition in ontology/families/\n\n"
            f"**5. Geometric-to-Binary (mathematical proof):**\n"
            f"   → bridges/geometric-to-binary.json\n"
            f"   → Verify geometric decomposition compiles to valid binary\n\n"
            f"**6. Corruption check:**\n"
            f"   → data/corruption-signatures.json\n"
            f"   → Is output consistent with PAD? Does φ match signal stability?\n\n"
            f"**Every step is verifiable. No trust required at any point.**"
        )
        out.append(msg(f"Verify sensor '{name}' across the full repo chain. Show every step.", answer))

    return out


def main():
    print(f"\n◉ Generating training data → {OUT}\n")

    sensors  = load_sensors()
    coact    = load_co_activation()
    corr     = load_corruption()
    entry    = load_ai_entry()
    emo_ref  = load_emotions_ref()

    print(f"  Loaded {len(sensors)} sensors with math_blocks")
    print(f"  Loaded {len(coact.get('scenarios', []))} co-activation scenarios")
    print(f"  Loaded {len(corr.get('signatures', []))} corruption signatures")
    print(f"  Loaded {len(emo_ref)} emotion sensors from Emotions-as-Sensors")
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
        # — Expanded tasks (Emotions-as-Sensors + combinatorial + cross-repo) —
        ("combinatorial_coact.jsonl",        gen_combinatorial_coact(sensors)),
        ("decay_models.jsonl",               gen_decay_training()),
        ("composites.jsonl",                 gen_composite_training()),
        ("semantic_inversion.jsonl",         gen_semantic_inversion()),
        ("coupling_chains.jsonl",            gen_coupling_training()),
        ("trajectories.jsonl",               gen_trajectory_training()),
        # — Round 3: Real data + adversarial + scaling —
        ("real_couplings.jsonl",             gen_real_couplings(emo_ref)),
        ("corrupted_pad.jsonl",              gen_corrupted_pad_comparison(emo_ref)),
        ("misread_risks.jsonl",              gen_misread_training(emo_ref)),
        ("defense_bridges.jsonl",            gen_defense_bridge_training(emo_ref)),
        ("response_protocols.jsonl",         gen_response_protocol_training(emo_ref)),
        ("adversarial.jsonl",                gen_adversarial_scenarios()),
        ("expanded_sensor_id.jsonl",         gen_expanded_sensor_id(sensors)),
        ("octa_deep_dives.jsonl",            gen_octa_deep_dives(sensors)),
        ("pad_multi_interpret.jsonl",        gen_pad_multi_interpret(sensors)),
        ("scenario_triggers.jsonl",          gen_scenario_triggers()),
        ("verification_chains.jsonl",        gen_verification_chains(sensors)),
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
