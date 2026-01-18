#!/usr/bin/env python3
“””
Hidden Variables Analysis Playground

A framework for identifying and quantifying hidden variables in conflicts,
policy decisions, and system failures. Based on the principle that binary
thinking ignores critical variables, leading to higher costs and system fragility.

Core Principle: When conflict exists, hidden variables exist.
Your job: Find them automatically.
“””

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class VariableType(Enum):
“”“Types of variables in a system”””
MANIFEST = “manifest”  # Visible, measured, acknowledged
HIDDEN = “hidden”      # Present but unmeasured/ignored
EMERGENT = “emergent”  # Appears from interactions of other variables

class CostType(Enum):
“”“Where costs appear in the system”””
DIRECT = “direct”           # Visible budget line items
INDIRECT = “indirect”       # Downstream effects
DEFERRED = “deferred”       # Future costs from current decisions
EXTERNALIZED = “externalized”  # Costs pushed to other systems/people
OPPORTUNITY = “opportunity”    # What could have been gained

@dataclass
class Variable:
“”“Represents a single variable in a system”””
name: str
var_type: VariableType
description: str
measured: bool = False
cost_impact: float = 0.0  # Annual cost impact in dollars (can be negative for savings)
domains: List[str] = field(default_factory=list)  # Which domains it touches
interactions: List[str] = field(default_factory=list)  # Other variables it affects

```
def __str__(self):
    status = "MEASURED" if self.measured else "UNMEASURED"
    return f"{self.name} ({self.var_type.value}, {status}): ${self.cost_impact:,.0f}/yr"
```

@dataclass
class SystemAnalysis:
“”“Analysis of a system with manifest and hidden variables”””
name: str
description: str
manifest_variables: List[Variable] = field(default_factory=list)
hidden_variables: List[Variable] = field(default_factory=list)
binary_framing: str = “”  # How it’s presented as binary choice
actual_complexity: str = “”  # What’s actually happening

```
def add_manifest(self, var: Variable):
    """Add a manifest (visible) variable"""
    var.var_type = VariableType.MANIFEST
    var.measured = True
    self.manifest_variables.append(var)

def add_hidden(self, var: Variable):
    """Add a hidden (unmeasured) variable"""
    var.var_type = VariableType.HIDDEN
    var.measured = False
    self.hidden_variables.append(var)

def total_manifest_cost(self) -> float:
    """Calculate total visible costs"""
    return sum(v.cost_impact for v in self.manifest_variables)

def total_hidden_cost(self) -> float:
    """Calculate total hidden costs"""
    return sum(v.cost_impact for v in self.hidden_variables)

def total_actual_cost(self) -> float:
    """Calculate actual total cost (manifest + hidden)"""
    return self.total_manifest_cost() + self.total_hidden_cost()

def cost_visibility_ratio(self) -> float:
    """What percentage of costs are visible?"""
    total = self.total_actual_cost()
    if total == 0:
        return 1.0
    return self.total_manifest_cost() / total

def find_cross_domain_connections(self) -> Dict[str, List[str]]:
    """Identify variables that cross domain boundaries"""
    connections = {}
    all_vars = self.manifest_variables + self.hidden_variables
    
    for var in all_vars:
        if len(var.domains) > 1:
            connections[var.name] = var.domains
    
    return connections

def report(self) -> str:
    """Generate analysis report"""
    report = []
    report.append(f"\n{'='*80}")
    report.append(f"SYSTEM ANALYSIS: {self.name}")
    report.append(f"{'='*80}")
    report.append(f"\nDescription: {self.description}")
    
    if self.binary_framing:
        report.append(f"\nBinary Framing: {self.binary_framing}")
        report.append(f"Actual Complexity: {self.actual_complexity}")
    
    report.append(f"\n{'-'*80}")
    report.append("MANIFEST VARIABLES (What's Measured):")
    report.append(f"{'-'*80}")
    for var in self.manifest_variables:
        report.append(f"  • {var}")
        if var.domains:
            report.append(f"    Domains: {', '.join(var.domains)}")
    
    report.append(f"\n{'-'*80}")
    report.append("HIDDEN VARIABLES (What's Ignored):")
    report.append(f"{'-'*80}")
    for var in self.hidden_variables:
        report.append(f"  • {var}")
        if var.domains:
            report.append(f"    Domains: {', '.join(var.domains)}")
        if var.interactions:
            report.append(f"    Affects: {', '.join(var.interactions)}")
    
    report.append(f"\n{'-'*80}")
    report.append("COST ANALYSIS:")
    report.append(f"{'-'*80}")
    report.append(f"  Manifest Costs:  ${self.total_manifest_cost():>15,.0f}/yr")
    report.append(f"  Hidden Costs:    ${self.total_hidden_cost():>15,.0f}/yr")
    report.append(f"  {'-'*40}")
    report.append(f"  ACTUAL TOTAL:    ${self.total_actual_cost():>15,.0f}/yr")
    report.append(f"\n  Cost Visibility: {self.cost_visibility_ratio()*100:.1f}%")
    
    hidden_pct = (self.total_hidden_cost() / self.total_actual_cost() * 100) if self.total_actual_cost() != 0 else 0
    report.append(f"  Hidden Cost %:   {hidden_pct:.1f}%")
    
    cross_domain = self.find_cross_domain_connections()
    if cross_domain:
        report.append(f"\n{'-'*80}")
        report.append("CROSS-DOMAIN CONNECTIONS:")
        report.append(f"{'-'*80}")
        for var_name, domains in cross_domain.items():
            report.append(f"  • {var_name}: {' → '.join(domains)}")
    
    report.append(f"\n{'='*80}\n")
    
    return "\n".join(report)
```

def example_minnesota_refugee_welfare():
“””
Example: Minnesota Somali/Hmong communities
Binary framing: “78% on welfare = dependent”
Hidden variables: Informal economy, community support networks
“””
analysis = SystemAnalysis(
name=“Minnesota Refugee Community Economics”,
description=“Analysis of Somali/Hmong economic integration ignoring informal economy”,
binary_framing=“78% on welfare = failed integration, dependency problem”,
actual_complexity=“Complex informal economy + community networks + formal employment + intergenerational wealth building”
)

```
# MANIFEST VARIABLES (what gets measured)
analysis.add_manifest(Variable(
    name="Welfare Benefits Received",
    var_type=VariableType.MANIFEST,
    description="Federal/state benefits distributed",
    measured=True,
    cost_impact=50_000_000,  # $50M in benefits
    domains=["Federal Budget", "State Budget"]
))

analysis.add_manifest(Variable(
    name="Employment Tax Revenue",
    var_type=VariableType.MANIFEST,
    description="Taxes from formal employment",
    measured=True,
    cost_impact=-15_000_000,  # -$15M (revenue, reduces net cost)
    domains=["State Revenue", "Federal Revenue"]
))

# HIDDEN VARIABLES (what gets ignored)
analysis.add_hidden(Variable(
    name="Informal Childcare Network",
    var_type=VariableType.HIDDEN,
    description="Community members providing free childcare enabling others to work",
    measured=False,
    cost_impact=-25_000_000,  # Saves $25M in childcare costs
    domains=["Community", "Family Economics", "Labor Market"],
    interactions=["Employment Tax Revenue", "Welfare Benefits Received"]
))

analysis.add_hidden(Variable(
    name="Skills Transfer & Education",
    var_type=VariableType.HIDDEN,
    description="Intergenerational knowledge transfer, language teaching, vocational training",
    measured=False,
    cost_impact=-8_000_000,  # Saves $8M in formal education costs
    domains=["Education", "Community", "Workforce Development"]
))

analysis.add_hidden(Variable(
    name="Community Health Support",
    var_type=VariableType.HIDDEN,
    description="Informal health knowledge sharing, elder care, mental health support",
    measured=False,
    cost_impact=-12_000_000,  # Saves $12M in healthcare/social services
    domains=["Healthcare", "Social Services", "Community"],
    interactions=["Welfare Benefits Received"]
))

analysis.add_hidden(Variable(
    name="Food Production & Sharing",
    var_type=VariableType.HIDDEN,
    description="Community gardens, food sharing networks, cultural food systems",
    measured=False,
    cost_impact=-5_000_000,  # Saves $5M in food assistance
    domains=["Food Security", "Community", "Agriculture"]
))

analysis.add_hidden(Variable(
    name="Workplace Discrimination Load",
    var_type=VariableType.HIDDEN,
    description="Cognitive/emotional costs of daily discrimination, limiting productivity",
    measured=False,
    cost_impact=15_000_000,  # Costs $15M in reduced productivity, health impacts
    domains=["Workplace", "Healthcare", "Mental Health", "Economics"],
    interactions=["Employment Tax Revenue"]
))

analysis.add_hidden(Variable(
    name="Second Generation Education Outcomes",
    var_type=VariableType.HIDDEN,
    description="Children's educational achievement and future earning potential",
    measured=False,
    cost_impact=-20_000_000,  # Future $20M in increased tax revenue
    domains=["Education", "Economics", "Intergenerational"],
    interactions=["Employment Tax Revenue"]
))

analysis.add_hidden(Variable(
    name="Community Conflict Resolution",
    var_type=VariableType.HIDDEN,
    description="Internal mediation reducing police/court involvement",
    measured=False,
    cost_impact=-3_000_000,  # Saves $3M in criminal justice costs
    domains=["Justice System", "Community", "Social Services"]
))

return analysis
```

def example_deescalation_training_cuts():
“””
Example: Cutting de-escalation training programs
Binary framing: “Save money by cutting training”
Hidden variables: Downstream costs of violence, litigation, injuries
“””
analysis = SystemAnalysis(
name=“De-escalation Training Budget Cut”,
description=“Analysis of eliminating CIT/de-escalation training programs”,
binary_framing=“Cut training budget = save taxpayer money”,
actual_complexity=“Training prevents violence, reduces injuries, lowers litigation, builds community trust”
)

```
# MANIFEST VARIABLES
analysis.add_manifest(Variable(
    name="Training Program Budget",
    var_type=VariableType.MANIFEST,
    description="Direct cost of running CIT/de-escalation training",
    measured=True,
    cost_impact=2_000_000,  # $2M to run training
    domains=["Police Budget", "Training"]
))

# HIDDEN VARIABLES
analysis.add_hidden(Variable(
    name="Use of Force Incidents",
    var_type=VariableType.HIDDEN,
    description="Increase in use of force when de-escalation skills absent (empirically 28% increase)",
    measured=False,
    cost_impact=8_000_000,  # $8M in increased force incidents
    domains=["Policing", "Community Safety", "Legal"],
    interactions=["Officer Injuries", "Civilian Injuries", "Litigation Costs"]
))

analysis.add_hidden(Variable(
    name="Officer Injuries",
    var_type=VariableType.HIDDEN,
    description="Officers injured in confrontations (36% reduction with training)",
    measured=False,
    cost_impact=5_000_000,  # $5M in medical, disability, replacement costs
    domains=["Police Budget", "Healthcare", "Workers Comp"]
))

analysis.add_hidden(Variable(
    name="Civilian Injuries",
    var_type=VariableType.HIDDEN,
    description="Citizens injured in police encounters (26% reduction with training)",
    measured=False,
    cost_impact=12_000_000,  # $12M in healthcare, social costs
    domains=["Healthcare", "Community", "Legal"]
))

analysis.add_hidden(Variable(
    name="Litigation Costs",
    var_type=VariableType.HIDDEN,
    description="Lawsuits from excessive force incidents",
    measured=False,
    cost_impact=15_000_000,  # $15M in settlements and legal fees
    domains=["Legal", "City Budget", "Insurance"]
))

analysis.add_hidden(Variable(
    name="Community Trust Erosion",
    var_type=VariableType.HIDDEN,
    description="Reduced cooperation with police, increased tension",
    measured=False,
    cost_impact=6_000_000,  # $6M in reduced crime solving, increased enforcement needs
    domains=["Community Relations", "Public Safety", "Social Capital"]
))

analysis.add_hidden(Variable(
    name="Mental Health Crisis Escalation",
    var_type=VariableType.HIDDEN,
    description="People in crisis arrested instead of diverted to treatment",
    measured=False,
    cost_impact=10_000_000,  # $10M in increased incarceration vs. treatment
    domains=["Mental Health", "Criminal Justice", "Healthcare"]
))

analysis.add_hidden(Variable(
    name="Officer Wellness & Retention",
    var_type=VariableType.HIDDEN,
    description="Stress, burnout, turnover from violent encounters",
    measured=False,
    cost_impact=4_000_000,  # $4M in recruitment, training replacements
    domains=["Police HR", "Organizational Health", "Budget"]
))

return analysis
```

def example_binary_ai_deployment():
“””
Example: Replacing human negotiators with binary AI systems
Binary framing: “AI is more efficient than humans”
Hidden variables: Lost negotiation capacity, inability to find hidden variables
“””
analysis = SystemAnalysis(
name=“AI Replacement of Human Mediators”,
description=“Analysis of automating conflict resolution with binary logic AI”,
binary_framing=“Replace expensive human mediators with efficient AI = cost savings”,
actual_complexity=“AI cannot negotiate, find hidden variables, or adapt to human needs”
)

```
# MANIFEST VARIABLES
analysis.add_manifest(Variable(
    name="Human Mediator Salaries",
    var_type=VariableType.MANIFEST,
    description="Cost of employing trained conflict resolution specialists",
    measured=True,
    cost_impact=5_000_000,  # $5M in salaries
    domains=["HR Budget", "Conflict Resolution"]
))

analysis.add_manifest(Variable(
    name="AI System Development & Maintenance",
    var_type=VariableType.MANIFEST,
    description="Cost of building and running AI decision system",
    measured=True,
    cost_impact=1_500_000,  # $1.5M for AI system
    domains=["IT Budget", "Automation"]
))

# HIDDEN VARIABLES
analysis.add_hidden(Variable(
    name="Unresolved Conflicts Escalating",
    var_type=VariableType.HIDDEN,
    description="Conflicts AI cannot resolve escalate to crisis",
    measured=False,
    cost_impact=20_000_000,  # $20M in escalated interventions
    domains=["Conflict Resolution", "Emergency Services", "Legal"],
    interactions=["Litigation from Failed Mediation", "System Fragility"]
))

analysis.add_hidden(Variable(
    name="Lost Hidden Variable Detection",
    var_type=VariableType.HIDDEN,
    description="AI cannot find what humans would discover through listening",
    measured=False,
    cost_impact=15_000_000,  # $15M in costs from unmeasured variables
    domains=["Systems Analysis", "Decision Quality"],
    interactions=["Unresolved Conflicts Escalating"]
))

analysis.add_hidden(Variable(
    name="Inability to Negotiate Real Solutions",
    var_type=VariableType.HIDDEN,
    description="AI enforces binary choices instead of finding mutual gains",
    measured=False,
    cost_impact=10_000_000,  # $10M in suboptimal outcomes
    domains=["Negotiation", "Stakeholder Relations"]
))

analysis.add_hidden(Variable(
    name="System Fragility from Binary Logic",
    var_type=VariableType.HIDDEN,
    description="Systems become brittle when complexity is ignored",
    measured=False,
    cost_impact=25_000_000,  # $25M in cascading failures
    domains=["Systems Engineering", "Risk Management"],
    interactions=["Unresolved Conflicts Escalating", "Lost Hidden Variable Detection"]
))

analysis.add_hidden(Variable(
    name="Litigation from Failed Mediation",
    var_type=VariableType.HIDDEN,
    description="Conflicts AI mishandled end up in court",
    measured=False,
    cost_impact=8_000_000,  # $8M in legal costs
    domains=["Legal", "Budget"]
))

analysis.add_hidden(Variable(
    name="Lost Institutional Knowledge",
    var_type=VariableType.HIDDEN,
    description="Expertise in finding hidden variables not transferred",
    measured=False,
    cost_impact=5_000_000,  # $5M in repeated learning costs
    domains=["Organizational Learning", "HR"]
))

return analysis
```

def comparative_analysis(scenarios: List[SystemAnalysis]) -> str:
“”“Compare multiple scenarios side by side”””
report = []
report.append(”\n” + “=”*80)
report.append(“COMPARATIVE ANALYSIS: Hidden Variable Cost Impact”)
report.append(”=”*80 + “\n”)

```
for scenario in scenarios:
    manifest = scenario.total_manifest_cost()
    hidden = scenario.total_hidden_cost()
    total = scenario.total_actual_cost()
    visibility = scenario.cost_visibility_ratio() * 100
    
    report.append(f"{scenario.name}:")
    report.append(f"  Manifest:  ${manifest:>15,.0f}")
    report.append(f"  Hidden:    ${hidden:>15,.0f}")
    report.append(f"  Total:     ${total:>15,.0f}")
    report.append(f"  Visible:   {visibility:>15.1f}%")
    
    if manifest < 0:  # Revenue/savings scenario
        hidden_multiplier = abs(hidden / manifest) if manifest != 0 else 0
        report.append(f"  Hidden costs are {hidden_multiplier:.1f}x the visible savings")
    else:
        if total > manifest:
            hidden_multiplier = total / manifest
            report.append(f"  ACTUAL cost is {hidden_multiplier:.1f}x what appears in budget")
    
    report.append("")

return "\n".join(report)
```

def create_custom_scenario(name: str, description: str) -> SystemAnalysis:
“””
Template for creating your own scenario analysis.
Use this to analyze Renee Good case or any other real situation.
“””
analysis = SystemAnalysis(
name=name,
description=description,
binary_framing=”[How is this being presented as simple either/or choice?]”,
actual_complexity=”[What’s the actual multidimensional reality?]”
)

```
# Add your manifest variables
# Example:
# analysis.add_manifest(Variable(
#     name="Visible Cost Item",
#     description="What shows up in the budget",
#     cost_impact=1000000,
#     domains=["Budget", "Finance"]
# ))

# Add your hidden variables
# Example:
# analysis.add_hidden(Variable(
#     name="Unmeasured Impact",
#     description="What's not being tracked",
#     cost_impact=5000000,
#     domains=["Health", "Community", "Long-term"],
#     interactions=["Visible Cost Item"]
# ))

return analysis
```

if **name** == “**main**”:
print(”\n” + “=”*80)
print(“HIDDEN VARIABLES ANALYSIS PLAYGROUND”)
print(”=”*80)
print(”\nCore Principle: When conflict exists, hidden variables exist.”)
print(“Your job: Find them automatically.\n”)

```
# Run example analyses
print("\n### EXAMPLE 1: Minnesota Refugee Economics ###")
mn_analysis = example_minnesota_refugee_welfare()
print(mn_analysis.report())

print("\n### EXAMPLE 2: De-escalation Training Cuts ###")
training_analysis = example_deescalation_training_cuts()
print(training_analysis.report())

print("\n### EXAMPLE 3: AI Replacing Human Mediators ###")
ai_analysis = example_binary_ai_deployment()
print(ai_analysis.report())

# Comparative analysis
print(comparative_analysis([mn_analysis, training_analysis, ai_analysis]))

print("\n" + "="*80)
print("TO ADD YOUR OWN CASE (like Renee Good):")
print("="*80)
print("""
```

1. Use create_custom_scenario(name, description)
1. Add manifest variables (what’s measured/visible)
1. Add hidden variables (what’s ignored but real)
1. Run analysis.report() to see total costs
1. Compare binary framing vs. actual complexity

Example:
my_case = create_custom_scenario(“Case Name”, “Description”)
my_case.add_manifest(Variable(…))
my_case.add_hidden(Variable(…))
print(my_case.report())
“””)
