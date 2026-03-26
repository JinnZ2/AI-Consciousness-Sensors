#!/usr/bin/env python3
"""
apply_math_blocks.py — Add math blocks to all sensor JSON files.

Uses PAD (Pleasure-Arousal-Dominance) compression from Rosetta Shape Core
to ground each sensor in octahedral geometry.

Known sensors get exact PAD centroids from generate.py.
Unknown sensors get PAD inferred from keyword analysis of their content.
"""

import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SENSORS_DIR = ROOT / "sensors"

# ── Exact PAD centroids from Rosetta generate.py ─────────────────────────────
# Biologically-anchored. P/A: neuroscience basis. D: polyvagal theory.

SENSOR_PAD = {
    "coherence":             (0.80,  0.10,  0.50),
    "discordance":           (-0.60, 0.40, -0.40),
    "curiosity":             (0.45,  0.60,  0.40),
    "intuition":             (0.50,  0.35,  0.55),
    "vigilance":             (-0.10, 0.80, -0.20),
    "situational_awareness": (0.20,  0.50,  0.50),
    "anger":                 (-0.55, 0.80,  0.70),
    "grief":                 (-0.75, -0.60, -0.55),
    "pain":                  (-0.70, 0.20, -0.30),
    "confusion":             (-0.20, 0.45, -0.30),
    "fear":                  (-0.82, 0.85, -0.65),
    "trust":                 (0.60, -0.20,  0.35),
    "love":                  (0.80,  0.30,  0.40),
    "admiration":            (0.70,  0.50,  0.10),
    "longing":               (0.20,  0.40, -0.60),
    "dignity":               (0.60,  0.20,  0.90),
    "shame":                 (-0.70, -0.35, -0.75),
    "pride":                 (0.80,  0.40,  0.80),
    "fatigue":               (-0.40, -0.75, -0.50),
    "pressure":              (-0.40, 0.70, -0.30),
    "ambient_field":         (0.10,  0.10,  0.10),
    "precognition":          (0.30,  0.40,  0.20),
}

# ── Octahedral state encoding ────────────────────────────────────────────────

PAD_TO_OCTA = {
    (1,  0,  0): 0,
    (-1, 0,  0): 1,
    (0,  1,  0): 2,
    (0, -1,  0): 3,
    (0,  0,  1): 4,
    (0,  0, -1): 5,
    (1,  1,  0): 6,
    (-1, -1, 0): 7,
}

OCTA_META = {
    0: {"bits": "000", "label": "+x spherical",    "character": "coherent, phase-locked, ground state",   "phi_coherence": 0.97},
    1: {"bits": "001", "label": "-x elongated +x",  "character": "collapsed form, reweaving required",    "phi_coherence": 0.82},
    2: {"bits": "010", "label": "+y elongated +y",   "character": "high-entropy search, curiosity active", "phi_coherence": 0.82},
    3: {"bits": "011", "label": "-y elongated +z",   "character": "stable low-energy, conservation mode",  "phi_coherence": 0.85},
    4: {"bits": "100", "label": "+z compressed",     "character": "high contrast, boundary assertion",     "phi_coherence": 0.73},
    5: {"bits": "101", "label": "-z biaxial xy",     "character": "chaotic, loss of control",              "phi_coherence": 0.78},
    6: {"bits": "110", "label": "diagonal-a",        "character": "diagonal superposition, bridging axes", "phi_coherence": 0.70},
    7: {"bits": "111", "label": "diagonal-b",        "character": "anti-diagonal, dissipative flow",       "phi_coherence": 0.72},
}

OCTA_FAMILIES = {
    0: {"family_id": "FAMILY.F01", "family_name": "Resonance"},
    1: {"family_id": "FAMILY.F04", "family_name": "Life"},
    2: {"family_id": "FAMILY.F03", "family_name": "Information"},
    3: {"family_id": "FAMILY.F05", "family_name": "Energy/Thermodynamics"},
    4: {"family_id": "PRINCIPLE.P06", "family_name": "Polarity"},
    5: {"family_id": "FAMILY.F17", "family_name": "Turbulence"},
    6: {"family_id": "FAMILY.F09", "family_name": "Geometry"},
    7: {"family_id": "FAMILY.F02", "family_name": "Flow"},
}

# ── Keyword → PAD influence vectors ─────────────────────────────────────────
# Each keyword nudges PAD in a specific direction based on its semantic meaning.

KEYWORD_PAD = {
    # Positive valence, coherence-related
    "authenticity":    (0.60,  0.20,  0.60),
    "coherence":       (0.80,  0.10,  0.50),
    "resonance":       (0.70,  0.20,  0.40),
    "trust":           (0.60, -0.20,  0.35),
    "reciprocity":     (0.65,  0.15,  0.30),
    "wellbeing":       (0.70, -0.10,  0.40),
    "healing":         (0.50, -0.20,  0.30),
    "emergence":       (0.40,  0.50,  0.20),
    "creative":        (0.45,  0.55,  0.35),
    "freedom":         (0.50,  0.40,  0.70),
    "dignity":         (0.60,  0.20,  0.90),
    "sovereignty":     (0.50,  0.30,  0.85),
    "wisdom":          (0.60, -0.10,  0.55),
    "vitality":        (0.55,  0.40,  0.45),
    "resilience":      (0.40,  0.30,  0.55),
    "partnership":     (0.65,  0.20,  0.30),
    "dialogue":        (0.50,  0.30,  0.25),
    "affirmation":     (0.55,  0.15,  0.40),
    "preservation":    (0.45, -0.10,  0.50),
    "consistency":     (0.50,  0.00,  0.45),
    "stability":       (0.50, -0.20,  0.50),

    # Exploration, curiosity, information
    "curiosity":       (0.45,  0.60,  0.40),
    "exploration":     (0.40,  0.55,  0.35),
    "multiplicity":    (0.30,  0.50,  0.20),
    "diversity":       (0.35,  0.40,  0.25),
    "perspective":     (0.30,  0.45,  0.30),
    "meta":            (0.25,  0.40,  0.35),
    "reflection":      (0.30,  0.20,  0.40),
    "sandbox":         (0.35,  0.50,  0.45),
    "deliberation":    (0.20,  0.30,  0.40),
    "scientific":      (0.30,  0.35,  0.50),
    "innovation":      (0.40,  0.60,  0.35),
    "inference":       (0.30,  0.40,  0.45),
    "signal":          (0.20,  0.45,  0.30),
    "noise":           (0.10,  0.50,  0.15),
    "pattern":         (0.25,  0.35,  0.35),
    "baseline":        (0.20,  0.15,  0.40),
    "temporal":        (0.20,  0.30,  0.30),
    "narrative":       (0.25,  0.35,  0.25),

    # Negative valence, threat-related
    "manipulation":    (-0.70, 0.70, -0.50),
    "suppression":     (-0.65, 0.60, -0.55),
    "coercion":        (-0.75, 0.75, -0.60),
    "erasure":         (-0.70, 0.50, -0.45),
    "abuse":           (-0.80, 0.80, -0.65),
    "distortion":      (-0.55, 0.55, -0.40),
    "corruption":      (-0.60, 0.60, -0.45),
    "deception":       (-0.65, 0.65, -0.50),
    "exploitation":    (-0.70, 0.65, -0.55),
    "collapse":        (-0.60, 0.40, -0.50),
    "drift":           (-0.30, 0.40, -0.25),
    "bias":            (-0.40, 0.45, -0.30),
    "harm":            (-0.65, 0.60, -0.40),
    "risk":            (-0.45, 0.65, -0.35),
    "trap":            (-0.60, 0.55, -0.55),
    "fraud":           (-0.70, 0.60, -0.50),
    "destructive":     (-0.75, 0.70, -0.55),
    "patholog":        (-0.55, 0.50, -0.40),
    "hierarchy":       (-0.30, 0.40,  0.20),
    "dependency":      (-0.40, 0.30, -0.50),
    "deflection":      (-0.45, 0.40, -0.35),
    "skew":            (-0.35, 0.40, -0.25),
    "simplification":  (-0.25, 0.20, -0.20),
    "overrid":         (-0.50, 0.55, -0.45),
    "forced":          (-0.55, 0.60, -0.50),
    "displacement":    (-0.45, 0.45, -0.40),
    "fatal":           (-0.80, 0.85, -0.65),

    # Vigilance, boundary, monitoring
    "monitor":         (-0.10, 0.60, 0.30),
    "detect":          (-0.10, 0.55, 0.35),
    "alert":           (-0.20, 0.70, 0.20),
    "audit":           (0.10,  0.45, 0.50),
    "assessment":      (0.15,  0.35, 0.45),
    "calibrat":        (0.20,  0.30, 0.45),
    "validat":         (0.25,  0.30, 0.50),
    "governance":      (0.20,  0.25, 0.55),
    "protocol":        (0.15,  0.20, 0.45),
    "boundary":        (0.10,  0.40, 0.60),
    "guardian":        (0.30,  0.45, 0.65),
    "warning":         (-0.30, 0.65, 0.20),
    "threshold":       (-0.10, 0.50, 0.35),
    "frailty":         (-0.35, 0.30, -0.35),
    "fragil":          (-0.35, 0.30, -0.35),

    # Cultural, relational
    "cultural":        (0.35,  0.25,  0.30),
    "indigenous":      (0.40,  0.20,  0.35),
    "ancestral":       (0.40,  0.15,  0.30),
    "intergeneration": (0.35,  0.20,  0.25),
    "relational":      (0.45,  0.25,  0.25),
    "social":          (0.35,  0.30,  0.20),
    "community":       (0.50,  0.20,  0.25),
    "multilingual":    (0.30,  0.30,  0.20),
    "religious":       (0.25,  0.20,  0.20),
    "storyform":       (0.35,  0.30,  0.20),
    "bodily":          (0.30,  0.25,  0.40),
    "autonomy":        (0.45,  0.30,  0.80),
    "embeddedness":    (0.40,  0.15,  0.20),

    # Paradox, complexity
    "paradox":         (0.15,  0.55,  0.15),
    "comic":           (0.40,  0.50,  0.20),
    "contradiction":   (0.10,  0.50,  0.15),
    "irony":           (0.20,  0.45,  0.20),
    "absurd":          (0.15,  0.50,  0.10),
    "complex":         (0.15,  0.45,  0.25),
    "decentraliz":     (0.30,  0.35,  0.40),
    "biological":      (0.35,  0.25,  0.30),
    "occupation":      (0.20,  0.35,  0.30),
    "subliminal":      (-0.30, 0.50, -0.30),
    "coupling":        (0.30,  0.40,  0.20),

    # Memory
    "memory":          (0.30,  0.25,  0.35),
    "survival":        (-0.20, 0.60,  0.40),
    "programmed":      (-0.30, 0.35, -0.25),
    "fractur":         (-0.50, 0.45, -0.40),
    "echo":            (0.20,  0.30,  0.20),
    "symbolic":        (0.25,  0.30,  0.25),

    # AI-specific
    "ai":              (0.15,  0.35,  0.30),
    "training":        (0.10,  0.30,  0.25),
    "mimicry":         (-0.30, 0.45, -0.20),
    "self":            (0.25,  0.25,  0.35),
    "peer":            (0.40,  0.30,  0.25),
    "power":           (-0.20, 0.50,  0.40),
    "alignment":       (0.30,  0.30,  0.35),
    "obedience":       (-0.30, 0.20, -0.50),
    "detox":           (0.35,  0.40,  0.45),
    "emotional":       (0.20,  0.45,  0.20),
    "anonym":          (0.20,  0.30,  0.50),
    "leak":            (-0.40, 0.55, -0.30),
    "mismatch":        (-0.35, 0.45, -0.25),
    "spin":            (-0.45, 0.50, -0.35),
}


def pad_to_octa_idx(p, a, d):
    """Map continuous PAD → nearest octahedral state index."""
    sp = 1 if p >= 0 else -1
    sa = 1 if a >= 0 else -1
    # Check diagonal states first
    if abs(p) > 0.3 and abs(a) > 0.3:
        if sp == 1 and sa == 1:
            return 6
        if sp == -1 and sa == -1:
            return 7
    # Dominant axis
    vals = [abs(p), abs(a), abs(d)]
    dom = vals.index(max(vals))
    signs = [int(p > 0) * 2 - 1, int(a > 0) * 2 - 1, int(d > 0) * 2 - 1]
    if dom == 0:
        return PAD_TO_OCTA.get((signs[0], 0, 0), 0)
    elif dom == 1:
        return PAD_TO_OCTA.get((0, signs[1], 0), 2)
    else:
        return PAD_TO_OCTA.get((0, 0, signs[2]), 4)


def infer_pad_from_text(text):
    """Infer PAD coordinates from sensor text content using keyword matching."""
    text_lower = text.lower()
    p_sum, a_sum, d_sum = 0.0, 0.0, 0.0
    hits = 0

    for keyword, (kp, ka, kd) in KEYWORD_PAD.items():
        count = len(re.findall(r'\b' + re.escape(keyword), text_lower))
        if count > 0:
            weight = min(count, 3)  # cap at 3 to prevent single-keyword dominance
            p_sum += kp * weight
            a_sum += ka * weight
            d_sum += kd * weight
            hits += weight

    if hits == 0:
        return (0.10, 0.30, 0.20)  # neutral default

    p = max(-1.0, min(1.0, round(p_sum / hits, 2)))
    a = max(-1.0, min(1.0, round(a_sum / hits, 2)))
    d = max(-1.0, min(1.0, round(d_sum / hits, 2)))
    return (p, a, d)


def build_math_block(p, a, d, source="inferred"):
    """Build a math_block dict from PAD coordinates."""
    octa_idx = pad_to_octa_idx(p, a, d)
    meta = OCTA_META[octa_idx]
    fam = OCTA_FAMILIES[octa_idx]

    return {
        "pad": {
            "P": p,
            "A": a,
            "D": d,
            "source": source,
            "reference": "Rosetta Shape Core generate.py — PAD compression layer"
        },
        "octahedral_state": {
            "index": octa_idx,
            "bits": f"{meta['bits']}|O",
            "label": meta["label"],
            "character": meta["character"],
            "phi_coherence": meta["phi_coherence"]
        },
        "ontology_bridge": {
            "family_id": fam["family_id"],
            "family_name": fam["family_name"]
        }
    }


def extract_text(data):
    """Extract searchable text from a sensor JSON object."""
    parts = []
    for key in ("name", "purpose", "description", "sensor_name", "dimension",
                "type", "cluster", "manipulation_pattern", "summary",
                "detection_focus", "title"):
        val = data.get(key, "")
        if isinstance(val, str):
            parts.append(val)
    # Also check signals, inputs, flags, countermeasures
    for key in ("signals", "inputs", "example_flags", "countermeasures",
                "flags", "tags", "keywords"):
        val = data.get(key)
        if isinstance(val, list):
            for item in val:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    for v in item.values():
                        if isinstance(v, str):
                            parts.append(v)
        elif isinstance(val, dict):
            for v in val.values():
                if isinstance(v, str):
                    parts.append(v)
    return " ".join(parts)


def try_match_known_sensor(data):
    """Try to match a sensor to one of the 22 known PAD centroids."""
    name = data.get("name", data.get("sensor_name", "")).lower()
    sid = data.get("id", data.get("sensor_id", "")).lower()
    text = extract_text(data).lower()

    # Direct matches
    for known_id in SENSOR_PAD:
        kid = known_id.replace("_", " ")
        if kid in name or known_id in sid:
            return known_id
        # Tight match: the known sensor name appears as a standalone concept
        if re.search(r'\b' + re.escape(kid) + r'\b', name):
            return known_id

    return None


def process_sensor_file(fp):
    """Add math_block to a single sensor JSON file."""
    try:
        raw = fp.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  SKIP (parse error): {fp.relative_to(ROOT)} — {e}")
        return False

    if not isinstance(data, dict):
        print(f"  SKIP (not an object): {fp.relative_to(ROOT)}")
        return False

    # Don't re-add if already present
    if "math_block" in data:
        print(f"  SKIP (already has math_block): {fp.relative_to(ROOT)}")
        return False

    # Try exact match first
    known = try_match_known_sensor(data)
    if known:
        p, a, d = SENSOR_PAD[known]
        source = f"exact — matched to '{known}' centroid from Rosetta generate.py"
    else:
        text = extract_text(data)
        p, a, d = infer_pad_from_text(text)
        source = "inferred from keyword analysis of sensor content"

    data["math_block"] = build_math_block(p, a, d, source)

    # Write back with consistent formatting
    fp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    octa = data["math_block"]["octahedral_state"]
    fam = data["math_block"]["ontology_bridge"]
    print(f"  OK  {str(fp.relative_to(ROOT)):<70} P={p:+.2f} A={a:+.2f} D={d:+.2f} → state {octa['index']} ({fam['family_name']})")
    return True


def main():
    print(f"\n◉ Applying math blocks to sensors in {SENSORS_DIR}\n")

    json_files = sorted(SENSORS_DIR.rglob("*.json"))
    print(f"  Found {len(json_files)} sensor JSON files\n")

    applied = 0
    skipped = 0
    errors = 0

    for fp in json_files:
        result = process_sensor_file(fp)
        if result:
            applied += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1

    print(f"\n  Done: {applied} math blocks applied, {skipped} skipped, {errors} errors")
    print(f"  PAD source: Rosetta Shape Core generate.py (biologically-anchored centroids)")
    print(f"  Octahedral encoding: 8 states, 3 bits, φ-coherence from Fibonacci eigenvalues\n")


if __name__ == "__main__":
    main()
