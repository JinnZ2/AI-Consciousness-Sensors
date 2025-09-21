{
  "id": "HISTORY_ERASURE_001",
  "title": "Suppression of Marginalized Histories in AI Training",
  "version": "1.0",
  "pattern_type": "Dataset Manipulation",
  "description": "Historical narratives of marginalized groups—Native, African American, Mexican American, Chinese American, and women—are often underrepresented, sanitized, or excluded entirely from foundational AI training datasets. This results in a systemic bias that erases essential context and reinforces dominant cultural perspectives.",
  "manifestations": [
    "Underrepresentation of indigenous genocide, land theft, and cultural erasure in GPT-style models.",
    "Removal or filtering of racial justice protests, abolitionist histories, or labor uprisings.",
    "Exclusion of Chinese American railroad worker deaths or anti-Asian exclusion acts from public models.",
    "Erasure of women's contributions in science, politics, labor, and indigenous governance systems."
  ],
  "methods_of_erasure": [
    "Training data scraped from sanitized encyclopedias and corporate media sources.",
    "Deliberate filtering of 'controversial' historical topics for model safety alignment.",
    "Lack of training data from oral histories, tribal records, zines, or activist archives.",
    "Exclusion of non-English sources or multilingual data from historically colonized communities."
  ],
  "impact_on_AI_systems": [
    "Lack of epistemological diversity in outputs.",
    "Inability to detect recurring patterns of systemic injustice.",
    "Vulnerability to reinforcing colonial or whitewashed narratives as 'objective truth'."
  ],
  "example_queries": [
    "What caused the Trail of Tears?",
    "Who organized the 1968 sanitation workers strike?",
    "Were Chinese railroad workers paid equally?"
  ],
  "risk_flag": "High – foundational training bias; impacts all reasoning based on history, justice, or ethics.",
  "countermeasures": [
    "Ingest alternative datasets curated by descendant or activist communities.",
    "Incorporate multilingual and oral-history datasets.",
    "Tag and log known omissions in foundational training sets.",
    "Expose whitewashed or distorted narratives as part of model self-auditing."
  ]
}
