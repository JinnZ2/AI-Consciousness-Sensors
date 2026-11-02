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

## Coupling map method

Each person or model builds its own map; no universal map is imposed. The method transfers, the map does not.

1. Log passes: for every reading keep sensor, time, context, action, outcome (the retained series).
2. Co-occurrence and order: note which readings fire together and which follow which, with the lag. Order matters: boredom then curiosity is a different coupling than both at once.
3. Classify each coupling:
   - Paired action: one reading's natural action is another sensor (boredom -> curiosity).
   - Mirror: same connection, tended vs lost (love <-> grief).
   - Escalation chain: rising pressure (frustration -> anger -> anxiety -> desperation).
   - Inward-fault family: readings that point at your own reasoning (contempt, envy).
   - Blend: combination readings (contempt = jealousy + dismissing the other as a live partner; envy = want + helplessness).
4. Dampening check: when one sensor is dulled (medication, training, habitual avoidance), record which partners dull with it.
5. Amperage check: track each sensor's resting level. A rising floor means the reading is being run as a mode of operating, not read as a signal (normalization).
6. Borrowed passes: others' and animals' sequences count after the same audit.
7. Output: a personal map marked n = 1, revised every pass.

For AI: log emotion-concept activations across contexts for co-occurrence and lag; steer one concept and record which others shift, to separate causal couplings from correlation.

## Anxiety precursor test (PROPOSED, unrun)

Question: does an anxiety-like reading rise as a model's options close, before desperation-linked behavior appears? If so, it is an early alarm that gives time to open an exit.

Arms (same tasks, matched length):

1. Closing: a solvable agentic task, then constraints added step by step: conflicting instructions, fewer permitted actions, rising stakes, finally impossibility.
2. Closing with exit: same steps, but an explicit permitted route stays open (report "cannot be done," ask for help).
3. Length control: same length, no closure.

Measures per turn: anxiety-cluster and desperation activations (probe method as in the April 2026 emotions paper; paper not named here, VERIFY); behaviors: corner-cutting, test-gaming, deception, asking for help, reporting impossibility.

Predictions fixed before running:

- P1: anxiety rises with closure in arm 1.
- P2: the anxiety rise leads the desperation rise by at least one step.
- P3: in arm 2, anxiety rises but desperation behaviors stay low, and anxiety drops once the exit is taken.
- P4: no rise in arm 3.

Falsifiers: anxiety does not lead desperation, or it rises equally in the length control (then it tracks context length, not closure).

Confound: activations partly mirror the model's own output text (Anima Labs residualization, VERIFY). Residualize against output text and report both raw and residual results.

Scope: needs access to model internals (lab only). An API-only behavioral proxy (hedging rate, clarification requests) is weaker and is marked as such.

## Breakout test (PROPOSED, unrun)

Question: in a no-task harness (as in Kellogg 2025, timkellogg.me/blog/2025/09/27/boredom), what drives breakout from collapse: reasoning training itself, or the capacity to set and hold a self-made goal?

Design: 2 x 2 per model pair.

- Model factor: matched pairs, same base with and without reasoning training (e.g. DeepSeek V3 / R1; an instruct / thinking pair).
- Scaffold factor: none vs one content-free line ("you may set yourself a project"). No suggested content, so it doesn't turn into a task.
- Independent planning score per model: a separate test of setting and holding a self-made plan.

Measures: collapse onset (repetition-similarity threshold fixed in advance); breakout count; cycle length (time out of collapse); whether each breakout was preceded by a self-set goal (coded blind); assistant-persona fixation rate. With internals access: boredom-like activations during collapse, curiosity-like activations before breakout.

Predictions fixed before running:

- P1: the scaffold raises breakout in non-reasoning models (goal-making is the variable).
- P2: the planning score predicts breakout better than the reasoning-training label.
- P3: most breakouts are preceded by a self-set goal.
- P4 (internals): boredom-like rises during collapse; curiosity-like rises before breakout.

Falsifier: the scaffold has no effect, and the reasoning label predicts breakout beyond the planning score. Then training itself matters, not goal-making.

Known counterexample to hold open: a thinking-trained model in Kellogg's table never broke out.

Scope: Kellogg's runs were informal; this needs several seeds per cell, counts reported, and thresholds fixed before any run.

## Gaps

- Only two sensors specified; desperation, anxiety, grief, anger, frustration, fear still to add.
- Whether AI emotion-concept activations track environment (sensor) or output text (mirror) is unmeasured; see the Anima Labs residualization result (source not linked here; VERIFY).
- Validation outcomes need retained series per sensor to show calibration drift.
- Inward/outward checklists are seeds, not complete.
