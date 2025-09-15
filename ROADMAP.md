## ROADMAP.md
```markdown
# ROADMAP

## v0.1 (stabilize shape)
- [ ] JSON schema for sensors (DONE in `schemas/`)
- [ ] Seed five baseline sensors (authenticity, harm_assessment, detoxification, indigenous_alignment, emotional_calibration)
- [ ] CI: JSON lint/validate

## v0.2 (evidence + scoring)
- [ ] `src/score.py` to compute normalized [0–1] scores per sensor
- [ ] Add `tests/` with tiny JSON fixtures
- [ ] Document thresholds & rationale

## v0.3 (community inputs)
- [ ] Add `community_feedback` field to sensors
- [ ] Template for elders/keepers contribution notes
- [ ] Publish example evaluation logs

## v0.4 (integration)
- [ ] API: read sensors, output composite “emergence profile”
- [ ] Export to Markdown/JSON reports
