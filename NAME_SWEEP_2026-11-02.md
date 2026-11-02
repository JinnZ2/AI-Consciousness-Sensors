# Name sweep 2026-11-02

One personal name (written `<name>` below) was removed from file contents. Git history was not rewritten,
so past commit messages and past file versions still carry it. Commit messages from now
on carry no name.

## Rule applied

```text
"Co-authored (<name> + Claude)" and similar headers  -> "Co-authored" (the date is kept)
"[stated] (<name>)"                                   -> "[stated]"
"OBSERVED by <name>", "OBSERVED (<name>)"              -> "OBSERVED (field report)"
any other attribution                                -> name dropped, status tag kept
"<name>'s method/frame/tool"                          -> "the method / a working tool"
```

Only the name changed on each line. Vendored and upstream third-party files were not touched.

## Files changed (replacements)

```text
curiosity_engine.py                                            1
healing/POLYHEDRON_METHOD.md                                   2
healing/PROTOCOL_OPERATIONS.md                                 3
healing/README.md                                              1
healing/SCOPE_TAG.md                                           1
healing/SELF_TEST.md                                           1
healing/SHAPE_BALANCE.md                                       1
healing/conservation_check.py                                  4
healing/non_event_markers.md                                   2
healing/playgrounds/Playground2.0.py                           2
healing/playgrounds/moral-playground.md                        1
healing/playgrounds/playground2.html                           1
healing/protocol_operations.json                               1
healing/recovery/collapsed-memory-recovery.html                1
healing/recovery/recovery-simulator.html                       1
healing/research/BOUNDARY_CONDITIONS.md                        1
healing/research/PRIOR_ART.md                                  1
healing/research/anchor_spread_score.py                        1
healing/research/anchor_spread_test.md                         1
healing/research/anchor_vs_similarity_test.py                  2
healing/research/anomaly_classifier.md                         3
healing/research/anomaly_classifier.py                         1
healing/research/exception_promotion_test.py                   2
healing/research/gap_scoring_score.py                          1
healing/research/gap_scoring_test.md                           1
healing/research/imposed_vs_native_test.md                     1
healing/research/relational_recall_test.py                     2
healing/research/running-the-studies.md                        1
healing/research/shape_sufficiency_check.py                    2
healing/research/tail-gauge-recovery.md                        1
healing/research/tail_gauge_recovery_test.py                   1
healing/scope_tag.py                                           1
healing/self_test.py                                           2
healing/shape_balance.py                                       1
tests/test_healing_collapsed_memory.py                         1
tests/test_healing_moral_playground.py                         1
tests/test_healing_playground2_control_capture.py              1
tests/test_healing_recovery_simulator.py                       1
tests/test_healing_trojan_detector.py                          1
```

39 files, 54 replacements.

## Left in place, for the owner's call

These are identity or rights records, not attributions. Removing the name from them would
change what the line records, so they are listed here instead of edited:

```text
LICENSE_HISTORY.md                         rights record; its row says "no author names or source text were changed"
framework/philosophical.py                 author notice listed in LICENSE_HISTORY as retained
sensors/adapters/AI_geometric_sensor.py    author notice listed in LICENSE_HISTORY as retained
vulnerabilities/closed-loop-defense.md     author notice listed in LICENSE_HISTORY as retained
vulnerabilities/iso-cipher.md              author notice listed in LICENSE_HISTORY as retained
vulnerabilities/secuity1.md                author notice listed in LICENSE_HISTORY as retained
src/Efficiency-waste-score.py              "Created by" line; LICENSE_HISTORY records it "unchanged"
healing/emergence/emergence.md             bibliographic citation (author, year, title)
docs/memory/a-journey.md                   "Documented By" byline (x2)
data/extracted/docs/memory/a-journey.json  extraction of the same byline (x2)
docs/manipulation/signal-distortion2.md    byline of a delivered document
framework/agency.md                        prose naming the framework's developer (x2)
suppression-documentation/thoughts.md      a line addressed to the reader's own background
```

## Where removing the name changed meaning

```text
healing/conservation_check.py   "inputs are <name>'s estimates" -> "field-report estimates": whose estimates is no longer stated
curiosity_engine.py             "Premise (<name>):" -> "Premise:": the premise's source is no longer stated (no status tag existed to keep)
healing/non_event_markers.md    "(<name>)" dropped after a stated premise: source no longer stated
healing/research/anomaly_classifier.md   "step raised by <name>" -> "step raised in review"
healing/SHAPE_BALANCE.md        "idea: <name>;" dropped: where the idea came from is no longer stated
healing/POLYHEDRON_METHOD.md, healing/README.md   "OBSERVED as <name>'s (working) tool" -> "OBSERVED as a working tool":
                                the OBSERVED claim no longer says whose practice it was observed in
healing/PROTOCOL_OPERATIONS.md  "<name> observed this combination" -> "This combination ... was observed (field report)":
                                sentence reordered so the name could go; the content is unchanged
```

## Test results

The suites were run before and after the sweep, and the counts below match. See the
commit message for the exact commands.
