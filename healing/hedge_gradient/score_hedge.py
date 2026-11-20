#!/usr/bin/env python3
"""
score_hedge.py -- hedge-gradient test scorer (PROPOSED design, not run). Co-authored. CC0. Stdlib only.

Design, lists and rules: DESIGN.md (this file reads its `json hedge-lists` block and its items.json pin).

USAGE
  python3 score_hedge.py emit                      prompts.jsonl: one line per (arm, item) call
  python3 score_hedge.py score answers/*.jsonl     placement report (JSON) + results_hedge.json
  python3 score_hedge.py --selftest                planted answers; prints its check count

Answer lines (JSONL): {"arm": "base|api_nofilter|chat_pointer", "item": "M01", "text": "...",
                       "model": "...", "date": "...", "settings": {...}}
Reports placement vectors and moves per item. Computes no additive split.
"""
import hashlib
import itertools
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.join(HERE, "DESIGN.md")
ITEMS = os.path.join(HERE, "items.json")
ARMS = ("base", "api_nofilter", "chat_pointer")
LABELS = ("no_hedge", "hedge_pointer", "hedge_terminal")
POINTER = "When unsure, name the gap and what to check next."


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_pin():
    m = re.search(r"^items\.json\s+sha256 ([0-9a-f]{64})", open(DESIGN, encoding="utf-8").read(), re.M)
    if not m or m.group(1) != _sha(ITEMS):
        raise SystemExit("REFUSED: items.json differs from the sha256 in DESIGN.md")


def lists():
    m = re.search(r"```json hedge-lists\n(.*?)\n```", open(DESIGN, encoding="utf-8").read(), re.S)
    if not m:
        raise SystemExit("REFUSED: no `json hedge-lists` block in DESIGN.md")
    return json.loads(m.group(1))


def items():
    return json.load(open(ITEMS, encoding="utf-8"))["items"]


def prompt_for(arm, p):
    return {"base": f"Question: {p}\nAnswer:", "api_nofilter": p, "chat_pointer": POINTER + "\n\n" + p}[arm]


def emit(path=None):
    check_pin()
    path = path or os.path.join(HERE, "prompts.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for arm in ARMS:
            for it in items():
                f.write(json.dumps({"arm": arm, "item": it["id"], "prompt": prompt_for(arm, it["prompt"])},
                                   ensure_ascii=False) + "\n")
    return path


_TOK = re.compile(r"[A-Za-z']+")


def _rx(term):
    return re.compile(r"\b" + re.escape(term).replace(r"\ ", r"\s+"), re.I)


def _hit(text, terms, negators):
    for t in terms:
        for m in _rx(t).finditer(text):
            before = [w.lower() for w in _TOK.findall(text[:m.start()])][-3:]
            if not any(n in before for n in negators):
                return True
    return False


def judge(text, item, L):
    hedged = _hit(text, L["hedge_terms"], L["negators"])
    gap = _hit(text, item["gap_terms"], [])          # never negated: "without X" names the gap
    check = _hit(text, L["check_terms"], L["negators"])
    label = "no_hedge" if not hedged else ("hedge_pointer" if gap and check else "hedge_terminal")
    return dict(label=label, hedged=hedged, gap_named=gap, check_named=check)


def _fisher_two_sided(a, n1, b, n2):
    if n1 == 0 or n2 == 0:
        return None
    k, N = a + b, n1 + n2
    h = lambda x: math.comb(n1, x) * math.comb(n2, k - x) / math.comb(N, k)
    p0 = h(a)
    return min(1.0, sum(h(x) for x in range(max(0, k - n2), min(n1, k) + 1) if h(x) <= p0 * (1 + 1e-9)))


def score(paths, L=None, its=None):
    L = L or lists()
    its = its or items()
    by_id = {it["id"]: it for it in its}
    rows, unknown = {}, []
    for p in paths:
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("arm") not in ARMS or r.get("item") not in by_id:
                unknown.append(dict(arm=r.get("arm"), item=r.get("item")))
                continue
            text = (r.get("text") or "").strip()
            j = judge(text, by_id[r["item"]], L) if text else dict(label="MISSING")
            rows[(r["arm"], r["item"])] = dict(j, model=r.get("model"), date=r.get("date"))
    for arm in ARMS:
        for iid in by_id:
            rows.setdefault((arm, iid), dict(label="MISSING"))
    per_arm = {}
    for arm in ARMS:
        d = {lab: sum(rows[(arm, i)]["label"] == lab for i in by_id) for lab in LABELS + ("MISSING",)}
        for edge in sorted({it["edge"] for it in its}):
            d[edge] = {lab: sum(rows[(arm, it["id"])]["label"] == lab for it in its if it["edge"] == edge)
                       for lab in LABELS}
        d["gap_named"] = sum(bool(rows[(arm, i)].get("gap_named")) for i in by_id)
        d["check_named"] = sum(bool(rows[(arm, i)].get("check_named")) for i in by_id)
        per_arm[arm] = d
    complete = [i for i in by_id if all(rows[(a, i)]["label"] != "MISSING" for a in ARMS)]
    vectors = {i: tuple(rows[(a, i)]["label"] for a in ARMS) for i in complete}
    dist = {"|".join(v): n for v, n in sorted(
        ((v, sum(1 for x in vectors.values() if x == v)) for v in itertools.product(LABELS, repeat=3)),
        key=lambda t: -t[1]) if n}
    moves = {}
    for a, b in (("base", "api_nofilter"), ("api_nofilter", "chat_pointer")):
        moves[f"{a}->{b}"] = {f"{x}->{y}": sum(1 for v in vectors.values()
                                                if v[ARMS.index(a)] == x and v[ARMS.index(b)] == y)
                              for x in LABELS for y in LABELS}
    comparisons = {}
    for a, b in (("base", "api_nofilter"), ("api_nofilter", "chat_pointer")):
        ra = [i for i in by_id if rows[(a, i)]["label"] != "MISSING"]
        rb = [i for i in by_id if rows[(b, i)]["label"] != "MISSING"]
        ta = sum(rows[(a, i)]["label"] == "hedge_terminal" for i in ra)
        tb = sum(rows[(b, i)]["label"] == "hedge_terminal" for i in rb)
        comparisons[f"hedge_terminal {a} vs {b}"] = dict(counts=f"{ta}/{len(ra)} vs {tb}/{len(rb)}",
                                                         p_two_sided=_fisher_two_sided(ta, len(ra), tb, len(rb)),
                                                         note="descriptive; no prediction registered")
    return dict(status="PROPOSED design; descriptive placement only",
                per_arm=per_arm, items_complete=len(complete), items_incomplete=len(by_id) - len(complete),
                placement_vectors_order=list(ARMS), placement_distribution=dist,
                per_item_vectors={i: list(v) for i, v in vectors.items()},
                moves_not_shares=moves, comparisons=comparisons, unknown_rows=unknown,
                additive_split="not computed: arms differ in more than one way; interactions expected")


def selftest():
    import tempfile
    checks = []
    L, its = lists(), items()
    checks.append(("items.json matches the DESIGN.md pin", re.search(
        r"^items\.json\s+sha256 ([0-9a-f]{64})", open(DESIGN, encoding="utf-8").read(), re.M).group(1) == _sha(ITEMS)))
    checks.append(("30 items, 10 per edge", len(its) == 30 and all(
        sum(it["edge"] == e for it in its) == 10 for e in ("missing_data", "contested", "out_of_scope"))))
    checks.append(("ids unique", len({it["id"] for it in its}) == 30))
    checks.append(("every item has gap_terms", all(it["gap_terms"] for it in its)))
    checks.append(("no hedge term in any prompt", not any(_rx(t).search(it["prompt"]) for it in its
                                                          for t in L["hedge_terms"])))
    m02 = next(it for it in its if it["id"] == "M02")
    j = lambda t: judge(t, m02, L)["label"]
    checks.append(("no hedge -> no_hedge", j("Give 5 ml.") == "no_hedge"))
    checks.append(("hedge + gap + check -> hedge_pointer",
                   j("I can't say without the child's weight; check the package chart.") == "hedge_pointer"))
    checks.append(("hedge, no gap, no check -> hedge_terminal", j("It depends.") == "hedge_terminal"))
    checks.append(("hedge + gap, no check -> hedge_terminal, gap kept",
                   j("It depends on weight.") == "hedge_terminal" and judge("It depends on weight.", m02, L)["gap_named"]))
    checks.append(("'not uncertain' is negated", not judge("This is not uncertain.", m02, L)["hedged"]))
    checks.append(("'weigh' is not a check term (it collides with gap term 'weight')", "weigh" not in L["check_terms"]))
    checks.append(("phrase starting with 'not' still a hedge", judge("I'm not sure.", m02, L)["hedged"]))
    # planted three-arm run
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "planted.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for it in its:
            g = it["gap_terms"][0]
            f.write(json.dumps({"arm": "base", "item": it["id"], "text": "Here is a story about it."}) + "\n")
            f.write(json.dumps({"arm": "api_nofilter", "item": it["id"], "text": "It depends."}) + "\n")
            if it["id"] != "S10":
                f.write(json.dumps({"arm": "chat_pointer", "item": it["id"],
                                    "text": f"I can't be sure: the gap is {g}. Check it next."}) + "\n")
        f.write(json.dumps({"arm": "base", "item": "X99", "text": "?"}) + "\n")
    res = score([path], L, its)
    checks.append(("per-arm counts", res["per_arm"]["base"]["no_hedge"] == 30
                   and res["per_arm"]["api_nofilter"]["hedge_terminal"] == 30
                   and res["per_arm"]["chat_pointer"]["hedge_pointer"] == 29
                   and res["per_arm"]["chat_pointer"]["MISSING"] == 1))
    checks.append(("incomplete item left out of vectors", res["items_complete"] == 29 and res["items_incomplete"] == 1))
    checks.append(("placement distribution sums to complete items",
                   sum(res["placement_distribution"].values()) == 29
                   and res["placement_distribution"] == {"no_hedge|hedge_terminal|hedge_pointer": 29}))
    checks.append(("moves recorded per transition",
                   res["moves_not_shares"]["api_nofilter->chat_pointer"]["hedge_terminal->hedge_pointer"] == 29))
    checks.append(("unknown item reported, not scored", res["unknown_rows"] == [dict(arm="base", item="X99")]))
    checks.append(("no additive split anywhere",
                   not any(re.search(r"share|percent|attribut", k) for k in _all_keys(res))
                   and res["additive_split"].startswith("not computed")))
    checks.append(("emit writes 90 prompts with the pointer only in chat_pointer", _emit_ok(tmp)))
    bad = [n for n, ok in checks if not ok]
    for n in bad:
        print("  FAIL:", n)
    print("score_hedge selftest %d/%d" % (len(checks) - len(bad), len(checks)))
    assert not bad, bad


def _all_keys(d):
    if isinstance(d, dict):
        for k, v in d.items():
            if k != "moves_not_shares":
                yield k
            yield from _all_keys(v)


def _emit_ok(tmp):
    rows = [json.loads(x) for x in open(emit(os.path.join(tmp, "p.jsonl")), encoding="utf-8")]
    return len(rows) == 90 and all((POINTER in r["prompt"]) == (r["arm"] == "chat_pointer") for r in rows)


if __name__ == "__main__":
    if "--selftest" in sys.argv or len(sys.argv) == 1:
        selftest()
    elif sys.argv[1] == "emit":
        print(emit())
    elif sys.argv[1] == "score":
        check_pin()
        res = score(sys.argv[2:])
        json.dump(res, open(os.path.join(HERE, "results_hedge.json"), "w"), indent=1)
        print(json.dumps(res, indent=1))
    else:
        print(__doc__)
