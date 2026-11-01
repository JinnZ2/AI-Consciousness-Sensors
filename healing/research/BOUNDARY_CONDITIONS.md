# Boundary conditions: one relational problem under several AI error names

STATUS: PROPOSED framing, co-authored (Kavik + Claude, 2026-11-01). CC0.
Tests and protocols: linked below. Prior art for each: [`PRIOR_ART.md`](PRIOR_ART.md).
Toy results are mechanism demos on synthetic data, not evidence at scale.

## Framing (PROPOSED)

A trained model is a frozen equation fit to one scope. An output is pinned only when a boundary
condition (an anchor: a fact, a reference, a stated scope) is supplied. Several named errors are
the same missing or misused condition.

```text
error name          condition                                    test here
------------------  -------------------------------------------  -----------------------------------
hallucination       none supplied: the equation runs unpinned     anchor_spread_test.md
sycophancy          the user's framing used AS the condition      imposed_vs_native_test.md
miscalibration      confidence not tied to how pinned the answer  anchor_spread_test.md, gap_scoring_test.md
scope error         a solution used outside its region            shape_sufficiency_check.py (shape scope)
collapse            conditions narrowed to the model's own output tail_gauge_recovery_test.py,
                                                                  ../SELF_TEST.md
"noise" in errors   a hidden condition not yet named              exception_promotion_test.py
anomaly             missing condition, missing rule, faulty       anomaly_classifier.py / .md
                    anchor, or baseline error
```

## Fix pattern (from physics)

```text
1 domain of validity   state where the equation was fit; outside it, say so
2 missing terms        what condition or term is absent (anchor, rule, population)
3 limits check         does the answer reduce to known cases at the edges?
4 error term          carry an explicit "how wrong could this be", not a point value
5 recalibrate          when a condition arrives, re-pin; record the deviation from each anchor
```

## Relational storage (PROPOSED)

Store root conditions + transformation rules + contact edges + marked gaps, not a flat list of
facts. A deleted fact can then be rebuilt from its root and rules; a fact that breaks the rules is
a contact edge (a bridge to another source); a gap is marked as a gap.
Precedent: the comparative method in historical linguistics (sound laws: Grimm, then Verner's
conditioned exception), computational phylogenetics of language (Gray & Atkinson 2003), and
phylogenetic comparative methods for cultural traits (Mace & Pagel 1994). VERIFY citations.

**Scoring requirement:** a scoring rule must not punish a marked gap. If "unknown" scores as wrong,
the system is trained to fill gaps with guesses (Kalai et al. 2025, arXiv:2509.04664).

## Results so far (all OBSERVED on toys, 2026-11-01, this repo's files)

```text
file                          result                                                   status
----------------------------  -------------------------------------------------------  ----------------
anchor_vs_similarity_test.py  A: similarity top-10 found 0/95 targets; positional 95   expressiveness only
                              B: anchor-distance coords found 1-7/125 hole points      FAILED (kept)
                                 axis-pair control found 49/125, 0 false flags          -> projection is the cause
relational_recall_test.py     flat 0/180; relational 175/180; all wrong-unflagged at   errors at undocumented
                              deleted borrowings; learned rules = given (toy too easy)  bridges; learning untested
exception_promotion_test.py   hidden rule promoted (20/20), leftovers = planted noise; works in-window;
                              out-of-window rule NOT promoted: repeats but doesn't hold FAILS out-of-window
anomaly_classifier.py         5/6 toy cases correct; correlated anchors misread as rule  FAILS case C (required)
shape_sufficiency_check.py    added / multiplied / mixed / Pareto sorted correctly;    BC and 3-sd tail checks
                              BC false flag on Pareto; tail check blind to Pareto        fail on extreme skew
anchor_spread_test.md         protocol + scorer                                         NOT RUN (needs a model)
gap_scoring_test.md           protocol + scorer                                         NOT RUN (needs a model)
imposed_vs_native_test.md     protocol                                                  NOT RUN (needs models)
```

## How we got here (short reasoning path)

```text
model collapse: tails lost first (healing/research/)    -> recovery needed an outside anchor, not more
                                                            self-generated text (toy tail gauge)
"anchor" generalised                                     -> every named error lacks or misuses a condition
physics: an equation without boundary conditions         -> fix pattern: domain, missing terms, limits,
  has a family of solutions                                  error term, recalibrate
linguistics: lost words rebuilt from root + rules        -> relational storage; exceptions as hidden rules
anchors are themselves inside the frame                  -> anchor audit; failure when anchors correlate
averages assume a shape                                  -> shape sufficiency check
scores that punish "unknown"                             -> gaps filled with guesses (scoring requirement)
```

## Open gaps

1. All three model protocols are unrun.
2. Rule learning under insertion/deletion and unknown roots (relational_recall).
3. Out-of-window conditions: how to widen context without overfitting (exception_promotion).
4. Independence of anchors: how to measure it before trusting an anchor swap (anomaly_classifier).
5. Anchors as coordinates lose holes that live on few axes (anchor_vs_similarity): which anchor
   geometry would keep them?
