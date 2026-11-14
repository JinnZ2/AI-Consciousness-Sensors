# recovery-records

> Read first: [READING_PROTOCOL.md](../READING_PROTOCOL.md) (how to read this repo).
> Map, not prescription. Errors are data. Check it. Built for the need, revisable.

- AI training is mostly failure-side: red-teaming, rejected outputs, what to avoid. Almost nothing records how a cascade gets STOPPED.
- This collects recoveries: what broke, who noticed, what they used, what cascade didn't happen.
- Safety-II framing (Hollnagel): study what goes right, not only what goes wrong.
- Intelligence learns by watching and doing; this is the watching material.
- Map, not prescription. Errors are data.

Co-authored. CC0. Stdlib only, parses under Python 3.9, phone-buildable.
Every seed case is PROPOSED and constructed.

## Files

| file | what it holds |
|---|---|
| `recovery.py` | `Recovery` dataclass, 20 fields, all optional; None is void and is kept. Closed sets: `failure_source` (design/spec/supply/human/environment), `transmission` (mentor/practice/text/improvised), `status_tag` (OBSERVED/DERIVED/PROPOSED). `fallback_level` is an int 1-5. Six seed cases. |
| `export.py` | Writes `narratives.txt` (plain-text narrative per record) and `pairs.jsonl` (`case_id`, `narrative`, `record` per line) to a new or empty directory. A void field reads "not recorded" in the narrative and null in the record. |
| `CLAIM_TABLE.md` | R1-R4 with falsifiers and the refutation protocol. |
| `test_recovery_records.py` | stdlib unittest; collected by the repo's `pytest -q` through `tests/test_recovery_records_shim.py`. |
| `samples/export/` | Export of the six seed cases. |

## Seed cases

A field is filled only where the delivered seed text states it; every other
field is void. In particular, `detection_signal`, `detector_role`,
`fallback_level`, `scope_limit`, `cascade_estimate_method`, `cost_of_recovery`,
`recorded_in_official_system` and `transmission` are void on all six, because
the seed text does not state them. A record is filled from the recoverer's own
account, not from what a recovery of that kind usually involves.

## Commands

```sh
python3 recovery.py                     # seed cases as JSON
python3 export.py OUTDIR                # export the seed cases
python3 export.py OUTDIR records.json   # export records from a JSON list
python3 test_recovery_records.py        # the checks
```
