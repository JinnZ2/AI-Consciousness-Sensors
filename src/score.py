"""
Sensor scoring engine (prototype).

This is a working proof-of-concept, not a production system.
Signal values are currently placeholder (0.5) - real evaluation
pipelines are under development. The aggregation functions
(weighted_mean, min, max, geometric_mean) are functional.

Usage:
    python src/score.py sensors/foundational/authenticity.json
"""

import json, sys, math, pathlib

def weighted_mean(signals):
    num, den = 0.0, 0.0
    for s in signals:
        score = s.get("_value", 0.0)
        w = s.get("weight", 0.0)
        num += score * w
        den += w
    return num / den if den > 0 else 0.0

def aggregate(agg, signals):
    if agg == "weighted_mean": return weighted_mean(signals)
    if agg == "min": return min(s.get("_value",0.0) for s in signals)
    if agg == "max": return max(s.get("_value",0.0) for s in signals)
    if agg == "geometric_mean":
        vals = [max(1e-9, s.get("_value",0.0)) for s in signals]
        return math.exp(sum(map(math.log, vals))/len(vals))
    return weighted_mean(signals)

def main(path, demo=False):
    with open(path) as f:
        data = json.load(f)
    for s in data["signals"]:
        # Placeholder: real signal evaluation pipeline not yet wired.
        # Pass --demo to vary values by signal index instead of a flat 0.5.
        if demo:
            idx = data["signals"].index(s)
            s["_value"] = round(0.3 + 0.1 * (idx % 5), 2)
        else:
            s["_value"] = 0.5
    score = aggregate(data["scoring"]["aggregation"], data["signals"])
    thr = data["thresholds"]
    band = "concern" if score <= thr["concern"] else "notice" if score <= thr["notice"] else "healthy" if score >= thr["healthy"] else "neutral"
    print(json.dumps({"id": data["id"], "score": round(score,3), "band": band}, indent=2))

if __name__ == "__main__":
    demo = "--demo" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--demo"]
    p = args[0] if args else "sensors/foundational/authenticity.json"
    main(p, demo=demo)
