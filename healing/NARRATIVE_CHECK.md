# Narrative Structure Check for AI

CC0. Stdlib-only. Co-authored (Kavik + Claude). Code: [`narrative_check.py`](narrative_check.py)
(`--markers`, `--selftest`).

## Purpose

This is an instrument an AI can run on any pitch, video transcript, article or its own draft response. It flags structural moves that narratives use, whatever the topic and whichever side. It reports the **structure**. It does not rule on whether any claim is true or on any side's position. A flag means "check this part separately," not "this is false."

## Origin case

An interview-channel speaker strung together: the US as the world's only breadbasket (false), the last armed society before one world government (false), deer so scarce in the Depression that a sighting made national news (timing misplaced: the low point came earlier, from market hunting), and "90 days without power kills 25–50%" (a modeled worst case repeated as if measured; the Puerto Rico Maria record is about 0.1%). One true piece carried the rest: most people can't survive off the land. Then came the special-knowledge claim and the ask to follow.

## Markers

```text
stakes_inflation       stakes raised to survival level before evidence
true_carrier           one true claim placed so trust transfers to unverified neighbours
provenance_stripped    numbers or facts without source, method or scope
model_as_measurement   a projection or worst case stated as observed
unstated_bridge        the conclusion needs a step the text never states
causal_timing          an effect pinned on a cause that came after it
counter_case_omitted   known cases that went the other way left out
special_knowledge      the speaker claims to see what the population cannot
in_out_group           listeners sorted into those who get it and those who don't
homogeneity_push       differing knowledge framed as threat, not resource
join_ask               the structure ends in follow / buy / join / subscribe
```

Each marker carries its question, observable signal and the case where the flag is innocent:
`python3 healing/narrative_check.py --markers`. Each flag carries a status: OBSERVED (in text),
DERIVED (inferred from structure) or PROPOSED.

## Rules for the AI using it

- Report structure flat: which markers fired, the excerpt, and the status tag. No verdict on the speaker's side or motives.
- Run it on every side the same way. If it only fires on one camp, check whether the instrument or the sampling is skewed.
- Kept branches distinct: "unsourced" is not "false"; "counter-case omitted" is not "conclusion wrong."
- **Inward turn:** run it on your own draft before sending. AI training corpora carry these same moves, and fluent confident output looks like authority.
- Tell the user what fired and what to check, then hand the checking back to them.

## Gaps

- No validated weights: which marker combinations actually predict false or harmful content is unmeasured.
- Detection here is manual or by the model's judgment; a keyword matcher would misfire badly on irony and quotation.
- False-positive rates by genre (news, academic, marketing, oral teaching) are unknown.
- Whether telling users about flags improves their own checking or just shifts trust onto the AI is unmeasured.
