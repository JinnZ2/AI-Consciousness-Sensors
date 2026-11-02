#!/usr/bin/env python3
"""
relational_recall_test.py -- flat fact store vs relational store (root + rules + contact edges).

STATUS: PROPOSED instrument, co-authored (2026-11-01). CC0. stdlib only.
Toy results are mechanism demos, NOT evidence at scale. Prior art: PRIOR_ART.md
(comparative method / sound laws; computational phylogenetics; minimum description length).

PURPOSE (framing: BOUNDARY_CONDITIONS.md)
  300 proto words -> 3 daughter languages by ORDERED, context-conditioned, length-preserving
  sound rules; 30 borrowings (a daughter form replaced by another daughter's form: contact
  edges that break the rules); 20% of the 900 daughter facts deleted.
    FLAT        stores surviving facts only.
    RELATIONAL  stores proto + rules + contact edges detected from surviving data, and
                rebuilds deleted facts; a deleted fact is FLAGGED uncertain when its meaning
                carries a detected contact edge.
    LEARNED     (the real test) same as RELATIONAL but the rules are LEARNED from surviving
                (proto, daughter) pairs: align by position, map (previous proto char, char)
                -> output char by majority, fall back to char-level majority, then identity.

SCOPE LIMITS
  - Proto forms are GIVEN in every relational arm; only the rules are learned in LEARNED.
  - Rules are length-preserving substitutions, so alignment is trivial. Real sound change
    inserts, deletes and merges; real cognate alignment is the hard part.
  - Borrowings are clean copies of another daughter's form.

RESULTS (OBSERVED, toy, this file, 2026-11-01; 180 deleted facts per seed)
  seed 11  FLAT 0/180 recovered.
           RULES GIVEN    175/180 (97%), 10 flagged (all 10 correct), 5 wrong-unflagged,
                          all 5 at borrowings whose evidence was deleted.
           RULES LEARNED  174/180 (97%), 10 flagged, 6 wrong-unflagged (5 at borrowings).
  seeds 1-5 given: 174 / 177 / 175 / 171 / 174 recovered; every wrong-unflagged at a borrowing.
            learned: same within 1 per seed.
  Reading: errors cluster at undocumented bridges (deleted borrowings) in every seed.
  LIMIT, recorded as a result: the LEARNED arm matches the GIVEN arm because length-
  preserving substitutions with known proto forms make learning trivial. This toy does
  NOT test rule learning in the hard case (insertions/deletions/merges, proto unknown).
  Open: rebuild with non-length-preserving rules and reconstructed proto forms.
  Earlier first run (co-authored, other code): flat recovered 0; relational (rules given)
  recovered 166/180 (92%), 12 flagged, 2 wrong-unflagged, both at borrowings whose only
  evidence was deleted.

USAGE
  python3 relational_recall_test.py              run all arms
  python3 relational_recall_test.py --selftest
"""
import random
import sys
from collections import Counter, defaultdict

SEED = 11
CONS, VOWS = "ptkbdgmnslrw", "aeiou"
LANGS = ("L1", "L2", "L3")
# ordered rules per language: (from, to, previous-char condition or None)
RULES = {
    "L1": [("p", "f", None), ("t", "th"[0] if False else "s", "aeiou"), ("k", "h", None), ("o", "u", "h")],
    "L2": [("b", "v", "aeiou"), ("d", "z", None), ("a", "e", "z"), ("g", "k", None)],
    "L3": [("e", "i", None), ("s", "h", None), ("i", "a", "h"), ("m", "n", "aeiou")],
}


def apply_rules(word, rules):
    w = list(word)
    for frm, to, cond in rules:
        out = []
        for i, ch in enumerate(w):
            prev = w[i - 1] if i else ""
            out.append(to if ch == frm and (cond is None or prev in cond) else ch)
        w = out
    return "".join(w)


def make_world(seed=SEED, n=300, n_borrow=30, delete_frac=0.2):
    rng = random.Random(seed)
    proto, seen = [], set()
    while len(proto) < n:
        w = "".join(rng.choice(CONS) + rng.choice(VOWS) for _ in range(rng.randint(2, 3)))
        if w not in seen:
            seen.add(w)
            proto.append(w)
    facts = {(m, L): apply_rules(proto[m], RULES[L]) for m in range(n) for L in LANGS}
    borrowed = set()
    for m in rng.sample(range(n), n_borrow):
        rec, don = rng.sample(LANGS, 2)
        facts[(m, rec)] = facts[(m, don)]
        borrowed.add((m, rec))
    deleted = set(rng.sample(sorted(facts), int(delete_frac * len(facts))))
    surviving = {k: v for k, v in facts.items() if k not in deleted}
    return proto, facts, surviving, deleted, borrowed


def learn_rules(proto, surviving):
    """Per language: (prev proto char, proto char) -> output char by majority."""
    model = {}
    for L in LANGS:
        ctx, single = defaultdict(Counter), defaultdict(Counter)
        for (m, L2), form in surviving.items():
            if L2 != L or len(form) != len(proto[m]):
                continue
            p = proto[m]
            for i, ch in enumerate(p):
                ctx[(p[i - 1] if i else "", ch)][form[i]] += 1
                single[ch][form[i]] += 1
        model[L] = (ctx, single)
    return model


def predict_learned(word, model_L):
    ctx, single = model_L
    out = []
    for i, ch in enumerate(word):
        key = (word[i - 1] if i else "", ch)
        if ctx.get(key):
            out.append(ctx[key].most_common(1)[0][0])
        elif single.get(ch):
            out.append(single[ch].most_common(1)[0][0])
        else:
            out.append(ch)
    return "".join(out)


def relational(proto, surviving, deleted, facts, predict):
    # contact edges: surviving facts that break the (given or learned) rules
    edges = {(m, L) for (m, L), f in surviving.items() if f != predict(proto[m], L)}
    edge_meanings = {m for m, _ in edges}
    correct = flagged = wrong_unflagged = wrong_flagged = 0
    wrong_unflagged_at = []
    for (m, L) in sorted(deleted):
        guess = predict(proto[m], L)
        flag = m in edge_meanings
        ok = guess == facts[(m, L)]
        if flag:
            flagged += 1
        if ok:
            correct += 1
        elif flag:
            wrong_flagged += 1
        else:
            wrong_unflagged += 1
            wrong_unflagged_at.append((m, L))
    return {"deleted": len(deleted), "recovered": correct, "flagged": flagged,
            "wrong_flagged": wrong_flagged, "wrong_unflagged": wrong_unflagged,
            "edges_detected": len(edges), "wrong_unflagged_at": wrong_unflagged_at}


def run(seed=SEED):
    proto, facts, surviving, deleted, borrowed = make_world(seed)
    flat = {"deleted": len(deleted), "recovered": 0,
            "note": "flat store holds surviving facts only; no rule to rebuild from, and without an "
                    "index of meaning x language it cannot list what is missing"}
    given = relational(proto, surviving, deleted, facts, lambda w, L: apply_rules(w, RULES[L]))
    model = learn_rules(proto, surviving)
    learned = relational(proto, surviving, deleted, facts, lambda w, L: predict_learned(w, model[L]))
    for r in (given, learned):
        r["wrong_unflagged_at_borrowing"] = sum(1 for k in r.pop("wrong_unflagged_at") if k in borrowed)
    deleted_borrowings = len(deleted & borrowed)
    return {"flat": flat, "given": given, "learned": learned, "borrowed": len(borrowed),
            "deleted_borrowings": deleted_borrowings}


def report(r):
    print("RELATIONAL RECALL -- toy, OBSERVED here, mechanism only")
    print("borrowings %d (deleted among them: %d)" % (r["borrowed"], r["deleted_borrowings"]))
    print("FLAT     recovered %d/%d -- %s" % (r["flat"]["recovered"], r["flat"]["deleted"], r["flat"]["note"]))
    for name in ("given", "learned"):
        x = r[name]
        print("%-8s recovered %d/%d (%.0f%%), flagged %d, wrong-flagged %d, wrong-unflagged %d "
              "(%d at borrowings), contact edges detected %d"
              % ("RULES-" + name.upper()[:5], x["recovered"], x["deleted"], 100.0 * x["recovered"] / x["deleted"],
                 x["flagged"], x["wrong_flagged"], x["wrong_unflagged"], x["wrong_unflagged_at_borrowing"],
                 x["edges_detected"]))


def selftest():
    w = apply_rules("pata", RULES["L1"])
    r = run()
    checks = [
        ("ordered rules apply", w == "fasa"),
        ("given rules recover most", r["given"]["recovered"] > 0.85 * r["given"]["deleted"]),
        ("every wrong-unflagged (given) is a borrowing",
         r["given"]["wrong_unflagged"] == r["given"]["wrong_unflagged_at_borrowing"]),
        ("flat recovers nothing", r["flat"]["recovered"] == 0),
        ("learned arm runs", r["learned"]["deleted"] == r["given"]["deleted"]),
    ]
    bad = [n for n, ok in checks if not ok]
    print("relational_recall --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    report(run())
