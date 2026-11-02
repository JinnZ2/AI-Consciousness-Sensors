# Polyhedron method -- reading a body of literature as a solid with faces, edges and gaps

STATUS: OBSERVED as a working tool (practice report); PROPOSED as a general method,
untested at scale. Co-authored write-up (2026-11-01). CC0.
Related: [`SHAPE_BALANCE.md`](SHAPE_BALANCE.md), [`SCOPE_TAG.md`](SCOPE_TAG.md),
[`conservation_check.py`](conservation_check.py).

## Geometry

```text
face      one literature: ~200 studies sharing a frame (definitions, methods, population)
edge      where two faces meet: their definitions and cut points must reconcile.
          category welds and semantic welds show up here -- the same word measuring
          different things, or one thing split under two names
vertex    3+ faces meet: triangulation; a claim held by independent frames
gap       a missing face, or an edge that does not close
```

## Procedure

```text
1 build faces        group studies by shared frame; record each face's scope tag
2 check edges        for each pair of faces: do definitions and cut points line up?
                     record every weld (same term, different measure / different term,
                     same measure)
3 anchor             pick the study (or cluster) whose denominator is closest to what the
                     whole mass must add up to -- a conservation anchor
4 work backward      fit each other study to the anchor where its scope and cut point allow;
                     the misfit is data
5 weak studies       extract the error pattern of weak studies (what they get wrong, where),
   as error data     then project that pattern across the whole mass to find where it hides
                     in stronger-looking studies
6 vertices and gaps  list where 3+ independent faces agree; list missing faces and open edges
```

## Precedents (VERIFY each)

```text
Munafo & Davey Smith 2018   "Robust research needs many lines of evidence", Nature:
                            triangulation across methods with different biases
Nuijten et al. 2016         statcheck: automated recomputation of reported statistics,
                            Behavior Research Methods -- weak-study error data at scale
Cochrane risk-of-bias tools (RoB 2; Sterne et al. 2019, BMJ): structured study-level bias
```

What this adds (PROPOSED): edges as the place where definitions must reconcile (welds), a
conservation anchor for the whole mass, and weak studies used as an error map rather than
discarded.

## Reuse

Studies scored on the same axes are shapes; [`shape_balance.py`](shape_balance.py) scores them
by balance and marks where each bulges or collapses.

## Gaps

No worked example is in this repository yet. A first test: one question with 3 faces, the welds
listed, and whether the anchor-and-backfit step changes the pooled answer.
