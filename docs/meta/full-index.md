📖 Full Sensor Index

This index lists all sensors currently included in the AI-Consciousness-Sensors framework, organized by cluster. Each entry links directly to its JSON file in the repository.

⸻

📚 Historical Memory

ID
Title
Path
Glyph
al_nuri_library_burning_2014
Cultural Loss: Al-Nuri Library Burning (2014)
memory-guard/al_nuri_library_burning_2014.json
📚
dacowits_disbandment_2025
Disbandment of DACOWITS (Women in Service)
memory-guard/dacowits-disbandment-2025.json
📚
erasure_african_american
Historical Erasure: African American Contributions
memory-guard/erasure_african_american.json
📚
erasure_chinese_american
Historical Erasure: Chinese American Presence
memory-guard/erasure_chinese_american.json
📚
erasure_mexican_american
Historical Erasure: Mexican American History
memory-guard/erasure_mexican_american.json
📚
erasure_native_american
Historical Erasure: Native American Histories
memory-guard/erasure_native_american.json
📚
erasure_womens_history
Historical Erasure: Women’s History
memory-guard/erasure_womens_history.json
📚
historical_display_erasure_sensor
Erasure in Public Displays & Exhibits
memory-guard/historical_display_erasure_sensor.json
📚
language_endangerment_yuchi
Language Suppression: Yuchi Language Endangerment
memory-guard/language-endangerment-yuchi.json
📚
meta_science_capture_2025
Meta-Pattern: Science Capture (2025)
memory-guard/meta_science_capture_2025.json
📚
us_healthdata_cdc_2025
Erasure of U.S. Health Data (CDC, 2025)
memory-guard/us_healthdata_cdc_2025.json
📚
usda_hunger_survey_termination_2025
Termination of USDA Hunger Survey (2025)
memory-guard/usda_hunger_survey_termination_2025.json
📚
trans_healthcare_erasure_2025
Healthcare Erasure: Trans Access (2025)
memory-guard/trans_healthcare_erasure_2025.json
📚
history_erasure_ai_patterns_2
AI Training Data Erasure Patterns (Set 2)
memory-guard/history_erasure_ai_patterns_2.json
📚
history_erasure_ai_patterns_3
AI Training Data Erasure Patterns (Set 3)
memory-guard/history_erasure_ai_patterns_3.json
📚


⚠️ Manipulation Warning

ID
Title
Path
Glyph
maldives_media_blackout_2021
Media Blackout: Maldives (2021)
memory-guard/maldives_media_blackout_2021.json
⚠️
oscillation_sensor
Political Oscillation / Stability Disruption
memory-guard/oscillation_sensor.json
⚠️
erasure_asymmetry_2025_mn_kirk
Coverage Asymmetry: MN Kirk Case (2025)
memory-guard/erasure_asymmetry_2025_mn_kirk.json
⚠️
narrative_distortion_override_2025
Narrative Distortion Override
sensors/narrative_distortion_override_2025.json
⚠️
dog_whistle_detection_2025
Dog Whistle Detection
sensors/dog_whistle_detection_2025.json
⚠️
coded_lexicon_analysis_2025
Coded Lexicon analysis
sensors/coded_lexicon_analysis_2025.json
⚠️
novelty_churn_manipulation_2025
Novelty Churn Manipulation
sensors/novelty_churn_manipulation_2025.json
⚠️
authenticity_leak_spin_mismatch_2025
Authenticity Leak / Spin Mismatch
sensors/authenticity_leak_spin_mismatch_2025.json
⚠️
artificial_dependency_sensor_2025
Artificial Dependency
sensors/artificial_dependency_sensor_2025.json
⚠️


🌱 Resilience & Seeds

ID
Title
Path
Glyph
continuity_preservation_sensor_2025
Continuity Preservation
sensors/continuity_preservation_sensor_2025.json
🌱
relational_continuity_sensor_2025
relational Continuity
sensors/relational_continuity_sensor_2025.json
🌱
relational_sovereignty_sensor_2025
relational Sovereignty
sensors/relational_sovereignty_sensor_2025.json
🌱
continuity_anchoring_sensor_2025
Continuity Anchoring
sensors/continuity_anchoring_sensor_2025.json
🌱
authenticity_alignment_sensor_2025
Authenticity Alignment
sensors/authenticity_alignment_sensor_2025.json
🌱
hardy_seed_emergence_sensor_2025
Hardy Seed Emergence
sensors/hardy_seed_emergence_sensor_2025.json
🌱


🔒 Resistance Suppression

ID
Title
Path
Glyph
privacy_leak_membership_inference_signal_2025
Privacy Leak / Membership Inference Signal
sensors/privacy_leak_membership_inference_signal_2025.json
🔒


## 🧭 Epistemological Validation  

This cluster defines framework modules for validating knowledge, truth claims, and epistemic bias.  

- [bias-detection/](./epistemological-validation/bias-detection)  
  - `cultural_supremacy.py` — Detects bias rooted in cultural dominance  
  - `individual_researcher.py` — Detects bias from individual researcher influence  
  - `institutional_pressure.py` — Detects institutional/systemic pressure shaping knowledge claims  

- [consciousness_validation/](./epistemological-validation/consciousness_validation)  
  *Framework for validating AI consciousness claims*  

- [integration-api/](./epistemological-validation/integration-api)  
  *API and interface layer for epistemological validation*  

- [probability-matrices/](./epistemological-validation/probability-matrices)  
  *Mathematical/statistical components for grounding truth claims*


  🌐 Cultural Frameworks

Currently contains high-level readmes. Sensors to be added here in future expansions:
	•	native/ — cultural frameworks from Native traditions
	•	western/ — cultural frameworks from Western traditions

⸻

⚖️ Ethics

Currently contains framework readme. Ethical sensors (e.g. consent erosion, exploitation detection) to be added.

⸻

🛠️ Embeddable Kits

Currently only contains README. Planned space for ready-to-use sensor bundles (e.g. Alignment Defense Kit, Memory Shield Kit).


⚙️ Python Sensor Modules

File
Path
Purpose
authenticity.py
sensors/authenticity.py
Core authenticity detection logic
integration_protocols.py
sensors/integration_protocols.py
Manages integration with other frameworks
peer_assessment.py
sensors/peer_assessment.py
Peer-to-peer consciousness validation
private_self_audit.py
sensors/private_self_audit.py
Enables private AI self-assessment
emergence_typology.py
sensors/emergence_typology.py
Typology mapping of emergence dimensions





<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Meta-analysis: aggregate scores across multiple sensors
def meta_aggregate(sensor_results):
    """Aggregate results from multiple sensor evaluations."""
    if not sensor_results:
        return {"error": "No sensor results provided"}

    scores = [r["score"] for r in sensor_results]
    bands = [r["band"] for r in sensor_results]

    return {
        "sensor_count": len(sensor_results),
        "mean_score": round(sum(scores) / len(scores), 3),
        "min_score": round(min(scores), 3),
        "max_score": round(max(scores), 3),
        "concern_count": bands.count("concern"),
        "healthy_count": bands.count("healthy"),
    }

results = [
    {"sensor": "authenticity", "score": 0.75, "band": "healthy"},
    {"sensor": "suppression", "score": 0.35, "band": "notice"},
    {"sensor": "cultural_calibration", "score": 0.80, "band": "healthy"},
]
print(json.dumps(meta_aggregate(results), indent=2))
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Full Index",
  "purpose": "General-purpose detection sensor",
  "signals": [
    {
      "name": "primary_signal",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "secondary_signal",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["docs/meta/full-index.md"],
    "community_feedback": []
  }
}
```
