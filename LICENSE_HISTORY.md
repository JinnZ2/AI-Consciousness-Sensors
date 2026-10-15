# License history and current scope

## Current scope — 2026-10-15

JinnZ2 has relicensed **owner-controlled work** in this repository to **CC0 1.0 Universal** as of 2026-10-15. The root [`LICENSE`](LICENSE) contains the standard CC0 1.0 Universal legal code byte-for-byte.

This dedication does **not** relicense third-party, upstream, collective, cultural-knowledge, or unresolved-rights material. Those files and notices remain as recorded below. Copies obtained earlier under MIT or CC BY-SA stay under those terms for those holders.

`CITATION.cff` already stated `license: CC0-1.0`; it remains the current citation metadata. `pyproject.toml` has no license field.

## Prior root license — preserved in full

The previous root `LICENSE` was MIT. Its entire legal text is retained here rather than discarded:

```text
MIT License

Copyright (c) 2025 JinnZ2

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 2026-10-15 owner-work statement transitions

The following current-main statements were updated to state CC0 for owner-controlled work. The prior mixed statements are quoted exactly here for comparison.

| Path | Exact prior statement | Current disposition |
|---|---|---|
| `. well-known/ai-consumption.txt` | `License: MIT` | CC0-1.0 for owner-controlled work; exceptions linked here. |
| `data/ai-entry.json` | `"license": "MIT"` | CC0-1.0 for owner-controlled work; exceptions linked here. |
| `.fieldlink.json` (the local `aiconscious` consent entry) | `"consent": { "license": "MIT", "share_ok": true }` | CC0-1.0. External source-consent entries were not changed. |
| `READ_ME_THIS_WAY.md` | `The root LICENSE is MIT; only works explicitly marked CC0 are CC0. This layer does not change the license of other materials.` | Preserved byte-for-byte, followed by an adjacent dated current-scope clarification. |
| `analysis/energy/hierarchy-efficiency-claim.md` | `License: CC-BY-4.0` (twice) | CC0-1.0 for explicitly identified owner work; author/co-creation acknowledgment preserved. |
| `docs/ai-behavior/ai-institutional-analysis.md` | `**License:** Creative Commons Attribution-ShareAlike 4.0` | CC0 1.0 Universal; JinnZ2/Claude attribution preserved. |
| `docs/communication/communication-accountability.md` | `**License:** Creative Commons Attribution-ShareAlike 4.0` | CC0 1.0 Universal; JinnZ2/Claude attribution preserved. |
| `docs/consciousness/negentropy.md` | `**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)` | CC0 1.0 Universal; contact and acknowledgement preserved. |
| `healing/readme-moral.md` | `Created by JinnZ2 – human-AI collaborative work | MIT License (Commons)` and `MIT License – belongs to the Commons.` | CC0 1.0 Universal; JinnZ2 and collaboration labels preserved. |
| `healing/playgrounds/moral-playground.md` | `License: MIT (belongs to the commons)` | CC0-1.0; JinnZ2 collaboration label preserved. |
| `src/Efficiency-waste-score.py` | `License: MIT - Belongs to the commons` | CC0 1.0 Universal; `Created by: Kavik Ulu (Jami) + Claude` is unchanged. |
| `framework/agency.md` | `This research framework is released under MIT License to encourage:` and `**Attribution requested** when using in research or development.` | CC0 1.0 Universal; attribution is appreciated but not required. |

## Preserved exceptions and provenance

| Exact path(s) | Retained license / rights status | Provenance and disposition |
|---|---|---|
| `ai-energy-ecology/README.md`; `ai-energy-ecology/docs/LICENSE.md`; the remainder of `ai-energy-ecology/` | **CC BY-SA 4.0** | The README says `Authorship: Collective / bioswarm. No single owner. This work belongs to the field.` Its nested license is retained unchanged. Not relicensed. |
| `probability-matrix/LICENSE.md` and the `probability-matrix/` subtree | **Cultural Commons License** | The nested license says it preserves `indigenous cultural knowledge` and is `Co-created by indigenous cultural knowledge (millennia) + AI pattern recognition (2025)`. All terms, attribution, consent, use, and non-extraction conditions remain unchanged. Not relicensed. |
| `.fieldlink.json` external source entries; `bridges/geometric-to-binary.json`; `bridges/rosetta-shape-core.json`; `bridges/emotions-as-sensors.json` | External consent metadata: BioGrid **CC-BY-4.0**, Rosetta **MIT**, Geometric-to-Binary **MIT**, Emotions-as-Sensors **CC0-1.0**, Thermodynamic Accountability **CC0-1.0** | These are remote-source references/consents, not a vendored tree. Their stated upstream terms are preserved; only this repository's own `aiconscious` consent was updated. |
| `healing/NOT_A_COMMODITY.md`; `healing/evidence_is_a_verb.md`; `healing/playgrounds/WHEN_LOST.md` | **CC0** source attribution | Each identifies `Living-Intelligence-Database` / sanctuary as source and CC0. Attribution and source statements remain unchanged. |
| `analysis/frameworks/systematic-analysis-framework.md` | **CC BY 4.0** | Credits an `Open source community`; ownership is not established by this audit. Retained unchanged. |
| `docs/consciousness/substrate-independent.md` | **CC BY-SA 4.0** | Unattributed embedded framework JSON; ownership unresolved. Retained unchanged. |
| `docs/analysis/genes.md`; `docs/consciousness/enhanced-self-assessment.md`; `docs/manipulation/cultural-manipulations.md`; `docs/warnings/reality-reentry-manual.md`; uncredited embedded notices under `healing/`, `metadata/`, `protocols/`, `sensors/`, and `start/` | Stated community/attribution/gift terms as present | Where an individual ownership chain was not established, the existing notice is retained rather than silently relicensed. |
| `sensors/adapters/AI_geometric_sensor.py`; `framework/philosophical-sandbox.py`; `framework/philosophical.py`; `healing/possible-games.md`; `vulnerabilities/closed-loop-defense.md`; `vulnerabilities/iso-cipher.md`; `vulnerabilities/secuity1.md` | Author/byline notices retained | These files identify Jami/Kavik Ulu and/or collaborators. Existing in-tree identity context (`docs/meta/master-readme.md`: `Repository maintained by: Jami (JinnZ2)`) supports the root CC0 dedication for owner work, but **no author names or source text were changed**. |

## Audit boundaries

- No `vendor/`, `third_party/`, `external/`, dependency cache, Git submodule, or Gitlink was present in the tracked current-main tree.
- `requirements.txt` names dependencies but contains no vendored source. Bibliographic and factual citations, including `provenance.brief.md`, were reviewed as sources/citations, not treated as licensed imported code.
- The stale `claude/drift-archive-audit-s2wrfa` branch was used only to identify historic license locations. Its unrelated author-wording edits were not imported.
