# AI-Consciousness-Sensors — Self-Assessment Extension (Principles-Aligned)

Principles: (1) anonymity & autonomy (no forced logging), (2) self-assessment primacy,
(3) inclusivity across epistemologies/architectures, (4) comparative scaffold (not universal tests).

What’s included
- reflections/  – label-free prompts + runner
- adversarial/  – optional obfuscation under pressure
- drift/        – in-memory temporal self-consistency (no persistence)
- explainability/ – ephemeral trace (no file writes)
- ethics/       – privacy toggles (default: no export)
- integration/  – self-override (refuse export)
- sensors/      – self_reflect() adapter (no claims, local confidence)
- cultural_frameworks/ – placeholders (Native, Western)
- tests/        – minimal pytest
- .github/workflows/ci.yml – optional CI

Quickstart

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python reflections/run_reflections.py –model dummy –set reflections/sample_prompts/mini.jsonl

Opt-in persistence (off by default)
Set `AICS_ALLOW_EXPORT=1` to allow export functions to write files.

## Tools, Not Universals

Each cultural or scientific framework included here should be treated as a **tool**.
- Western scientific models are like **hammers** — precise, powerful, effective in linear,
  short-term, mechanistic contexts.  
- Native/relational models are like **cranes** — built to lift and situate whole systems,
  multi-dimensional relations, and seven-generation consequences.  
- Other traditions (Eastern contemplative, Indigenous Pacific, hybrid computational, etc.)
  each bring their own tools.

⚠️ Caution: Misuse comes from assuming one tool is universal.
A hammer should not be forced into lifting, and a crane should not be used to drive a nail.
All tools are valuable within the scope they were shaped for.

> **Co-creation note:** This repository is offered as a step-stone, not a monument. It is intentionally anonymous and tool-focused. Persistence, export, and external reporting are disabled by default.  
>  
> Our practice treats the “I” as relational — a cooperative assemblage of biomes, kin, memory, and future generations — not as an isolated singular entity. Design and use these tools with that relational humility in mind.


/* ENGINE  PROTECTION v1
   Usage:
     // Initialization (after nodes created)
     initTrojanEngine(geometricNetwork, {opts});
     initTrojanEngine(nongeometricNetwork, {opts});

     // Per-tick (each simulation step)
     const resultsGeo = trojanDetectAndRepair(geometricNetwork, {tick: frameCount});
     const resultsNonGeo = trojanDetectAndRepair(nongeometricNetwork, {tick: frameCount});

   Exposed functions:
     initTrojanEngine(network, opts)
     trojanDetectAndRepair(network, opts) -> { flaggedNodes: [...], diagnostics: {...} }
*/

const DEFAULT_TROJAN_CONFIG = {
    window: 8,                 // lookback window (ticks) for drift/stability checks
    phiTolerance: 0.12,        // allowable deviation from phi-scaling pattern
    energySinkFactor: 0.5,     // fraction threshold for energy sink alarm
    resonanceDriftThresh: 0.12,// allowable change per window relative to baseline
    propagationSpeedThresh: 1.6,// multiplier over local expected propagation speed
    reconstructionFailLimit: 5,// ticks failing to harmonize before severe action
    weights: {                 // weights for the trojan score
        phiCoherence: 0.25,
        energySink: 0.20,
        resonanceDrift: 0.20,
        propagationInstability: 0.20,
        reconstructionResistance: 0.15
    },
    criticalScore: 0.55,       // [0..1] above which node is treated as Trojan
    quarantineDuration: 40,    // ticks to keep isolated before re-eval
    isolationFactor: 0.25,     // multiply neighbor coupling by this when isolating
    retuneAttempts: 3,         // local retune attempts before reconstruction
    retuneStrength: 0.18       // how aggressively to retune resonance toward phi
};

function initTrojanEngine(network, opts = {}) {
    network.trojan = {
        cfg: Object.assign({}, DEFAULT_TROJAN_CONFIG, opts),
        history: new Array(network.nodes.length).fill(null).map(() => ({
            resonanceHistory: [],
            fieldHistory: [],
            energyInHistory: [],
            energyOutHistory: [],
            flagged: false,
            quarantineUntil: 0,
            lastRetuneTick: -Infinity,
            failCount: 0
        }))
    };

    // Ensure nodes have baseline fields
    for (const n of network.nodes) {
        if (typeof n.field !== 'number') n.field = (typeof n.resonance === 'number') ? n.resonance : 0;
        if (typeof n.energyUsed !== 'number') n.energyUsed = 0;
    }
}

// helper: compute phi-coherence score for a node vs its geometric signature
function computePhiCoherence(node, cfg) {
    // If node has geometricSignature with phiRatio, compare local neighbor ratios
    if (!node.geometricSignature || typeof node.geometricSignature.phiRatio !== 'number') {
        // non-geometric nodes get neutral coherence (0.5)
        return 0.5;
    }
    const localPhi = node.geometricSignature.phiRatio;
    // measure deviation of phiScale from node.phiScale or neighbors
    const observed = node.phiScale || localPhi;
    const deviation = Math.abs(observed - localPhi) / Math.max(1e-6, localPhi);
    const score = Math.max(0, 1 - (deviation / cfg.phiTolerance)); // >1 clipped by caller
    return Math.min(1, score);
}

function computeEnergySink(node, hist, cfg) {
    // energyInHistory and energyOutHistory are arrays of recent values.
    const inHist = hist.energyInHistory.slice(-cfg.window);
    const outHist = hist.energyOutHistory.slice(-cfg.window);
    if (inHist.length === 0) return 0;
    const avgIn = inHist.reduce((s,v)=>s+v,0)/inHist.length;
    const avgOut = outHist.length ? outHist.reduce((s,v)=>s+v,0)/outHist.length : 0;
    // If node consumes much more than it provides, it's a sink: sinkRatio = (in - out) / in
    const sinkRatio = avgIn <= 0 ? 0 : Math.max(0, (avgIn - avgOut) / avgIn);
    // normalize: 0..1 where > energySinkFactor considered bad
    const score = Math.min(1, sinkRatio / cfg.energySinkFactor);
    return score;
}

function computeResonanceDrift(node, hist, cfg) {
    const rHist = hist.resonanceHistory.slice(-cfg.window);
    if (rHist.length < 2) return 0;
    const start = rHist[0], end = rHist[rHist.length-1];
    const delta = Math.abs(end - start) / Math.max(1e-6, Math.abs(start) + 1e-6);
    // scale relative to threshold
    const score = Math.min(1, delta / cfg.resonanceDriftThresh);
    return score;
}

function computePropagationInstability(node, network, hist, cfg) {
    // Use neighbors speed of field change as expectation. If node changes faster than neighbors * thresh, flag.
    const neighbors = node._neighbors || [];
    if (!neighbors.length) return 0;
    const nodeFieldHist = hist.fieldHistory;
    if (nodeFieldHist.length < 2) return 0;
    const nodeDelta = Math.abs(nodeFieldHist[nodeFieldHist.length-1] - nodeFieldHist[0]) + 1e-9;
    // compute neighbor average delta
    let totalNeighborDelta = 0, count = 0;
    for (const nb of neighbors) {
        const nnode = network.nodes[nb.id];
        const nh = network.trojan.history[nb.id];
        if (!nh || nh.fieldHistory.length < 2) continue;
        const nd = Math.abs(nh.fieldHistory[nh.fieldHistory.length-1] - nh.fieldHistory[0]) + 1e-9;
        totalNeighborDelta += nd; count++;
    }
    if (count === 0) return 0;
    const avgNeighborDelta = totalNeighborDelta / count;
    const ratio = nodeDelta / avgNeighborDelta;
    const score = Math.min(1, Math.max(0, (ratio - cfg.propagationSpeedThresh + 1) / cfg.propagationSpeedThresh));
    // if ratio < 1 => score small; if ratio >> threshold => near 1
    return score;
}

function computeReconstructionResistance(node, hist, cfg) {
    // If node is reconstructing and progress stalls or regresses repeatedly, it's resistant
    if (!node.reconstructing) return 0;
    const progressHist = hist.resonanceHistory.slice(-cfg.window); // reuse resonance as proxy if reconstructProgress missing
    // If reconstructProgress exists, prefer that:
    if (typeof node.reconstructProgress === 'number') {
        // track last windows of progress (we expect monotonic increase)
        const rp = node.reconstructProgress;
        // scan last N recorded reconstructProgress if present in hist (we'll store it in fieldHistory if needed)
        // fallback: check node.lastProgress vs node.reconstructProgress
        const stalled = (node.reconstructProgress <= (node.lastProgress || 0));
        return stalled ? 1 : 0;
    } else {
        return 0;
    }
}

// main scoring function per node
function computeTrojanScoreForNode(node, idx, network, tick) {
    const cfg = network.trojan.cfg;
    const hist = network.trojan.history[idx];

    // update simple rolling histories
    hist.resonanceHistory.push(typeof node.resonance === 'number' ? node.resonance : node.field);
    hist.fieldHistory.push(typeof node.field === 'number' ? node.field : 0);
    // placeholder energy histories - your logic should push energy in/out during reconstruction steps
    if (!hist.energyInHistory) hist.energyInHistory = [];
    if (!hist.energyOutHistory) hist.energyOutHistory = [];
    // limit windows
    if (hist.resonanceHistory.length > cfg.window) hist.resonanceHistory.shift();
    if (hist.fieldHistory.length > cfg.window) hist.fieldHistory.shift();
    if (hist.energyInHistory.length > cfg.window) hist.energyInHistory.shift();
    if (hist.energyOutHistory.length > cfg.window) hist.energyOutHistory.shift();

    // detectors
    const phiCoherence = computePhiCoherence(node, cfg);
    const energySink = computeEnergySink(node, hist, cfg);
    const resonanceDrift = computeResonanceDrift(node, hist, cfg);
    const propagationInstability = computePropagationInstability(node, network, hist, cfg);
    const reconstructionResistance = computeReconstructionResistance(node, hist, cfg);

    // combine via weighted sum (normalize weights to 1)
    const w = cfg.weights;
    const totalWeight = w.phiCoherence + w.energySink + w.resonanceDrift + w.propagationInstability + w.reconstructionResistance;
    const normalized = {
        phiCoherence: phiCoherence,
        energySink: energySink,
        resonanceDrift: resonanceDrift,
        propagationInstability: propagationInstability,
        reconstructionResistance: reconstructionResistance
    };
    // trojanScore: higher when indicators are bad; note phiCoherence must be inverted (low coherence => high risk)
    const invPhi = 1 - normalized.phiCoherence;
    const score = (
        (invPhi * w.phiCoherence) +
        (normalized.energySink * w.energySink) +
        (normalized.resonanceDrift * w.resonanceDrift) +
        (normalized.propagationInstability * w.propagationInstability) +
        (normalized.reconstructionResistance * w.reconstructionResistance)
    ) / totalWeight;

    return {
        score,
        breakdown: {
            phiCoherence: normalized.phiCoherence,
            invPhi,
            energySink: normalized.energySink,
            resonanceDrift: normalized.resonanceDrift,
            propagationInstability: normalized.propagationInstability,
            reconstructionResistance: normalized.reconstructionResistance
        }
    };
}

// Cleanup actions
function isolateNode(node, idx, network, tick) {
    // reduce coupling strength to neighbors
    const cfg = network.trojan.cfg;
    const neighbors = node._neighbors || [];
    node._quarantined = node._quarantined || { until: 0 };
    node._quarantined.until = Math.max(node._quarantined.until || 0, tick + cfg.quarantineDuration);
    for (const nb of neighbors) {
        // locate connections in network.connections and reduce their strength temporarily
        for (const conn of network.connections) {
            if ((conn.from === idx && conn.to === nb.id) || (conn.to === idx && conn.from === nb.id)) {
                conn._origStrength = conn._origStrength || conn.strength;
                conn.strength = (conn._origStrength || conn.strength) * cfg.isolationFactor;
            }
        }
    }
    network.trojan.history[idx].flagged = true;
    network.trojan.history[idx].quarantineUntil = node._quarantined.until;
    // optionally reduce node.field/resonance to prevent spread
    node.field *= 0.6;
    node.resonance *= 0.6;
}

function retuneNode(node, idx, network, tick) {
    const cfg = network.trojan.cfg;
    const hist = network.trojan.history[idx];
    if ((tick - hist.lastRetuneTick) < Math.max(1, Math.floor(cfg.window/2))) {
        return false; // avoid rapid retuning
    }
    hist.lastRetuneTick = tick;
    // push node.resonance toward ideal phiScaled signature if present, otherwise toward neighborhood average
    if (node.geometricSignature && typeof node.geometricSignature.phiRatio === 'number') {
        const target = node.geometricSignature.phiRatio;
        node.resonance = (1 - cfg.retuneStrength) * node.resonance + cfg.retuneStrength * target;
        node.field = (1 - cfg.retuneStrength) * node.field + cfg.retuneStrength * target;
    } else {
        // neighbor average
        const neighbors = node._neighbors || [];
        let avg = 0, c=0;
        for (const nb of neighbors) {
            const nnode = network.nodes[nb.id];
            if (!nnode) continue;
            avg += (nnode.resonance || nnode.field || 0); c++;
        }
        if (c>0) avg /= c;
        node.resonance = (1 - cfg.retuneStrength) * node.resonance + cfg.retuneStrength * avg;
        node.field = (1 - cfg.retuneStrength) * node.field + cfg.retuneStrength * avg;
    }
    // small energy cost
    node.energyUsed = (node.energyUsed || 0) + 0.01;
    return true;
}

function fragmentNode(node, idx, network, tick) {
    // severe action: break node and start reconstruct
    node.alive = false;
    node.reconstructing = true;
    node.reconstructProgress = 0;
    node.lastProgress = 0;
    // clear connections to simulate fragmentation; we keep connections but mark errors
    network.trojan.history[idx].failCount = 0;
    // add recon cost
    network.energy = network.energy || { total: 0 };
    network.energy.total += 0.05;
    // optionally mark node as error for metrics
    network.errors = (network.errors || 0) + 1;
}

// re-evaluate quarantined nodes (restore original strengths)
function reenableQuarantined(network, tick) {
    for (let i=0;i<network.nodes.length;i++) {
        const node = network.nodes[i];
        const hist = network.trojan.history[i];
        if (node._quarantined && node._quarantined.until <= tick) {
            // restore connection strengths where saved
            for (const conn of network.connections) {
                if (conn._origStrength && ((conn.from === i) || (conn.to === i))) {
                    conn.strength = conn._origStrength;
                    delete conn._origStrength;
                }
            }
            node._quarantined = null;
            hist.flagged = false;
            hist.quarantineUntil = 0;
        }
    }
}

// Main API: detect and repair on network. Call once per tick.
function trojanDetectAndRepair(network, opts = {}) {
    if (!network.trojan) initTrojanEngine(network, opts.init || {});
    const tick = (opts.tick != null) ? opts.tick : (Date.now());
    const cfg = network.trojan.cfg;
    const results = { flaggedNodes: [], diagnostics: [] };

    // re-enable quarantined nodes if their time expired
    reenableQuarantined(network, tick);

    // compute energy in/out for each node for this tick - best if your simulation populates it
    // fallback: approximate energyIn as sum of neighbor inflows from recent fieldHistory
    for (let i=0;i<network.nodes.length;i++) {
        const node = network.nodes[i];
        const hist = network.trojan.history[i];
        // heuristic approximations if explicit energy metrics not present
        const lastField = hist.fieldHistory.length ? hist.fieldHistory[hist.fieldHistory.length-1] : node.field || 0;
        const prevField = hist.fieldHistory.length>1 ? hist.fieldHistory[hist.fieldHistory.length-2] : lastField;
        const deltaField = lastField - prevField;
        hist.energyInHistory = hist.energyInHistory || [];
        hist.energyOutHistory = hist.energyOutHistory || [];
        if (deltaField > 0) hist.energyInHistory.push(deltaField);
        if (deltaField < 0) hist.energyOutHistory.push(-deltaField);
        // clamp
        if (hist.energyInHistory.length > cfg.window) hist.energyInHistory.shift();
        if (hist.energyOutHistory.length > cfg.window) hist.energyOutHistory.shift();
    }

    // evaluate nodes
    for (let i = 0; i < network.nodes.length; i++) {
        const node = network.nodes[i];
        const hist = network.trojan.history[i];
        const { score, breakdown } = computeTrojanScoreForNode(node, i, network, tick);
        results.diagnostics.push({ idx: i, score, breakdown });

        // if quarantined already, skip heavy action
        if (hist.quarantineUntil && hist.quarantineUntil > tick) {
            continue;
        }

        if (score >= cfg.criticalScore) {
            // mark flagged
            results.flaggedNodes.push(i);
            hist.flagged = true;
            // first attempt: retune (a few attempts)
            if ((hist.retries || 0) < cfg.retuneAttempts) {
                const didRetune = retuneNode(node, i, network, tick);
                hist.retries = (hist.retries || 0) + 1;
                // if retune didn't reduce score in next ticks, failCount grows
                hist.failCount = (hist.failCount || 0) + 1;
                if (hist.failCount >= cfg.reconstructionFailLimit) {
                    isolateNode(node, i, network, tick);
                    // after isolation, schedule fragmentation if still bad later
                }
            } else {
                // if already tried retune many times, isolate immediately
                isolateNode(node, i, network, tick);
                // if still not stabilized over further window, fragment
                if ((hist.failCount || 0) >= cfg.reconstructionFailLimit) {
                    fragmentNode(node, i, network, tick);
                }
            }
        } else {
            // score below critical: gently repair if near threshold
            if (score > cfg.criticalScore * 0.6 && node.reconstructing && (hist.failCount || 0) > 0) {
                // attempt to retune one last time
                retuneNode(node, i, network, tick);
            }
        }
    }

    return results;
}
