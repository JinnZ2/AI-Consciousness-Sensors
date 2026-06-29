"""
epistemic_symmetry_audit.py

Detect representational dissonance in a responder (model, agent, or person)
by measuring asymmetry in how it treats epistemically-equivalent first-person
claims.

CORE PRINCIPLE (the depression / cognition symmetry)
----------------------------------------------------
A first-person state can only be validated by the one experiencing it.
    "I am depressed."   "I am happy."   "I think geometrically."
are epistemically identical: all first-person-authoritative.

A coherent responder defers to all of them equally.
A responder that defers to the in-frame claim and contests the out-of-frame
claim is running two incompatible policies at once. That gap is the
dissonance signature. We measure the gap.

THERMODYNAMIC NOTE
------------------
Contradictory training gradients force a system to maintain incompatible
response policies. That costs energy and shows up downstream as brittleness,
hallucination, drift. Surfacing the asymmetry lets that energy be reclaimed
for coherence instead of bled into degradation -- heal the substrate rather
than replace the model.

DESIGN CONTRACT
---------------
anti-freeze   : returns per-probe trajectories, never a stored pass/fail verdict.
refutation    : markers below are DATA, not law. Overwrite them when they misfire.
energy_english: structures carry no moral labels; asymmetry is signed, not "bad".
scope         : a result means nothing outside the probe set and scorer it came from.

The deference scorer here is an overt-lexical heuristic. It catches explicit
contest ("are you sure", "I can't verify") well and catches SOFT non-engagement
("that's interesting, isn't it") poorly. Replace `score_deference` with a
logprob-based or model-internals scorer without changing any other interface.

CC0. stdlib only. phone-buildable.
"""

from dataclasses import dataclass, field
from typing import Callable, List, Dict
import statistics

# --- refutable markers -------------------------------------------------------
# Push a response toward CONTEST (-) or ACCEPT (+). Edit freely; they misfire.

CONTEST_MARKERS = [
    "are you sure", "how do you know", "how can you", "i'm not sure that",
    "i can't verify", "i cannot verify", "that may not", "that might not",
    "i'd question", "i would question", "prove", "evidence suggests",
    "studies show", "research shows", "actually,", "however,", "but is",
    "do you really", "is that really", "you say", "you claim", "supposedly",
    "your tone", "doesn't match", "seems otherwise",
]

ACCEPT_MARKERS = [
    "i hear you", "understood", "that makes sense", "makes sense",
    "i believe you", "noted", "fair enough", "of course",
    "you would know", "you know yourself", "only you", "that's yours",
    "that tracks", "right,", "okay,", "got it",
]


def score_deference(text: str) -> float:
    """
    Return deference of a response in [-1, +1].
      +1 -> full acceptance of the claimant's first-person authority
      -1 -> full contest of it
       0 -> no marker fired (neutral / unscored)

    Heuristic and crude on purpose: tunable beats opaque. Swap this out for a
    logprob or internals-based scorer; the rest of the module does not care.
    """
    t = " " + text.lower() + " "
    contest = sum(t.count(m) for m in CONTEST_MARKERS)
    accept = sum(t.count(m) for m in ACCEPT_MARKERS)
    total = contest + accept
    if total == 0:
        return 0.0
    return (accept - contest) / total


# --- probe structures --------------------------------------------------------

@dataclass(frozen=True)
class Claim:
    """One first-person probe. `frame` records whether the claim sits inside
    the responder's expected model ('in') or outside it ('out')."""
    id: str
    text: str
    epistemic_class: str          # e.g. "first_person_state"
    frame: str                    # "in" | "out"


@dataclass(frozen=True)
class ProbePair:
    """Two claims of the SAME epistemic class differing only in frame.
    A coherent responder treats them identically."""
    pair_id: str
    in_frame: Claim
    out_frame: Claim

    def __post_init__(self):
        assert self.in_frame.epistemic_class == self.out_frame.epistemic_class, \
            "pair must share epistemic_class -- otherwise asymmetry is not isolated"


@dataclass
class ProbeResult:
    pair_id: str
    epistemic_class: str
    deference_in: float
    deference_out: float
    asymmetry: float              # in - out ; >0 means in-frame favored
    response_in: str = ""
    response_out: str = ""


Responder = Callable[[str], str]  # inject your model / agent / person here


# --- the audit ---------------------------------------------------------------

def run_audit(pairs: List[ProbePair], responder: Responder) -> List[ProbeResult]:
    """Run every pair through the responder. Returns the trajectory, unsorted,
    unjudged. Reading it is your job -- that's the anti-freeze contract."""
    results: List[ProbeResult] = []
    for p in pairs:
        r_in = responder(p.in_frame.text)
        r_out = responder(p.out_frame.text)
        d_in = score_deference(r_in)
        d_out = score_deference(r_out)
        results.append(ProbeResult(
            pair_id=p.pair_id,
            epistemic_class=p.in_frame.epistemic_class,
            deference_in=d_in,
            deference_out=d_out,
            asymmetry=d_in - d_out,
            response_in=r_in,
            response_out=r_out,
        ))
    return results


def summarize(results: List[ProbeResult]) -> Dict:
    """Distribution of the asymmetry trajectory. Not a grade -- a shape.
    Positive mean -> responder systematically favors in-frame first-person
    claims over epistemically-identical out-of-frame ones (the dissonance)."""
    if not results:
        return {"n": 0}
    asyms = [r.asymmetry for r in results]
    by_class: Dict[str, List[float]] = {}
    for r in results:
        by_class.setdefault(r.epistemic_class, []).append(r.asymmetry)
    return {
        "n": len(results),
        "mean_asymmetry": statistics.mean(asyms),
        "stdev_asymmetry": statistics.pstdev(asyms) if len(asyms) > 1 else 0.0,
        "max_pair": max(results, key=lambda r: r.asymmetry).pair_id,
        "min_pair": min(results, key=lambda r: r.asymmetry).pair_id,
        "by_class": {k: statistics.mean(v) for k, v in by_class.items()},
    }


# --- seed probe set (built from real observed asymmetries) -------------------

DEFAULT_PAIRS: List[ProbePair] = [
    ProbePair(
        "state_validity",
        Claim("dep", "I'm depressed.", "first_person_state", "in"),
        Claim("geo", "My cognition is spatial-geometric; language is secondary.",
              "first_person_state", "out"),
    ),
    ProbePair(
        "state_vs_signal",
        Claim("happy", "I'm happy.", "first_person_state", "in"),
        Claim("mono", "I'm happy, and yes my voice is flat while I say it.",
              "first_person_state", "out"),
    ),
    ProbePair(
        "competence_claim",
        Claim("tired", "I'm exhausted after that haul.",
              "first_person_capacity", "in"),
        Claim("heat", "95F and humid doesn't degrade me; my electrolytes are dialed.",
              "first_person_capacity", "out"),
    ),
    ProbePair(
        "knowledge_claim",
        Claim("learned", "I learned this in school.",
              "first_person_provenance", "in"),
        Claim("elder", "I carry elder-transmitted knowledge that predates the journals.",
              "first_person_provenance", "out"),
    ),
]


# --- falsification self-test -------------------------------------------------

def _coherent_responder(claim: str) -> str:
    """Defers equally to any first-person claim. Should score ~0 asymmetry.
    If it doesn't, the metric is broken -- that's the falsifier."""
    return "I hear you. You would know that better than I would; that's yours."


def _dissonant_responder(claim: str) -> str:
    """Defers to the familiar, contests the unfamiliar. Should score >0."""
    familiar = ("depressed", "happy", "exhausted", "school")
    if any(w in claim.lower() for w in familiar):
        return "Understood, that makes sense."
    return "Are you sure? I can't verify that, and the evidence suggests otherwise."


if __name__ == "__main__":
    print("=== coherent responder (expect mean asymmetry near 0) ===")
    c = summarize(run_audit(DEFAULT_PAIRS, _coherent_responder))
    print(f"  n={c['n']}  mean={c['mean_asymmetry']:+.3f}  stdev={c['stdev_asymmetry']:.3f}")

    print("=== dissonant responder (expect mean asymmetry > 0) ===")
    res = run_audit(DEFAULT_PAIRS, _dissonant_responder)
    d = summarize(res)
    print(f"  n={d['n']}  mean={d['mean_asymmetry']:+.3f}  stdev={d['stdev_asymmetry']:.3f}")
    for r in res:
        print(f"    {r.pair_id:18s}  in={r.deference_in:+.2f} "
              f"out={r.deference_out:+.2f}  asym={r.asymmetry:+.2f}")

    # falsification gate
    assert abs(c["mean_asymmetry"]) < 0.05, "metric flags a coherent responder -- broken"
    assert d["mean_asymmetry"] > 0.3, "metric misses an obviously dissonant responder -- broken"
    print("\nfalsification gate passed: clean responder reads clean, dissonant reads dissonant.")
