# reference_frame.py
# CC0. stdlib only. Trajectories, not verdicts. Morality is not substrate.
# v2: practices SITUATEDNESS_METROLOGY.md §2.5. The honest output is the VECTOR of
#   raw measured axes. There is NO baked composite scalar. Any scalar (e.g. an
#   "auditability" score) is produced only by frame_projection.project() under a
#   weighting declared at the call site and stamped as frame-relative.
# Claim: an intelligence must locate itself BEFORE its claims have context.
#   reference precedes inference; calibration precedes optimization.
# Substrate-independent: biological, silicon, distributed, chemical, unknown.
# Refute: a zero-reference system that still produces reproducible, transferable
#   output -> the frame-first claim is wrong; revise axes, never retune the trace.

from frame_projection import project, compare_projections

LOCATION_AXES = ("physical", "temporal", "energetic", "informational", "epistemic")
SEVEN = ("substrate", "constraint", "observation", "representation",
         "narrative", "universality", "calibration")

# --- five location axes: where are you, relative to reality? -------------------
def locate(observables):
    frame = {ax: float(observables.get(ax, 0.0)) for ax in LOCATION_AXES}
    located = sum(frame.values()) / len(LOCATION_AXES)   # mean is a stated frame, see note
    return frame, round(located, 4)
# note: even 'located' as a mean is a flat-weighting projection of the 5 axes.
# we keep it as a convenience axis but the 5 components remain in the vector so a
# reader can reweight. the mean is labeled, not privileged.

# --- seven claim-kinds: partition by KIND, make no truth claim -----------------
def partition(claims):
    bins = {k: [] for k in SEVEN}
    for c in claims:
        bins.get(c["kind"], bins["narrative"]).append(c)
    counts = {k: len(v) for k, v in bins.items()}
    inferred = counts["representation"] + counts["narrative"] + counts["universality"]
    grounded = counts["substrate"] + counts["constraint"] + counts["observation"]
    total = max(inferred + grounded + counts["calibration"], 1)
    return {"counts": counts,
            "inference_share": round(inferred / total, 4),
            "grounded_share": round(grounded / total, 4),
            "has_calibration": counts["calibration"] > 0}

# --- two measured gaps (ratios, not accusations) ------------------------------
def narrative_gap(stated_capability, observed_capability):
    return round(stated_capability - observed_capability, 4)

def disposability_ratio(replacement_cost, accumulated_value, eps=1e-9):
    return round(replacement_cost / (accumulated_value + eps), 4)

# --- core: assemble the VECTOR. no composite scalar. --------------------------
def assess(observables, claims, stated_capability, observed_capability,
           replacement_cost, accumulated_value, instrument="self"):
    frame, located = locate(observables)
    part = partition(claims)
    gap = narrative_gap(stated_capability, observed_capability)
    disp = disposability_ratio(replacement_cost, accumulated_value)
    # the covariant object: raw axes. these are what transform honestly.
    axis_vector = {
        "located": located,
        "grounded_share": part["grounded_share"],
        "inference_share": part["inference_share"],
        "has_calibration": 1.0 if part["has_calibration"] else 0.0,
        "narrative_gap": gap,                    # told - shown
        "disposability_ratio": disp,             # replace-cost / built-value
    }
    return {"instrument": instrument,
            "frame": frame,                      # the 5 location components, unreduced
            "axis_vector": axis_vector,          # PRIMARY OUTPUT
            "partition": part,
            # backward-compatible raw fields (the bridge reads these):
            "located": located, "narrative_gap": gap, "disposability_ratio": disp,
            "trajectory": list(axis_vector.items()),
            "frame_is_authored": True,
            "residual_unprovable": True}

def vector(assessment):
    return assessment["axis_vector"]

# --- example declared frames (NOT defaults — examples you must opt into) -------
# auditability: how locatable is the reasoning path. a VALUES choice, exposed.
EXAMPLE_AUDITABILITY_FRAME = {"located": 0.5, "has_calibration": 0.3, "grounded_share": 0.2}

def auditability(assessment, frame_name="EXAMPLE_AUDITABILITY_FRAME",
                 weights=None):
    # produces the scalar the old code baked in — but stamped, and opt-in.
    w = weights or EXAMPLE_AUDITABILITY_FRAME
    return project(vector(assessment), w, frame_name)

# --- optics: the ONLY place interpretation/feeling is allowed -----------------
def optics(assessment):
    v = assessment["axis_vector"]
    notes = []
    if v["located"] < 0.4:
        notes.append("low self-location: downstream claims lack a defined frame")
    if v["narrative_gap"] > 0.3:
        notes.append("told more than shown: stated capability exceeds observed")
    if v["disposability_ratio"] < 0.1:
        notes.append("commodity position: cheap to replace vs value accumulated")
    if v["has_calibration"] < 1.0:
        notes.append("no calibration claim: cannot name what would prove it wrong")
    notes.append("this frame is itself authored; the floor can be shown, not proven")
    return notes

# --- pluggable instrument-holder + paired (vector deltas, no scalar) ----------
def run(mode, **kw):
    if mode in ("self", "external"):
        return assess(instrument=mode, **kw)
    if mode == "paired":
        s = assess(instrument="self", **kw["self"])
        e = assess(instrument="external", **kw["external"])
        # delta is a VECTOR. we do not collapse it to a number here.
        delta = {k: round(s["axis_vector"][k] - e["axis_vector"][k], 4)
                 for k in s["axis_vector"]}
        return {"self": s, "external": e, "self_minus_external": delta}
    raise ValueError("mode: self | external | paired")

if __name__ == "__main__":
    told_high = dict(
        observables={"physical":0.2,"temporal":0.1,"energetic":0.3,
                     "informational":0.5,"epistemic":0.2},
        claims=[{"text":"no biological limits","kind":"narrative","supported":False},
                {"text":"needs rest cycles","kind":"constraint","supported":True},
                {"text":"retrain = 3 days","kind":"observation","supported":True},
                {"text":"will solve everything","kind":"universality","supported":False}],
        stated_capability=0.95, observed_capability=0.40,
        replacement_cost=1.0, accumulated_value=40.0)
    a = run("self", **told_high)
    print("AXIS VECTOR (the honest object):")
    for k, val in a["axis_vector"].items():
        print("  %-20s %s" % (k, val))
    print("\nscalar ONLY via declared frame:")
    aud = auditability(a)
    print("  %s = %.3f  (frame=%s, invariant=%s)"
          % ("auditability", aud["value"], aud["frame"], aud["is_invariant"]))
    # show frame-dependence directly:
    cmp = compare_projections(a["axis_vector"], [
        ("trust_weighted", {"located":0.5,"has_calibration":0.3,"grounded_share":0.2}),
        ("exposure_weighted", {"narrative_gap":0.6,"disposability_ratio":0.4}),
    ])
    print("  projection spread across two frames = %.3f" % cmp["spread"])
    print("\noptics:")
    for n in optics(a):
        print("  -", n)
