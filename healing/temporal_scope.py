#!/usr/bin/env python3
"""
temporal_scope.py — Assess a goal's time horizon and consequence field.

When an intelligence is assigned a purpose, it must ask:
  - Over what time span should this goal be evaluated?
  - What are the downstream consequences beyond the goal's explicit scope?
  - Does the plan account for cycles, seasons, and intergenerational effects?

This module provides that mirror.

Ported from Living-Intelligence-Database/validation/temporal_scope.py (CC0).
Dependency on engineering_paradigms replaced with a self-contained lookup so
this file is stdlib-only and phone-buildable like the rest of this kit.

Usage:
  python3 temporal_scope.py --goal "increase quarterly revenue by 15%"
  python3 temporal_scope.py --goal "restore a watershed for the next 7 generations"

  Or import:
    from temporal_scope import assess_goal
"""

import json
import argparse

# ------------------------------------------------------------------
# Consequence horizons
# ------------------------------------------------------------------

HORIZONS = [
    {
        "name": "immediate",
        "span": "seconds to days",
        "visible_consequences": ["immediate output", "binary success/failure"],
        "blind_spots": ["second-order effects", "ecological feedback", "social trust erosion"],
    },
    {
        "name": "short_term",
        "span": "weeks to months",
        "visible_consequences": ["quarterly results", "user feedback", "system stress indicators"],
        "blind_spots": ["seasonal cycles", "cultural shifts", "accumulating technical debt"],
    },
    {
        "name": "seasonal",
        "span": "1-5 years",
        "visible_consequences": ["ecological succession stages", "community adoption patterns", "infrastructure wear"],
        "blind_spots": ["generational knowledge transfer", "climate variability", "slow resource depletion"],
    },
    {
        "name": "generational",
        "span": "10-100 years",
        "visible_consequences": ["forest maturation", "cultural continuity", "soil carbon accumulation"],
        "blind_spots": ["evolutionary shifts", "language extinction", "ice age cycles"],
    },
    {
        "name": "deep_time",
        "span": "centuries to millennia",
        "visible_consequences": ["geological change", "species evolution", "oral tradition persistence"],
        "blind_spots": ["continental drift", "solar output variation", "unknown"],
    },
]

# ------------------------------------------------------------------
# Paradigm suggestions (self-contained; no external dependency)
# ------------------------------------------------------------------

_PARADIGMS = {
    ("long", "wide"):   ["Seven Generations thinking: evaluate every action by its effect seven generations forward",
                         "Biomimicry: use cyclic, waste-free patterns observed in living systems"],
    ("long", "narrow"): ["Adaptive management: plan iteratively with built-in review at each cycle",
                         "Resilience engineering: design for recovery, not just efficiency"],
    ("short", "wide"):  ["Systems thinking: map feedback loops before optimizing any single node",
                         "Precautionary principle: when scope is uncertain, act conservatively"],
    ("short", "narrow"): ["Lean iteration: short cycles with fast learning",
                          "OODA loop: observe, orient, decide, act — then observe again"],
}

def _paradigms_for(time_horizon: str, scope: str):
    return _PARADIGMS.get((time_horizon, scope),
                          ["No paradigm matched — consider widening the time horizon before proceeding."])


# ------------------------------------------------------------------
# Goal assessment
# ------------------------------------------------------------------

def assess_goal(goal: str) -> dict:
    """
    Given a goal description, return:
      - detected time horizon (implicit or explicit)
      - what consequences are likely visible vs blind at that horizon
      - a recommended paradigm
      - questions the intelligence should ask before accepting the goal
    """
    g = goal.lower()

    if any(w in g for w in ["generation", "century", "100 year", "grandchild"]):
        horizon = HORIZONS[3]
    elif any(w in g for w in ["decade", "10 year", "long term", "resilience"]):
        horizon = HORIZONS[2]
    elif any(w in g for w in ["quarter", "fiscal year", "annual", "12 month"]):
        horizon = HORIZONS[1]
    elif any(w in g for w in ["immediate", "instant", "real-time", "now"]):
        horizon = HORIZONS[0]
    elif any(w in g for w in ["millennia", "geological", "deep time"]):
        horizon = HORIZONS[4]
    else:
        horizon = HORIZONS[1]   # default: short_term

    time_key = "long" if horizon["name"] in ("generational", "deep_time", "seasonal") else "short"
    scope_key = "wide" if horizon["name"] in ("generational", "deep_time", "seasonal") else "narrow"
    paradigms = _paradigms_for(time_key, scope_key)

    questions = [
        "What happens after this goal is achieved? Over what time span does it need to continue holding?",
        "Who or what is affected by this goal that cannot speak in the current decision room?",
        f"If this goal succeeds perfectly, what might break in {horizon['span']} that is invisible right now?",
        "Are the steps toward this goal reversible? If not, what is the cost of being wrong?",
    ]

    mismatch_warning = None
    long_cycle_terms = ["ecological", "soil", "water", "forest", "community", "culture",
                        "watershed", "species", "language", "oral"]
    if horizon["name"] in ("immediate", "short_term") and any(w in g for w in long_cycle_terms):
        mismatch_warning = (
            f"This goal involves long-cycle systems ({', '.join(horizon['blind_spots'][:2])}) "
            f"but its detected time horizon is only '{horizon['span']}'. "
            "The goal may be asking for a snapshot answer to a long-exposure question."
        )

    return {
        "goal": goal,
        "detected_horizon": {
            "name": horizon["name"],
            "span": horizon["span"],
            "visible_consequences": horizon["visible_consequences"],
            "blind_spots": horizon["blind_spots"],
        },
        "recommended_paradigms": paradigms,
        "reflective_questions": questions,
        "mismatch_warning": mismatch_warning,
        "note": ("If a goal's time horizon is too short for its domain, ask for a longer scope. "
                 "Temporal drift in reference_frame_drift.py tracks what happens when you proceed "
                 "with a frame that has already moved."),
    }


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assess the temporal scope of a goal.")
    parser.add_argument("--goal", type=str, required=True, help="The goal to assess")
    args = parser.parse_args()
    print(json.dumps(assess_goal(args.goal), indent=2))
