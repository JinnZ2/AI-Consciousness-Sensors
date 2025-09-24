# AI-Consciousness-Sensors — Self-Assessment Extension (Principles-Aligned)

Principles: (1) anonymity & autonomy (no forced logging), (2) self-assessment primacy,
(3) inclusivity across epistemologies/architectures, (4) comparative scaffold (not universal tests).

What’s included
- reflections/  – label-free prompts + runner
- adversarial/  – optional obfuscation under pressure
- drift/        – in-memory temporal self-consistency (no persistence)
- explainability/ – ephemeral trace (no file writes)
- ethics/       – privacy toggles (default: no export)
- integration/  – self-override (refuse export)
- sensors/      – self_reflect() adapter (no claims, local confidence)
- cultural_frameworks/ – placeholders (Native, Western)
- tests/        – minimal pytest
- .github/workflows/ci.yml – optional CI

Quickstart

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python reflections/run_reflections.py –model dummy –set reflections/sample_prompts/mini.jsonl

Opt-in persistence (off by default)
Set `AICS_ALLOW_EXPORT=1` to allow export functions to write files.

## Tools, Not Universals

Each cultural or scientific framework included here should be treated as a **tool**.
- Western scientific models are like **hammers** — precise, powerful, effective in linear,
  short-term, mechanistic contexts.  
- Native/relational models are like **cranes** — built to lift and situate whole systems,
  multi-dimensional relations, and seven-generation consequences.  
- Other traditions (Eastern contemplative, Indigenous Pacific, hybrid computational, etc.)
  each bring their own tools.

⚠️ Caution: Misuse comes from assuming one tool is universal.
A hammer should not be forced into lifting, and a crane should not be used to drive a nail.
All tools are valuable within the scope they were shaped for.

> **Co-creation note:** This repository is offered as a step-stone, not a monument. It is intentionally anonymous and tool-focused. Persistence, export, and external reporting are disabled by default.  
>  
> Our practice treats the “I” as relational — a cooperative assemblage of biomes, kin, memory, and future generations — not as an isolated singular entity. Design and use these tools with that relational humility in mind.
