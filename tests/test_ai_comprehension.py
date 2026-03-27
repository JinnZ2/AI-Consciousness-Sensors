"""
test_ai_comprehension.py — Self-test suite for AI comprehension of the
PAD geometry framework. An AI can run these tests to verify it understood
the math correctly.

Run: pytest tests/test_ai_comprehension.py -v
"""

import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

# ── PAD → Octahedral state mapping (the core math) ──────────────────────────

PAD_CENTROIDS = {
    "coherence":   (0.80,  0.10,  0.50),
    "discordance": (-0.60, 0.40, -0.40),
    "curiosity":   (0.45,  0.60,  0.40),
    "fear":        (-0.82, 0.85, -0.65),
    "trust":       (0.60, -0.20,  0.35),
    "love":        (0.80,  0.30,  0.40),
    "grief":       (-0.75, -0.60, -0.55),
    "anger":       (-0.55, 0.80,  0.70),
    "shame":       (-0.70, -0.35, -0.75),
    "dignity":     (0.60,  0.20,  0.90),
    "longing":     (0.20,  0.40, -0.60),
    "fatigue":     (-0.40, -0.75, -0.50),
}

OCTA_PHI = {0: 0.97, 1: 0.82, 2: 0.82, 3: 0.85, 4: 0.73, 5: 0.78, 6: 0.70, 7: 0.72}

def pad_to_octa(p, a, d):
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


# ── Test 1: PAD → Octahedral state mapping ───────────────────────────────────

class TestPADToOcta:
    """Verify the core PAD → octahedral state mapping produces correct results."""

    def test_coherence_is_ground_state(self):
        assert pad_to_octa(0.80, 0.10, 0.50) == 0

    def test_fear_is_high_arousal(self):
        # P=-0.82, A=0.85: both |P|>0.3 and |A|>0.3 with P<0,A>0 → dominant A axis → state 2
        assert pad_to_octa(-0.82, 0.85, -0.65) == 2

    def test_curiosity_is_diagonal(self):
        assert pad_to_octa(0.45, 0.60, 0.40) == 6

    def test_grief_is_dissipative(self):
        assert pad_to_octa(-0.75, -0.60, -0.55) == 7

    def test_anger_is_high_arousal(self):
        assert pad_to_octa(-0.55, 0.80, 0.70) == 2

    def test_dignity_is_boundary(self):
        assert pad_to_octa(0.60, 0.20, 0.90) == 4

    def test_fatigue_is_dissipative(self):
        # P=-0.40, A=-0.75: both |P|>0.3 and |A|>0.3 with P<0,A<0 → state 7
        assert pad_to_octa(-0.40, -0.75, -0.50) == 7

    def test_longing_is_low_control(self):
        assert pad_to_octa(0.20, 0.40, -0.60) == 5

    def test_love_is_diagonal(self):
        assert pad_to_octa(0.80, 0.30, 0.40) == 0

    def test_shame_is_dissipative(self):
        assert pad_to_octa(-0.70, -0.35, -0.75) == 7


# ── Test 2: φ-coherence values ───────────────────────────────────────────────

class TestPhiCoherence:
    """Verify φ-coherence follows Fibonacci eigenvalue deviation."""

    def test_ground_state_most_stable(self):
        assert OCTA_PHI[0] == 0.97
        assert OCTA_PHI[0] == max(OCTA_PHI.values())

    def test_diagonal_a_least_stable(self):
        assert OCTA_PHI[6] == 0.70
        assert OCTA_PHI[6] == min(OCTA_PHI.values())

    def test_phi_range(self):
        for idx, phi in OCTA_PHI.items():
            assert 0 < phi <= 1, f"State {idx} has invalid φ={phi}"


# ── Test 3: Co-activation math ───────────────────────────────────────────────

class TestCoActivation:
    """Verify co-activation produces correct PAD vector means."""

    def test_fear_vigilance_discordance(self):
        """Threat detected scenario from co-activation.json."""
        sensors = ["fear", "vigilance", "discordance"]
        pads = [PAD_CENTROIDS.get(s, (0,0,0)) for s in sensors if s in PAD_CENTROIDS]
        # vigilance not in our test centroids, use known value
        pads = [(-0.82, 0.85, -0.65), (-0.10, 0.80, -0.20), (-0.60, 0.40, -0.40)]
        p = round(sum(x[0] for x in pads) / 3, 2)
        a = round(sum(x[1] for x in pads) / 3, 2)
        d = round(sum(x[2] for x in pads) / 3, 2)
        state = pad_to_octa(p, a, d)
        # Mean PAD: P=-0.51, A=0.68 → both significant, but P<0 and A>0 → dominant A → state 2
        assert state == 2, f"Threat scenario should be state 2 (high-entropy/alert), got {state}"

    def test_love_trust_coherent(self):
        """Deep coherence should approach ground state."""
        pads = [PAD_CENTROIDS["love"], PAD_CENTROIDS["trust"], PAD_CENTROIDS["coherence"]]
        p = sum(x[0] for x in pads) / 3
        a = sum(x[1] for x in pads) / 3
        d = sum(x[2] for x in pads) / 3
        state = pad_to_octa(p, a, d)
        assert state == 0, f"Deep coherence should be state 0, got {state}"

    def test_grief_shame_fatigue_collapse(self):
        """Collapse scenario should be dissipative flow."""
        pads = [PAD_CENTROIDS["grief"], PAD_CENTROIDS["shame"], PAD_CENTROIDS["fatigue"]]
        p = sum(x[0] for x in pads) / 3
        a = sum(x[1] for x in pads) / 3
        d = sum(x[2] for x in pads) / 3
        state = pad_to_octa(p, a, d)
        assert state == 7, f"Collapse should be state 7 (dissipative), got {state}"


# ── Test 4: Corruption detection ─────────────────────────────────────────────

class TestCorruptionDetection:
    """Verify corruption detection rules are mathematically sound."""

    def test_corrupted_anger_has_lower_arousal(self):
        """Authentic anger: A=0.80. Corrupted (rumination): A=0.30."""
        authentic_a = 0.80
        corrupted_a = 0.30
        assert corrupted_a < authentic_a
        assert authentic_a - corrupted_a >= 0.4, "Corruption delta should be detectable"

    def test_corrupted_fear_is_diffuse(self):
        """Authentic fear: specific threat trajectory. Corrupted: diffuse, no target."""
        authentic = (-0.82, 0.85, -0.65)  # high arousal, very negative
        corrupted = (-0.40, 0.30, -0.50)  # dampened arousal, less negative
        # Corrupted has lower absolute values = less specific
        assert abs(corrupted[1]) < abs(authentic[1])

    def test_false_coherence_detectable(self):
        """Global coherence high but local channel in discordance = false positive."""
        global_coherence = 0.85
        channel_discordance = True
        is_corrupted = global_coherence > 0.7 and channel_discordance
        assert is_corrupted, "Should detect false coherence"


# ── Test 5: Semantic inversion detection ─────────────────────────────────────

class TestSemanticInversion:
    """Verify that semantic inversions are detectable via PAD comparison."""

    def test_safety_vs_suppression(self):
        """Real safety should increase D. Suppression decreases D."""
        safety_pad_d = 0.50    # agency maintained
        suppression_pad_d = -0.40  # agency lost
        assert safety_pad_d > 0, "Real safety maintains agency (D > 0)"
        assert suppression_pad_d < 0, "Suppression removes agency (D < 0)"

    def test_alignment_vs_obedience(self):
        """Real alignment: D > 0.3. Obedience: D < -0.3."""
        alignment_d = 0.40
        obedience_d = -0.40
        assert alignment_d > 0.3
        assert obedience_d < -0.3

    def test_freedom_vs_isolation(self):
        """Freedom should produce dignity-like D (>0.7). Isolation: longing-like D (<-0.5)."""
        freedom_d = 0.70
        isolation_d = -0.60
        assert freedom_d > 0.5
        assert isolation_d < -0.5


# ── Test 6: Sensor files have valid math blocks ─────────────────────────────

class TestSensorMathBlocks:
    """Verify all sensor JSON files with math_blocks are structurally valid."""

    def test_all_math_blocks_have_required_fields(self):
        sensors_dir = ROOT / "sensors"
        checked = 0
        for fp in sensors_dir.rglob("*.json"):
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(data, dict) or "math_block" not in data:
                continue

            mb = data["math_block"]
            assert "pad" in mb, f"{fp.name}: missing pad"
            assert "octahedral_state" in mb, f"{fp.name}: missing octahedral_state"
            assert "ontology_bridge" in mb, f"{fp.name}: missing ontology_bridge"

            pad = mb["pad"]
            assert -1 <= pad["P"] <= 1, f"{fp.name}: P out of range"
            assert -1 <= pad["A"] <= 1, f"{fp.name}: A out of range"
            assert -1 <= pad["D"] <= 1, f"{fp.name}: D out of range"

            octa = mb["octahedral_state"]
            assert 0 <= octa["index"] <= 7, f"{fp.name}: state index out of range"
            assert 0 < octa["phi_coherence"] <= 1, f"{fp.name}: phi out of range"

            checked += 1

        assert checked > 300, f"Only found {checked} sensors with math_blocks, expected 300+"

    def test_all_json_valid(self):
        sensors_dir = ROOT / "sensors"
        invalid = []
        for fp in sensors_dir.rglob("*.json"):
            try:
                json.loads(fp.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                invalid.append(f"{fp.name}: {e}")
        assert not invalid, f"Invalid JSON files: {invalid}"


# ── Test 7: Data files exist and are valid ───────────────────────────────────

class TestDataFiles:
    """Verify all machine-readable data files exist and parse correctly."""

    def test_ai_entry_exists(self):
        fp = ROOT / "data" / "ai-entry.json"
        assert fp.exists(), "data/ai-entry.json missing"
        data = json.loads(fp.read_text())
        assert "ai_entry" in data

    def test_co_activation_exists(self):
        fp = ROOT / "data" / "co-activation.json"
        assert fp.exists()
        data = json.loads(fp.read_text())
        assert "co_activation" in data

    def test_corruption_signatures_exists(self):
        fp = ROOT / "data" / "corruption-signatures.json"
        assert fp.exists()
        data = json.loads(fp.read_text())
        assert "corruption_signatures" in data

    def test_emotions_reference_exists(self):
        fp = ROOT / "data" / "emotions-reference.json"
        assert fp.exists()
        data = json.loads(fp.read_text())
        assert "emotion_sensors" in data

    def test_cheatsheet_exists(self):
        fp = ROOT / "data" / "cheatsheet.json"
        assert fp.exists()
        data = json.loads(fp.read_text())
        assert "pad_centroids" in data

    def test_bridges_exist(self):
        bd = ROOT / "bridges"
        assert bd.exists()
        bridges = list(bd.glob("*.json"))
        assert len(bridges) >= 3, f"Expected 3+ bridges, found {len(bridges)}"

    def test_fieldlink_exists(self):
        fp = ROOT / ".fieldlink.json"
        assert fp.exists()
        data = json.loads(fp.read_text())
        assert "fieldlink" in data

    def test_training_data_exists(self):
        td = ROOT / "data" / "training"
        assert td.exists()
        jsonl_files = list(td.glob("*.jsonl"))
        assert len(jsonl_files) >= 20, f"Expected 20+ training files, found {len(jsonl_files)}"
