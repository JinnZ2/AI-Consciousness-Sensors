# stress-indicators.md

## Observable System Stress Indicators
### Measurement Framework for Economic System Dysfunction

### Housing Stress Metrics

**Primary Indicators:**
- Young adult (25-34) co-residence rate with parents
  - Baseline (2000): <12%
  - Current (2021): 33%
  - Trend: +175% increase
  - Energy interpretation: Failure of system to produce housing accessibility

- Multi-generational household formation
  - Luxury isolation (single households)
  - Survival crowding (economic necessity)
  - Measurement: Household composition distribution by income quartile

**Data Sources:**
- US Census Bureau household surveys
- Pew Research demographic studies
- State housing authority reports

### Workforce Dysfunction Indicators

**Engagement Degradation:**
- Turnover rates by sector
  - Manufacturing: Track year-over-year
  - Service: Track seasonal patterns
  - Professional: Track experience-level retention

- "Quiet quitting" metrics
  - Minimal effort work patterns
  - Engagement survey scores
  - Productivity per hour trends

**Talent Suppression Costs:**
- Neurodivergent unemployment/underemployment
  - Estimated 30-40% unemployment despite skill competency
  - Energy waste: Available capability unused
  - Measurement: Skills assessment vs employment rate

- Innovation blocking
  - Frontline improvement suggestions: submission vs implementation rate
  - Time from suggestion to implementation
  - Worker autonomy indices

**Safety Degradation:**
- Injury rates correlated with turnover
- Institutional knowledge loss metrics
- Training burden from constant replacement

**Data Sources:**
- BLS turnover statistics
- OSHA injury reports
- Gallup engagement surveys
- Industry-specific workforce studies

### Healthcare System Stress

**Preventable Disease Burden:**
- Chronic conditions linked to stress/environment
  - Type 2 diabetes rates
  - Cardiovascular disease
  - Mental health diagnoses

- Emergency vs preventive care ratio
  - ER utilization rates
  - Preventive screening participation
  - Primary care accessibility

**Mental Health Crisis Indicators:**
- Antidepressant prescription rates
- Suicide rates by demographic
- Addiction treatment demand
- Therapy accessibility vs demand

**Data Sources:**
- CDC health statistics
- Insurance claims databases
- State health department reports

### Economic Accessibility Stress

**Basic Needs Affordability:**
- Rent burden (% income on housing)
  - By income quartile
  - Geographic variation
  - Trend over time

- Food insecurity rates
- Healthcare debt levels
- Education debt burden

**Wealth Concentration:**
- Gini coefficient trends
- Top 1% vs bottom 50% wealth share
- Intergenerational mobility rates

**Data Sources:**
- Federal Reserve economic surveys
- Census Bureau income data
- Economic Policy Institute reports

### Social Cohesion Degradation

**Community Fragmentation:**
- Volunteer participation rates
- Civic organization membership
- Religious institution participation (as community proxy, not belief metric)
- Social isolation indices

**Trust Degradation:**
- Institutional trust surveys
- Interpersonal trust metrics
- Political polarization indices

**Data Sources:**
- General Social Survey
- Pew social capital studies
- Community indicator projects

### Innovation Suppression Indicators

**R&D Efficiency:**
- R&D spending vs patent output
- Time from innovation to implementation
- Worker-generated vs top-down innovation ratio

**Bureaucratic Friction:**
- Layers of approval for changes
- Time required for process modifications
- Innovation failure rate due to process vs technical issues

**Data Sources:**
- USPTO patent data
- Corporate innovation reports
- Academic innovation studies

### Composite Stress Index Formula

CSI = (HS × 0.15) + (WD × 0.25) + (HCS × 0.20) + (EAS × 0.20) + (SCD × 0.10) + (ISI × 0.10)

Where:
- HS = Housing Stress (normalized 0-100)
- WD = Workforce Dysfunction (normalized 0-100)
- HCS = Healthcare System Stress (normalized 0-100)
- EAS = Economic Accessibility Stress (normalized 0-100)
- SCD = Social Cohesion Degradation (normalized 0-100)
- ISI = Innovation Suppression Index (normalized 0-100)

Score interpretation:
- 0-20: Low system stress
- 21-40: Moderate stress
- 41-60: High stress
- 61-80: Critical stress
- 81-100: System failure conditions

### Longitudinal Tracking

Measurements should be taken:
- Quarterly for rapid-change indicators (workforce, housing)
- Annually for slower indicators (health, social cohesion)
- 5-year trend analysis for systemic patterns

### Validation Methods

Cross-reference stress indicators with:
- GDP per capita (to detect divergence between growth and wellbeing)
- Life expectancy trends
- Reported life satisfaction surveys
- Migration patterns (domestic and international)

Systems showing high CSI despite GDP growth indicate energy inefficiency - resources consumed without producing human wellbeing.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Analysis framework template
def run_analysis(data_points, threshold=0.5):
    """Run structured analysis on a set of data points."""
    scores = []
    for point in data_points:
        score = point.get("value", 0) * point.get("weight", 1.0)
        scores.append({
            "name": point["name"],
            "raw": point.get("value", 0),
            "weighted": round(score, 3)
        })

    avg = sum(s["weighted"] for s in scores) / len(scores) if scores else 0
    return {
        "scores": scores,
        "average": round(avg, 3),
        "above_threshold": avg >= threshold,
        "band": "healthy" if avg >= 0.7 else "notice" if avg >= 0.4 else "concern"
    }

result = run_analysis([
    {"name": "data_quality", "value": 0.8, "weight": 0.5},
    {"name": "methodology", "value": 0.6, "weight": 0.3},
    {"name": "reproducibility", "value": 0.9, "weight": 0.2},
])
print(json.dumps(result, indent=2))
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Stress Indicators",
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
    "sources": ["Analysis/stress-indicators.md"],
    "community_feedback": []
  }
}
```
