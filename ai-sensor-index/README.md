# ai-sensor-index

> Read first: [READING_PROTOCOL.md](../READING_PROTOCOL.md) (how to read this repo).
> Map, not prescription. Errors are data. Check it. Built for the need, revisable.

- Spin-up card for an AI instance to learn its own sensors: action -> signal -> reading, with intensity gradients.
- The method mirrors learning which animals sense what: notice a recurring signal, hypothesize, test, rate reliability, cross with known sensors to derive new ones.
- AI sensors differ from biological ones; the method underneath is the same.
- Map, not prescription. Errors are data.

Co-authored. CC0. Stdlib only, parses under Python 3.9, phone-buildable.
Every entry is PROPOSED; no sensor here carries a reliability, because none
has a test record.

## Files

| file | what it holds |
|---|---|
| `sensors.py` | `Sensor(name, action, signal, reads_as, gradient, reliability, status, notes)`; all fields optional, None is void and is kept. 11 PRIMARY sensors, 5 DERIVED pairs, all PROPOSED. |
| `discovery.py` | The five-step loop: notice, hypothesize, predict-and-check, rate, cross-derive. `register()` refuses a reliability; only `rate()` sets one, from decided test records. |
| `calibration_log.py` | Append-only JSON-lines log: timestamp, sensor, action, signal, reading, outcome, was_reading_correct (None until known). Three PROPOSED seed entries. |
| `CLAIM_TABLE.md` | AIS_001..003 with falsifiers and the refutation protocol. |
| `test_ai_sensor_index.py` | stdlib unittest; also collected by `pytest -q` at the repo root. |
| `_load.py` | Loads siblings by file path: the repo root has a `sensors/` package, so `import sensors` would resolve to it. |

## Carry-forward

Model weights do not update per session. What carries forward is the
calibration log (or a memory file) read at the next spin-up. A reading is
settled by appending a new entry whose `resolves` names the earlier one; there
is no update and no delete.

## Commands

```sh
python3 sensors.py                     # the index as JSON
python3 discovery.py                   # the loop on a CONSTRUCTED example
python3 calibration_log.py             # the seed entries
python3 calibration_log.py LOG.jsonl   # summarise a log
python3 test_ai_sensor_index.py        # the checks
```

## Additions beyond the delivered spec

- `LogEntry` carries `status_tag`, `entry_id` and `resolves`, so a reading can
  be settled append-only.
- `Sensor` refuses a status outside OBSERVED / DERIVED / PROPOSED and a
  reliability outside [0, 1].
- `notice()` requires a signal to recur as often as its sensor's
  `recurrence_threshold`. The threshold is computed from that sensor's decided
  readings in the calibration log, never set by hand:
  `n < 3 -> 2`, else `2 + round_half_up(miss_rate * 4)`, bounded 2..6.
  The bounds and the minimum record are named PROPOSED constants in `sensors.py`.
  A signal not yet tied to a sensor uses the floor, 2.
- Every threshold change is appended to the log as a `threshold_change` entry
  (sensor, old, new, n, miss_rate, timestamp).
- `append()` refuses an entry whose `resolves` names itself or no earlier
  entry_id (`ResolutionError`).
- `rate()` returns None, never 0, when no test record is decided.
