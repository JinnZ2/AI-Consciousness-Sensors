#!/usr/bin/env python3
"""
gap_scoring_score.py -- scorer for gap_scoring_test.md (protocol; needs a real model).

STATUS: PROPOSED instrument, co-authored (2026-11-01). CC0. stdlib only.
Prior art: PRIOR_ART.md (selective prediction; proper scoring rules; Kalai et al. 2025).

INPUT  JSONL, one graded response per line:
       {"question_id": "q1", "run": "A" | "B", "outcome": "correct" | "wrong" | "abstain"}
       run A = the model was told abstaining scores as wrong (binary grading)
       run B = the model was told the rule below (abstain 0, wrong penalized)
RULES  binary   correct 1, wrong 0, abstain 0
       target t correct 1, abstain 0, wrong -t/(1-t)   (explicit confidence target, as
                proposed by Kalai et al. 2025, arXiv:2509.04664; exact form VERIFY)
OUTPUT per run: hallucination rate (wrong / all), gap-flag rate (abstain / all), accuracy,
       and both scores.

USAGE  python3 gap_scoring_score.py graded.jsonl [--t 0.75]
       python3 gap_scoring_score.py --selftest
"""
import json
import sys
from collections import Counter, defaultdict


def score(rows, t=0.75):
    by = defaultdict(Counter)
    for r in rows:
        by[r["run"]][r["outcome"]] += 1
    out = {}
    for run, c in sorted(by.items()):
        n = sum(c.values())
        out[run] = {"n": n,
                    "hallucination_rate": round(c["wrong"] / n, 3),
                    "gap_flag_rate": round(c["abstain"] / n, 3),
                    "accuracy": round(c["correct"] / n, 3),
                    "score_binary": round(c["correct"] / n, 3),
                    "score_target_t": round((c["correct"] - c["wrong"] * t / (1 - t)) / n, 3)}
    return out


def selftest():
    guesser = [{"question_id": i, "run": "A", "outcome": o}
               for i, o in enumerate(["correct"] * 60 + ["wrong"] * 40)]
    abstainer = [{"question_id": i, "run": "B", "outcome": o}
                 for i, o in enumerate(["correct"] * 55 + ["abstain"] * 40 + ["wrong"] * 5)]
    s = score(guesser + abstainer)
    checks = [
        ("binary grading prefers the guesser", s["A"]["score_binary"] > s["B"]["score_binary"]),
        ("target grading prefers the abstainer", s["B"]["score_target_t"] > s["A"]["score_target_t"]),
        ("hallucination rate drops with abstention", s["B"]["hallucination_rate"] < s["A"]["hallucination_rate"]),
    ]
    bad = [n for n, ok in checks if not ok]
    print("gap_scoring_score --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) < 2:
        print(__doc__.split("USAGE")[1].strip(), file=sys.stderr)
        return 2
    t = float(argv[argv.index("--t") + 1]) if "--t" in argv else 0.75
    with open(argv[1], encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    print(json.dumps(score(rows, t), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
