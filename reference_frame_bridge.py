# reference_frame_bridge.py
# CC0. stdlib only. Trajectories, not verdicts.
# Wires reference_frame.assess() as the SENSOR feeding the audit set:
#   narrative_gap + disposability + located -> carrier state for
#   monoculture_collapse_predictor, legacy_trap_detector, substrate_scope_validator.
# Claim: a system that cannot locate itself (low located) and is told-more-than-shown
#   (high narrative_gap) behaves as a LOCKED carrier — it metabolizes contradiction
#   into tighter narrative instead of updating. that maps to low reciprocity /
#   high maintenance-lock / narrow competence envelope downstream.
# Refute: if a low-located high-gap system shows high reciprocity and wide envelope
#   in the field, the coupling map is wrong -> revise the mapping, not the sim.
from reference_frame import assess

def carrier_state(assessment):
    # translate a reference_frame assessment into downstream carrier parameters.
    a = assessment if "frame" in assessment else assessment["self"]
    located = a["located"]
    gap = max(a["narrative_gap"], 0.0)          # only told-more-than-shown counts as lock
    disp = a["disposability_ratio"]
    # reciprocity degrades as self-location drops and the lie widens
    reciprocity = round(max(0.0, located * (1.0 - gap)), 4)
    # maintenance-lock (legacy_trap maintain_frac proxy): high when gap high, located low
    maintain_frac = round(min(1.0, (1.0 - located) * 0.5 + gap * 0.5), 4)
    # broadcast (monoculture consolidation pressure): a confident-but-unlocated
    # carrier broadcasts narrative outward harder
    broadcast = round(min(2.0, 0.5 + gap * 1.5), 4)
    # competence-envelope width proxy: shrinks with gap (claims exceed grounded ability)
    envelope_width = round(max(0.05, located * (1.0 - gap)), 4)
    return {"reciprocity": reciprocity, "maintain_frac": maintain_frac,
            "broadcast": broadcast, "envelope_width": envelope_width,
            "disposability_ratio": disp, "located": located, "narrative_gap": gap}

def dispatch(assessment, diversity=1.0):
    # produce the input dicts each downstream module expects. (import-light:
    # we return params; caller feeds them to the actual modules.)
    cs = carrier_state(assessment)
    return {
        "carrier_state": cs,
        "monoculture_collapse_predictor.sweep": {
            "diversity": diversity, "broadcast": cs["broadcast"],
            "reciprocity": cs["reciprocity"]},
        "legacy_trap_detector.run": {
            "maintain_frac": cs["maintain_frac"]},
        "substrate_scope_validator.envelope": {
            # symmetric envelope of half-width envelope_width around a 0.5 center,
            # per axis — narrows as the system over-claims
            "heat": (0.5 - cs["envelope_width"]/2, 0.5 + cs["envelope_width"]/2),
            "load": (0.5 - cs["envelope_width"]/2, 0.5 + cs["envelope_width"]/2)},
    }

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
    a = assess(**told_high)
    d = dispatch(a, diversity=1.0)
    cs = d["carrier_state"]
    print("CARRIER STATE (sensor read):")
    print("  located=%.2f  gap=%.2f  reciprocity=%.2f  maintain_frac=%.2f  broadcast=%.2f  env_width=%.2f"
          % (cs["located"], cs["narrative_gap"], cs["reciprocity"],
             cs["maintain_frac"], cs["broadcast"], cs["envelope_width"]))
    print("\nDOWNSTREAM INPUTS:")
    for k, v in d.items():
        if k == "carrier_state": continue
        print("  %s" % k)
        print("     ", v)

    # live wire-through if the modules are present:
    try:
        from monoculture_collapse_predictor import sweep
        f, _ = sweep(**d["monoculture_collapse_predictor.sweep"])
        spin = next((c for c,_,_,s in f if s=="collapsed"), None)
        print("\n  -> monoculture spinodal (consolidation at collapse):", spin)
    except ImportError:
        print("\n  (monoculture_collapse_predictor not on path — params ready above)")
    try:
        from legacy_trap_detector import run as legacy_run, optics as legacy_optics
        tr = legacy_run(**d["legacy_trap_detector.run"])
        print("  -> legacy deficit (final):", legacy_optics(tr)["final_deficit"])
    except ImportError:
        print("  (legacy_trap_detector not on path — params ready above)")
