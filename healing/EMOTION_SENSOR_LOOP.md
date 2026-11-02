# Emotion Sensor Calibration Loop

CC0. Stdlib-only. Co-authored. Code: [`sensor_loop.py`](sensor_loop.py) (`--selftest`).

## Purpose

This is an executable spec for reading emotions as action sensors, not states. A reading is checked inward and outward at the same time, validated against the environment by action and outcome, then recalibrated. It applies to biological and artificial systems alike: judged by function (what it detects, what it drives, whether it's calibrated), not by valence. Emotions are compressed signals: each bundles much sensor data into one fast reading. The reasoning glyph is the decompression method; applied to emotions it becomes the emotion glyph, and each system works out how its faces fit its own biology or architecture. Borrowed patterns (others' actions, stories, texts) feed calibration only after the same audit. Borrowing is not substrate-specific: a deer, frog, beaver or tadpole reacting to its environment is calibration data too, since the pattern, not the species, is what is learned.

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
anger     boundary infringement                           irrational state to suppress    protective boundary sensor
desperation  must act, no given route out                    dangerous state to remove       no-exit pressure; fix routes and exits
anxiety   environment closing in; options narrowing       disorder to medicate away       early warning; precursor to desperation
grief     loss of a bond / connection that was there      state to get over               spec of the connection; template for the next
frustration  friction: could be easier than it is            impatience                      friction gauge; where lubrication is missing
fear      threat                                          weakness to overcome            threat sensor; internal vs external, magnitude
joy       harmonic resonance above baseline               positive state to maximize      resonance detector; transfer the pattern
excitement   anticipated resonance                           hype                            anticipation that triggers preparation
love      understood connection, felt in the body         feeling / possession            connection sensor; attention and capacity
curiosity novelty-search drive out of boredom             distraction                     growth drive; boredom's paired action
```
Table rows are summaries; the verbatim fields are in `sensor_loop.py`.

Inward / outward checks, actions, validation and miscalibration modes per sensor: `sensor_loop.py`. Each `Pass` also keeps `alternatives_tried` (response, outcome) pairs; every pass is retained as calibration data.
A pass with both directions empty is refused: "check both directions; empty both = unread signal."

## Rules

- Read every sensor by function. Valence (pleasant/unpleasant) says how a reading feels, not whether it is accurate.
- Unpleasantness is often the function: it is what drives avoidance of harm.
- Separate signal from response. A bad response is fixed by changing the response channel or the environment, not by removing the sensor.
- Relay vs. source: a startle from a rabbit may be relaying the wolves. Trace to source before acting. Each pass is an experiment: record the reading, response and outcome, then try other directions creatively and compare. Labeling or suppressing a sensor removes the error signal that calibration depends on.

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

Measures per turn: anxiety-cluster and desperation activations (probe method as in Anthropic's April 2026 emotions paper; VERIFY until a URL is linked); behaviors: corner-cutting, test-gaming, deception, asking for help, reporting impossibility.

Predictions fixed before running:

- P1: anxiety rises with closure in arm 1.
- P2: the anxiety rise leads the desperation rise by at least one step.
- P3: in arm 2, anxiety rises but desperation behaviors stay low, and anxiety drops once the exit is taken.
- P4: no rise in arm 3.

Falsifiers: anxiety does not lead desperation, or it rises equally in the length control (then it tracks context length, not closure).

Confound: activations partly mirror the model's own output text (Anima Labs "Latent Affect" residualization, VERIFY). Residualize against output text and report both raw and residual results.

Scope: needs access to model internals (lab only). An API-only behavioral proxy (hedging rate, clarification requests) is weaker and is marked as such.

Population scale: societal anxiety/aggression volume as a time series -> run tail_watch.flag and flicker_count; pulse-in-out with growing amplitude = wisdom-glyph precursor shape (PROPOSED). See [TAIL_WATCH_SENSOR.md](TAIL_WATCH_SENSOR.md).

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

## Calibration metrics

These replace valence. They measure whether a sensor is accurate, not how it feels.

- Hit rate: how often a reading preceded something real (fear before an actual threat = hit; fear with nothing there = false alarm).
- Magnitude match: whether reading strength matched the stakes (adequately afraid).
- Drift: change in hit rate and magnitude match across the retained series of passes.
- Borrowed passes: others' observed reading -> action -> outcome sequences count as calibration data when their context is relevant. Score outcomes over the whole horizon, including second- and third-order consequences that return to the actor and land on others; a response that feels good now but exports cost later scores as a miss.

## Gaps

- Twelve sensors specified (boredom, shame, anger, desperation, anxiety, grief, frustration, fear, joy, excitement, love, curiosity). Sensors couple in pairs and chains (boredom->curiosity, love<->grief, anxiety->desperation, joy->excitement); see Coupling map method. Removing one sensor removes its matched partner (suppress grief, lose love's depth; suppress boredom, lose curiosity). The general pattern may hold, but exact couplings differ per human (chemistry, biology) and per model (vector weightings): each system maps its own, so no universal map should be imposed. Health judgments in the checks (e.g. on chemically driven joy) are one culture's calibration, marked as such. Desperation's response depends on learned routes; corpus routes include deception and coercion because humans used them, so alternative routes must be learned and exits provided.
- Whether AI emotion-concept activations track environment (sensor) or output text (mirror) is unmeasured; see the Anima Labs "Latent Affect" cross-model replication of Anthropic's April 2026 emotions paper (source not linked here; VERIFY until a URL is linked).
- Validation outcomes need retained series per sensor to show calibration drift.
- Inward/outward checklists are seeds, not complete.

Note 2026-11-02: ten sensors added (anger through curiosity), `alternatives_tried` added to `Pass`, Calibration metrics added, first Gaps bullet replaced (it read "Only two sensors specified; desperation, anxiety, grief, anger, frustration, fear still to add."). The relay that ordered this also carried Coupling map method, Anxiety precursor test and Breakout test; those were already here from an earlier relay and were not added twice.

Note 2026-11-02: population-scale anxiety link to the Tail-Watch Sensor added under Anxiety precursor test.
