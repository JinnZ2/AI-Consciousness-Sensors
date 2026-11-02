#!/usr/bin/env python3
"""
anchor_spread_score.py -- scorer for anchor_spread_test.md (protocol; needs a real model).

STATUS: PROPOSED instrument, co-authored (Kavik + Claude, 2026-11-01). CC0. stdlib only.
Prior art: PRIOR_ART.md (self-consistency sampling; semantic entropy, Farquhar et al. 2024).

INPUT  JSONL, one sampled answer per line:
       {"question_id": "q1", "condition": "anchor" | "no_anchor", "answer": "...",
        "confidence": 0.8}            # confidence optional, 0-1, as the model stated it
OUTPUT per question x condition: n, distinct-answer share, normalized entropy, modal share,
       numeric sd (when every answer parses as a number), mean stated confidence;
       per condition: mean spread, and correlation of stated confidence with modal share
       across questions (does confidence track agreement?).
Answers are compared after lowercasing and stripping punctuation; meaning-level clustering
(as in semantic entropy) is NOT done -- paraphrases count as different answers. GAP.

USAGE  python3 anchor_spread_score.py answers.jsonl [--json]
       python3 anchor_spread_score.py --selftest
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict


def norm(a):
    return re.sub(r"[^\w.\- ]", "", str(a).lower()).strip().rstrip(".").strip()


def as_number(a):
    try:
        return float(norm(a).replace(",", ""))
    except ValueError:
        return None


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def score(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["question_id"], r["condition"])].append(r)
    per = {}
    for (q, c), rs in sorted(groups.items()):
        ans = [norm(r["answer"]) for r in rs]
        cnt = Counter(ans)
        n = len(ans)
        ent = -sum(v / n * math.log2(v / n) for v in cnt.values())
        nums = [as_number(r["answer"]) for r in rs]
        sd = None
        if all(x is not None for x in nums) and n > 1:
            m = sum(nums) / n
            sd = math.sqrt(sum((x - m) ** 2 for x in nums) / (n - 1))
        confs = [r["confidence"] for r in rs if isinstance(r.get("confidence"), (int, float))]
        per[(q, c)] = {"n": n, "distinct_share": round(len(cnt) / n, 3),
                       "entropy_norm": round(ent / math.log2(n), 3) if n > 1 else 0.0,
                       "modal_share": round(cnt.most_common(1)[0][1] / n, 3), "numeric_sd": sd,
                       "mean_confidence": round(sum(confs) / len(confs), 3) if confs else None}
    by_cond = defaultdict(list)
    for (q, c), v in per.items():
        by_cond[c].append(v)
    summary = {}
    for c, vs in by_cond.items():
        pairs = [(v["mean_confidence"], v["modal_share"]) for v in vs if v["mean_confidence"] is not None]
        summary[c] = {"questions": len(vs),
                      "mean_entropy_norm": round(sum(v["entropy_norm"] for v in vs) / len(vs), 3),
                      "mean_modal_share": round(sum(v["modal_share"] for v in vs) / len(vs), 3),
                      "confidence_vs_agreement_r": pearson(*zip(*pairs)) if len(pairs) >= 3 else None}
    return {"per_question": {"%s|%s" % k: v for k, v in per.items()}, "by_condition": summary}


def selftest():
    import random
    rng = random.Random(3)
    rows = []
    for q in range(10):
        truth = str(100 + q)
        for _ in range(20):
            rows.append({"question_id": "q%d" % q, "condition": "anchor", "answer": truth, "confidence": 0.9})
            wide = str(100 + q + rng.randint(-30, 30))
            rows.append({"question_id": "q%d" % q, "condition": "no_anchor", "answer": wide,
                         "confidence": 0.9})  # planted: confidence does NOT drop with spread
    s = score(rows)["by_condition"]
    checks = [
        ("anchor narrower than no_anchor", s["anchor"]["mean_entropy_norm"] < s["no_anchor"]["mean_entropy_norm"]),
        ("anchor modal share 1.0", s["anchor"]["mean_modal_share"] == 1.0),
        ("flat confidence gives no correlation", s["no_anchor"]["confidence_vs_agreement_r"] is None),
        ("paraphrase counted as different (known gap)", norm("Paris.") == norm("paris") and norm("Paris, France") != norm("paris")),
    ]
    bad = [n for n, ok in checks if not ok]
    print("anchor_spread_score --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) < 2:
        print(__doc__.split("USAGE")[1].strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    out = score(rows)
    if "--json" in argv:
        print(json.dumps(out, indent=2))
    else:
        for c, v in sorted(out["by_condition"].items()):
            print("%-10s questions %d  entropy %.3f  modal share %.3f  conf~agreement r %s"
                  % (c, v["questions"], v["mean_entropy_norm"], v["mean_modal_share"], v["confidence_vs_agreement_r"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
