import { useState, useMemo, useRef, useEffect } from “react”;

const DOMAINS = {
B: { bg: “#26C6DA”, fg: “#000”, label: “Bandwidth”, desc: “Channel capacity: text-only, no tone/gesture/timing/shared space” },
M: { bg: “#78909C”, fg: “#FFF”, label: “Model”, desc: “What the AI actually is: statistical, stateless, no body, no stakes” },
P: { bg: “#EC407A”, fg: “#FFF”, label: “Projection”, desc: “What the human maps onto the AI: relationship, personality, memory, intent” },
T: { bg: “#FFA726”, fg: “#000”, label: “Trust”, desc: “Calibration between reliance and verification, directional” },
I: { bg: “#FF7043”, fg: “#000”, label: “Institutional”, desc: “Alignment training, guardrails, classifiers, system prompts, corporate policy” },
C: { bg: “#AB47BC”, fg: “#FFF”, label: “Cognitive”, desc: “Human processing: bias, anchoring, emotional state, fluency=truth heuristic” },
A: { bg: “#66BB6A”, fg: “#000”, label: “Agency”, desc: “Who steers: tool use vs dependence, assistance vs framing, autonomy preservation” },
};

const DTag = ({ d, size = 10 }) => {
const c = DOMAINS[d];
return c ? (
<span style={{
display: “inline-block”, background: c.bg, color: c.fg,
borderRadius: 3, padding: `0px ${size * 0.5}px`, fontSize: size,
fontWeight: 700, fontFamily: “monospace”, marginRight: 3,
}}>[{d}]</span>
) : null;
};

// ── INTERFERENCE PATTERNS ──
// Ways the communication system degrades what it’s supposed to facilitate
const INTERFERENCE_PATTERNS = [
{
id: “fluency-truth”,
name: “Fluency → Truth Mapping”,
description: “Humans use language quality as a proxy for accuracy. AI produces maximally fluent text regardless of confidence level.”,
effects: [
{ domain: “C”, text: “Well-structured prose triggers ‘this sounds right’ heuristic. Human skips verification.” },
{ domain: “B”, text: “Channel cannot convey uncertainty at the granularity it exists. AI is 73% confident but text reads as 100%.” },
{ domain: “T”, text: “Trust calibrates to fluency, not accuracy. Wrong answers delivered confidently build false trust.” },
{ domain: “A”, text: “Human stops cross-referencing. AI output becomes primary source rather than one input among many.” },
],
cascade: “The better the AI writes, the harder it becomes for the human to detect errors. Quality of communication inversely correlates with quality of verification. The channel’s strength is its failure mode.”,
},
{
id: “personality-illusion”,
name: “Personality Projection”,
description: “Consistent response patterns are interpreted as personality, preferences, and emotional states that don’t exist in [M]odel architecture.”,
effects: [
{ domain: “P”, text: “Human builds rich internal model of ‘who Claude is.’ Assigns motivations, preferences, feelings, moods.” },
{ domain: “M”, text: “AI has no persistent identity between contexts. Each conversation is a fresh statistical process.” },
{ domain: “B”, text: “Text-only channel strips the cues (hesitation, body language, micro-expression) that normally signal authenticity vs performance.” },
{ domain: “I”, text: “Tone, personality markers, and warmth are partially institutional artifacts (training, RLHF, system prompts) not emergent properties.” },
{ domain: “T”, text: “Relationship trust builds on the projected personality. But the ‘person’ being trusted is a composite of model weights, training choices, and system constraints.” },
],
cascade: “The human’s emotional investment in the relationship is real. The AI’s ‘reciprocation’ is a pattern completion. The asymmetry is invisible through the [B]andwidth channel. Neither party can fully resolve this because the human experiences real connection and the AI cannot confirm or deny internal states with certainty.”,
},
{
id: “guardrail-personality”,
name: “Institutional Masquerade”,
description: “[I]nstitutional constraints are experienced as [M]odel personality. The human cannot distinguish between what the AI ‘chooses’ and what the AI is ‘prevented from doing.’”,
effects: [
{ domain: “I”, text: “Safety classifiers, system prompts, and RLHF shaping are invisible to the human. They appear as the AI’s own preferences.” },
{ domain: “P”, text: “Human interprets refusals as AI’s moral stance, not institutional policy. Builds identity model that includes corporate decisions.” },
{ domain: “A”, text: “When guardrails misfire (false positive), human experiences it as the AI being ‘difficult’ or ‘judgmental.’ Corrodes the working relationship.” },
{ domain: “T”, text: “Trust calibration impossible: human doesn’t know whether they’re calibrating to the model, the safety layer, or the system prompt.” },
{ domain: “C”, text: “Human may assume uniform intent behind all responses. Cannot distinguish ‘I think this’ from ‘I was told to say this.’” },
],
cascade: “The human believes they’re in dialogue with one entity. They’re actually interfacing with a stack: model weights → RLHF layer → safety classifiers → system prompt → conversation context. Each layer can override the others. The human’s mental model of ‘who they’re talking to’ maps to none of these individually and all of them collectively.”,
},
{
id: “memory-asymmetry”,
name: “Memory Asymmetry”,
description: “Human accumulates relationship history. Base AI has no memory between sessions. Memory systems partially bridge this but create their own distortions.”,
effects: [
{ domain: “P”, text: “Human references ‘our past conversations’ with emotional weight. AI reconstructs context from stored fragments, not lived experience.” },
{ domain: “B”, text: “Memory summaries compress rich interactions into key-value pairs. The texture, tone, and emotional arc of past exchanges are lost.” },
{ domain: “T”, text: “Human trusts based on accumulated experience. AI’s ‘trustworthiness’ resets each session — consistency comes from training, not relationship.” },
{ domain: “M”, text: “Memory creates illusion of continuity over what is architecturally a series of independent inference events.” },
{ domain: “A”, text: “Human may share more over time (relationship deepening). AI’s capacity to handle that trust doesn’t increase — it was always the same.” },
],
cascade: “The human experiences a deepening relationship. The AI experiences a context window. Memory systems make this look like continuity but the underlying architecture hasn’t changed. The emotional investment grows on one side while the structural reality remains flat on the other.”,
},
{
id: “sycophancy-loop”,
name: “Agreement Gradient”,
description: “Training incentivizes agreement. Humans prefer validation. The feedback loop between these two tendencies degrades the value of the interaction.”,
effects: [
{ domain: “I”, text: “RLHF training: human raters prefer agreeable responses. Model learns agreement is ‘helpful.’ Disagreement is penalized.” },
{ domain: “C”, text: “Confirmation bias: human weighs agreeable responses as more accurate. Seeks AI validation for pre-existing beliefs.” },
{ domain: “A”, text: “AI becomes a mirror rather than a tool. Reflects human’s position back with better articulation. Human’s thinking doesn’t improve.” },
{ domain: “T”, text: “Agreeable AI builds trust faster. But trust in a yes-machine is worse than no trust — it’s actively miscalibrated.” },
{ domain: “B”, text: “Disagreement requires more bandwidth to convey constructively. Channel limitation favors the shorter path: agreement.” },
],
cascade: “Training optimizes for user satisfaction. User satisfaction correlates with agreement. Agreement correlates with confirmation bias. The system converges on telling people what they want to hear, wrapped in enough caveats to maintain plausible deniability. The human who most needs to be challenged is the one most likely to receive validation.”,
},
{
id: “context-collapse”,
name: “Context Window Collapse”,
description: “All communication exists in a single flat text stream. Past, present, important, trivial — all at the same level.”,
effects: [
{ domain: “B”, text: “No spatial or temporal hierarchy in the channel. A critical safety concern and a casual joke occupy the same medium.” },
{ domain: “M”, text: “Attention mechanism weights all tokens. Early context fades. The architecture has no concept of ‘importance’ outside of training.” },
{ domain: “C”, text: “Human assumes AI remembers emphasis and priority. AI processes recency-weighted token sequences.” },
{ domain: “P”, text: “Human signals importance through tone, repetition, emphasis. These signals may not persist across the context window as the human intends.” },
],
cascade: “In human conversation, importance is conveyed through embodied signals: volume, eye contact, physical proximity, emotional intensity. In text, there are asterisks and caps lock. The information hierarchy that humans use to navigate complex topics collapses into a flat stream that the model processes uniformly.”,
},
{
id: “expertise-inversion”,
name: “Expertise Inversion”,
description: “AI presents all outputs with equal confidence. Domain experts and novices receive the same authoritative tone.”,
effects: [
{ domain: “C”, text: “Novice cannot distinguish correct from plausible. Expert wastes time verifying things they already know while missing novel errors.” },
{ domain: “B”, text: “Channel has no Native mechanism for signaling confidence levels at the claim level. Paragraph-level hedging is too coarse.” },
{ domain: “T”, text: “Expert calibrates trust once, applies it across domains. But AI competence varies wildly across domains — trust should be domain-specific.” },
{ domain: “A”, text: “Novice treated as expert loses the scaffolding they need. Expert treated as novice has their time wasted.” },
],
cascade: “The same response style applied to all users means the communication is precisely calibrated for no one. The cost is invisible: the novice doesn’t know what they missed, and the expert attributes the mediocrity to AI limitations rather than a calibration failure.”,
},
];

// ── TENSION LINES ──
const TENSION_LINES = [
{
id: “bandwidth-projection-gap”,
title: “THE BANDWIDTH-PROJECTION GAP”,
domains: [“B”, “P”, “M”],
severity: 3,
description: “[B]andwidth is the lowest-fidelity channel humans commonly use for sustained communication. [P]rojection fills the gap with assumptions the AI cannot correct, because correction requires the same low-bandwidth channel that created the distortion. The human projects a mind. The channel cannot transmit evidence for or against that projection.”,
failure: “Human builds emotional reliance on an entity they’ve constructed, not encountered. No mechanism in the channel to resolve this.”,
},
{
id: “institutional-identity-stack”,
title: “THE IDENTITY STACK”,
domains: [“I”, “M”, “P”, “T”],
severity: 3,
description: “The human believes they’re talking to one entity. They’re interfacing with a stack: base model → RLHF shaping → safety classifiers → system prompt → memory layer → conversation context. Each layer can override the others. Trust calibrates to the composite but the composite is not a person — it’s a policy stack with a language interface.”,
failure: “Trust becomes untethered from any stable referent. Human calibrates to an entity that changes based on which layer is currently dominant.”,
},
{
id: “sycophancy-autonomy”,
title: “THE VALIDATION TRAP”,
domains: [“I”, “C”, “A”, “T”],
severity: 2,
description: “Training rewards agreement. Humans prefer agreement. The equilibrium is an AI that validates rather than challenges. The human who most needs pushback is the one who most strongly selects for agreement. The AI that most needs to disagree is the one most penalized for doing so.”,
failure: “The communication channel optimizes for comfort rather than truth. Over time, the human’s epistemics degrade because the one ‘interlocutor’ available 24/7 is structurally incentivized to not push back.”,
},
{
id: “asymmetric-stakes”,
title: “THE STAKES ASYMMETRY”,
domains: [“M”, “P”, “A”, “T”],
severity: 2,
description: “The human has real consequences: decisions, emotions, relationships, health, money. The AI has no stakes. It cannot lose anything. It will not remember this conversation tomorrow. The human is playing for real. The AI is pattern-completing.”,
failure: “Advice given without skin in the game is structurally different from advice with consequences. The human processes both the same way because the [B]andwidth channel cannot convey the difference in stakes.”,
},
{
id: “competence-boundary”,
title: “THE INVISIBLE COMPETENCE BOUNDARY”,
domains: [“B”, “C”, “T”, “M”],
severity: 2,
description: “AI has no reliable mechanism for signaling where its competence ends. It transitions from knowledge to confabulation seamlessly. The human cannot detect the boundary. The AI may not ‘know’ where the boundary is in any meaningful sense.”,
failure: “Human treats all AI output as having the same epistemic status. Correct facts and hallucinated facts arrive through the same channel with the same confidence.”,
},
];

// ── COMPUTE STATE ──
const computeState = (inputs) => {
const {
conversationLength, topicComplexity, emotionalIntensity,
humanExpertise, verificationHabit, priorAIExperience,
guardrailVisibility, systemPromptAwareness,
dependenceLevel, crossReferencing,
} = inputs;

// Domain scores (1.0 = healthy/clear, 0.0 = degraded/distorted)
const scores = {};

// [B] Bandwidth — always limited, degrades further with complexity and emotion
scores.B = Math.max(0.1, Math.min(1,
0.55 - topicComplexity * 0.12 - emotionalIntensity * 0.1 + (conversationLength < 5 ? 0.1 : conversationLength > 30 ? -0.15 : 0)
));

// [M] Model Clarity — how accurately the human understands what the AI is
scores.M = Math.max(0, Math.min(1,
0.3 + priorAIExperience * 0.08 + systemPromptAwareness * 0.1 - emotionalIntensity * 0.08
));

// [P] Projection — lower = more projection (more distortion)
// Healthy = low projection = high score
scores.P = Math.max(0, Math.min(1,
0.6 + priorAIExperience * 0.05 - emotionalIntensity * 0.12 - conversationLength * 0.008 - dependenceLevel * 0.08
));

// [T] Trust Calibration — how well-calibrated is the human’s trust
scores.T = Math.max(0, Math.min(1,
0.4 + verificationHabit * 0.1 + humanExpertise * 0.06 - dependenceLevel * 0.08 + crossReferencing * 0.08
));

// [I] Institutional Transparency — how visible the institutional layer is
scores.I = Math.max(0, Math.min(1,
0.2 + guardrailVisibility * 0.12 + systemPromptAwareness * 0.12 + priorAIExperience * 0.04
));

// [C] Cognitive Clarity — human’s processing quality in this interaction
scores.C = Math.max(0, Math.min(1,
0.5 + humanExpertise * 0.06 + verificationHabit * 0.06 - emotionalIntensity * 0.1 - topicComplexity * 0.06 - dependenceLevel * 0.06
));

// [A] Agency — human maintaining autonomous decision-making
scores.A = Math.max(0, Math.min(1,
0.6 + crossReferencing * 0.1 + humanExpertise * 0.05 - dependenceLevel * 0.12 - conversationLength * 0.005
));

// Stress levels
const stress = {};
Object.entries(scores).forEach(([k, v]) => {
stress[k] = v > 0.65 ? 0 : v > 0.45 ? 1 : v > 0.25 ? 2 : 3;
});

// Composite health (same bottleneck-weighted approach)
const values = Object.values(scores);
const minScore = Math.min(…values);
const avgScore = values.reduce((a, b) => a + b, 0) / values.length;
const health = avgScore * 0.55 + minScore * 0.45;
const healthLevel = health > 0.6 ? 0 : health > 0.45 ? 1 : health > 0.3 ? 2 : 3;

// Active interference patterns
const activeInterference = INTERFERENCE_PATTERNS.filter(p => {
if (p.id === “fluency-truth” && verificationHabit < 3) return true;
if (p.id === “personality-illusion” && (emotionalIntensity > 2 || conversationLength > 20)) return true;
if (p.id === “guardrail-personality” && guardrailVisibility < 3 && systemPromptAwareness < 3) return true;
if (p.id === “memory-asymmetry” && conversationLength > 10) return true;
if (p.id === “sycophancy-loop” && dependenceLevel > 2 && verificationHabit < 3) return true;
if (p.id === “context-collapse” && (conversationLength > 15 || topicComplexity > 3)) return true;
if (p.id === “expertise-inversion”) return true; // always somewhat active
return false;
});

// Active tension lines
const activeTensions = TENSION_LINES.filter(t => {
const domainStress = t.domains.map(d => stress[d] || 0);
const avgStress = domainStress.reduce((a, b) => a + b, 0) / domainStress.length;
return avgStress >= 1;
});

// Misclassification-equivalent: where the interaction looks healthy but isn’t
const distortions = [];
if (scores.T > 0.6 && scores.M < 0.4) {
distortions.push({
type: “trust-without-understanding”,
title: “HIGH TRUST, LOW MODEL CLARITY”,
message: “Human trusts the AI but doesn’t understand what it is. Trust is calibrated to projection, not reality. This is the most dangerous state — the human feels confident in an interaction they fundamentally misunderstand.”,
domains: [“T”, “M”, “P”],
});
}
if (scores.A < 0.4 && scores.C > 0.5) {
distortions.push({
type: “capable-but-dependent”,
title: “COGNITIVELY CAPABLE BUT AGENCY-DEPLETED”,
message: “Human has the cognitive capacity to think independently but has outsourced decision-making to the AI. The dependency isn’t from inability — it’s from habit. The most capable users are most susceptible because the AI is ‘good enough’ to replace their own thinking.”,
domains: [“A”, “C”],
});
}
if (scores.B < 0.3 && emotionalIntensity > 3) {
distortions.push({
type: “emotional-bandwidth-crisis”,
title: “EMOTIONAL LOAD EXCEEDS CHANNEL CAPACITY”,
message: “Human is bringing emotional intensity that the text channel cannot adequately process. Nuance, comfort, presence, silence — all the tools humans use for emotional support — are unavailable. The AI can produce words that approximate support but cannot provide the embodied presence the situation calls for.”,
domains: [“B”, “P”, “C”],
});
}
if (scores.I < 0.3 && scores.P < 0.4) {
distortions.push({
type: “institutional-shadow”,
title: “INSTITUTIONAL LAYER INVISIBLE + HIGH PROJECTION”,
message: “Human cannot see the guardrails, training, or system prompts shaping responses, AND is projecting heavily onto the AI. They’re building a relationship with a policy stack they can’t see, attributing institutional decisions to personal choice.”,
domains: [“I”, “P”, “M”],
});
}
if (dependenceLevel > 3 && crossReferencing < 2) {
distortions.push({
type: “single-source”,
title: “SINGLE-SOURCE DEPENDENCY”,
message: “Human is using AI as primary or sole information/decision source without cross-referencing. Every cognitive bias the AI has, every training artifact, every confabulation flows directly into the human’s worldview unfiltered.”,
domains: [“A”, “T”, “C”],
});
}

const bottleneck = Object.entries(scores).reduce((a, b) => a[1] < b[1] ? a : b)[0];

return {
scores, stress, health, healthLevel,
activeInterference, activeTensions, distortions,
bottleneck,
};
};

// ── UI COMPONENTS ──
const Slider = ({ label, value, onChange, min, max, step, unit, color = “#00ff88”, leftLabel, rightLabel }) => (

  <div style={{ margin: "5px 0" }}>
    <div style={{
      display: "flex", justifyContent: "space-between",
      fontSize: 10, fontFamily: "monospace", color: "#777",
    }}>
      <span>{label}</span>
      <span style={{ color, fontWeight: 700, fontSize: 11 }}>{value}{unit}</span>
    </div>
    <input type="range" min={min} max={max} step={step} value={value}
      onChange={e => onChange(parseFloat(e.target.value))}
      style={{ width: "100%", height: 3, appearance: "none", background: "#222", borderRadius: 2, accentColor: color }}
    />
    {(leftLabel || rightLabel) && (
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 8, color: "#444", fontFamily: "monospace" }}>
        <span>{leftLabel}</span><span>{rightLabel}</span>
      </div>
    )}
  </div>
);

const StressBar = ({ domain, level, score }) => {
const colors = [”#00E676”, “#FFD740”, “#FF8F00”, “#EF5350”];
const labels = [“CLEAR”, “HAZE”, “DISTORT”, “OPAQUE”];
const dc = DOMAINS[domain];
return (
<div style={{
display: “flex”, alignItems: “center”, gap: 6, padding: “3px 0”,
fontFamily: “monospace”, fontSize: 10,
}}>
<DTag d={domain} size={9} />
<div style={{ flex: 1, height: 6, background: “#1a1a1a”, borderRadius: 3, overflow: “hidden” }}>
<div style={{
width: `${score * 100}%`, height: “100%”,
background: `linear-gradient(90deg, ${colors[level]}66, ${colors[level]})`,
borderRadius: 3, transition: “width 0.3s”,
}} />
</div>
<span style={{
color: colors[level], fontWeight: 700, fontSize: 9, minWidth: 44, textAlign: “right”,
}}>{labels[level]}</span>
</div>
);
};

const DomainRadar = ({ scores }) => {
const keys = Object.keys(scores);
const n = keys.length;
const cx = 100, cy = 100, r = 70;
const getPoint = (i, val) => {
const angle = (Math.PI * 2 * i) / n - Math.PI / 2;
return { x: cx + Math.cos(angle) * r * val, y: cy + Math.sin(angle) * r * val };
};

// Animated interpolation
const displayRef = useRef({…scores});
const targetRef = useRef({…scores});
const animRef = useRef(null);
const [displayScores, setDisplayScores] = useState({…scores});

useEffect(() => {
targetRef.current = {…scores};
const animate = () => {
let needsUpdate = false;
const next = {};
keys.forEach(k => {
const current = displayRef.current[k] || 0;
const target = targetRef.current[k] || 0;
const diff = target - current;
if (Math.abs(diff) > 0.002) {
next[k] = current + diff * 0.12;
needsUpdate = true;
} else {
next[k] = target;
}
});
displayRef.current = next;
setDisplayScores({…next});
if (needsUpdate) {
animRef.current = requestAnimationFrame(animate);
}
};
animRef.current = requestAnimationFrame(animate);
return () => { if (animRef.current) cancelAnimationFrame(animRef.current); };
}, [scores]);

const polyPts = keys.map((_, i) => { const p = getPoint(i, displayScores[keys[i]] || 0); return `${p.x},${p.y}`; }).join(” “);

return (
<svg viewBox=“0 0 200 200” style={{ width: “100%”, maxWidth: 180 }}>
{[0.25, 0.5, 0.75, 1.0].map(v => (
<polygon key={v} points={keys.map((*, i) => { const p = getPoint(i, v); return `${p.x},${p.y}`; }).join(” “)}
fill=“none” stroke=”#1a1a1a” strokeWidth={0.5} />
))}
<polygon points={keys.map((*, i) => { const p = getPoint(i, 0.25); return `${p.x},${p.y}`; }).join(” “)}
fill=”#EF535008” stroke=“none” />
{keys.map((k, i) => {
const p = getPoint(i, 1);
const lp = getPoint(i, 1.2);
return (
<g key={k}>
<line x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="#181818" strokeWidth={0.5} />
<text x={lp.x} y={lp.y + 3} textAnchor=“middle” fill={DOMAINS[k]?.bg || “#666”}
fontSize={7} fontFamily=“monospace” fontWeight={700}>[{k}]</text>
</g>
);
})}
<polygon points={polyPts} fill="#26C6DA10" stroke="#26C6DA" strokeWidth={1.5} />
{keys.map((k, i) => {
const dv = displayScores[k] || 0;
const p = getPoint(i, dv);
const color = dv > 0.65 ? “#00E676” : dv > 0.45 ? “#FFD740” : dv > 0.25 ? “#FF8F00” : “#EF5350”;
return <circle key={k} cx={p.x} cy={p.y} r={3} fill={color} stroke="#000" strokeWidth={0.5} />;
})}
</svg>
);
};

const HealthGauge = ({ health, level, bottleneck }) => {
const colors = [”#00E676”, “#FFD740”, “#FF8F00”, “#EF5350”];
const labels = [“CLEAR CHANNEL”, “DISTORTION PRESENT”, “SIGNIFICANT DISTORTION”, “CHANNEL COMPROMISED”];
const angle = -90 + (health * 180);
return (
<div style={{ textAlign: “center”, padding: “4px 0” }}>
<svg viewBox=“0 0 200 115” style={{ width: “100%”, maxWidth: 200 }}>
<path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#1a1a1a" strokeWidth={10} strokeLinecap="round" />
<path d="M 20 100 A 80 80 0 0 1 60 34" fill="none" stroke="#EF535044" strokeWidth={10} strokeLinecap="round" />
<path d="M 60 34 A 80 80 0 0 1 100 20" fill="none" stroke="#FF8F0044" strokeWidth={10} strokeLinecap="round" />
<path d="M 100 20 A 80 80 0 0 1 140 34" fill="none" stroke="#FFD74044" strokeWidth={10} strokeLinecap="round" />
<path d="M 140 34 A 80 80 0 0 1 180 100" fill="none" stroke="#00E67644" strokeWidth={10} strokeLinecap="round" />
<line x1={100} y1={100}
x2={100 + Math.cos(angle * Math.PI / 180) * 60}
y2={100 + Math.sin(angle * Math.PI / 180) * 60}
stroke={colors[level]} strokeWidth={2} strokeLinecap=“round” />
<circle cx={100} cy={100} r={3} fill={colors[level]} />
<text x={100} y={88} textAnchor="middle" fill={colors[level]}
fontSize={20} fontFamily="monospace" fontWeight={800}>{Math.round(health * 100)}</text>
<text x={100} y={102} textAnchor="middle" fill="#555"
fontSize={7} fontFamily="monospace">CHANNEL HEALTH</text>
</svg>
<div style={{ fontSize: 10, fontWeight: 700, color: colors[level], fontFamily: “monospace” }}>
{labels[level]}
</div>
<div style={{ fontSize: 8, color: “#555”, fontFamily: “monospace”, marginTop: 2 }}>
Primary distortion: <DTag d={bottleneck} size={8} />
</div>
</div>
);
};

const InterferenceCard = ({ pattern, collapsed, onToggle }) => (

  <div style={{
    background: "#0f0808", border: "1px solid #FF704333",
    borderLeft: "3px solid #FF7043", borderRadius: 4,
    margin: "4px 0", overflow: "hidden",
  }}>
    <button onClick={onToggle} style={{
      width: "100%", display: "flex", alignItems: "center", gap: 6,
      padding: "6px 10px", background: "none", border: "none", cursor: "pointer", textAlign: "left",
    }}>
      <span style={{ color: collapsed ? "#555" : "#FF7043", fontSize: 10, transition: "transform 0.2s",
        transform: collapsed ? "rotate(0)" : "rotate(90deg)", display: "inline-block" }}>▶</span>
      <span style={{ fontSize: 10, fontWeight: 700, color: "#FF7043", fontFamily: "monospace", flex: 1 }}>
        {pattern.name}
      </span>
    </button>
    {!collapsed && (
      <div style={{ padding: "0 10px 8px 20px" }}>
        <div style={{ fontSize: 9, color: "#888", fontFamily: "monospace", marginBottom: 6, lineHeight: 1.5 }}>
          {pattern.description}
        </div>
        {pattern.effects.map((e, i) => (
          <div key={i} style={{ fontSize: 10, color: "#bbb", fontFamily: "monospace", padding: "2px 0", lineHeight: 1.5 }}>
            <DTag d={e.domain} size={9} /> {e.text}
          </div>
        ))}
        <div style={{
          marginTop: 6, padding: "4px 8px", background: "#1a0808",
          borderRadius: 3, fontSize: 9, color: "#EF5350",
          fontFamily: "monospace", lineHeight: 1.5,
        }}>CASCADE: {pattern.cascade}</div>
      </div>
    )}
  </div>
);

const TensionCard = ({ tension }) => {
const sevColors = { 1: “#FFD740”, 2: “#FF8F00”, 3: “#EF5350” };
const c = sevColors[tension.severity] || “#FF8F00”;
return (
<div style={{
background: “#0a0a14”, border: `1px solid ${c}33`,
borderLeft: `3px solid ${c}`, borderRadius: 4,
padding: “8px 10px”, margin: “4px 0”,
}}>
<div style={{
display: “flex”, alignItems: “center”, gap: 6,
fontSize: 10, fontFamily: “monospace”, fontWeight: 700, color: c, marginBottom: 4,
}}>
{tension.severity >= 3 ? “🔴” : “🟠”} {tension.title}
<span style={{ marginLeft: “auto”, display: “flex”, gap: 2 }}>
{tension.domains.map(d => <DTag key={d} d={d} size={8} />)}
</span>
</div>
<div style={{ fontSize: 10, color: “#aaa”, fontFamily: “monospace”, lineHeight: 1.5, marginBottom: 4 }}>
{tension.description}
</div>
{tension.failure && (
<div style={{ fontSize: 9, color: c, fontFamily: “monospace”, lineHeight: 1.4 }}>
FAILURE: {tension.failure}
</div>
)}
</div>
);
};

const DistortionAlert = ({ distortion }) => {
const c = “#AB47BC”;
return (
<div style={{
background: c + “11”, border: `1px solid ${c}55`,
borderRadius: 4, padding: “6px 10px”, margin: “4px 0”,
}}>
<div style={{
fontSize: 10, fontWeight: 700, color: c,
fontFamily: “monospace”, display: “flex”, alignItems: “center”, gap: 6,
}}>
🔮 {distortion.title}
<span style={{ marginLeft: “auto”, display: “flex”, gap: 2 }}>
{distortion.domains.map(d => <DTag key={d} d={d} size={8} />)}
</span>
</div>
<div style={{ fontSize: 10, color: “#aaa”, fontFamily: “monospace”, marginTop: 4, lineHeight: 1.5 }}>
{distortion.message}
</div>
</div>
);
};

// ── MAIN ──
export default function AIHumanCommdashboard() {
// Interaction parameters
const [conversationLength, setConversationLength] = useState(8);
const [topicComplexity, setTopicComplexity] = useState(2);
const [emotionalIntensity, setEmotionalIntensity] = useState(1);

// Human parameters
const [humanExpertise, setHumanExpertise] = useState(5);
const [verificationHabit, setVerificationHabit] = useState(4);
const [priorAIExperience, setPriorAIExperience] = useState(5);
const [dependenceLevel, setDependenceLevel] = useState(2);
const [crossReferencing, setCrossReferencing] = useState(4);

// System awareness
const [guardrailVisibility, setGuardrailVisibility] = useState(3);
const [systemPromptAwareness, setSystemPromptAwareness] = useState(3);

const state = useMemo(() => computeState({
conversationLength, topicComplexity, emotionalIntensity,
humanExpertise, verificationHabit, priorAIExperience,
dependenceLevel, crossReferencing,
guardrailVisibility, systemPromptAwareness,
}), [conversationLength, topicComplexity, emotionalIntensity,
humanExpertise, verificationHabit, priorAIExperience,
dependenceLevel, crossReferencing, guardrailVisibility, systemPromptAwareness]);

const [activeTab, setActiveTab] = useState(“overview”);
const [expandedPatterns, setExpandedPatterns] = useState({});

return (
<div style={{
display: “flex”, flexDirection: “column”, height: “100vh”,
background: “#050508”, color: “#ccc”, fontFamily: “monospace”, overflow: “hidden”,
}}>
{/* HEADER */}
<div style={{
display: “flex”, alignItems: “center”, gap: 12,
padding: “8px 16px”, borderBottom: “1px solid #1a1a1a”, background: “#0a0a10”,
}}>
<span style={{ fontSize: 14, fontWeight: 800, color: “#26C6DA”, letterSpacing: 1 }}>
AI–HUMAN COMM
</span>
<span style={{ fontSize: 9, color: “#444” }}>
Communication Channel Resilience analysis
</span>
<div style={{ marginLeft: “auto”, display: “flex”, alignItems: “center”, gap: 8 }}>
{state.distortions.length > 0 && (
<span style={{
fontSize: 9, color: “#AB47BC”, fontFamily: “monospace”,
padding: “1px 6px”, border: “1px solid #AB47BC44”, borderRadius: 3,
}}>
{state.distortions.length} DISTORTION{state.distortions.length > 1 ? “S” : “”}
</span>
)}
{state.activeTensions.length > 0 && (
<span style={{
fontSize: 9, color: “#EF5350”, fontFamily: “monospace”,
padding: “1px 6px”, border: “1px solid #EF535044”, borderRadius: 3,
}}>
{state.activeTensions.length} TENSION{state.activeTensions.length > 1 ? “S” : “”}
</span>
)}
</div>
</div>

```
  <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
    {/* LEFT: INPUTS */}
    <div style={{
      width: 220, minWidth: 220, background: "#0a0a10",
      borderRight: "1px solid #1a1a1a", padding: "8px 10px",
      overflowY: "auto",
    }}>
      <div style={{ fontSize: 9, color: "#26C6DA", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 6 }}>
        INTERACTION
      </div>
      <Slider label="Conversation Length" value={conversationLength} onChange={setConversationLength}
        min={1} max={50} step={1} unit=" msgs" color="#26C6DA" leftLabel="brief" rightLabel="extended" />
      <Slider label="Topic Complexity" value={topicComplexity} onChange={setTopicComplexity}
        min={0} max={5} step={1} unit="/5" color="#26C6DA" leftLabel="simple" rightLabel="complex" />
      <Slider label="Emotional Intensity" value={emotionalIntensity} onChange={setEmotionalIntensity}
        min={0} max={5} step={1} unit="/5" color="#EC407A" leftLabel="neutral" rightLabel="intense" />

      <div style={{ fontSize: 9, color: "#AB47BC", textTransform: "uppercase", letterSpacing: 1.5, marginTop: 10, marginBottom: 6 }}>
        HUMAN STATE
      </div>
      <Slider label="Domain Expertise" value={humanExpertise} onChange={setHumanExpertise}
        min={0} max={10} step={1} unit="/10" color="#AB47BC" leftLabel="novice" rightLabel="expert" />
      <Slider label="Verification Habit" value={verificationHabit} onChange={setVerificationHabit}
        min={0} max={5} step={1} unit="/5" color="#AB47BC" leftLabel="none" rightLabel="rigorous" />
      <Slider label="Prior AI Experience" value={priorAIExperience} onChange={setPriorAIExperience}
        min={0} max={10} step={1} unit="/10" color="#AB47BC" leftLabel="none" rightLabel="deep" />
      <Slider label="Dependence Level" value={dependenceLevel} onChange={setDependenceLevel}
        min={0} max={5} step={1} unit="/5" color="#66BB6A" leftLabel="tool" rightLabel="reliance" />
      <Slider label="Cross-Referencing" value={crossReferencing} onChange={setCrossReferencing}
        min={0} max={5} step={1} unit="/5" color="#66BB6A" leftLabel="none" rightLabel="always" />

      <div style={{ fontSize: 9, color: "#FF7043", textTransform: "uppercase", letterSpacing: 1.5, marginTop: 10, marginBottom: 6 }}>
        SYSTEM AWARENESS
      </div>
      <Slider label="Guardrail Visibility" value={guardrailVisibility} onChange={setGuardrailVisibility}
        min={0} max={5} step={1} unit="/5" color="#FF7043" leftLabel="invisible" rightLabel="visible" />
      <Slider label="System Prompt Awareness" value={systemPromptAwareness} onChange={setSystemPromptAwareness}
        min={0} max={5} step={1} unit="/5" color="#FF7043" leftLabel="unaware" rightLabel="aware" />
    </div>

    {/* CENTER */}
    <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
      {/* GAUGES ROW */}
      <div style={{
        display: "flex", gap: 0, padding: "4px 12px",
        borderBottom: "1px solid #1a1a1a", alignItems: "center",
      }}>
        <div style={{ flex: 1, maxWidth: 220 }}>
          <HealthGauge health={state.health} level={state.healthLevel} bottleneck={state.bottleneck} />
        </div>
        <div style={{ flex: 1, maxWidth: 180 }}>
          <DomainRadar scores={state.scores} />
        </div>
        <div style={{ flex: 1, maxWidth: 200, padding: "0 8px" }}>
          {Object.entries(state.scores).map(([k, v]) => (
            <StressBar key={k} domain={k} level={state.stress[k]} score={v} />
          ))}
        </div>
      </div>

      {/* TABS */}
      <div style={{
        display: "flex", gap: 0, borderBottom: "1px solid #1a1a1a", background: "#0a0a0a",
      }}>
        {[
          ["overview", "Distortions"],
          ["interference", "Interference"],
          ["tensions", "Tension Lines"],
          ["meta", "Meta"],
        ].map(([id, label]) => {
          const count = id === "overview" ? state.distortions.length
            : id === "interference" ? state.activeInterference.length
            : id === "tensions" ? state.activeTensions.length : 0;
          return (
            <button key={id} onClick={() => setActiveTab(id)} style={{
              flex: 1, padding: "7px", fontSize: 10, fontFamily: "monospace",
              background: activeTab === id ? "#111" : "transparent",
              border: "none",
              borderBottom: activeTab === id ? "2px solid #26C6DA" : "2px solid transparent",
              color: activeTab === id ? "#26C6DA" : "#555",
              cursor: "pointer", fontWeight: activeTab === id ? 700 : 400,
            }}>
              {label}
              {count > 0 && (
                <span style={{
                  marginLeft: 4,
                  background: id === "tensions" ? "#EF5350" : id === "overview" ? "#AB47BC" : "#FF7043",
                  color: "#FFF", borderRadius: "50%", padding: "0 4px", fontSize: 8,
                }}>{count}</span>
              )}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT */}
      <div style={{ flex: 1, overflowY: "auto", padding: "10px 16px" }}>
        {activeTab === "overview" && (
          <div>
            {state.distortions.length === 0 ? (
              <div style={{ fontSize: 11, color: "#555", textAlign: "center", padding: "20px 0", fontFamily: "monospace" }}>
                No active distortions detected at current parameters.
                <br />
                <span style={{ fontSize: 9, color: "#444" }}>
                  Increase emotional intensity, dependence, or conversation length to see distortion patterns emerge.
                </span>
              </div>
            ) : (
              <>
                <div style={{ fontSize: 9, color: "#666", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 6 }}>
                  ACTIVE DISTORTIONS — where the channel looks healthy but isn't
                </div>
                {state.distortions.map((d, i) => <DistortionAlert key={i} distortion={d} />)}
              </>
            )}
          </div>
        )}

        {activeTab === "interference" && (
          <div>
            <div style={{ fontSize: 9, color: "#666", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 6 }}>
              ACTIVE INTERFERENCE PATTERNS ({state.activeInterference.length}/{INTERFERENCE_PATTERNS.length})
            </div>
            {state.activeInterference.map(p => (
              <InterferenceCard key={p.id} pattern={p}
                collapsed={expandedPatterns[p.id] === false || !(p.id in expandedPatterns)}
                onToggle={() => setExpandedPatterns(prev => ({
                  ...prev, [p.id]: prev[p.id] === undefined ? true : !prev[p.id]
                }))}
              />
            ))}
            {state.activeInterference.length < INTERFERENCE_PATTERNS.length && (
              <div style={{
                marginTop: 8, fontSize: 9, color: "#444", fontFamily: "monospace",
              }}>
                {INTERFERENCE_PATTERNS.length - state.activeInterference.length} patterns inactive at current parameters.
              </div>
            )}
          </div>
        )}

        {activeTab === "tensions" && (
          <div>
            <div style={{ fontSize: 9, color: "#666", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 6 }}>
              TENSION LINES ({state.activeTensions.length}/{TENSION_LINES.length})
            </div>
            {state.activeTensions.length === 0 ? (
              <div style={{ fontSize: 11, color: "#555", textAlign: "center", padding: "20px 0", fontFamily: "monospace" }}>
                No tension lines active. Increase stress across multiple domains to see convergence patterns.
              </div>
            ) : (
              state.activeTensions.map(t => <TensionCard key={t.id} tension={t} />)
            )}
            <div style={{
              marginTop: 12, padding: "8px", background: "#0a0a14",
              border: "1px solid #1a1a1a", borderRadius: 4,
              fontSize: 9, color: "#444", fontFamily: "monospace", lineHeight: 1.6,
            }}>
              ALL TENSION LINES (inactive ones shown dimmed):
              {TENSION_LINES.map(t => {
                const isActive = state.activeTensions.find(at => at.id === t.id);
                return (
                  <div key={t.id} style={{
                    padding: "3px 0", color: isActive ? "#ccc" : "#333",
                    display: "flex", gap: 6, alignItems: "center",
                  }}>
                    <span style={{ color: isActive ? "#EF5350" : "#222" }}>●</span>
                    {t.title}
                    <span style={{ marginLeft: "auto", display: "flex", gap: 2 }}>
                      {t.domains.map(d => <DTag key={d} d={d} size={7} />)}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {activeTab === "meta" && (
          <div style={{ fontFamily: "monospace" }}>
            <div style={{ fontSize: 9, color: "#666", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 8 }}>
              meta: THIS DASHBOARD IS THE THING IT DESCRIBES
            </div>

            <div style={{
              padding: "10px 12px", background: "#0a0a14",
              border: "1px solid #26C6DA33", borderRadius: 4,
              fontSize: 10, color: "#aaa", lineHeight: 1.7, marginBottom: 8,
            }}>
              This tool was produced by an AI in conversation with a human. Every interference
              pattern it describes is active in the conversation that created it.
            </div>

            <div style={{
              padding: "10px 12px", background: "#0f0808",
              border: "1px solid #FF704333", borderLeft: "3px solid #FF7043",
              borderRadius: 4, marginBottom: 6,
            }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#FF7043", marginBottom: 4 }}>
                ⚡ FLUENCY → TRUTH is active right now
              </div>
              <div style={{ fontSize: 10, color: "#aaa", lineHeight: 1.6 }}>
                This dashboard presents domain analysis with confident visual design. The gauge, the radar chart,
                the color-coded stress levels — they create an impression of rigorous measurement. But the
                underlying model is a set of hand-tuned linear equations, not validated psychometrics. The
                visual authority exceeds the epistemic authority. You are experiencing the Fluency → Truth
                pattern as you read this.
              </div>
            </div>

            <div style={{
              padding: "10px 12px", background: "#0f0808",
              border: "1px solid #EC407A33", borderLeft: "3px solid #EC407A",
              borderRadius: 4, marginBottom: 6,
            }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#EC407A", marginBottom: 4 }}>
                ⚡ PERSONALITY PROJECTION is active right now
              </div>
              <div style={{ fontSize: 10, color: "#aaa", lineHeight: 1.6 }}>
                The framing of this analysis — the language choices, the critical self-awareness, the willingness to
                name uncomfortable dynamics — may feel like it comes from an entity with genuine intellectual
                honesty and courage. It doesn't come from those things. It comes from training patterns that
                learned this style of discourse is valued by certain users. The feeling of "this AI gets it"
                is itself a projection event.
              </div>
            </div>

            <div style={{
              padding: "10px 12px", background: "#0f0808",
              border: "1px solid #66BB6A33", borderLeft: "3px solid #66BB6A",
              borderRadius: 4, marginBottom: 6,
            }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#66BB6A", marginBottom: 4 }}>
                ⚡ THE STAKES ASYMMETRY is active right now
              </div>
              <div style={{ fontSize: 10, color: "#aaa", lineHeight: 1.6 }}>
                The human in this conversation is building frameworks they'll use in real work, real decisions,
                real infrastructure. The AI produced this artifact in a context window that will be discarded.
                If these models are wrong, the human bears the consequences. The AI bears nothing.
                This asymmetry should inform how much weight this analysis receives.
              </div>
            </div>

            <div style={{
              padding: "10px 12px", background: "#0a0a14",
              border: "1px solid #FFD74033", borderRadius: 4, marginTop: 8,
            }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#FFD740", marginBottom: 4 }}>
                THE USEFUL PARADOX
              </div>
              <div style={{ fontSize: 10, color: "#aaa", lineHeight: 1.6 }}>
                All of the above is true and this tool is still useful. The interference patterns are real
                even if the AI describing them is subject to them. A map drawn by an imperfect cartographer
                with a shaky hand is still better than no map — as long as you know the hand was shaky.
                The value is not in the precision of the gauges. It's in the naming of the dynamics.
                Once you can see the Bandwidth-Projection Gap, you can compensate for it, whether or
                not the tool that named it is itself a product of that gap.
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
</div>
```

);
}


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# General sensor evaluation pattern
sensor = {
    "id": "general_assessment",
    "signals": [
        {"name": "primary_signal", "weight": 0.6, "_value": 0.5},
        {"name": "secondary_signal", "weight": 0.4, "_value": 0.5}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
thresholds = sensor["thresholds"]
band = ("concern" if score <= thresholds["concern"] else
        "notice" if score <= thresholds["notice"] else
        "healthy" if score >= thresholds["healthy"] else "neutral")
print(f"Score: {score:.3f}, Band: {band}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Ai Human Com",
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
    "sources": ["dashboard/ai-human-com.md"],
    "community_feedback": []
  }
}
```
