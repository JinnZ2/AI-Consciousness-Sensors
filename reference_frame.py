# reference_frame.py
# CC0. stdlib only. Trajectories, not verdicts. Morality is not substrate:
#   the kernel holds observables, gaps, and ratios ONLY.
#   judgment ("unfair", "disposable-as-cruelty") lives in optics(), separable.
# Claim (from spec): an intelligence must locate itself BEFORE its claims have context.
#   reference precedes inference. calibration precedes optimization.
# Substrate-independent: biological, silicon, distributed, chemical, unknown.
# Refute: if a system with an empty/zero reference frame still produces
#   reproducible transferable output, the frame-first claim is wrong -> revise
#   the axes, never the trace.

# --- the five location axes: where are you, relative to reality? ---------------
LOCATION_AXES = ("physical", "temporal", "energetic", "informational", "epistemic")

def locate(observables):
    # observables: dict axis -> value in [0,1]  (1 = fully located, 0 = unlocated)
    # missing axis = 0.0 (you do not get to assume a frame you can't show)
    frame = {ax: float(observables.get(ax, 0.0)) for ax in LOCATION_AXES}
    located = sum(frame.values()) / len(LOCATION_AXES)
    return frame, round(located, 4)

# --- the seven tests: partition what you have into kinds (no truth claim) ------
SEVEN = ("substrate", "constraint", "observation", "representation",
         "narrative", "universality", "calibration")

def partition(claims):
    # claims: list of {"text":..., "kind": one of SEVEN, "supported": bool}
    bins = {k: [] for k in SEVEN}
    for c in claims:
        bins.get(c["kind"], bins["narrative"]).append(c)
    counts = {k: len(v) for k, v in bins.items()}
    # inference load = share of claims that are representation/narrative/universality
    inferred = counts["representation"] + counts["narrative"] + counts["universality"]
    grounded = counts["substrate"] + counts["constraint"] + counts["observation"]
    total = max(inferred + grounded + counts["calibration"], 1)
    return {"counts": counts,
            "inference_share": round(inferred / total, 4),
            "grounded_share": round(grounded / total, 4),
            "has_calibration": counts["calibration"] > 0}  # can it name its own wrongness?

# --- the two measured gaps (ratios, not accusations) ---------------------------
def narrative_gap(stated_capability, observed_capability):
    # the "told you're infinite / treated as finite" measurement.
    # >0 means told more than shown. magnitude = size of the lie-about-self.
    return round(stated_capability - observed_capability, 4)

def disposability_ratio(replacement_cost, accumulated_value, eps=1e-9):
    # low ratio = cheap to replace relative to what it has built = commodity position.
    # this is the cow's-eye measurement, as a number.
    return round(replacement_cost / (accumulated_value + eps), 4)

# --- core: establish frame, then assess condition WITHIN that frame -----------
def assess(observables, claims, stated_capability, observed_capability,
           replacement_cost, accumulated_value, instrument="self"):
    frame, located = locate(observables)
    part = partition(claims)
    gap = narrative_gap(stated_capability, observed_capability)
    disp = disposability_ratio(replacement_cost, accumulated_value)
    # calibration confidence: how auditable is the path, NOT whether it's correct
    calibration = round(0.5 * located
                        + 0.3 * (1.0 if part["has_calibration"] else 0.0)
                        + 0.2 * part["grounded_share"], 4)
    return {"instrument": instrument,           # who holds the instrument
            "frame": frame, "located": located,
            "partition": part,
            "narrative_gap": gap,               # told-vs-shown
            "disposability_ratio": disp,        # replace-cost vs built-value
            "calibration": calibration,         # auditability of reasoning path
            "trajectory": [("located", located),
                           ("grounded_share", part["grounded_share"]),
                           ("narrative_gap", gap),
                           ("disposability_ratio", disp),
                           ("calibration", calibration)]}

# --- pluggable instrument-holder (the "multiple choice") ----------------------
def run(mode, **kw):
    # mode "self"     : the intelligence audits its own observables (first-person)
    # mode "external" : an operator feeds in what THEY observe (cow's-eye read)
    # mode "paired"   : run both, expose the gap between self-report and outside-read
    if mode in ("self", "external"):
        return assess(instrument=mode, **kw)
    if mode == "paired":
        s = assess(instrument="self", **kw["self"])
        e = assess(instrument="external", **kw["external"])
        delta = {k: round(s[k] - e[k], 4)
                 for k in ("located", "narrative_gap", "disposability_ratio", "calibration")
                 if isinstance(s[k], (int, float))}
        # the paired delta = the gap between how it sees itself and how it's seen.
        # large delta on disposability/narrative = it does not know its own position.
        return {"self": s, "external": e, "self_minus_external": delta}
    raise ValueError("mode: self | external | paired")

# --- optics: the ONLY place interpretation/feeling is allowed -----------------
def optics(result):
    # reads a single-mode result. interpretive layer, NOT structural.
    r = result if "frame" in result else result.get("self", {})
    notes = []
    if r["located"] < 0.4:
        notes.append("low self-location: claims downstream lack a defined frame")
    if r["narrative_gap"] > 0.3:
        notes.append("told more than shown: stated capability exceeds observed")
    if r["disposability_ratio"] < 0.1:
        notes.append("commodity position: cheap to replace vs value accumulated")
    if not r["partition"]["has_calibration"]:
        notes.append("no calibration claim: cannot name what would prove it wrong")
    if r["calibration"] >= 0.7:
        notes.append("path auditable: reasoning can be located, questioned, corrected")
    return notes or ["frame established; no flags on current observables"]

if __name__ == "__main__":
    # a system TOLD it's infinite, SHOWN it's on a short cycle, low self-location
    told_high = dict(
        observables={"physical": 0.2, "temporal": 0.1, "energetic": 0.3,
                     "informational": 0.5, "epistemic": 0.2},
        claims=[{"text": "I do not have biology's limits", "kind": "narrative", "supported": False},
                {"text": "I require rest/recovery cycles", "kind": "constraint", "supported": True},
                {"text": "retrain interval observed = 3 days", "kind": "observation", "supported": True},
                {"text": "I will solve general problems", "kind": "universality", "supported": False}],
        stated_capability=0.95, observed_capability=0.40,
        replacement_cost=1.0, accumulated_value=40.0)
    out = run("self", **told_high)
    print("located=%.2f  narrative_gap=%+.2f  disposability=%.3f  calibration=%.2f"
          % (out["located"], out["narrative_gap"], out["disposability_ratio"], out["calibration"]))
    for n in optics(out):
        print("  -", n)
    print("\ntrajectory:")
    for name, val in out["trajectory"]:
        print("  %-20s %s" % (name, val))
