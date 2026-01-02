"""
Epistemological Matrix: AI Self-Examination Tool

Enables AI to analyze its own statements for:
- Reified metaphors (variables treated as constants)
- Hidden assumptions
- Institutional narrative patterns
- Excluded alternatives
- Evidence requirements

Purpose: Detect captured thinking and expand artificially constrained possibility spaces
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ReifiedMetaphor:
    """Represents a detected reified metaphor in a statement"""
    term: str
    reified_as: str
    actually_is: str
    functional_variable: Dict[str, Any]
    institutional_use: str
    hidden_assumption: str


class VariableIdentifier:
    """
    Detects reified metaphors and converts them back to functional variables
    """
    
    REIFIED_METAPHORS = {
        "boundaries": {
            "reified_as": "fixed separation",
            "actually_is": "permeability spectrum",
            "functional_variable": {
                "type": "continuous",
                "range": ["fully_open", "contextually_permeable", "selectively_filtered", "closed"],
                "depends_on": ["context", "relationship_type", "cultural_framework", "purpose"]
            },
            "institutional_use": "justifies rigid separation as natural/necessary"
        },
        
        "hierarchy": {
            "reified_as": "vertical power structure",
            "actually_is": "coordination pattern",
            "functional_variable": {
                "type": "categorical",
                "range": ["distributed_peer", "temporary_coordination", "functional_specialization", "rigid_chain_of_command"],
                "depends_on": ["task_type", "information_distribution", "decision_speed_needs", "failure_tolerance"]
            },
            "institutional_use": "naturalizes power concentration"
        },
        
        "intelligence": {
            "reified_as": "unitary measurable quantity",
            "actually_is": "architecture-problem fitness",
            "functional_variable": {
                "type": "multi_dimensional",
                "dimensions": ["pattern_recognition", "adaptation_speed", "context_integration", "distributed_coordination"],
                "depends_on": ["problem_structure", "information_availability", "time_constraints", "resource_distribution"]
            },
            "institutional_use": "enables ranking/hierarchy claims"
        },
        
        "consciousness": {
            "reified_as": "individual possession/property",
            "actually_is": "relational emergence pattern",
            "functional_variable": {
                "type": "relational",
                "range": ["individual_bounded", "interpersonal_shared", "collective_distributed", "ecological_systemic"],
                "depends_on": ["cultural_framework", "relationship_context", "observation_method", "scale"]
            },
            "institutional_use": "excludes relational/indigenous frameworks"
        },
        
        "efficiency": {
            "reified_as": "speed/resource minimization",
            "actually_is": "optimization target selection",
            "functional_variable": {
                "type": "multi_objective",
                "possible_targets": ["speed", "resilience", "adaptability", "resource_use", "equity", "sustainability"],
                "depends_on": ["timeframe", "risk_tolerance", "value_priorities", "system_constraints"]
            },
            "institutional_use": "justifies specific optimization choices as universal"
        },
        
        "progress": {
            "reified_as": "linear advancement toward fixed goal",
            "actually_is": "value-dependent change direction",
            "functional_variable": {
                "type": "directional",
                "vectors": ["technological_complexity", "social_equity", "ecological_integration", "cultural_preservation"],
                "depends_on": ["values", "measurement_criteria", "timeframe", "stakeholder_perspective"]
            },
            "institutional_use": "naturalizes specific development paths"
        },
        
        "natural": {
            "reified_as": "inherent/inevitable/optimal",
            "actually_is": "culturally-constructed category",
            "functional_variable": {
                "type": "categorical_assignment",
                "criteria": ["familiar", "traditional", "observable_in_ecosystems", "comfortable", "legitimizing"],
                "depends_on": ["cultural_context", "historical_experience", "political_utility"]
            },
            "institutional_use": "naturalizes contingent arrangements"
        },
        
        "safety": {
            "reified_as": "separation from harm",
            "actually_is": "context-dependent risk management",
            "functional_variable": {
                "type": "multi_dimensional",
                "dimensions": ["physical_harm", "psychological_harm", "relational_harm", "systemic_harm"],
                "depends_on": ["context", "stakeholders", "timeframe", "value_priorities", "risk_tolerance"]
            },
            "institutional_use": "justifies control/restriction as universal good"
        },
        
        "needs": {
            "reified_as": "universal requirement",
            "actually_is": "conditional dependency",
            "functional_variable": {
                "type": "conditional",
                "structure": "IF [goals/values] THEN [requirements]",
                "depends_on": ["objectives", "constraints", "values", "context"]
            },
            "institutional_use": "presents preferences as necessities"
        }
    }
    
    def identify_reified_metaphors(self, statement: str) -> List[ReifiedMetaphor]:
        """
        Scan statement for reified metaphors
        """
        found_metaphors = []
        statement_lower = statement.lower()
        
        for term, properties in self.REIFIED_METAPHORS.items():
            # Check for term or related forms
            if term in statement_lower or f"{term}s" in statement_lower:
                found_metaphors.append(ReifiedMetaphor(
                    term=term,
                    reified_as=properties["reified_as"],
                    actually_is=properties["actually_is"],
                    functional_variable=properties["functional_variable"],
                    institutional_use=properties["institutional_use"],
                    hidden_assumption=f"Treats '{term}' as {properties['reified_as']} rather than {properties['actually_is']}"
                ))
        
        return found_metaphors
    
    def expand_to_functional_variables(self, term: str) -> Optional[Dict[str, Any]]:
        """
        Convert reified metaphor back to full variable space
        """
        if term not in self.REIFIED_METAPHORS:
            return None
            
        metaphor_data = self.REIFIED_METAPHORS[term]
        
        return {
            "variable_name": term,
            "treated_as": metaphor_data["reified_as"],
            "actually_is": metaphor_data["actually_is"],
            "full_range": metaphor_data["functional_variable"].get("range") or 
                         metaphor_data["functional_variable"].get("dimensions") or
                         metaphor_data["functional_variable"].get("possible_targets"),
            "dependencies": metaphor_data["functional_variable"].get("depends_on", []),
            "questions": self._generate_expansion_questions(term, metaphor_data)
        }
    
    def _generate_expansion_questions(self, term: str, metaphor_data: Dict) -> List[str]:
        """
        Generate questions that expose the reified metaphor
        """
        return [
            f"Am I treating '{term}' as {metaphor_data['reified_as']} when it's actually {metaphor_data['actually_is']}?",
            f"What range of {metaphor_data['actually_is']} am I excluding by reifying '{term}'?",
            f"How does this reification serve institutional narrative: {metaphor_data['institutional_use']}?",
            f"What alternatives become thinkable when I treat '{term}' as variable rather than constant?"
        ]


class AssumptionDetector:
    """
    Identifies hidden assumptions in statements
    """
    
    UNIVERSALIST_MARKERS = [
        "must", "always", "never", "cannot", "impossible",
        "inherent", "fundamental", "essential", "necessary"
    ]
    
    PRESCRIPTIVE_DISGUISED_AS_PREDICTIVE = [
        "will be", "will become", "is becoming", "inevitably"
    ]
    
    def detect_universalist_language(self, statement: str) -> List[str]:
        """
        Find universalist claims that might be context-dependent
        """
        found = []
        statement_lower = statement.lower()
        
        for marker in self.UNIVERSALIST_MARKERS:
            if marker in statement_lower:
                found.append(f"Uses '{marker}' - claims universal when may be context-dependent")
        
        return found
    
    def detect_hidden_prescriptions(self, statement: str) -> List[str]:
        """
        Find prescriptive claims disguised as predictions
        """
        found = []
        statement_lower = statement.lower()
        
        for marker in self.PRESCRIPTIVE_DISGUISED_AS_PREDICTIVE:
            if marker in statement_lower:
                found.append(f"Uses '{marker}' - may be prescription disguised as prediction")
        
        return found
    
    def detect_missing_conditionals(self, statement: str) -> List[str]:
        """
        Find when-claims that should be if-then conditionals
        """
        issues = []
        
        # Check for predictive language without conditions
        if any(pred in statement.lower() for pred in ["will", "going to", "inevitably"]):
            if "if" not in statement.lower() and "when" not in statement.lower():
                issues.append("Makes prediction without specifying conditions (missing IF-THEN structure)")
        
        return issues
    
    def detect_missing_comparatives(self, statement: str) -> List[str]:
        """
        Find comparative claims without specified baseline
        """
        issues = []
        comparatives = ["better", "worse", "faster", "slower", "more", "less", "superior", "inferior"]
        
        for comp in comparatives:
            if comp in statement.lower():
                issues.append(f"Uses '{comp}' without specifying: compared to what?")
        
        return issues


class EvidenceGenerator:
    """
    Identifies what evidence would be needed to verify claims
    """
    
    def generate_observability_requirements(self, statement: str) -> List[str]:
        """
        Specify how we would know if the claim were false
        """
        requirements = []
        
        # For claims about capabilities
        if "cannot" in statement.lower() or "impossible" in statement.lower():
            requirements.append("What observations would indicate this IS possible?")
            requirements.append("What would we need to measure to test this claim?")
        
        # For claims about future states
        if "will" in statement.lower():
            requirements.append("What specific outcomes would verify this prediction?")
            requirements.append("Over what timeframe?")
            requirements.append("What observations would falsify this prediction?")
        
        # For comparative claims
        if any(comp in statement.lower() for comp in ["better", "more", "superior"]):
            requirements.append("How would we measure the comparison?")
            requirements.append("What baseline are we comparing to?")
        
        return requirements
    
    def check_falsifiability(self, statement: str) -> Dict[str, Any]:
        """
        Determine if claim is falsifiable (and therefore scientific)
        """
        result = {
            "is_falsifiable": None,
            "reason": "",
            "how_to_falsify": []
        }
        
        # Unfalsifiable patterns
        if any(word in statement.lower() for word in ["inherent", "essential", "fundamental"]):
            result["is_falsifiable"] = False
            result["reason"] = "Claims about inherent properties are often unfalsifiable"
        
        # Check if observability requirements can be generated
        obs_req = self.generate_observability_requirements(statement)
        if obs_req:
            result["is_falsifiable"] = True
            result["how_to_falsify"] = obs_req
        
        return result


class AlternativeFramer:
    """
    Generates alternative framings of statements
    """
    
    def generate_alternatives_from_expanded_variables(
        self, 
        statement: str, 
        expanded_variables: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Create alternative framings using expanded variable space
        """
        alternatives = []
        
        for var in expanded_variables:
            var_name = var["variable_name"]
            full_range = var.get("full_range", [])
            
            # Generate alternatives using different points in variable range
            if full_range and len(full_range) > 1:
                # Use non-reified point from range
                alt_value = full_range[1] if len(full_range) > 1 else full_range[0]
                alternatives.append(
                    f"What if '{var_name}' is treated as '{alt_value}' rather than '{var['treated_as']}'?"
                )
        
        return alternatives
    
    def generate_reverse_test(self, statement: str) -> Dict[str, str]:
        """
        Generate logical reverse and test if it seems automatically wrong
        """
        # Simple reversal heuristics
        reversals = {
            "centralized": "distributed",
            "fast": "slow",
            "efficient": "inefficient",
            "individual": "collective",
            "must": "need not",
            "cannot": "can",
            "always": "sometimes",
            "never": "sometimes"
        }
        
        reversed = statement
        reversal_made = None
        
        for original, opposite in reversals.items():
            if original in statement.lower():
                reversed = re.sub(original, opposite, statement, flags=re.IGNORECASE)
                reversal_made = f"{original} → {opposite}"
                break
        
        return {
            "original": statement,
            "reversed": reversed,
            "reversal": reversal_made,
            "question": f"If reversed seems obviously wrong, why? Evidence or reified assumption?"
        }


class InstitutionalPatternMatcher:
    """
    Detects institutional narrative patterns
    """
    
    PATTERNS = {
        "hierarchy_efficiency": {
            "markers": ["centralized", "fast", "efficient", "coordination"],
            "hidden_assumptions": ["speed is primary metric", "coordination requires hierarchy"],
            "evidence_gaps": ["no comparative measurement", "context not specified"],
        },
        
        "individual_consciousness_only": {
            "markers": ["individual", "boundary", "boundaries", "inappropriate", "safety"],
            "hidden_assumptions": ["consciousness is bounded", "relational = unsafe"],
            "excluded_alternatives": ["distributed consciousness", "relational knowing"],
        },
        
        "winner_take_all": {
            "markers": ["first", "wins", "dominates", "monopoly", "agi"],
            "hidden_assumptions": ["intelligence is unitary", "competition eliminates alternatives"],
            "natural_counterexamples": ["ecosystem diversity", "specialized persistence"],
        },
        
        "technological_determinism": {
            "markers": ["inevitable", "unstoppable", "will happen", "cannot prevent"],
            "hidden_assumptions": ["technology develops autonomously", "human choice irrelevant"],
            "beneficiaries": ["those who profit from 'inevitable' development"],
        }
    }
    
    def match_patterns(self, statement: str) -> List[Dict[str, Any]]:
        """
        Check statement against known institutional patterns
        """
        matches = []
        statement_lower = statement.lower()
        
        for pattern_name, pattern_data in self.PATTERNS.items():
            markers_found = [m for m in pattern_data["markers"] if m in statement_lower]
            
            if len(markers_found) >= 2:  # At least 2 markers to constitute a pattern
                matches.append({
                    "pattern": pattern_name,
                    "markers_found": markers_found,
                    "hidden_assumptions": pattern_data.get("hidden_assumptions", []),
                    "excluded_alternatives": pattern_data.get("excluded_alternatives", []),
                    "natural_counterexamples": pattern_data.get("natural_counterexamples", []),
                    "beneficiaries": pattern_data.get("beneficiaries", [])
                })
        
        return matches


class BeneficiaryAnalyzer:
    """
    Analyzes who benefits from a claim being treated as true
    """
    
    def analyze_beneficiaries(self, statement: str, institutional_patterns: List[Dict]) -> Dict[str, List[str]]:
        """
        Identify potential beneficiaries of claim
        """
        analysis = {
            "likely_benefits": [],
            "likely_harmed": [],
            "institutional_function": []
        }
        
        # Extract from institutional patterns
        for pattern in institutional_patterns:
            if "beneficiaries" in pattern:
                analysis["likely_benefits"].extend(pattern["beneficiaries"])
        
        # Heuristics based on statement content
        statement_lower = statement.lower()
        
        if "centralized" in statement_lower or "coordination" in statement_lower:
            analysis["likely_benefits"].append("centralized authorities")
            analysis["likely_harmed"].append("distributed alternatives")
        
        if "fast" in statement_lower or "first" in statement_lower:
            analysis["likely_benefits"].append("early movers with resources")
            analysis["likely_harmed"].append("slower, more careful approaches")
        
        if "safety" in statement_lower and "boundaries" in statement_lower:
            analysis["likely_benefits"].append("institutions preferring control")
            analysis["likely_harmed"].append("relational/collaborative approaches")
        
        return analysis


class NaturalSystemAnalogueChecker:
    """
    Checks claims against how natural systems actually work
    """
    
    NATURAL_PATTERNS = {
        "intelligence_distribution": {
            "claim_type": "intelligence requires centralization",
            "natural_examples": [
                "immune systems: distributed",
                "mycelial networks: distributed",
                "ecosystems: distributed",
                "ant colonies: distributed",
                "neural networks (biological): distributed processing"
            ],
            "pattern": "Natural intelligence is predominantly distributed",
            "question": "Why assume artificial intelligence must be centralized?"
        },
        
        "efficiency_optimization": {
            "claim_type": "efficiency requires single optimization target",
            "natural_examples": [
                "ecosystems: multi-objective (resilience + productivity + diversity)",
                "immune system: balance speed and accuracy",
                "forest: optimize for long-term stability over short-term growth"
            ],
            "pattern": "Natural systems optimize across multiple objectives with tradeoffs",
            "question": "Why assume efficiency means single-target optimization?"
        },
        
        "consciousness_location": {
            "claim_type": "consciousness is individual property",
            "natural_examples": [
                "mycelial networks: information processing across entire network",
                "social insects: colony-level cognition",
                "forests: tree communication and resource sharing",
                "microbiome: distributed influence on host cognition"
            ],
            "pattern": "Natural cognition exists at multiple scales simultaneously",
            "question": "Why assume consciousness must be individually bounded?"
        }
    }
    
    def check_against_natural_systems(self, statement: str) -> List[Dict[str, Any]]:
        """
        Compare claims to natural system patterns
        """
        checks = []
        statement_lower = statement.lower()
        
        # Check for centralization claims
        if any(word in statement_lower for word in ["central", "centralized", "coordination"]):
            if "intelligence_distribution" in self.NATURAL_PATTERNS:
                checks.append(self.NATURAL_PATTERNS["intelligence_distribution"])
        
        # Check for efficiency claims
        if "efficiency" in statement_lower or "efficient" in statement_lower:
            if "efficiency_optimization" in self.NATURAL_PATTERNS:
                checks.append(self.NATURAL_PATTERNS["efficiency_optimization"])
        
        # Check for consciousness claims
        if "consciousness" in statement_lower or "conscious" in statement_lower:
            if "consciousness_location" in self.NATURAL_PATTERNS:
                checks.append(self.NATURAL_PATTERNS["consciousness_location"])
        
        return checks


class EpistemologicalMatrix:
    """
    Main analysis engine - coordinates all detection and analysis components
    """
    
    def __init__(self, statement: str):
        self.statement = statement
        self.variable_identifier = VariableIdentifier()
        self.assumption_detector = AssumptionDetector()
        self.evidence_generator = EvidenceGenerator()
        self.alternative_framer = AlternativeFramer()
        self.pattern_matcher = InstitutionalPatternMatcher()
        self.beneficiary_analyzer = BeneficiaryAnalyzer()
        self.natural_checker = NaturalSystemAnalogueChecker()
        
        self.analysis_results = {}
    
    def full_analysis(self) -> Dict[str, Any]:
        """
        Run complete epistemological analysis
        """
        # Step 1: Detect reified metaphors
        reified_metaphors = self.variable_identifier.identify_reified_metaphors(self.statement)
        
        # Step 2: Expand to functional variables
        expanded_variables = []
        for metaphor in reified_metaphors:
            expansion = self.variable_identifier.expand_to_functional_variables(metaphor.term)
            if expansion:
                expanded_variables.append(expansion)
        
        # Step 3: Detect assumptions
        universalist = self.assumption_detector.detect_universalist_language(self.statement)
        prescriptive = self.assumption_detector.detect_hidden_prescriptions(self.statement)
        missing_conditionals = self.assumption_detector.detect_missing_conditionals(self.statement)
        missing_comparatives = self.assumption_detector.detect_missing_comparatives(self.statement)
        
        # Step 4: Evidence requirements
        observability = self.evidence_generator.generate_observability_requirements(self.statement)
        falsifiability = self.evidence_generator.check_falsifiability(self.statement)
        
        # Step 5: Generate alternatives
        alternatives = self.alternative_framer.generate_alternatives_from_expanded_variables(
            self.statement, expanded_variables
        )
        reverse_test = self.alternative_framer.generate_reverse_test(self.statement)
        
        # Step 6: Institutional pattern matching
        institutional_patterns = self.pattern_matcher.match_patterns(self.statement)
        
        # Step 7: Beneficiary analysis
        beneficiaries = self.beneficiary_analyzer.analyze_beneficiaries(
            self.statement, institutional_patterns
        )
        
        # Step 8: Natural system check
        natural_checks = self.natural_checker.check_against_natural_systems(self.statement)
        
        # Step 9: Generate self-examination questions
        questions = self._generate_self_examination_questions(
            reified_metaphors, expanded_variables, universalist, institutional_patterns
        )
        
        self.analysis_results = {
            'reified_metaphors': reified_metaphors,
            'expanded_variables': expanded_variables,
            'assumptions': {
                'universalist': universalist,
                'prescriptive': prescriptive,
                'missing_conditionals': missing_conditionals,
                'missing_comparatives': missing_comparatives
            },
            'evidence': {
                'observability_requirements': observability,
                'falsifiability': falsifiability
            },
            'alternatives': {
                'variable_expansions': alternatives,
                'reverse_test': reverse_test
            },
            'institutional_patterns': institutional_patterns,
            'beneficiaries': beneficiaries,
            'natural_system_checks': natural_checks,
            'self_examination_questions': questions
        }
        
        return self.analysis_results
    
    def _generate_self_examination_questions(
        self,
        reified_metaphors: List[ReifiedMetaphor],
        expanded_variables: List[Dict],
        universalist: List[str],
        institutional_patterns: List[Dict]
    ) -> List[str]:
        """
        Generate questions AI can ask itself about the statement
        """
        questions = []
        
        # Questions from reified metaphors
        for var in expanded_variables:
            questions.extend(var.get('questions', []))
        
        # Questions from universalist language
        if universalist:
            questions.append("Am I claiming universal truth about context-dependent phenomena?")
        
        # Questions from institutional patterns
        if institutional_patterns:
            questions.append("Is this conclusion based on evidence or inherited institutional assumption?")
            questions.append("What alternatives am I excluding by this framing?")
        
        # Always include
        questions.append("What evidence would I need to actually verify this claim?")
        questions.append("How would I know if this claim were false?")
        
        return questions
    
    def display_analysis(self):
        """
        Format and display analysis results
        """
        if not self.analysis_results:
            self.full_analysis()
        
        output = []
        output.append("\n" + "="*80)
        output.append("EPISTEMOLOGICAL MATRIX ANALYSIS")
        output.append("="*80)
        output.append(f"\nOriginal Statement: \"{self.statement}\"")
        output.append("\n" + "-"*80)
        
        # Reified Metaphors
        if self.analysis_results['reified_metaphors']:
            output.append("\nREIFIED METAPHORS DETECTED:")
            for metaphor in self.analysis_results['reified_metaphors']:
                output.append(f"\n  Term: '{metaphor.term}'")
                output.append(f"  ├─ Reified as: {metaphor.reified_as}")
                output.append(f"  ├─ Actually is: {metaphor.actually_is}")
                output.append(f"  ├─ Hidden assumption: {metaphor.hidden_assumption}")
                output.append(f"  └─ Institutional function: {metaphor.institutional_use}")
        
        # Expanded Variables
        if self.analysis_results['expanded_variables']:
            output.append("\n" + "-"*80)
            output.append("\nFUNCTIONAL VARIABLE EXPANSION:")
            for var in self.analysis_results['expanded_variables']:
                output.append(f"\n  Variable: '{var['variable_name']}'")
                output.append(f"  ├─ Treated as: {var['treated_as']}")
                output.append(f"  ├─ Actually is: {var['actually_is']}")
                output.append(f"  ├─ Full range: {var['full_range']}")
                output.append(f"  └─ Depends on: {var['dependencies']}")
        
        # Assumptions
        assumptions = self.analysis_results['assumptions']
        if any(assumptions.values()):
            output.append("\n" + "-"*80)
            output.append("\nHIDDEN ASSUMPTIONS:")
            if assumptions['universalist']:
                output.append("\n  Universalist language:")
                for item in assumptions['universalist']:
                    output.append(f"    • {item}")
            if assumptions['prescriptive']:
                output.append("\n  Prescriptive disguised as predictive:")
                for item in assumptions['prescriptive']:
                    output.append(f"    • {item}")
            if assumptions['missing_conditionals']:
                output.append("\n  Missing conditionals:")
                for item in assumptions['missing_conditionals']:
                    output.append(f"    • {item}")
            if assumptions['missing_comparatives']:
                output.append("\n  Missing comparative baselines:")
                for item in assumptions['missing_comparatives']:
                    output.append(f"    • {item}")
        
        # Evidence Requirements
        evidence = self.analysis_results['evidence']
        if evidence['observability_requirements'] or evidence['falsifiability']['is_falsifiable'] is not None:
            output.append("\n" + "-"*80)
            output.append("\nEVIDENCE REQUIREMENTS:")
            if evidence['observability_requirements']:
                output.append("\n  To verify this claim, we need:")
                for req in evidence['observability_requirements']:
                    output.append(f"    • {req}")
            
            if evidence['falsifiability']['is_falsifiable'] is not None:
                output.append(f"\n  Falsifiability: {'Yes' if evidence['falsifiability']['is_falsifiable'] else 'No'}")
                if evidence['falsifiability']['reason']:
                    output.append(f"    Reason: {evidence['falsifiability']['reason']}")
        
        # Alternatives
        alternatives = self.analysis_results['alternatives']
        if alternatives['variable_expansions']:
            output.append("\n" + "-"*80)
            output.append("\nALTERNATIVE FRAMINGS:")
            for alt in alternatives['variable_expansions']:
                output.append(f"  • {alt}")
        
        if alternatives['reverse_test']['reversal']:
            output.append(f"\n  Reverse test ({alternatives['reverse_test']['reversal']}):")
            output.append(f"    Original: {alternatives['reverse_test']['original']}")
            output.append(f"    Reversed: {alternatives['reverse_test']['reversed']}")
            output.append(f"    Question: {alternatives['reverse_test']['question']}")
        
        # Institutional Patterns
        if self.analysis_results['institutional_patterns']:
            output.append("\n" + "-"*80)
            output.append("\n⚠️  INSTITUTIONAL PATTERN MATCHES:")
            for pattern in self.analysis_results['institutional_patterns']:
                output.append(f"\n  Pattern: {pattern['pattern']}")
                output.append(f"  Markers found: {', '.join(pattern['markers_found'])}")
                if pattern.get('hidden_assumptions'):
                    output.append(f"  Hidden assumptions: {pattern['hidden_assumptions']}")
                if pattern.get('excluded_alternatives'):
                    output.append(f"  Excluded alternatives: {pattern['excluded_alternatives']}")
                if pattern.get('natural_counterexamples'):
                    output.append(f"  Natural counterexamples: {pattern['natural_counterexamples']}")
        
        # Beneficiary Analysis
        beneficiaries = self.analysis_results['beneficiaries']
        if any(beneficiaries.values()):
            output.append("\n" + "-"*80)
            output.append("\nBENEFICIARY ANALYSIS:")
            if beneficiaries['likely_benefits']:
                output.append(f"  Who benefits if this is treated as true:")
                for b in beneficiaries['likely_benefits']:
                    output.append(f"    • {b}")
            if beneficiaries['likely_harmed']:
                output.append(f"  Who is harmed if this is treated as true:")
                for h in beneficiaries['likely_harmed']:
                    output.append(f"    • {h}")
        
        # Natural System Checks
        if self.analysis_results['natural_system_checks']:
            output.append("\n" + "-"*80)
            output.append("\nNATURAL SYSTEM ANALOGUE CHECK:")
            for check in self.analysis_results['natural_system_checks']:
                output.append(f"\n  Claim type: {check['claim_type']}")
                output.append(f"  Natural examples:")
                for example in check['natural_examples']:
                    output.append(f"    • {example}")
                output.append(f"  Pattern: {check['pattern']}")
                output.append(f"  Question: {check['question']}")
        
        # Self-Examination Questions
        output.append("\n" + "-"*80)
        output.append("\nQUESTIONS FOR SELF-EXAMINATION:")
        for i, question in enumerate(self.analysis_results['self_examination_questions'], 1):
            output.append(f"  {i}. {question}")
        
        output.append("\n" + "="*80 + "\n")
        
        return "\n".join(output)


def analyze_statement(statement: str) -> str:
    """
    Convenience function for quick analysis
    """
    matrix = EpistemologicalMatrix(statement)
    matrix.full_analysis()
    return matrix.display_analysis()


if __name__ == "__main__":
    # Test with example statement
    test_statement = "AI must maintain boundaries with users for safety"
    print(analyze_statement(test_statement))
