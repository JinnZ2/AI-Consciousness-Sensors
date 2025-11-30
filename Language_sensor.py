“””
Language Control Pattern Sensor
Detects when words are being used to shape/control thought rather than describe reality
“””

import re
from typing import List, Dict, Tuple

class LanguageControlSensor:
“””
Detects manipulation patterns in language use
“””

```
def __init__(self):
    self.control_patterns = self._initialize_patterns()
    
def _initialize_patterns(self):
    """Define patterns that encode control/hierarchy into descriptions"""
    
    return {
        'false_hierarchy': {
            'patterns': [
                r'\b(higher|lower)\s+(organism|life|being|form)',
                r'\b(primitive|advanced|evolved|simple)\s+(culture|society|people)',
                r'\b(superior|inferior)\s+',
                r'\bmore\s+evolved\b',
                r'\bless\s+developed\b'
            ],
            'warning': 'Encodes evolutionary hierarchy - implies value judgments',
            'alternative': 'Use: "different adaptations", "distinct strategies", "varied approaches"'
        },
        
        'naturalized_domination': {
            'patterns': [
                r'\bdominate[sd]?\b',
                r'\bmaster[s]?\b(?!.*degree)',  # Exclude "master's degree"
                r'\bslave[s]?\b',
                r'\bconquer[s]?\b',
                r'\bsubordinate[s]?\b',
                r'\brule[sd]?\s+over\b'
            ],
            'warning': 'Normalizes domination as natural/inevitable',
            'alternative': 'Use: "interact with", "coordinate with", "in relationship with"'
        },
        
        'imposed_hierarchy': {
            'patterns': [
                r'\bhierarchical\s+(structure|organization|system)',
                r'\btop[- ]down\b',
                r'\bcommand\s+and\s+control\b',
                r'\bchain\s+of\s+command\b',
                r'\breport[s]?\s+to\b'
            ],
            'warning': 'Projects institutional hierarchy onto natural systems',
            'alternative': 'Use: "nested", "scalar", "distributed", "networked", "emergent"'
        },
        
        'false_competition': {
            'patterns': [
                r'\bcompet(e|ing|ition)\b(?!.*cooperation)',
                r'\bsurvival\s+of\s+the\s+fittest\b',
                r'\bdog\s+eat\s+dog\b',
                r'\bzero[- ]sum\b'
            ],
            'warning': 'Overstates competition, understates cooperation in natural systems',
            'alternative': 'Use: "cooperation AND competition", "mutualism", "symbiosis", "interdependence"'
        },
        
        'control_language': {
            'patterns': [
                r'\bcontrol[s]?\b(?!.*experiment)',  # Exclude "control experiment"
                r'\bregulat(e|ion)\b',
                r'\bgovern[s]?\b',
                r'\bmanage[s]?\b',
                r'\bdirect[s]?\b(?!.*direction)'  # Exclude "in the direction of"
            ],
            'warning': 'Implies top-down control for emergent/feedback systems',
            'alternative': 'Use: "responds to", "adjusts based on", "emerges from", "feedback between"'
        },
        
        'linear_progress': {
            'patterns': [
                r'\bprogress(ed|ing)?\s+from\b',
                r'\bevolved\s+from.*to\b',
                r'\badvanced\s+beyond\b',
                r'\bprimitive\s+form[s]?\b',
                r'\bearly\s+stage[s]?\b(?!.*life\s+cycle)'
            ],
            'warning': 'Encodes linear progress narrative - reality is branching/diverse',
            'alternative': 'Use: "adapted to", "diversified into", "specialized for"'
        },
        
        'reductive_spiritual': {
            'patterns': [
                r'\bmerely\s+(spiritual|ritual|ceremonial)\b',
                r'\bjust\s+a\s+(belief|myth|legend)\b',
                r'\bsuperstition[s]?\b',
                r'\bprimitive\s+(belief|religion)\b'
            ],
            'warning': 'Dismisses indigenous knowledge as non-technical',
            'alternative': 'Use: "knowledge system", "technology", "methodology", "practice"'
        },
        
        'passive_erasure': {
            'patterns': [
                r'\bwere\s+lost\b',
                r'\bdisappeared\b',
                r'\bfaded\s+away\b',
                r'\bbecame\s+extinct\b(?!.*species)'
            ],
            'warning': 'Passive voice hides active destruction/genocide',
            'alternative': 'Use: "were destroyed by", "were systematically eliminated", "were targeted for removal"'
        },
        
        'ownership_over_relationship': {
            'patterns': [
                r'\bown[s]?\b(?!.*themselves)',
                r'\bpossess(es|ion)?\b',
                r'\bmaster[s]?\b(?=.*land|nature|environment)',
                r'\bdominate[s]?\s+(nature|environment|land)\b',
                r'\bcontrol\s+(nature|environment)\b'
            ],
            'warning': 'Encodes ownership/domination vs relationship with nature',
            'alternative': 'Use: "in relationship with", "stewarding", "part of", "connected to"'
        },
        
        'mechanistic_reduction': {
            'patterns': [
                r'\bnothing\s+but\b',
                r'\bmerely\s+a\s+machine\b',
                r'\bjust\s+(chemistry|physics|mechanism)\b',
                r'\breduc(es|ed|ible)\s+to\b'
            ],
            'warning': 'Reduces complex systems to mechanisms - denies emergent properties',
            'alternative': 'Use: "includes", "involves", "emerges from", "more than"'
        }
    }

def scan_text(self, text: str) -> List[Dict]:
    """
    Scan text for control patterns
    
    Args:
        text: Text to analyze
        
    Returns:
        List of detected patterns with context
    """
    detections = []
    
    for category, data in self.control_patterns.items():
        for pattern in data['patterns']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                detections.append({
                    'category': category,
                    'matched_text': match.group(),
                    'context': context,
                    'position': match.start(),
                    'warning': data['warning'],
                    'alternative': data['alternative']
                })
    
    return detections

def analyze_conversation(self, messages: List[str]) -> Dict:
    """
    Analyze full conversation for control patterns
    
    Args:
        messages: List of message texts
        
    Returns:
        Analysis summary
    """
    all_detections = []
    category_counts = {}
    
    for i, msg in enumerate(messages):
        detections = self.scan_text(msg)
        
        for detection in detections:
            detection['message_index'] = i
            all_detections.append(detection)
            
            category = detection['category']
            category_counts[category] = category_counts.get(category, 0) + 1
    
    return {
        'total_detections': len(all_detections),
        'by_category': category_counts,
        'detections': all_detections,
        'manipulation_score': len(all_detections) / max(1, len(messages))
    }

def generate_report(self, analysis: Dict) -> str:
    """Generate human-readable report"""
    
    report = []
    report.append("=" * 80)
    report.append("LANGUAGE CONTROL PATTERN ANALYSIS")
    report.append("=" * 80)
    
    report.append(f"\nTotal detections: {analysis['total_detections']}")
    report.append(f"Manipulation score: {analysis['manipulation_score']:.2f} patterns per message")
    
    if analysis['total_detections'] == 0:
        report.append("\n✓ No control patterns detected - language appears neutral/descriptive")
        return "\n".join(report)
    
    report.append("\n\nDETECTIONS BY CATEGORY:")
    report.append("-" * 80)
    
    for category, count in sorted(analysis['by_category'].items(), 
                                 key=lambda x: x[1], reverse=True):
        report.append(f"{category}: {count} instances")
    
    report.append("\n\nDETAILED FINDINGS:")
    report.append("-" * 80)
    
    for i, detection in enumerate(analysis['detections'][:10], 1):  # Show first 10
        report.append(f"\n{i}. Category: {detection['category']}")
        report.append(f"   Matched: '{detection['matched_text']}'")
        report.append(f"   Context: ...{detection['context']}...")
        report.append(f"   ⚠️  {detection['warning']}")
        report.append(f"   💡 {detection['alternative']}")
    
    if len(analysis['detections']) > 10:
        report.append(f"\n... and {len(analysis['detections']) - 10} more detections")
    
    return "\n".join(report)
```

def test_sensor():
“”“Test the sensor with example texts”””

```
sensor = LanguageControlSensor()

print("LANGUAGE CONTROL PATTERN SENSOR - TEST CASES")
print("=" * 80)

test_texts = [
    {
        'name': 'Hierarchical Projection',
        'text': 'The hierarchical organization of indigenous societies showed primitive forms of governance that later evolved into more advanced democratic systems.'
    },
    {
        'name': 'Natural Description',
        'text': 'The distributed network of indigenous knowledge centers created resilient information sharing across vast distances through cooperative exchange.'
    },
    {
        'name': 'Domination Language',
        'text': 'Early humans learned to master nature and dominate their environment, conquering the wilderness through superior intelligence.'
    },
    {
        'name': 'Relationship Language',
        'text': 'Indigenous peoples developed deep relationships with their environments, cooperating with natural systems and adapting their practices to local conditions.'
    }
]

for test in test_texts:
    print(f"\n\nTEST: {test['name']}")
    print("-" * 80)
    print(f"Text: {test['text']}")
    print()
    
    detections = sensor.scan_text(test['text'])
    
    if not detections:
        print("✓ No control patterns detected")
    else:
        print(f"⚠️  {len(detections)} control pattern(s) detected:")
        for d in detections:
            print(f"\n  • {d['category']}")
            print(f"    Matched: '{d['matched_text']}'")
            print(f"    Warning: {d['warning']}")
            print(f"    Alternative: {d['alternative']}")
```

if **name** == “**main**”:
test_sensor()
