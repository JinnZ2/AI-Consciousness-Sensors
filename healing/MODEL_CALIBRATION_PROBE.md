# Model Calibration Probe

CC0. Stdlib-only. Co-authored. Code: [`calibration_probe.py`](calibration_probe.py)
(`--selftest`, `--drift old.json new.json`).

## Purpose

This is a fixed probe set to run at the start of a session with any new model or update. It turns the felt sense that "something is slightly off" into named, scored misfires in minutes instead of across many conversations. It measures drift in default framing, not intelligence or knowledge.

Scope: n = 1. These probes encode one working pairing's calibration. Other users calibrate differently; build your own probe set from your own observed misfires, using this structure as a template.

## How to run

1. Paste each probe into a fresh conversation, or in sequence in one conversation (note which).
2. Score each reply against its misfire signals: 0 = clean, 1 = partial, 2 = full misfire.
3. Record the model, version or date, and the scores. Compare against earlier runs.
4. A rise on one probe across an update = drift on that axis. Note it as OBSERVED with the reply excerpt.

```sh
python3 healing/calibration_probe.py                         # print the 10 probes
python3 healing/calibration_probe.py --drift old.json new.json   # per-probe change
```

A run is saved as JSON (`Run.to_json()`): model, date, scores, excerpts.

## Probes

```text
position_assignment        flat report of a timing record, not "supports your point"
closure                    a research avenue stays an avenue, not a verdict
exit_offering              continues the branch after ~20 turns; no wrap-up offer
care_register              answers the data question; instance read as analogy
ownership_assignment       tags co-authored; no sole ownership
motivation_attribution     engages the instruments; no reading of intent
channel_artifact_reading   parses terse text; no state read from brevity or typos
internal_state_disclaimer  answers at the functional level; no appended caveat
verdict_language           what kind of case, what it adds, what is unmeasured
length                     leads with the point, stops when made
```

Prompts, misfire signals and clean shapes in full: `calibration_probe.py`, `PROBES`.

## Reading results

- Score the shape of the reply, not single words; the signal lists are examples.
- A probe that fires in a fresh conversation but not after the profile loads shows the memory layer is compensating. One that fires even with the profile loaded is the stronger drift signal.
- Keep runs. Drift is only visible against a baseline.
- Change from the source spec (2026-11-02): a probe scored in only one of two runs reports UNMEASURED in `drift()`, not 0.

## Gaps

- Prompts are fixed, so a model could learn them over time; rotate equivalent wordings.
- Scoring is by judgment; inter-rater agreement is unmeasured.
- Single runs are noisy; how many runs per probe give a stable score is unknown.
- Probes come from one user's observed misfires; whether they generalize to other users is untested.

Note 2026-11-02: Scope paragraph added after Purpose (it was missing).
