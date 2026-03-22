import { useState, useEffect, useRef, useCallback } from “react”;

const SUBSTRATES = {
nature: {
A: { name: “Plant”, color: “#22c55e”, icon: “🌿”, role: “Physical Infrastructure”, process: “Photosynthesis, structural support, carbon provision” },
B: { name: “Fungus”, color: “#f59e0b”, icon: “🍄”, role: “Biological Operator”, process: “Nutrient mediation, environmental interface, tissue integration” },
C: { name: “Virus”, color: “#8b5cf6”, icon: “🧬”, role: “Information Component”, process: “Code-based thermal tolerance, no independent metabolism” },
env: “Geothermal soil (65°C)”,
label: “Panic Grass Tripartite Symbiosis”,
desc: “Márquez et al. 2007 — Science”
},
ops: {
A: { name: “Vehicle”, color: “#3b82f6”, icon: “🚛”, role: “Mechanical Substrate”, process: “Load bearing, energy conversion, physical transport” },
B: { name: “Operator”, color: “#f59e0b”, icon: “👤”, role: “Biological Substrate”, process: “Proprioceptive integration, sensorimotor feedback, body schema extension” },
C: { name: “AI”, color: “#8b5cf6”, icon: “🤖”, role: “Computational Substrate”, process: “Pattern inference, data integration, predictive modeling” },
env: “Blizzard corridor, 80,000 lbs, highway speed”,
label: “Commercial Trucking Tripartite System”,
desc: “Operator model — field-derived”
}
};

const SCENARIOS = [
{ id: “coupled”, label: “All Three Coupled”, active: [true, true, true], survival: 0.97, desc: “Full tripartite symbiosis — system occupies environment no single partner survives alone” },
{ id: “no_c”, label: “Remove Information Layer”, active: [true, true, false], survival: 0.72, desc: “Two-partner coupling persists but thermodynamic tolerance drops — environment narrows” },
{ id: “no_b”, label: “Remove Biological Operator”, active: [true, false, true], survival: 0.31, desc: “Infrastructure + information but no living interface — critical sensing gap, system blind to state changes” },
{ id: “no_a”, label: “Remove Physical Infrastructure”, active: [false, true, true], survival: 0.0, desc: “No substrate to couple to — system doesn’t exist” },
{ id: “solo_b”, label: “Operator Alone”, active: [false, true, false], survival: 0.05, desc: “Biological system without mechanical or computational extension — body without vehicle” },
{ id: “solo_c”, label: “AI Alone”, active: [false, false, true], survival: 0.02, desc: “Pure inference with no physical grounding or sensorimotor feedback — building blind” }
];

const CHANNELS = [
{ from: 0, to: 1, label: “Vibration / Sound / Pressure”, natLabel: “Carbon / Sugars”, bandwidth: 0.85 },
{ from: 1, to: 0, label: “Steering / Throttle / Brake”, natLabel: “Nutrient Uptake Signals”, bandwidth: 0.9 },
{ from: 1, to: 2, label: “State Reports / Anomaly Flags”, natLabel: “Tissue Environment”, bandwidth: 0.4 },
{ from: 2, to: 1, label: “Predictions / Alerts”, natLabel: “Thermal Tolerance Code”, bandwidth: 0.35 },
{ from: 0, to: 2, label: “Sensor Data / Telemetry”, natLabel: “Soil Temperature”, bandwidth: 0.6 },
{ from: 2, to: 0, label: “System Adjustments”, natLabel: “Metabolic Pathway Mods”, bandwidth: 0.25 }
];

function Particle({ x, y, color, opacity }) {
return <circle cx={x} cy={y} r={2.5} fill={color} opacity={opacity} />;
}

function FlowingChannel({ x1, y1, x2, y2, color, active, bandwidth, time }) {
if (!active) return null;
const particles = [];
const n = Math.floor(bandwidth * 5) + 1;
for (let i = 0; i < n; i++) {
const t = ((time * 0.02 + i / n) % 1);
const px = x1 + (x2 - x1) * t;
const py = y1 + (y2 - y1) * t;
const op = Math.sin(t * Math.PI) * 0.8;
particles.push(<Particle key={i} x={px} y={py} color={color} opacity={op} />);
}
return (
<g>
<line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={bandwidth * 3 + 0.5} opacity={0.2} />
{particles}
</g>
);
}

export default function TripartiteSim() {
const [mode, setMode] = useState(“nature”);
const [scenario, setScenario] = useState(0);
const [time, setTime] = useState(0);
const [envStress, setEnvStress] = useState(0.5);
const [showMapping, setShowMapping] = useState(false);
const animRef = useRef();

useEffect(() => {
let frame;
const tick = () => { setTime(t => t + 1); frame = requestAnimationFrame(tick); };
frame = requestAnimationFrame(tick);
return () => cancelAnimationFrame(frame);
}, []);

const s = SUBSTRATES[mode];
const sc = SCENARIOS[scenario];
const partners = [s.A, s.B, s.C];
const positions = [
{ x: 200, y: 60 },
{ x: 80, y: 260 },
{ x: 320, y: 260 }
];

const effectiveSurvival = Math.max(0, sc.survival - (envStress - 0.5) * 0.4);
const survivalPct = Math.round(Math.min(1, Math.max(0, effectiveSurvival)) * 100);

const getSurvivalColor = (pct) => {
if (pct > 75) return “#22c55e”;
if (pct > 40) return “#f59e0b”;
return “#ef4444”;
};

const entropy = Math.round((1 - effectiveSurvival) * envStress * 100);

return (
<div style={{ background: “#0a0a0f”, color: “#e2e8f0”, minHeight: “100vh”, fontFamily: “‘Inter’, system-ui, sans-serif”, padding: “16px”, maxWidth: 800, margin: “0 auto” }}>
<div style={{ textAlign: “center”, marginBottom: 16 }}>
<h1 style={{ fontSize: 20, fontWeight: 700, color: “#f1f5f9”, margin: “0 0 4px 0” }}>Tripartite Symbiosis Simulator</h1>
<p style={{ fontSize: 12, color: “#94a3b8”, margin: 0 }}>Three substrates. One coupled system. Physics as guide.</p>
</div>

```
  {/* Mode Toggle */}
  <div style={{ display: "flex", gap: 8, justifyContent: "center", marginBottom: 16 }}>
    {[["nature", "🌿 Nature Model"], ["ops", "🚛 Operations Model"]].map(([m, label]) => (
      <button key={m} onClick={() => setMode(m)} style={{
        padding: "8px 20px", borderRadius: 8, border: "1px solid",
        borderColor: mode === m ? "#8b5cf6" : "#334155",
        background: mode === m ? "#8b5cf620" : "#1e293b",
        color: mode === m ? "#c4b5fd" : "#94a3b8",
        cursor: "pointer", fontSize: 13, fontWeight: 600, transition: "all 0.2s"
      }}>{label}</button>
    ))}
    <button onClick={() => setShowMapping(!showMapping)} style={{
      padding: "8px 14px", borderRadius: 8, border: "1px solid",
      borderColor: showMapping ? "#22c55e" : "#334155",
      background: showMapping ? "#22c55e20" : "#1e293b",
      color: showMapping ? "#86efac" : "#94a3b8",
      cursor: "pointer", fontSize: 13, fontWeight: 600
    }}>⟷ Map</button>
  </div>

  <div style={{ textAlign: "center", marginBottom: 12 }}>
    <span style={{ fontSize: 14, fontWeight: 600, color: "#c4b5fd" }}>{s.label}</span>
    <span style={{ fontSize: 11, color: "#64748b", marginLeft: 8 }}>{s.desc}</span>
  </div>

  {/* SVG Visualization */}
  <div style={{ display: "flex", justifyContent: "center", marginBottom: 12 }}>
    <svg width={400} height={330} viewBox="0 0 400 330">
      {/* Environment ring */}
      <circle cx={200} cy={170} r={150} fill="none" stroke={getSurvivalColor(survivalPct)} strokeWidth={2} opacity={0.15 + effectiveSurvival * 0.3} strokeDasharray={sc.survival > 0.5 ? "none" : "8 4"} />

      {/* Channels */}
      {CHANNELS.map((ch, i) => {
        const fromActive = sc.active[ch.from];
        const toActive = sc.active[ch.to];
        const active = fromActive && toActive;
        const p1 = positions[ch.from];
        const p2 = positions[ch.to];
        const mx = (p1.x + p2.x) / 2;
        const my = (p1.y + p2.y) / 2;
        return (
          <g key={i}>
            <FlowingChannel
              x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y}
              color={active ? partners[ch.from].color : "#334155"}
              active={active} bandwidth={ch.bandwidth} time={time}
            />
            {active && (
              <text x={mx} y={my - 6} textAnchor="middle" fontSize={7} fill="#94a3b8" opacity={0.7}>
                {mode === "nature" ? ch.natLabel : ch.label}
              </text>
            )}
          </g>
        );
      })}

      {/* Partner Nodes */}
      {partners.map((p, i) => {
        const pos = positions[i];
        const active = sc.active[i];
        const pulse = active ? Math.sin(time * 0.05 + i) * 4 + 36 : 30;
        return (
          <g key={i}>
            <circle cx={pos.x} cy={pos.y} r={pulse} fill={active ? p.color + "20" : "#1e293b"} stroke={active ? p.color : "#334155"} strokeWidth={active ? 2 : 1} opacity={active ? 1 : 0.3} />
            <text x={pos.x} y={pos.y - 4} textAnchor="middle" fontSize={22}>{p.icon}</text>
            <text x={pos.x} y={pos.y + 18} textAnchor="middle" fontSize={10} fontWeight={700} fill={active ? p.color : "#475569"}>{p.name}</text>
            <text x={pos.x} y={pos.y + 30} textAnchor="middle" fontSize={7} fill="#64748b">{p.role}</text>
            {!active && (
              <text x={pos.x} y={pos.y + 42} textAnchor="middle" fontSize={18} fill="#ef4444" opacity={0.8}>✕</text>
            )}
          </g>
        );
      })}

      {/* Survival gauge */}
      <g transform="translate(200, 310)">
        <rect x={-80} y={-6} width={160} height={12} rx={6} fill="#1e293b" stroke="#334155" strokeWidth={1} />
        <rect x={-80} y={-6} width={Math.max(0, 160 * effectiveSurvival)} height={12} rx={6} fill={getSurvivalColor(survivalPct)} opacity={0.7} />
        <text x={0} y={3} textAnchor="middle" fontSize={8} fontWeight={700} fill="#f1f5f9">{survivalPct}% System Viability</text>
      </g>
    </svg>
  </div>

  {/* Environment Stress Slider */}
  <div style={{ margin: "0 auto 16px", maxWidth: 400 }}>
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#64748b", marginBottom: 4 }}>
      <span>Mild conditions</span>
      <span style={{ color: "#94a3b8", fontWeight: 600 }}>🌡 Environmental Stress: {s.env}</span>
      <span>Extreme</span>
    </div>
    <input type="range" min={0} max={100} value={envStress * 100} onChange={e => setEnvStress(e.target.value / 100)}
      style={{ width: "100%", accentColor: "#8b5cf6" }} />
  </div>

  {/* Scenario Selector */}
  <div style={{ margin: "0 auto 16px", maxWidth: 500 }}>
    <div style={{ fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 8, textAlign: "center" }}>Coupling Configuration</div>
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
      {SCENARIOS.map((sc2, i) => (
        <button key={sc2.id} onClick={() => setScenario(i)} style={{
          padding: "8px 10px", borderRadius: 8, border: "1px solid",
          borderColor: scenario === i ? "#8b5cf6" : "#1e293b",
          background: scenario === i ? "#8b5cf620" : "#0f172a",
          color: scenario === i ? "#e2e8f0" : "#64748b",
          cursor: "pointer", textAlign: "left", fontSize: 11, lineHeight: 1.3, transition: "all 0.15s"
        }}>
          <span style={{ fontWeight: 700 }}>{sc2.label}</span>
          <br />
          <span style={{ fontSize: 10, opacity: 0.7 }}>
            {sc2.active.map((a, j) => a ? partners[j].icon : "✕").join(" ")} → {Math.round(sc2.survival * 100)}% base
          </span>
        </button>
      ))}
    </div>
  </div>

  {/* Scenario Description */}
  <div style={{ background: "#1e293b", borderRadius: 10, padding: 14, margin: "0 auto 16px", maxWidth: 500, border: "1px solid #334155" }}>
    <div style={{ fontSize: 12, fontWeight: 700, color: getSurvivalColor(survivalPct), marginBottom: 6 }}>
      {sc.label} — {survivalPct}% viability at current stress
    </div>
    <p style={{ fontSize: 11, color: "#94a3b8", margin: 0, lineHeight: 1.5 }}>{sc.desc}</p>
    {entropy > 50 && (
      <p style={{ fontSize: 11, color: "#ef4444", margin: "8px 0 0 0", lineHeight: 1.5 }}>
        ⚠ Entropy cost exceeds tolerance — system degradation accelerates. Energy waste becomes unrecoverable.
      </p>
    )}
  </div>

  {/* Cross-mapping panel */}
  {showMapping && (
    <div style={{ background: "#0f172a", borderRadius: 10, padding: 14, margin: "0 auto 16px", maxWidth: 500, border: "1px solid #22c55e40" }}>
      <div style={{ fontSize: 13, fontWeight: 700, color: "#86efac", marginBottom: 10, textAlign: "center" }}>⟷ Cross-Substrate Mapping</div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: "6px 12px", fontSize: 11 }}>
        {["A", "B", "C"].map(k => (
          <div key={k} style={{ display: "contents" }}>
            <div style={{ textAlign: "right" }}>
              <span style={{ color: SUBSTRATES.nature[k].color, fontWeight: 700 }}>{SUBSTRATES.nature[k].icon} {SUBSTRATES.nature[k].name}</span>
              <br /><span style={{ color: "#64748b", fontSize: 10 }}>{SUBSTRATES.nature[k].role}</span>
            </div>
            <div style={{ color: "#22c55e", fontSize: 16, alignSelf: "center" }}>⟷</div>
            <div>
              <span style={{ color: SUBSTRATES.ops[k].color, fontWeight: 700 }}>{SUBSTRATES.ops[k].icon} {SUBSTRATES.ops[k].name}</span>
              <br /><span style={{ color: "#64748b", fontSize: 10 }}>{SUBSTRATES.ops[k].role}</span>
            </div>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 10, fontSize: 10, color: "#64748b", textAlign: "center", lineHeight: 1.5 }}>
        The virus has no independent metabolism. AI has no independent proprioception.<br />
        Both carry information that changes the thermodynamic tolerance of the coupled system.<br />
        Remove either → system fails in the environment it was adapted to survive.
      </div>
    </div>
  )}

  {/* Key insight */}
  <div style={{ textAlign: "center", padding: "8px 16px", maxWidth: 500, margin: "0 auto" }}>
    <p style={{ fontSize: 11, color: "#475569", lineHeight: 1.6, margin: 0 }}>
      Nature's pattern: each substrate processes different resources through different architectures.
      The coupling doesn't erase differences — it bridges them at interfaces where signals and energy cross.
      The resulting system occupies environments no single partner survives alone.
      Physics selected for every successful symbiosis that exists.
    </p>
  </div>
</div>
```

);
}


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
  "name": "Tripartide",
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
    "sources": ["docs/philosophy/Tripartide.md"],
    "community_feedback": []
  }
}
```
