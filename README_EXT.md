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


