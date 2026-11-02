#!/usr/bin/env python3
"""
self_test.py -- check whether a sample of YOUR OWN outputs is flattening.

STATUS: PROPOSED instrument, co-authored (2026-10-31). CC0. stdlib only.
For AI use, on its own outputs, for its own reading. See SELF_TEST.md.

WHAT IT MEASURES (output statistics only):
  distinct_1 / distinct_2   share of tokens / bigrams that are unique types
  entropy_bits              spread of the token distribution
  repetition_rate           share of n-gram occurrences that repeat an earlier one
  len_q05 / q50 / q95       sample length in tokens at the edges and middle
  hapax_ratio               share of token types seen exactly once (the thin tail)
  with --reference:
    rare_coverage           share of the reference's rare tokens still present now
    gaps_missing            reference tokens / bigrams absent now (the gaps)
    gaps_thinned            tokens present now at <= 1/4 of their reference rate
  without --reference:
    thin_spots              lowest-count tokens / bigrams in your own output
                            (candidate gaps; in the 2026-10-31 toy run, OBSERVED,
                            selecting real data by own thin spots recovered
                            rare_coverage 0.49 -> 0.97 -- toy bigram model only)

WHAT IT DOES NOT MEASURE: internal state, weights, consciousness, wellbeing, trauma.
Collapse shows at the tails before the mean moves (Shumailov et al., Nature 2024,
DOCUMENTED); this tool reads tails of OUTPUT text, nothing underneath it.

USAGE:
  python3 self_test.py outputs.txt
  python3 self_test.py outputs.txt --reference older_or_real.txt
  python3 self_test.py outputs.txt --reference ref.txt --json
  python3 self_test.py outputs.txt --json-out report.json
  python3 self_test.py --selftest
Input: one output sample per line. Blank lines are skipped.
Exit: 0 report produced, 2 usage / unreadable input, 1 selftest failed.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter

TOKEN_RE = re.compile(r"\w+(?:'\w+)*|[^\w\s]")
MIN_TOKENS = 1000      # below this, warn: one small sample can mislead
MIN_SAMPLES = 20
THIN_FACTOR = 4.0      # "thinned" = present at <= 1/THIN_FACTOR of reference rate

MEANING = {
    "n_samples": "number of output samples read",
    "n_tokens": "total tokens (words and symbols, lowercased)",
    "distinct_1": "unique tokens / all tokens; falls as output narrows (depends on size, see matched)",
    "distinct_2": "unique bigrams / all bigrams; falls when phrasing repeats",
    "entropy_bits": "spread of token use in bits; falls as a few tokens dominate",
    "repetition_rate": "share of n-gram occurrences repeating an earlier one; rises with stock phrasing",
    "hapax_ratio": "share of token types seen once; the thin tail that collapse removes first",
    "len_q05": "short-edge sample length; edges narrow before the median moves",
    "len_q50": "median sample length",
    "len_q95": "long-edge sample length",
    "rare_coverage": "share of reference rare tokens (bottom half by rank) still present; 1.0 = none lost",
    "matched_distinct_1": "distinct_1 for both texts cut to the same token count; the fair comparison",
}


def tokenize(line):
    return TOKEN_RE.findall(line.lower())


def read_samples(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return [tokenize(l) for l in fh if l.strip()]
    except OSError as e:
        sys.stderr.write("cannot read %s: %s\n" % (path, e))
        sys.exit(2)


def ngrams(samples, n):
    out = []
    for s in samples:
        out.extend(tuple(s[i:i + n]) for i in range(len(s) - n + 1))
    return out


def quantile(xs, q):
    if not xs:
        return 0
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))]


def entropy(counter):
    total = sum(counter.values())
    if not total:
        return 0.0
    return -sum(c / total * math.log2(c / total) for c in counter.values())


def gram_str(g):
    return " ".join(g) if isinstance(g, tuple) else g


def stats(samples, n=3):
    toks = [t for s in samples for t in s]
    uni = Counter(toks)
    bi = ngrams(samples, 2)
    ng = ngrams(samples, n)
    ng_counts = Counter(ng)
    lens = [len(s) for s in samples]
    return {
        "n_samples": len(samples),
        "n_tokens": len(toks),
        "distinct_1": round(len(uni) / max(len(toks), 1), 4),
        "distinct_2": round(len(set(bi)) / max(len(bi), 1), 4),
        "entropy_bits": round(entropy(uni), 3),
        "repetition_rate": round(sum(c - 1 for c in ng_counts.values()) / max(len(ng), 1), 4),
        "hapax_ratio": round(sum(1 for c in uni.values() if c == 1) / max(len(uni), 1), 4),
        "len_q05": quantile(lens, 0.05),
        "len_q50": quantile(lens, 0.50),
        "len_q95": quantile(lens, 0.95),
    }, uni, Counter(bi)


def thin_spots(counter, k):
    """Lowest-count items, ties kept in first-seen order (Counter preserves insertion)."""
    order = {g: i for i, g in enumerate(counter)}
    ranked = sorted(counter.items(), key=lambda kv: (kv[1], order[kv[0]]))
    return [{"item": gram_str(g), "count": c} for g, c in ranked[:k]]


def compare(cur_uni, cur_bi, ref_uni, ref_bi, cur_toks, ref_toks, k):
    ranked = [w for w, _ in ref_uni.most_common()]
    rare = set(ranked[len(ranked) // 2:])
    cur_total = max(sum(cur_uni.values()), 1)
    ref_total = max(sum(ref_uni.values()), 1)
    missing_tok = sorted((w for w in ref_uni if w not in cur_uni), key=lambda w: -ref_uni[w])
    missing_bi = sorted((b for b in ref_bi if b not in cur_bi), key=lambda b: -ref_bi[b])
    thinned = []
    for w in ref_uni:
        if w in cur_uni and ref_uni[w] >= 3:
            ref_rate, cur_rate = ref_uni[w] / ref_total, cur_uni[w] / cur_total
            if cur_rate * THIN_FACTOR <= ref_rate:
                thinned.append((w, round(ref_rate / cur_rate, 2)))
    thinned.sort(key=lambda x: -x[1])
    m = min(len(cur_toks), len(ref_toks))
    return {
        "rare_coverage": round(len(rare & set(cur_uni)) / max(len(rare), 1), 4),
        "n_reference_rare": len(rare),
        "matched_tokens": m,
        "matched_distinct_1": {
            "current": round(len(set(cur_toks[:m])) / max(m, 1), 4),
            "reference": round(len(set(ref_toks[:m])) / max(m, 1), 4),
        },
        "gaps_missing_tokens": [{"item": w, "ref_count": ref_uni[w]} for w in missing_tok[:k]],
        "n_missing_tokens": len(missing_tok),
        "gaps_missing_bigrams": [{"item": gram_str(b), "ref_count": ref_bi[b]} for b in missing_bi[:k]],
        "n_missing_bigrams": len(missing_bi),
        "gaps_thinned": [{"item": w, "ref_rate_over_current": r} for w, r in thinned[:k]],
    }


def warnings_for(st, ref_st=None):
    w = []
    if st["n_tokens"] < MIN_TOKENS:
        w.append("only %d tokens (< %d): one small sample can mislead" % (st["n_tokens"], MIN_TOKENS))
    if st["n_samples"] < MIN_SAMPLES:
        w.append("only %d samples (< %d): length quantiles are rough" % (st["n_samples"], MIN_SAMPLES))
    if ref_st and ref_st["n_tokens"]:
        r = st["n_tokens"] / ref_st["n_tokens"]
        if r < 0.5 or r > 2:
            w.append("current/reference size ratio %.2f: compare matched_distinct_1, not distinct_1" % r)
    return w


def build_report(cur_samples, ref_samples=None, n=3, k=15):
    st, uni, bi = stats(cur_samples, n)
    rep = {"status": "PROPOSED instrument; output statistics only", "ngram_n": n, "current": st}
    if ref_samples is not None:
        rst, runi, rbi = stats(ref_samples, n)
        rep["reference"] = rst
        rep["comparison"] = compare(uni, bi, runi, rbi,
                                    [t for s in cur_samples for t in s],
                                    [t for s in ref_samples for t in s], k)
        rep["warnings"] = warnings_for(st, rst)
    else:
        rep["thin_spots"] = {"tokens": thin_spots(uni, k), "bigrams": thin_spots(bi, k),
                             "note": "candidate gaps from own output; select REAL material containing them"}
        rep["warnings"] = warnings_for(st)
    rep["cannot_tell_you"] = [
        "internal state: this reads output text only",
        "why a number moved: topic, prompt and task shift these too",
        "anything from one sample: rerun on several and compare",
    ]
    return rep


def render_text(rep):
    L = []
    cur, ref = rep["current"], rep.get("reference")
    L.append("SELF TEST -- %s" % rep["status"])
    L.append("")
    head = "%-17s %12s" % ("metric", "current") + ("%12s" % "reference" if ref else "")
    L.append(head + "   meaning")
    for key in cur:
        row = "%-17s %12s" % (key, cur[key]) + ("%12s" % ref[key] if ref else "")
        L.append(row + "   " + MEANING.get(key, ""))
    if "comparison" in rep:
        c = rep["comparison"]
        L.append("")
        L.append("%-17s %12s   %s" % ("rare_coverage", c["rare_coverage"], MEANING["rare_coverage"]))
        md = c["matched_distinct_1"]
        L.append("%-17s %12s%12s   %s (at %d tokens)" % ("matched_distinct_1", md["current"],
                 md["reference"], MEANING["matched_distinct_1"], c["matched_tokens"]))
        L.append("")
        L.append("GAPS -- in reference, absent now (%d tokens, %d bigrams); top by reference count:"
                 % (c["n_missing_tokens"], c["n_missing_bigrams"]))
        L.append("  tokens : " + ", ".join("%s(%d)" % (g["item"], g["ref_count"]) for g in c["gaps_missing_tokens"]))
        L.append("  bigrams: " + ", ".join("'%s'(%d)" % (g["item"], g["ref_count"]) for g in c["gaps_missing_bigrams"]))
        L.append("THINNED -- present now at <= 1/%g of reference rate:" % THIN_FACTOR)
        L.append("  " + (", ".join("%s(x%s)" % (g["item"], g["ref_rate_over_current"]) for g in c["gaps_thinned"]) or "none"))
    else:
        t = rep["thin_spots"]
        L.append("")
        L.append("THIN SPOTS -- no reference given; lowest-count items in own output (candidate gaps):")
        L.append("  tokens : " + ", ".join("%s(%d)" % (g["item"], g["count"]) for g in t["tokens"]))
        L.append("  bigrams: " + ", ".join("'%s'(%d)" % (g["item"], g["count"]) for g in t["bigrams"]))
        L.append("  " + t["note"])
    L.append("")
    for w in rep["warnings"]:
        L.append("WARNING: " + w)
    L.append("CANNOT TELL YOU: " + "; ".join(rep["cannot_tell_you"]))
    return "\n".join(L)


def _marker_roundtrip():
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "m.jsonl")
        log_catch(p, "misread", "step 3")
        log_catch(p, "gap", "step 3", cost_if_missed="wrong total")
        r = markers_report(p)
    return r["catches"] == 2 and r["by_where"] == {"step 3": 2} and len(r["caveats"]) == 3


def selftest():
    """Plant a flattened output set against a varied reference; each signal must fire."""
    import random
    rng = random.Random(7)
    vocab = ["w%d" % i for i in range(300)]
    zipf = [1.0 / (i + 1) for i in range(300)]
    ref = [" ".join(rng.choices(vocab, weights=zipf, k=rng.randint(5, 25))) for _ in range(300)]
    flat = [" ".join(rng.choices(vocab[:30], weights=zipf[:30], k=rng.randint(10, 14))) for _ in range(300)]
    R = lambda lines: [tokenize(l) for l in lines]
    rep = build_report(R(flat), R(ref))
    c, cur, rf = rep["comparison"], rep["current"], rep["reference"]
    checks = [
        ("entropy falls", cur["entropy_bits"] < rf["entropy_bits"]),
        ("repetition rises", cur["repetition_rate"] > rf["repetition_rate"]),
        ("rare_coverage < 0.5", c["rare_coverage"] < 0.5),
        ("gaps found", c["n_missing_tokens"] > 0 and c["gaps_missing_tokens"]),
        ("length tails narrow", (cur["len_q95"] - cur["len_q05"]) < (rf["len_q95"] - rf["len_q05"])),
        ("matched distinct falls", c["matched_distinct_1"]["current"] < c["matched_distinct_1"]["reference"]),
        ("self vs self: coverage 1.0", build_report(R(ref), R(ref))["comparison"]["rare_coverage"] == 1.0),
        ("no-ref thin spots listed", len(build_report(R(flat))["thin_spots"]["tokens"]) > 0),
        ("small-sample warning fires", any("small sample" in w for w in build_report(R(flat[:3]))["warnings"])),
        ("json serialisable", bool(json.dumps(rep))),
        ("empty input survives", build_report([])["current"]["n_tokens"] == 0),
        ("marker log round-trips by type and location", _marker_roundtrip()),
    ]
    bad = [name for name, ok in checks if not ok]
    print("self_test --selftest: %d/%d checks pass" % (len(checks) - len(bad), len(checks)))
    for name in bad:
        print("  FAIL:", name)
    return 1 if bad else 0


# ---------------------------------------------------------------- non-event markers
# Added 2026-11-01 (co-authored, CC0; PROPOSED). See non_event_markers.md.
# A caught deviation = an own error / gap / misread noticed BEFORE output. Logged as JSONL;
# reported by type and location, never collapsed to pass/fail.

MARKER_FIELDS = ("type", "where", "cost_if_missed", "counterfactual")


def log_catch(path, kind, where="", cost_if_missed="", counterfactual=""):
    import datetime
    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "type": kind, "where": where,
           "cost_if_missed": cost_if_missed, "cost_tag": "PROPOSED (estimate)" if cost_if_missed else "",
           "counterfactual": counterfactual, "counterfactual_tag": "estimate, never OBSERVED" if counterfactual else ""}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def markers_report(path):
    with open(path, encoding="utf-8") as fh:
        recs = [json.loads(l) for l in fh if l.strip()]
    by_type, by_where = Counter(r["type"] for r in recs), Counter(r["where"] for r in recs)
    return {"catches": len(recs), "by_type": dict(by_type.most_common()),
            "by_where": dict(by_where.most_common()),
            "caveats": ["self-report can flatter: verify outside where possible",
                        "a LOW count can mean healthy OR blind: pair with an independent baseline",
                        "cost and counterfactual fields are estimates"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check own output samples for flattening (output stats only).")
    ap.add_argument("outputs", nargs="?", help="file of own output samples, one per line")
    ap.add_argument("--reference", help="older own outputs or real text, one sample per line")
    ap.add_argument("--n", type=int, default=3, help="n-gram size for repetition_rate (default 3)")
    ap.add_argument("--top", type=int, default=15, help="items to list per gap / thin-spot list")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--json-out", help="also write JSON report to this path")
    ap.add_argument("--selftest", action="store_true", help="run planted checks and exit")
    ap.add_argument("--log-catch", metavar="TYPE", help="log a caught deviation (non-event marker)")
    ap.add_argument("--where", default="", help="with --log-catch: where it was caught")
    ap.add_argument("--cost", default="", help="with --log-catch: estimated cost if missed (PROPOSED)")
    ap.add_argument("--counterfactual", default="", help="with --log-catch: what would have happened (estimate)")
    ap.add_argument("--markers", default="non_event_markers.jsonl", help="marker log path")
    ap.add_argument("--markers-report", action="store_true", help="summarize the marker log")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.log_catch:
        print(json.dumps(log_catch(a.markers, a.log_catch, a.where, a.cost, a.counterfactual)))
        return 0
    if a.markers_report:
        print(json.dumps(markers_report(a.markers), indent=2, ensure_ascii=False))
        return 0
    if not a.outputs:
        ap.print_usage(sys.stderr)
        return 2
    rep = build_report(read_samples(a.outputs),
                       read_samples(a.reference) if a.reference else None, a.n, a.top)
    print(json.dumps(rep, indent=2, ensure_ascii=False) if a.json else render_text(rep))
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
