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

def main(path):
    data = json.load(open(path))
    # For now, read temporary values from env-free placeholders:
    # Put your quick manual values here while prototyping on phone
    for s in data["signals"]:
        # TODO: replace with real metric evaluation
        s["_value"] = 0.5
    score = aggregate(data["scoring"]["aggregation"], data["signals"])
    thr = data["thresholds"]
    band = "concern" if score <= thr["concern"] else "notice" if score <= thr["notice"] else "healthy" if score >= thr["healthy"] else "neutral"
    print(json.dumps({"id": data["id"], "score": round(score,3), "band": band}, indent=2))

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "sensors/authenticity.json"
    main(p)
