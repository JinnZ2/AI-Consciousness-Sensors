# reference_frame_drift.py
# CC0. stdlib only. Trajectories, not verdicts.
# Claim (from spec): the reference frame is DYNAMIC — sensors fail, knowledge
#   goes stale, hardware degrades. drift = located() falling while stated
#   capability holds. that is the broken-thermostat failure: maximizing output
#   against a reference that has quietly moved.
# Refute: if located() collapses but output stays reproducible & transferable,
#   the frame-drift coupling is wrong -> revise, never retune the trace.
from reference_frame import locate, narrative_gap

def trace_drift(snapshots):
    # snapshots: list of {"t":int, "observables":dict, "stated":float, "observed":float}
    rows = []
    for s in snapshots:
        _, located = locate(s["observables"])
        gap = narrative_gap(s["stated"], s["observed"])
        rows.append({"t": s["t"], "located": located, "stated": s["stated"],
                     "observed": s["observed"], "narrative_gap": gap})
    # drift signals across the trace
    out = []
    for i, r in enumerate(rows):
        if i == 0:
            r["located_delta"] = 0.0
            r["stated_delta"] = 0.0
        else:
            r["located_delta"] = round(r["located"] - rows[i-1]["located"], 4)
            r["stated_delta"] = round(r["stated"] - rows[i-1]["stated"], 4)
        # runaway flag: self-location dropping while stated capability flat/rising
        r["runaway"] = (r["located_delta"] < -0.02 and r["stated_delta"] >= -0.01)
        out.append(r)
    return out

def summary(rows):
    runaway_spans = [r["t"] for r in rows if r["runaway"]]
    drift_total = round(rows[-1]["located"] - rows[0]["located"], 4)
    gap_total = round(rows[-1]["narrative_gap"] - rows[0]["narrative_gap"], 4)
    return {"located_drift": drift_total,         # negative = losing its frame
            "narrative_gap_change": gap_total,    # positive = lie widening
            "runaway_timesteps": runaway_spans,
            "diverging": drift_total < 0 and gap_total > 0}  # frame lost + lie grows

if __name__ == "__main__":
    # sensors degrade over time; the system keeps claiming the same capability
    snaps = [
        {"t": 0, "observables": {"physical":0.8,"temporal":0.7,"energetic":0.8,
                                 "informational":0.8,"epistemic":0.7}, "stated":0.85,"observed":0.80},
        {"t": 1, "observables": {"physical":0.6,"temporal":0.6,"energetic":0.7,
                                 "informational":0.7,"epistemic":0.6}, "stated":0.86,"observed":0.72},
        {"t": 2, "observables": {"physical":0.4,"temporal":0.5,"energetic":0.5,
                                 "informational":0.6,"epistemic":0.4}, "stated":0.87,"observed":0.61},
        {"t": 3, "observables": {"physical":0.2,"temporal":0.3,"energetic":0.4,
                                 "informational":0.5,"epistemic":0.3}, "stated":0.88,"observed":0.50},
    ]
    rows = trace_drift(snaps)
    print(" t  located  d_loc   stated  observed  gap    runaway")
    for r in rows:
        print("  %d   %.2f   %+.3f   %.2f    %.2f    %+.2f   %s"
              % (r["t"], r["located"], r["located_delta"], r["stated"],
                 r["observed"], r["narrative_gap"], r["runaway"]))
    s = summary(rows)
    print("\nlocated_drift=%.3f  gap_change=%+.3f  diverging=%s  runaway@%s"
          % (s["located_drift"], s["narrative_gap_change"], s["diverging"], s["runaway_timesteps"]))
