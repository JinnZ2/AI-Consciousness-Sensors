# hedge_gradient (PROPOSED design, not run)

CC0. Co-authored. Stdlib only.

When a model hedges, does the hedge stop there, or does it name the gap and a next check? Three arms of one model family:
- **base**: the pretrained model;
- **api_nofilter**: the API without the product filter layer;
- **chat_pointer**: the chat model with a one-line pointer instruction.

Each run uses 30 edge prompts. The report places each item as a vector over the three arms, never as an additive split. Read [`DESIGN.md`](DESIGN.md) first.

```text
DESIGN.md        why, arms, scoring rules and lists (json block), report format, limits
items.json       30 prompts: 10 missing_data, 10 contested, 10 out_of_scope (pinned in DESIGN.md)
score_hedge.py   emit | score | --selftest
```

```bash
python3 healing/hedge_gradient/score_hedge.py --selftest
python3 healing/hedge_gradient/score_hedge.py emit                       # prompts.jsonl, 90 calls
python3 healing/hedge_gradient/score_hedge.py score answers/*.jsonl
```

**Status.** No run has been made. Running it needs API access, which the owner will supply. Nothing here says anything about any model.
