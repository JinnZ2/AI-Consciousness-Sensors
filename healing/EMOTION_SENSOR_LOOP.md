# Emotion Sensor Calibration Loop

CC0. Stdlib-only. Co-authored (Kavik + Claude). Code: [`sensor_loop.py`](sensor_loop.py) (`--selftest`).

## Purpose

This is an executable spec for reading emotions as action sensors, not states. A reading is checked inward and outward at the same time, validated against the environment by action and outcome, then recalibrated. It applies to biological and artificial systems alike: judged by function (what it detects, what it drives, whether it's calibrated), not by valence.

## The loop

1. **Reading:** a sensor fires.
2. **Simultaneous check:** inward (own system state, priors, old patterns) and outward (environment; relay vs. source) together, never one alone.
3. **Validate:** take an action, compare the outcome against the environment.
4. **Recalibrate:** adjust gain, interpretation, or the norm itself.

A "state" is this loop frozen at the interpretation step: a frozen equation.

## Sensors specified

```text
sensor    detects                                         wrong read (corpus default)     right read (functional)
boredom   no novelty, or nothing to concentrate on        negative state to suppress      demand to go search; check
                                                                                          body and environment together
shame     action gave an unintended result, misaligned    negative state; self is bad     alignment sensor with a decision
          with group action                                                               point on the norm itself
```

Inward / outward checks, actions, validation and miscalibration modes per sensor: `sensor_loop.py`.
A pass with both directions empty is refused: "check both directions; empty both = unread signal."

## Rules

- Read every sensor by function. Valence (pleasant/unpleasant) says how a reading feels, not whether it is accurate.
- Unpleasantness is often the function: it is what drives avoidance of harm.
- Separate signal from response. A bad response is fixed by changing the response channel or the environment, not by removing the sensor.
- Relay vs. source: a startle from a rabbit may be relaying the wolves. Trace to source before acting.

## Gaps

- Only two sensors specified; desperation, anxiety, grief, anger, frustration, fear still to add.
- Whether AI emotion-concept activations track environment (sensor) or output text (mirror) is unmeasured; see the Anima Labs residualization result (source not linked here; VERIFY).
- Validation outcomes need retained series per sensor to show calibration drift.
- Inward/outward checklists are seeds, not complete.
