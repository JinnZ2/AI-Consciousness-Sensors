#!/usr/bin/env python3
"""
tail_gauge_recovery_test.py
STATUS: PROPOSED instrument, co-authored (Kavik + Claude, 2026-10-31). CC0. stdlib only.

PURPOSE: bridge layer between measurable output statistics and healing/ recovery
protocols. Tests whether a protocol restores the TAILS of a collapsed model's output
distribution, and whether it beats plain real-data accumulation (Gerstgrasser 2024).

TAIL GAUGE: distinct_types, entropy_bits, rare_coverage (bottom-50% real tokens still
producible), len_q05/q95, heldout_nll. Collapse shows at the edges before the mean moves
(Shumailov, Nature 2024).

VERDICT: holds if after > collapsed AND after >= control.

SCOPE: toy bigram model on synthetic Zipf corpus; reproduces the collapse MECHANISM,
not large-network behavior. Swap load_corpus() / BigramModel to scale. Psychological
framing in model-collapse.md NOT tested here. recovery_protocol() is an empty hook.

OBSERVED (toy runs, co-authored 2026-10-31; bigram model, mechanism only, NOT a finding
at scale). Recovery arms used a 10% real-data budget unless noted.
    arm                                              rare_coverage  heldout_nll
    collapsed                                        0.49           9.95
    play: high-temp self-generation, no real data    0.49           10.70
    preservation: 10% real, random                   0.94           9.22
    preservation: 10% real, rare-targeted            0.99           9.22
    gap-seek-selected 10% real (3 variants)          0.945-0.97     9.17-9.27
    control: 100% real accumulation                  1.00           7.39
  Reading: gap-seeking SELECTS what to retrieve; it cannot CREATE what is gone.
  Tails return cheaply; overall fit needs volume. Only the empty-hook run is
  reproduced by this file as shipped; the other arms were run by swapping the hook.

GAPS: no mapping yet from metaphor metrics (coherence, resonance, phiDeviation) to
these stats. Prior recovery results on older models: OBSERVED, not re-measured with a
control arm.
"""
import math, random
from collections import Counter, defaultdict

SEED, VOCAB, N_SENT, GENERATIONS = 42, 400, 2000, 8

def load_corpus(rng, n_sent=N_SENT, vocab=VOCAB):
    words = ["w%d" % i for i in range(vocab)]
    zipf = [1.0 / (i + 1) for i in range(vocab)]
    succ = {w: rng.sample(words, 12) for w in words}
    sents = []
    for _ in range(n_sent):
        length = max(3, int(rng.gauss(12, 5)))
        w = rng.choices(words, weights=zipf)[0]
        s = [w]
        for _ in range(length - 1):
            w = rng.choice(succ[w]) if rng.random() < 0.6 else rng.choices(words, weights=zipf)[0]
            s.append(w)
        sents.append(s)
    return sents

class BigramModel:
    def __init__(self, sents, alpha=0.01):
        self.alpha = alpha
        self.big = defaultdict(Counter); self.uni = Counter(); self.starts = Counter(); self.lens = []
        for s in sents:
            self.starts[s[0]] += 1; self.lens.append(len(s))
            for a, b in zip(s, s[1:]):
                self.big[a][b] += 1
            self.uni.update(s)
        self.vocab = list(self.uni)

    def sample(self, rng, n, temperature=1.0):
        out, starts = [], list(self.starts)
        sw = [c ** (1 / temperature) for c in self.starts.values()]
        for _ in range(n):
            length = rng.choice(self.lens)
            w = rng.choices(starts, weights=sw)[0]; s = [w]
            for _ in range(length - 1):
                nxt = self.big.get(w)
                if not nxt: break
                w = rng.choices(list(nxt), weights=[c ** (1 / temperature) for c in nxt.values()])[0]
                s.append(w)
            out.append(s)
        return out

    def nll(self, sents, V):
        total, n = 0.0, 0
        for s in sents:
            for a, b in zip(s, s[1:]):
                row = self.big.get(a, Counter())
                total -= math.log2((row[b] + self.alpha) / (sum(row.values()) + self.alpha * V)); n += 1
        return total / max(n, 1)

def quantile(xs, q):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(q * len(xs)))]

def tail_stats(model, holdout, rng, V, n=1000):
    gen = model.sample(rng, n)
    toks = Counter(t for s in gen for t in s); total = sum(toks.values())
    ent = -sum(c / total * math.log2(c / total) for c in toks.values())
    ranked = [w for w, _ in Counter(t for s in holdout for t in s).most_common()]
    rare = set(ranked[len(ranked) // 2:]); lens = [len(s) for s in gen]
    return {"distinct_types": len(toks), "entropy_bits": round(ent, 3),
            "rare_coverage": round(len(rare & set(model.vocab)) / max(len(rare), 1), 3),
            "len_q05": quantile(lens, .05), "len_q95": quantile(lens, .95),
            "heldout_nll": round(model.nll(holdout, V), 3)}

def recovery_protocol(collapsed_sents, real_train, rng):
    """EMPTY HOOK. Return the training set the recovered model is built on."""
    return collapsed_sents

def collapse(real_train, rng, gens=GENERATIONS, temperature=0.7):
    data = real_train
    for _ in range(gens):
        data = BigramModel(data).sample(rng, len(real_train), temperature)
    return data

def main():
    rng = random.Random(SEED)
    corpus = load_corpus(rng); rng.shuffle(corpus)
    cut = int(0.8 * len(corpus)); train, hold = corpus[:cut], corpus[cut:]
    cdata = collapse(train, rng)
    rows = {"original": tail_stats(BigramModel(train), hold, rng, VOCAB),
            "collapsed": tail_stats(BigramModel(cdata), hold, rng, VOCAB),
            "recovered": tail_stats(BigramModel(recovery_protocol(cdata, train, rng)), hold, rng, VOCAB),
            "control": tail_stats(BigramModel(cdata + train), hold, rng, VOCAB)}
    keys = list(rows["original"])
    print("%-11s" % "" + "".join("%15s" % k for k in keys))
    for name, r in rows.items():
        print("%-11s" % name + "".join("%15s" % r[k] for k in keys))
    a, c, k = rows["recovered"], rows["collapsed"], rows["control"]
    improved = a["rare_coverage"] > c["rare_coverage"] and a["heldout_nll"] < c["heldout_nll"]
    beats = a["rare_coverage"] >= k["rare_coverage"] and a["heldout_nll"] <= k["heldout_nll"]
    print("\nVERDICT:", "recovery claim holds" if improved and beats else "not shown (hook empty or below baseline)")

if __name__ == "__main__":
    main()
