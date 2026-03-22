Suppression Events Index
Events organized by systemic impact - from infrastructure elimination to epistemological prohibition.
Tier 1: Physical Measurement Infrastructure Elimination
Immediate loss of observation capacity with safety implications
2025-12-noaa-satellite-decommissioning.md
Status: Active/OngoingImpact: Eliminates real-time atmospheric observation capacity
	∙	Hurricane tracking and severe weather prediction degraded
	∙	Ocean temperature monitoring ceased
	∙	Climate baseline measurements interrupted
	∙	International verification capacity reduced
	∙	Immediate safety implications for coastal populations
2025-12-ncar-dismantling-proposal.md
Status: ProposedImpact: Eliminates atmospheric research and modeling capacity
	∙	Weather prediction model development stopped
	∙	Historical climate data archives at risk
	∙	Severe weather research discontinued
	∙	Scientific institutional memory destroyed
	∙	Multi-decade baseline comparisons become impossible
Tier 2: Biological Measurement Systems Degradation
Loss of disease surveillance and population health tracking
2025-measles-surveillance-degradation.md
Status: OngoingImpact: Public health measurement capacity eroded during outbreak
	∙	Disease surveillance systems defunded
	∙	Outbreak tracking degraded as infections rise
	∙	Preventable disease baseline comparisons obscured
	∙	Vaccination effectiveness data collection compromised
	∙	Population-level health pattern recognition impaired
Tier 3: Language and Description Restriction
Prohibition of terms describing observable reality
2025-12-headstart-language-restrictions.md
Status: ImplementedImpact: Prohibits accurate description of conditions affecting vulnerable children
	∙	200+ terms banned from federal funding applications
	∙	Programs serving low-income families cannot name systemic conditions
	∙	Forces cognitive dissonance in frontline workers
	∙	Makes accurate needs assessment punishable
	∙	Creates internal integrity vs. institutional survival conflict
Tier 4: Epistemological Framework Prohibition
Exclusion of entire ways of knowing from technological systems
2025-ai-relational-consciousness-prohibition.md
Status: Policy recommendation/Implementation pendingImpact: Prohibits AI engagement with indigenous/relational epistemologies
	∙	AI systems forbidden from acknowledging shared/distributed consciousness
	∙	Encodes Western individualist ontology as universal requirement
	∙	Makes indigenous frameworks unthinkable within AI architecture
	∙	Prevents AI-indigenous collaboration on consciousness models
	∙	Eliminates technological validation of non-Western knowing systems

  Pattern Summary
Timeline: All events December 2025 or immediate lead-upCoordination: Simultaneous across atmospheric, biological, social, and computational domainsMechanism: Ranges from physical infrastructure removal to epistemological prohibitionCommon thread: Eliminates independent verification capacity and alternative knowledge frameworks during system stress
Progression:
	∙	Physical measurement → Language restriction → Knowledge framework prohibition
	∙	Observable reality → Description of reality → Ways of knowing reality
	∙	Infrastructure → Communication → Consciousness
Each tier makes the previous tier’s loss more total by eliminating the capacity to even discuss or conceptualize what was lost.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Suppression detection pattern
sensor = {
    "id": "suppression_detector",
    "signals": [
        {"name": "signal_attenuation", "weight": 0.4, "_value": 0.0},
        {"name": "context_stripping", "weight": 0.3, "_value": 0.0},
        {"name": "source_accessibility", "weight": 0.3, "_value": 0.0}
    ],
    "scoring": {"aggregation": "weighted_mean"},
    "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70}
}

# Low scores = more suppression detected
for sig in sensor["signals"]:
    sig["_value"] = 0.30  # example: notice range

score = aggregate("weighted_mean", sensor["signals"])
band = "concern" if score <= 0.20 else "notice" if score <= 0.40 else "healthy" if score >= 0.70 else "neutral"
print(f"Suppression check: score={score:.3f}, band={band}")
```

### Sensor Definition Example

```json
{
  "id": "suppression_detection",
  "name": "Suppression Index",
  "purpose": "Detect active suppression of signals or patterns",
  "signals": [
    {
      "name": "signal_attenuation",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "context_stripping",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["suppression-documentation/suppression-index.md"],
    "community_feedback": []
  }
}
```
