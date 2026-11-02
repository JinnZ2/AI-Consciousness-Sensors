#!/usr/bin/env python3
"""
exception_promotion_test.py -- when do exceptions become a rule? (Verner's law pattern)

STATUS: PROPOSED instrument, co-authored (2026-11-01). CC0. stdlib only.
Toy results are mechanism demos, NOT evidence at scale. Prior art: PRIOR_ART.md
(rule induction / ILP; anomaly clustering; Verner 1875 as the historical case).

PRECEDENT (DOCUMENTED, VERIFY wording): Karl Verner (1875/1877) showed that exceptions to
Grimm's law were regular once the position of the Indo-European accent was taken into
account -- a hidden conditioned rule, not noise.

PURPOSE
  Toy: 400 proto words; a KNOWN ordered rule set is applied; a HIDDEN conditioned rule
  (a -> e after k) is applied last; 5% of words get one random substitution (noise).
  1. Exceptions = positions where the attested daughter differs from the known-rule prediction.
  2. Group each difference by context (previous char, old, new).
  3. A group is PROMOTED to a rule only if it REPEATS (>= MIN_REPEAT) and HOLDS wherever its
     context occurs (share of context occurrences showing the change >= HOLD_SHARE).
     Repetition + relational coherence: the criteria in ../evidence_is_a_verb.md.
  4. Singletons and non-holding groups stay marked as one-offs; nothing is averaged in.
AI USE (PROPOSED): cluster a model's own errors by context; a recurring cluster that holds
  = a missing boundary condition; scattered singletons = noise. `--log` reads such a log.

SCOPE LIMITS
  - Length-preserving substitutions; one-character context. Real exceptions can need wider
    or non-adjacent context (Verner's needed stress position, absent from the written form).
  - Promotion thresholds are fixed by hand.

RESULTS (OBSERVED, toy, this file, 2026-11-01)
  seed 5   400 words, 32 with exceptions (13 planted noise). PROMOTED a -> e after k:
           20 times, holds 20/20. 13 singletons held back. After promotion: 13 exception
           words = the 13 planted noise words. Seeds 1-3: same pattern (21/21, 12/12, 26/26).
  FAILURE ARM (required): hidden rule a -> e word-finally (condition outside the 1-char
           window). 105 exception words, 0 promoted. Groups repeat 6-20 times but hold only
           0.25-0.53 -> held back. The method cannot see a condition it does not encode.
           Reading: "repeats but does not hold" is a separate signature from scattered
           singletons; it points at a missing context variable, not noise.
  Earlier first run (co-authored, other code): 30/400 exceptions; one context 15x
           (a -> e after k), held 15/15; others 1x; after promotion 15 left ~ planted noise.

USAGE
  python3 exception_promotion_test.py                    toy run
  python3 exception_promotion_test.py --log errors.csv   CSV: context,expected,got
                                                         (include correct rows, expected==got,
                                                          so 'holds' can be measured)
  python3 exception_promotion_test.py --selftest
"""
import csv
import random
import sys
from collections import Counter, defaultdict

SEED, N, NOISE = 5, 400, 0.05
MIN_REPEAT, HOLD_SHARE = 3, 0.9
CONS, VOWS = "ptkbdgmnslr", "aeiou"
KNOWN = [("p", "f", None), ("t", "d", "aeiou"), ("o", "u", None)]
HIDDEN = ("a", "e", "k")   # a -> e after k


def apply(word, rules):
    w = list(word)
    for frm, to, cond in rules:
        w = [to if ch == frm and (cond is None or (i and w[i - 1] in cond)) else ch for i, ch in enumerate(w)]
    return "".join(w)


def final_a_to_e(word):
    """Non-local hidden rule for the failure arm: a -> e in word-final position only.
    Its condition (position) is outside the one-character context window."""
    return word[:-1] + "e" if word.endswith("a") else word


def world(seed=SEED, hidden=None):
    rng = random.Random(seed)
    proto = ["".join(rng.choice(CONS) + rng.choice(VOWS) for _ in range(rng.randint(2, 4))) for _ in range(N)]
    attested, noisy = [], 0
    hidden = hidden or (lambda w: apply(w, [HIDDEN]))
    for p in proto:
        d = list(hidden(apply(p, KNOWN)))
        if rng.random() < NOISE:
            i = rng.randrange(len(d))
            d[i] = rng.choice([c for c in CONS + VOWS if c != d[i]])
            noisy += 1
        attested.append("".join(d))
    return proto, attested, noisy


def observations(proto, attested, rules):
    """Every position: (context, expected, got)."""
    obs = []
    for p, a in zip(proto, attested):
        e = apply(p, rules)
        for i, (x, y) in enumerate(zip(e, a)):
            obs.append((e[i - 1] if i else "^", x, y))
    return obs


def promote(obs):
    occ = Counter((c, x) for c, x, _ in obs)
    diff = Counter((c, x, y) for c, x, y in obs if x != y)
    promoted, held_back = [], []
    for (c, x, y), n in diff.most_common():
        share = n / occ[(c, x)]
        rec = {"context": c, "old": x, "new": y, "count": n, "occurrences": occ[(c, x)], "holds": round(share, 3)}
        (promoted if n >= MIN_REPEAT and share >= HOLD_SHARE else held_back).append(rec)
    return promoted, held_back, sum(diff.values())


def words_with_exceptions(proto, attested, rules):
    return sum(1 for p, a in zip(proto, attested) if apply(p, rules) != a)


def run(seed=SEED, hidden=None):
    proto, attested, noisy = world(seed, hidden)
    before = words_with_exceptions(proto, attested, KNOWN)
    promoted, held, n_diff = promote(observations(proto, attested, KNOWN))
    groups = (promoted, held, n_diff)
    new_rules = KNOWN + [(r["old"], r["new"], r["context"]) for r in promoted]
    after = words_with_exceptions(proto, attested, new_rules)
    return {"words": N, "planted_noise_words": noisy, "exception_words_before": before,
            "exception_positions": n_diff, "promoted": promoted,
            "held_back_groups": len(held), "held_back_singletons": sum(1 for h in held if h["count"] == 1),
            "exception_words_after": after, "_groups": groups}


def report(r):
    print("EXCEPTION PROMOTION -- toy, OBSERVED here, mechanism only")
    print("words %d, planted noise words %d, words with exceptions before %d"
          % (r["words"], r["planted_noise_words"], r["exception_words_before"]))
    for p in r["promoted"]:
        print("PROMOTED  %s -> %s after '%s': %d times, holds %d/%d (%.2f)"
              % (p["old"], p["new"], p["context"], p["count"], p["count"], p["occurrences"], p["holds"]))
    print("held back %d groups (%d singletons) -- kept as one-offs, not averaged"
          % (r["held_back_groups"], r["held_back_singletons"]))
    print("words with exceptions after promotion %d (planted noise %d)"
          % (r["exception_words_after"], r["planted_noise_words"]))


def report_failure_arm(r):
    print("FAILURE ARM -- hidden rule outside the context window (a -> e word-finally):")
    print("  words with exceptions before %d, promoted %d rules, after %d (planted noise %d)"
          % (r["exception_words_before"], len(r["promoted"]), r["exception_words_after"], r["planted_noise_words"]))
    promoted, held, _ = r["_groups"]
    rep = [h for h in held if h["count"] >= MIN_REPEAT]
    print("  held back: %d groups that REPEAT (>= %d) but do not HOLD (shares %.2f-%.2f)"
          % (len(rep), MIN_REPEAT, min(h["holds"] for h in rep), max(h["holds"] for h in rep)) if rep else "")
    print("  -> the method cannot promote a rule whose condition is outside its context window.")
    print("     'repeats but does not hold' differs from scattered singletons: it marks a")
    print("     missing context variable (as stress position was for Verner), not noise.")


def from_log(path):
    with open(path, newline="", encoding="utf-8") as f:
        obs = [(row["context"], row["expected"], row["got"]) for row in csv.DictReader(f)]
    promoted, held, n = promote(obs)
    print("error log: %d rows, %d errors" % (len(obs), n))
    for p in promoted:
        print("RECURRING + HOLDS (candidate missing condition): %r" % p)
    for h in held:
        print("one-off / not holding: %r" % h)


def selftest():
    r = run()
    hidden = [p for p in r["promoted"] if (p["old"], p["new"], p["context"]) == HIDDEN]
    checks = [
        ("hidden rule promoted", len(hidden) == 1),
        ("only the hidden rule promoted", len(r["promoted"]) == 1),
        ("after promotion, exceptions ~ planted noise", abs(r["exception_words_after"] - r["planted_noise_words"]) <= 3),
        ("noise-only world promotes nothing", run_noise_only()["promoted"] == []),
        ("failure arm: non-local rule NOT promoted (method limit)",
         not any((p["old"], p["new"]) == ("a", "e") for p in run(hidden=final_a_to_e)["promoted"])),
    ]
    bad = [n for n, ok in checks if not ok]
    print("exception_promotion --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


def run_noise_only(seed=9):
    global HIDDEN
    saved, HIDDEN = HIDDEN, ("z", "z", "z")
    try:
        return run(seed)
    finally:
        HIDDEN = saved


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--log" in sys.argv:
        from_log(sys.argv[sys.argv.index("--log") + 1])
        sys.exit(0)
    report(run())
    report_failure_arm(run(hidden=final_a_to_e))
