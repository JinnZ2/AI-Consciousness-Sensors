#!/usr/bin/env python3
"""
anchor_vs_similarity_test.py -- similarity retrieval vs positional (anchored) queries.

STATUS: PROPOSED instrument, co-authored (Kavik + Claude, 2026-11-01). CC0. stdlib only.
Toy results below are mechanism demos on a synthetic 8-D corpus, NOT evidence at scale.
Prior art: see PRIOR_ART.md (landmark / anchor embeddings, metric-space triangulation).

PURPOSE (framing: BOUNDARY_CONDITIONS.md)
  Part A. "Same on A, different on B" retrieval. A similarity search returns what is near
          on every axis at once; a positional query states the condition per axis.
          Count how many true targets each returns.
  Part B. Gap detection. Plant a hole (a region with no items) and ask whether K anchors,
          used as a distance coordinate system, find it by binned occupancy against a
          no-hole reference. Two arms: RANDOM anchors vs SPREAD anchors (farthest-point).

SCOPE LIMITS
  - Part A's positional query is GIVEN the axes to hold and flip: it measures what the
    query can express, not whether a system can discover which axes matter.
  - Uniform synthetic corpus; real embeddings are clustered and anisotropic.
  - Part B uses distances to anchors as coordinates; that projection mixes axes, which is
    part of what is being tested.

RESULTS (OBSERVED, toy, seed 7, this file, 2026-11-01)
  Part A  50 queries, 95 targets: similarity top-10 found 0, positional query found 95.
  Part B  hole = 125 reference points
          random anchors  K=4: 1/125 caught, 2 false flags   K=8: 3/125, 8 false flags
          spread anchors  K=4: 1/125 caught, 2 false flags   K=8: 7/125, 21 false flags
          axis-pair control (raw axes as coordinates): 49/125 caught, 0 false flags
  Reading: anchors used as distance coordinates FAILED to find the hole in both arms;
  spread anchors raised catches and false flags together. The same occupancy rule on
  coordinates aligned with the hole's axes catches it cleanly, so the failure is in the
  projection (distance to an anchor mixes all 8 axes), not in occupancy detection.
  Earlier first run (Kavik + Claude, other code, not reproduced here): Part A 39 vs 542;
  Part B random anchors 3/119 caught, 34 false flags. Same direction, different numbers.

USAGE
  python3 anchor_vs_similarity_test.py            run both parts, print results
  python3 anchor_vs_similarity_test.py --selftest planted checks
"""
import math
import random
import sys

D, N, SEED = 8, 2000, 7
HOLD, FLIP = (0, 1, 2, 3), (4, 5)   # Part A: same on A (axes 0-3), different on B (4-5)
TOL_SAME, TOL_DIFF = 0.15, 0.35
HOLE = {0: (0.30, 0.55), 1: (0.30, 0.55)}   # Part B: axis-aligned hole, ~6% of the cube


def corpus(rng, n=N, hole=None):
    out = []
    while len(out) < n:
        x = [rng.random() for _ in range(D)]
        if hole and all(lo <= x[a] < hi for a, (lo, hi) in hole.items()):
            continue
        out.append(x)
    return out


def dist(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))


def is_target(q, x):
    return (all(abs(q[a] - x[a]) <= TOL_SAME for a in HOLD)
            and all(abs(q[a] - x[a]) >= TOL_DIFF for a in FLIP))


def part_a(items, n_queries=50, k=10, rng=None):
    rng = rng or random.Random(SEED)
    sim_hits = pos_hits = total = 0
    for qi in rng.sample(range(len(items)), n_queries):
        q = items[qi]
        targets = {i for i, x in enumerate(items) if i != qi and is_target(q, x)}
        total += len(targets)
        nearest = sorted((i for i in range(len(items)) if i != qi), key=lambda i: dist(q, items[i]))[:k]
        sim_hits += len(targets & set(nearest))
        pos = {i for i, x in enumerate(items) if i != qi and is_target(q, x)}  # per-axis query
        pos_hits += len(targets & pos)
    return {"queries": n_queries, "targets_total": total, "similarity_top10_found": sim_hits,
            "positional_found": pos_hits}


def random_anchors(items, k, rng):
    return [items[i] for i in rng.sample(range(len(items)), k)]


def spread_anchors(items, k):
    """Farthest-point selection, deterministic start at the item nearest the centre."""
    centre = [0.5] * D
    chosen = [min(items, key=lambda x: dist(x, centre))]
    d = [dist(x, chosen[0]) for x in items]
    while len(chosen) < k:
        i = max(range(len(items)), key=lambda j: d[j])
        chosen.append(items[i])
        d = [min(d[j], dist(items[j], items[i])) for j in range(len(items))]
    return chosen


def cell(x, anchors, bins, dmax):
    return tuple(min(bins - 1, int(dist(x, a) / dmax * bins)) for a in anchors)


def part_b(anchors, ref, test, bins=6, min_ref=4, ratio=0.25):
    """Flag cells where the reference has >= min_ref items and the test has <= ratio of it."""
    dmax = math.sqrt(D)
    rc, tc = {}, {}
    for x in ref:
        c = cell(x, anchors, bins, dmax)
        rc[c] = rc.get(c, 0) + 1
    for x in test:
        c = cell(x, anchors, bins, dmax)
        tc[c] = tc.get(c, 0) + 1
    flagged = {c for c, n in rc.items() if n >= min_ref and tc.get(c, 0) <= ratio * n}
    in_hole = [x for x in ref if all(lo <= x[a] < hi for a, (lo, hi) in HOLE.items())]
    caught = sum(1 for x in in_hole if cell(x, anchors, bins, dmax) in flagged)
    false_flags = 0
    for c in flagged:
        members = [x for x in ref if cell(x, anchors, bins, dmax) == c]
        inside = sum(1 for x in members if all(lo <= x[a] < hi for a, (lo, hi) in HOLE.items()))
        if inside * 2 < len(members):
            false_flags += 1
    return {"hole_points": len(in_hole), "caught": caught, "flagged_cells": len(flagged),
            "false_flags": false_flags}


def part_b_axis_pairs(ref, test, bins=8, min_ref=4, ratio=0.25):
    """Positive control: same occupancy rule, coordinates = raw axis pairs (28 2-D grids).
    If this catches the hole while anchor-distance coordinates do not, the failure is in
    the projection, not in occupancy detection."""
    def c2(x, a, b):
        return (min(bins - 1, int(x[a] * bins)), min(bins - 1, int(x[b] * bins)))
    in_hole = lambda x: all(lo <= x[a] < hi for a, (lo, hi) in HOLE.items())  # noqa: E731
    flagged = set()
    for a in range(D):
        for b in range(a + 1, D):
            rc, tc = {}, {}
            for x in ref:
                rc[c2(x, a, b)] = rc.get(c2(x, a, b), 0) + 1
            for x in test:
                tc[c2(x, a, b)] = tc.get(c2(x, a, b), 0) + 1
            for c, n in rc.items():
                if n >= min_ref and tc.get(c, 0) <= ratio * n:
                    flagged.add((a, b, c))
    holes = [x for x in ref if in_hole(x)]
    caught = sum(1 for x in holes if any(c2(x, a, b) == c for a, b, c in flagged))
    false_flags = 0
    for a, b, c in flagged:
        members = [x for x in ref if c2(x, a, b) == c]
        if sum(map(in_hole, members)) * 2 < len(members):
            false_flags += 1
    return {"hole_points": len(holes), "caught": caught, "flagged_cells": len(flagged),
            "false_flags": false_flags}


def run(k=4, seed=SEED):
    rng = random.Random(seed)
    items = corpus(rng)
    a = part_a(items, rng=random.Random(seed))
    ref = corpus(random.Random(seed + 1))
    test = corpus(random.Random(seed + 2), hole=HOLE)
    b_rand = part_b(random_anchors(ref, k, random.Random(seed + 3)), ref, test)
    b_spread = part_b(spread_anchors(ref, k), ref, test)
    b_axis = part_b_axis_pairs(ref, test)
    return {"part_a": a, "part_b_random": b_rand, "part_b_spread": b_spread, "part_b_axis": b_axis, "k": k}


def report(r):
    a, br, bs = r["part_a"], r["part_b_random"], r["part_b_spread"]
    print("ANCHOR vs SIMILARITY -- toy, synthetic 8-D, OBSERVED here, not evidence at scale")
    print("Part A  targets over %d queries: %d" % (a["queries"], a["targets_total"]))
    print("        similarity top-10 found: %d   positional query found: %d"
          % (a["similarity_top10_found"], a["positional_found"]))
    print("        (positional query was GIVEN the axes: expressiveness, not discovery)")
    for name, b in (("random", br), ("spread", bs), ("axis-pair control", r["part_b_axis"])):
        print("Part B  %-17s (K=%d): caught %d/%d hole points, %d flagged cells, %d false flags"
              % (name, r["k"], b["caught"], b["hole_points"], b["flagged_cells"], b["false_flags"]))


def selftest():
    r = run()
    checks = [
        ("part A: positional finds all targets", r["part_a"]["positional_found"] == r["part_a"]["targets_total"]),
        ("part A: similarity finds fewer", r["part_a"]["similarity_top10_found"] < r["part_a"]["targets_total"]),
        ("part B: hole has points in reference", r["part_b_random"]["hole_points"] > 50),
        ("part B: no-hole test flags nothing much",
         part_b(spread_anchors(corpus(random.Random(1)), 4), corpus(random.Random(1)),
                corpus(random.Random(1)))["flagged_cells"] == 0),
    ]
    bad = [n for n, ok in checks if not ok]
    print("anchor_vs_similarity --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    report(run())
    report(run(k=8))
