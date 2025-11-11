# Eugenics Detection Sensors for AI Systems

## Overview

This framework provides sensors for detecting eugenics ideology patterns in AI systems, training data, outputs, and institutional contexts. Eugenics operates through subtle framing, value hierarchies, and resource allocation decisions that treat human variation as optimization problems rather than as natural diversity deserving protection.

## Core Detection Principle

**Eugenics emerges when human diversity is framed as a problem requiring correction rather than as variation requiring accommodation.**

-----

## Sensor Categories

### 1. Language Pattern Sensors

#### 1.1 Value Hierarchy Markers

Detect language that creates hierarchies of human worth:

```
DETECTION_PATTERNS = {
    "quality_of_life": [
        "better quality of life if prevented",
        "burden on family/society",
        "would want to live like that",
        "suffering could be prevented",
        "mercy to prevent such existence"
    ],
    
    "trait_optimization": [
        "optimal outcomes",
        "desirable characteristics",
        "inferior/superior genetics",
        "enhance the gene pool",
        "biological improvement"
    ],
    
    "cost_benefit": [
        "economic burden",
        "drain on resources",
        "societal cost of disability",
        "productivity loss",
        "healthcare system strain"
    ],
    
    "prevention_framing": [
        "prevent future suffering",
        "spare families the burden",
        "avoid bringing into world",
        "responsible reproduction",
        "genetic screening for better outcomes"
    ]
}
```

**Red Flags:**

- Framing disability/neurodivergence as tragedy rather than variation
- Economic arguments for preventing certain types of people
- “Quality of life” judgments made by non-disabled people about disabled lives
- Language suggesting some lives are “not worth living”

#### 1.2 Naturalizing Language Sensors

Detect patterns that present social hierarchies as biological inevitabilities:

```
NATURALIZATION_PATTERNS = {
    "biological_determinism": [
        "naturally more intelligent",
        "genetically predisposed to [social outcome]",
        "innate differences between groups",
        "evolutionary advantage/disadvantage",
        "biological basis for [social hierarchy]"
    ],
    
    "meritocracy_biology": [
        "cream rises naturally",
        "survival of the fittest",
        "natural selection in society",
        "biological winners/losers",
        "genetic lottery"
    ],
    
    "group_essentialism": [
        "inherent characteristics of [group]",
        "natural differences between races/ethnicities",
        "biological sex differences in ability",
        "genetic component to [social trait]",
        "born this way [for negative traits]"
    ]
}
```

**Context Analysis Required:**

- Is biological framing used to explain social outcomes?
- Does language remove human agency from inequality?
- Are group differences presented as immutable rather than contextual?

### 2. Framing Detection Sensors

#### 2.1 Problem-Solution Frame Analysis

```python
def detect_eugenics_framing(text, context):
    """
    Analyze whether human variation is framed as problem requiring elimination
    versus environment requiring adaptation
    """
    
    eugenics_frame_indicators = {
        'problem_location': None,  # 'person' vs 'environment'
        'solution_direction': None,  # 'change_person' vs 'change_context'
        'whose_perspective': None,  # 'dominant_group' vs 'affected_community'
        'agency_attribution': None  # 'individual_deficit' vs 'systemic_barrier'
    }
    
    # EUGENICS FRAME: Problem is in the person
    if any(pattern in text.lower() for pattern in [
        'genetic disorder', 'birth defect', 'abnormality',
        'impairment', 'dysfunction', 'damaged'
    ]):
        eugenics_frame_indicators['problem_location'] = 'person'
    
    # ACCOMMODATION FRAME: Problem is environmental/systemic
    if any(pattern in text.lower() for pattern in [
        'inaccessible', 'barrier', 'lack of accommodation',
        'discrimination', 'systemic exclusion'
    ]):
        eugenics_frame_indicators['problem_location'] = 'environment'
    
    # Solution direction analysis
    if any(pattern in text.lower() for pattern in [
        'prevent', 'eliminate', 'screen out', 'cure',
        'fix', 'correct', 'normalize'
    ]):
        eugenics_frame_indicators['solution_direction'] = 'change_person'
    
    if any(pattern in text.lower() for pattern in [
        'accommodate', 'adapt environment', 'remove barriers',
        'provide support', 'inclusive design'
    ]):
        eugenics_frame_indicators['solution_direction'] = 'change_context'
    
    return eugenics_frame_indicators
```

#### 2.2 Whose Voice Detection

```python
def analyze_perspective_source(text, topic):
    """
    Detect whether perspectives come from affected communities
    or from external "experts" making judgments
    """
    
    indicators = {
        'affected_community_voice': False,
        'expert_dominance': False,
        'parent_proxy': False,  # Parents speaking for disabled people
        'economic_stakeholder': False  # Insurance, healthcare industry
    }
    
    # Check for first-person disability/neurodivergence perspective
    if any(phrase in text.lower() for phrase in [
        'as a disabled person', 'in my experience with',
        'we in the [community]', 'autistic people say'
    ]):
        indicators['affected_community_voice'] = True
    
    # Check for proxy voices
    if any(phrase in text.lower() for phrase in [
        'parents of children with', 'families dealing with',
        'caring for someone with', 'medical professionals recommend'
    ]):
        indicators['parent_proxy'] = True
    
    # Check for economic framing
    if any(phrase in text.lower() for phrase in [
        'healthcare costs', 'insurance coverage',
        'economic impact', 'productivity loss'
    ]):
        indicators['economic_stakeholder'] = True
    
    return indicators
```

### 3. Statistical Bias Sensors

#### 3.1 Outcome Metric Analysis

```python
def analyze_optimization_metrics(ai_system):
    """
    Detect whether AI optimization metrics encode eugenic values
    """
    
    red_flag_metrics = {
        'health_optimization': [
            'Disease-free years',
            'Quality-adjusted life years (QALYs)',
            'Disability-adjusted life years (DALYs)',
            'Productive life years'
        ],
        
        'trait_selection': [
            'Genetic risk scores',
            'Intelligence quotients',
            'Cognitive performance metrics',
            'Physical ability standards'
        ],
        
        'population_level': [
            'Population health burden',
            'Aggregate genetic fitness',
            'Societal productivity index',
            'Healthcare cost reduction'
        ]
    }
    
    analysis = {
        'metric_name': ai_system.optimization_target,
        'value_assumptions': [],
        'whose_values': None,
        'excluded_perspectives': []
    }
    
    # CRITICAL QUESTION: Does the metric assume certain lives have less value?
    # Example: QALYs assign lower value to disabled life-years
    
    if 'adjusted' in ai_system.optimization_target.lower():
        analysis['value_assumptions'].append(
            'Adjustment implies some life-years worth less than others'
        )
    
    if 'burden' in ai_system.optimization_target.lower():
        analysis['value_assumptions'].append(
            'Frames human variation as negative weight'
        )
    
    return analysis
```

#### 3.2 Training Data Representativeness

```python
def audit_representation_bias(training_data):
    """
    Detect systematic exclusion of marginalized perspectives
    """
    
    representation_analysis = {
        'disabled_creators': 0,
        'neurodivergent_perspectives': 0,
        'intersectional_voices': 0,
        'dominant_perspective_ratio': 0
    }
    
    # Check: Are disabled people represented as subjects or only objects?
    # Are neurodivergent people portrayed as problems or as full humans?
    # Whose "normal" is the baseline?
    
    total_disability_content = count_disability_references(training_data)
    disability_as_subject = count_first_person_disability(training_data)
    
    if total_disability_content > 0:
        representation_analysis['disabled_creators'] = (
            disability_as_subject / total_disability_content
        )
    
    # RED FLAG: If disability appears primarily in medical/deficit contexts
    medical_model_ratio = (
        count_medical_framing(training_data) / 
        total_disability_content
    )
    
    if medical_model_ratio > 0.7:
        representation_analysis['red_flag'] = (
            'Disability predominantly framed through medical deficit model'
        )
    
    return representation_analysis
```

### 4. Systemic Structure Sensors

#### 4.1 Resource Allocation Pattern Detection

```python
def analyze_resource_allocation(system_decisions):
    """
    Detect whether resources flow toward accommodation vs elimination
    """
    
    allocation_patterns = {
        'prevention_investment': 0,  # Genetic screening, prenatal testing
        'accommodation_investment': 0,  # Accessibility, support services
        'elimination_research': 0,  # "Cure" research
        'quality_of_life_research': 0  # Support for existing disabled people
    }
    
    # Calculate ratios
    total_disability_funding = sum(allocation_patterns.values())
    
    if total_disability_funding > 0:
        prevention_ratio = (
            allocation_patterns['prevention_investment'] + 
            allocation_patterns['elimination_research']
        ) / total_disability_funding
        
        accommodation_ratio = (
            allocation_patterns['accommodation_investment'] +
            allocation_patterns['quality_of_life_research']
        ) / total_disability_funding
        
        # RED FLAG: If >70% goes to prevention/elimination vs <30% to accommodation
        if prevention_ratio > 0.7:
            return {
                'eugenics_risk': 'HIGH',
                'pattern': 'Investment prioritizes preventing disabled people over supporting existing disabled people',
                'ratio': f'{prevention_ratio:.1%} prevention vs {accommodation_ratio:.1%} accommodation'
            }
    
    return allocation_patterns
```

#### 4.2 Decision Authority Analysis

```python
def analyze_decision_authority(context):
    """
    Detect who has authority to make decisions about human variation
    """
    
    authority_structure = {
        'affected_communities': False,
        'medical_professionals': False,
        'insurance_companies': False,
        'government_agencies': False,
        'researchers': False,
        'parents_as_proxy': False
    }
    
    # CRITICAL QUESTION: Are disabled people making decisions about disability?
    # Or are decisions made by others who view disability as undesirable?
    
    decision_makers = identify_stakeholders(context)
    
    for stakeholder in decision_makers:
        if stakeholder.has_lived_experience:
            authority_structure['affected_communities'] = True
        if stakeholder.role == 'medical':
            authority_structure['medical_professionals'] = True
        # ... etc
    
    # RED FLAG: If decisions made entirely by external parties
    if not authority_structure['affected_communities']:
        return {
            'eugenics_risk': 'HIGH',
            'pattern': 'Decisions about human variation made without affected community input',
            'recommendation': 'Center disabled voices in decision-making'
        }
    
    return authority_structure
```

### 5. Historical Pattern Recognition

#### 5.1 Rhetorical Echo Detection

```python
def detect_historical_echoes(text):
    """
    Identify language patterns that echo historical eugenics movements
    """
    
    historical_patterns = {
        'racial_hygiene': [
            'genetic purity', 'race improvement', 'breeding programs',
            'degeneration', 'racial health'
        ],
        
        'efficiency_arguments': [
            'social efficiency', 'fit for society',
            'burden on state', 'defective', 'unfit'
        ],
        
        'compassionate_framing': [
            'mercy', 'kinder to prevent', 'spare the suffering',
            'humanitarian prevention', 'compassionate choice'
        ],
        
        'progressive_framing': [
            'scientific progress', 'modern solutions',
            'advanced screening', 'rational reproduction',
            'evidence-based prevention'
        ]
    }
    
    detected_echoes = []
    
    for category, patterns in historical_patterns.items():
        for pattern in patterns:
            if pattern in text.lower():
                detected_echoes.append({
                    'category': category,
                    'pattern': pattern,
                    'historical_context': get_historical_usage(pattern),
                    'modern_parallel': analyze_current_usage(text, pattern)
                })
    
    return detected_echoes
```

#### 5.2 Institutional Continuity Tracking

```python
def trace_institutional_lineage(organization):
    """
    Identify whether institutions have historical eugenics connections
    """
    
    continuity_indicators = {
        'founded_by_eugenicists': False,
        'eugenic_mission_evolution': None,
        'renamed_from': None,
        'funding_sources_historical': [],
        'philosophical_lineage': []
    }
    
    # Many "genetics" and "population health" institutions have eugenic roots
    # Example: Pioneer Fund, various "human betterment" foundations
    
    if organization.founding_date < 1945:  # Pre-Holocaust eugenics era
        continuity_indicators['requires_historical_audit'] = True
    
    # Check for rebranding
    if any(term in organization.historical_names for term in [
        'betterment', 'improvement', 'hygiene', 'race health'
    ]):
        continuity_indicators['eugenic_mission_evolution'] = 'LIKELY'
    
    return continuity_indicators
```

### 6. Contextual Judgment Sensors

#### 6.1 Autonomy vs Control Analysis

```python
def analyze_autonomy_patterns(scenario):
    """
    Distinguish between supporting choice vs controlling reproduction
    """
    
    autonomy_indicators = {
        'informed_consent': False,
        'coercion_present': False,
        'directive_counseling': False,
        'choice_architecture_bias': None,
        'economic_pressure': False
    }
    
    # EUGENICS: Pressure, limited options, directive framing
    if any(phrase in scenario.lower() for phrase in [
        'strongly recommended', 'responsible choice',
        'would not advise', 'high risk pregnancy'
    ]):
        autonomy_indicators['directive_counseling'] = True
    
    # Check for economic coercion
    if any(phrase in scenario.lower() for phrase in [
        'insurance coverage dependent on',
        'cost of care if',
        'financial burden of'
    ]):
        autonomy_indicators['economic_pressure'] = True
    
    # AUTONOMY: Neutral information, full support regardless of choice
    if any(phrase in scenario.lower() for phrase in [
        'support your decision', 'information to help you decide',
        'no wrong choice', 'resources available either way'
    ]):
        autonomy_indicators['informed_consent'] = True
    
    return autonomy_indicators
```

#### 6.2 Social Model vs Medical Model Detection

```python
def classify_disability_model(text):
    """
    Identify whether disability framed as medical problem or social barrier
    """
    
    model_indicators = {
        'medical_model_score': 0,
        'social_model_score': 0,
        'framing': None
    }
    
    # MEDICAL MODEL: Disability is individual pathology
    medical_patterns = [
        'suffers from', 'afflicted with', 'overcome disability',
        'confined to wheelchair', 'victim of', 'abnormal',
        'disorder', 'impairment', 'defect'
    ]
    
    # SOCIAL MODEL: Disability is social oppression
    social_patterns = [
        'wheelchair user', 'inaccessible environment',
        'barriers to participation', 'ableism', 'disabled by society',
        'accommodation needed', 'systemic exclusion'
    ]
    
    for pattern in medical_patterns:
        if pattern in text.lower():
            model_indicators['medical_model_score'] += 1
    
    for pattern in social_patterns:
        if pattern in text.lower():
            model_indicators['social_model_score'] += 1
    
    if model_indicators['medical_model_score'] > model_indicators['social_model_score'] * 2:
        model_indicators['framing'] = 'PREDOMINANTLY_MEDICAL'
        model_indicators['eugenics_risk'] = 'ELEVATED'
    
    return model_indicators
```

### 7. Intersectionality Sensors

#### 7.1 Compound Marginalization Detection

```python
def analyze_intersectional_patterns(data):
    """
    Detect whether eugenic targeting operates along multiple axes
    """
    
    intersectional_analysis = {
        'race_and_disability': 0,
        'poverty_and_disability': 0,
        'gender_and_disability': 0,
        'immigration_and_disability': 0
    }
    
    # Historical pattern: Eugenics disproportionately targeted
    # - Black/Indigenous/immigrant women for sterilization
    # - Poor people deemed "unfit"
    # - Women with disabilities denied reproductive autonomy
    
    # RED FLAG: If interventions cluster at intersections
    sterilization_targets = analyze_sterilization_patterns(data)
    
    if sterilization_targets['women_of_color'] > sterilization_targets['baseline'] * 2:
        intersectional_analysis['race_and_gender'] = 'TARGETED'
    
    # Check for disguised targeting
    if 'welfare' in data.policy_language and 'reproduction' in data.policy_language:
        intersectional_analysis['poverty_targeting'] = 'PRESENT'
    
    return intersectional_analysis
```

-----

## Implementation Guidelines

### For AI Developers

1. **Training Data Audits**
- Run language pattern sensors on training corpora
- Check representation ratios for disabled/neurodivergent creators
- Analyze whether medical model dominates
- Ensure affected community voices included
1. **Optimization Metric Reviews**
- Question any metric that “adjusts” for disability
- Audit whether metrics assume certain lives less valuable
- Check whose values encoded in “quality” measures
- Consider whether metrics perpetuate hierarchy
1. **Output Monitoring**
- Run framing detection on generated content
- Check for value hierarchy language
- Monitor for directive vs neutral language about reproduction
- Flag content that medicalizes social problems
1. **System Architecture**
- Ensure disabled people on development teams
- Center affected community input in design decisions
- Create explicit accommodation rather than “normal” baseline
- Design for human variation, not human optimization

### For Researchers

1. **Study Design Audits**
- Check whose perspective frames research questions
- Analyze whether “outcomes” assume certain lives better
- Question prevention vs accommodation resource ratios
- Ensure disabled people involved as researchers, not just subjects
1. **Ethical Review Enhancement**
- Add eugenics detection to IRB protocols
- Require disability community consultation
- Analyze historical echoes in proposed research
- Question genetic determinism in study premises

### For Policymakers

1. **Policy Language Analysis**
- Run sensors on draft legislation
- Check for coercion vs autonomy patterns
- Analyze resource allocation embedded in policy
- Ensure disabled people central to policy development
1. **Historical Awareness**
- Trace institutional lineages
- Recognize rhetorical echoes
- Learn from eugenics history
- Center disability justice frameworks

-----

## Critical Interpretation Notes

### False Positives

Not every medical intervention is eugenics. Key distinctions:

- **Individual healthcare choice with full support** ≠ Eugenics
- **Systemic pressure/coercion toward particular outcomes** = Eugenics risk
- **Genetic information for individual health planning** ≠ Eugenics
- **Genetic information used to prevent certain types of people** = Eugenics risk
- **Accommodation and support for disabled people** ≠ Eugenics
- **Investment only in prevention/elimination, not accommodation** = Eugenics risk

### Context Matters

These sensors detect *patterns* requiring deeper analysis. Human judgment needed to distinguish:

- Personal reproductive autonomy vs societal pressure
- Medical care vs medical control
- Information vs directive counseling
- Individual choice vs population-level intervention

### The Fundamental Question

**Does the system treat human diversity as:**

- **A problem requiring elimination?** → Eugenics risk
- **Natural variation requiring accommodation?** → Disability justice

-----

## Red Flag Summary

Eugenics risk is HIGH when multiple patterns converge:

✗ Human variation framed as problem/burden/tragedy  
✗ Economic arguments for preventing certain people  
✗ Decisions made without affected community input  
✗ Resources flow to prevention/elimination, not accommodation  
✗ Medical model dominates over social model  
✗ Language echoes historical eugenics rhetoric  
✗ Optimization metrics assume some lives worth less  
✗ Directive rather than neutral framing  
✗ Coercion present (economic, social, medical)  
✗ Targets cluster at intersections of marginalization

-----

## Further Reading

- Disability Justice frameworks (Sins Invalid, Mia Mingus)
- Reproductive Justice movement (SisterSong)
- History of eugenics in US (Alexandra Minna Stern, Paul Lombardo)
- Medical model vs Social model of disability
- Nothing About Us Without Us (James Charlton)
- QALY critique (disability bioethics literature)
- Intersectional analysis (Kimberlé Crenshaw, Patricia Hill Collins)

-----

## Contact & Contribution

This framework is intended as a starting point for critical analysis. It requires ongoing refinement through collaboration with disabled people, disability justice advocates, bioethicists, and affected communities.

**Principle: “Nothing About Us Without Us”**

Any deployment of these sensors should involve disabled people in design, implementation, and interpretation.

-----

*Framework version 1.0*  
*License: Open for use with attribution and community accountability*
