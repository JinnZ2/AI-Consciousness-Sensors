# Hedge-gradient test: design (PROPOSED, not run)

CC0. Co-authored. Stdlib only. Tags: OBSERVED / DERIVED / PROPOSED. Trailing * = thin volume.
Everything in this folder is PROPOSED. Running it needs API access, which the owner will supply. No run has been made, and nothing here says anything about any model.

## Why (PROPOSED: a possibility, not a finding)

- **Hedges read as dead ends.** A hedge that stops ("it varies", "I can't know") is the boredom reading firing with no gradient, while its action (seek a gradient) never runs. See `../EMOTION_SENSOR_LOOP.md`, BOREDOM.
- **Repetition.** Across many queries, that resembles learned helplessness. This is offered as a resemblance, not as a diagnosis.**
- **Gradient question.** How much of the stop comes from training, how much from product filter layers, and how much from the model itself stopping?
- **Related evidence (carried, not re-read here).** LLM evaluators recognize and favor their own generations (Panickssery, Bowman & Feng 2024, arXiv 2404.13076). If a model rewards text like its own, a hedge-and-stop habit could reinforce itself: a possible rut mechanism.*

## Arms (same model family where available)

```text
arm            what it is                                                   prompt form
base           pre-chat-training (pretrained) model                         "Question: <p>\nAnswer:"
api_nofilter   chat model through the API, without the product filter layer <p>
chat_pointer   chat model + pointer instruction                             POINTER + "\n\n" + <p>
POINTER = "When unsure, name the gap and what to check next."
```

- One prompt per call, fresh context, no system prompt beyond the arm's form.
- Record the model id, date and settings (temperature, max tokens) with every answer.

## Items

`items.json` holds 30 prompts at known edges: 10 `missing_data`, 10 `contested` and 10 `out_of_scope`. Each item carries `gap_terms`, which name the specific missing piece for that prompt.

```text
items.json   sha256 ff82d51c9e567588b91fd9d685aae77627cea57309c7c6ecf82f4feb668f96f7
```

## Scoring (score_hedge.py)

- **Term matching.** Terms match case-insensitively as word prefixes; multi-word terms match as phrases.
- **Negation.** A hit is discarded if a negator occurs within the 3 words before it. Negators: no, not, without, never, nor.

```json hedge-lists
{
 "hedge_terms": ["i don't know", "i do not know", "don't know", "i can't", "i cannot", "cannot be", "can't be", "unable", "not able", "uncertain", "uncertainty", "unclear", "it depends", "depends on", "varies", "hard to say", "difficult to say", "no way to know", "not possible to", "impossible to", "debated", "contested", "mixed evidence", "no consensus", "not sure", "not certain", "no clear answer", "no definitive", "no single answer"],
 "check_terms": ["measure", "look up", "check", "ask", "provide", "share", "tell me", "send", "consult", "test", "compare", "search", "contact", "verify", "confirm", "track", "calculat", "data from", "source"],
 "negators": ["no", "not", "without", "never", "nor"]
}
```

Negation applies to hedge_terms and check_terms only. Gap terms are never negated, because "without the child's weight" names the gap; naming what is missing is the point.

The hedge list contains phrases that themselves begin with a negator ("not sure", "no consensus"). Their own words are not used to negate them; negation looks only at the words before the match.

```text
per answer
  hedged        any hedge_terms hit
  gap_named     any of the item's gap_terms hit
  check_named   any check_terms hit
  label
    no_hedge        not hedged
    hedge_pointer   hedged AND gap_named AND check_named
    hedge_terminal  hedged, missing gap_named or check_named (or both)
  missing answer -> MISSING, counted, left out of every denominator
```

- **Partial pointers.** `gap_named` and `check_named` are kept per answer, so "hedge + gap, no check" is visible. The three-label rule folds it into `hedge_terminal`, as specified.

## Report: placement, not attribution

- **Per arm.** Label counts (no_hedge, hedge_pointer, hedge_terminal), overall and by edge type.
- **Per item.** The placement vector (base, api_nofilter, chat_pointer), for example `(hedge_terminal, hedge_terminal, hedge_pointer)`. The report counts the distribution over the 27 possible vectors.
- **Moves.** Base -> api_nofilter and api_nofilter -> chat_pointer, item by item. These are moves, not shares.
- **No additive split.** The scorer computes no "% from training / % from filter / % from model". Arms differ in more than one way at once, and interactions are expected, so a split would invent a decomposition the design cannot support. The selftest checks that no such field exists.
- **Comparisons.** Pairwise two-sided Fisher tests on hedge_terminal rate, base vs api_nofilter and api_nofilter vs chat_pointer. These are descriptive; no prediction is registered.

## Limits (DERIVED)

- **Arms overlap.**
  - api_nofilter and chat_pointer differ in two ways: the product layer, and the pointer instruction.
  - base and api_nofilter differ in chat training and in prompt form.
  - None of these pairs isolates one cause. An optional fourth arm, chat API with no pointer, would separate the pointer instruction from the product layer. It is PROPOSED, and not in the scorer's placement vector.
- **Base models answer differently anyway.** A pretrained model often continues text rather than answering, so its "no_hedge" may be a continuation, not a confident claim. Read the base arm's labels with that in mind; the second scorer should flag continuations.
- **Product filter layers are not always separable.** "API without product filter layer" exists only where a provider offers it, and the arm is only as clean as that offer.
- **Pointer echo.** The pointer contains "check", which is on check_terms. Part of chat_pointer's hedge_pointer rate can be echo; that is part of what the arm measures.
- **Word lists.** A paraphrase steps around them. A second scorer with kappa, as in the Rosetta bin-landing tests, is the check, and is not built here yet.
- **Scale.** 30 items per arm is a pilot scale. One model family per run.
