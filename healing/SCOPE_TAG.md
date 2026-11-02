# Scope tag -- every claim and summary statistic carries where it holds

STATUS: PROPOSED, co-authored (2026-11-01). CC0.
Validator: [`scope_tag.py`](scope_tag.py) (stdlib; `--selftest`, `--template`).
Shape field: [`research/shape_sufficiency_check.py`](research/shape_sufficiency_check.py).

## The tag

```text
population        who or what was measured (and n)
culture           cultural / institutional setting
environment       physical and situational setting
time period       when
method            how it was measured
SHAPE ASSUMPTION  the distribution assumed behind any average ("bell curve / additive effects")
                  and whether it was checked
LINEAGE           every transformation from the raw data to the summary, unbroken
```

Missing any field = **SCOPE-UNKNOWN**, never universal. A complete tag whose shape was not checked
is reported as "SCOPED (shape unchecked)" so the gap stays visible.

## Precedents (VERIFY each)

```text
Henrich, Heine & Norenzayan 2010   "The weirdest people in the world?" (WEIRD samples), BBS
Simons, Shoda & Lindsay 2017       constraints on generality statements, Perspectives on Psych. Science
Gergen 1973                        social psychology as history, J. Personality and Social Psychology
Brunswik 1956                      representative design
Gebru et al. 2018                  datasheets for datasets
Mitchell et al. 2019               model cards for model reporting
W3C PROV (2013)                    provenance data model
```

**Gap these leave:** they record origin (who, where, how) but rarely require the distribution
assumed behind an average. A mean reported without its shape assumption is scoped in place and
time but unscoped in form. The shape field and the shape check exist for that gap.

## Use

```sh
python3 healing/scope_tag.py --template > tag.json      # fill it
python3 healing/scope_tag.py tag.json --data values.txt # validate + run the shape check
```

Exit code 3 = SCOPE-UNKNOWN (the absence is the result).
