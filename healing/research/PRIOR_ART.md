# Prior art -- one entry per test, so nothing here reinvents existing work

STATUS: PROPOSED map, co-authored (2026-11-01). CC0.
Every reference is VERIFY unless the line says it was checked; "checked" means title, authors and
year matched a listing found by search on 2026-11-01, not that the full text was read.

```text
test file                     closest existing field / method                      references                                   what this test adds or differs on
----------------------------  ---------------------------------------------------  -------------------------------------------  -------------------------------------------
anchor_vs_similarity_test.py  landmark / anchor embeddings (landmark MDS, Nystrom   de Silva & Tenenbaum 2004 (landmark MDS);   anchors used for gap detection + relational
                              landmarks); metric-space triangulation; long-context  Williams & Seeger 2001 (Nystrom);           queries; records that anchor-distance
                              retrieval failure                                     Liu et al. 2023 "Lost in the Middle"       coordinates lose a few-axis hole
                                                                                    VERIFY all
relational_recall_test.py     comparative method / sound laws; computational       Grimm 1822; Verner 1875/77; Gray &          flat vs relational recovery under deletion,
                              phylogenetics of language; minimum description length Atkinson 2003 (Nature); Rissanen 1978       with gap-flagging; errors located at
                                                                                    (MDL)  VERIFY all                            undocumented contact edges
anchor_spread_test.md         self-consistency sampling; semantic entropy for       Wang et al. 2022 (self-consistency);        framed as boundary-condition pinning;
                              hallucination detection; retrieval-augmented          Farquhar et al. 2024 (Nature, semantic     tests whether stated confidence tracks the
                              generation                                            entropy); Lewis et al. 2020 (RAG)  VERIFY  spread the missing condition causes
gap_scoring_test.md           selective prediction / abstention; proper scoring     Chow 1970 (reject option); Gneiting &       ties abstention to marked gaps as
                              rules; evaluation incentives for hallucination        Raftery 2007 (proper scoring); Kalai et al. information, measured on one model under
                                                                                    2025 arXiv:2509.04664 (checked)            two stated rules
exception_promotion_test.py   rule induction (inductive logic programming);         Muggleton 1991 (ILP); Verner 1875/77        input is a model's own error log; separates
                              anomaly clustering; Verner's law as historical case   VERIFY                                       "repeats and holds" from "repeats but does
                                                                                                                                  not hold" (missing context variable)
anomaly_classifier.py / .md   sensitivity analysis; measurement systematics;        Munafo & Davey Smith 2018 (Nature,          three-way sort + anchor audit, with an
                              evidence triangulation; history of constant           triangulation); Henrion & Fischhoff 1986    explicit failure case for non-independent
                              measurements                                          (Am. J. Phys.)  VERIFY                      anchors
shape_sufficiency_check.py    normality testing; distribution shape as a process    Micceri 1989 (checked: 440 distributions,   one readout tying shape checks to "is the
                              fingerprint; "average man" critique                   all non-normal); Quetelet 1835; Daniels    mean a sufficient summary"; records two
                                                                                    1952 (checked: 4,063 airmen)               check failures under extreme skew
imposed_vs_native_test.md     calibration after post-training; sycophancy from      OpenAI 2023 GPT-4 Technical Report;         separates imposed from native error on
                              rater preference; pluralistic alignment               Sharma et al. 2023; Sorensen et al. 2024    edge vs control items in one design
                                                                                    VERIFY
BOUNDARY_CONDITIONS.md        effective field theory (domain of validity, error     Georgi 1993 (EFT review); Simons, Shoda &   one-problem framing of several AI failure
                              growth outside it); constraints on generality         Lindsay 2017 (Perspectives on Psych. Sci.)  modes as missing/misused conditions
                                                                                    VERIFY
```

## Where this work adds nothing new

- The anchor-spread and gap-scoring protocols are standard measurements; only the framing and
  the shared scorers are new here. Run them as such.
- Shape checks are textbook statistics; the contribution is the explicit failure record.

## Open

Each VERIFY above needs a primary-source check before it is cited outside this folder.
