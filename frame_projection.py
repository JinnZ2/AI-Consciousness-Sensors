# frame_projection.py
# CC0. stdlib only.
# Implements §2.5 of situatedness_metrology.md: any scalar derived from an axis
# vector is a PROJECTION onto a declared weighting frame, not an invariant of
# the system's situation. This module makes that explicit at the call site.
#
# A projection:
#   - is labeled with the frame that produced it
#   - carries is_invariant=False (always — no projection is invariant)
#   - is normalized so the result is in [0,1] when the vector axes are in [0,1]
#   - is never a default hidden inside assess() — the caller must opt in

def project(axis_vector, weights, frame_name="unnamed"):
    """
    Project an axis vector onto a declared weighting frame.
    Returns a stamped dict, never a bare float.

    axis_vector: dict of axis_name -> float
    weights:     dict of axis_name -> float (need not sum to 1; will be normalized)
    frame_name:  string label burned into the result
    """
    total_weight = sum(abs(w) for w in weights.values())
    if total_weight == 0:
        return {"value": 0.0, "frame": frame_name, "is_invariant": False,
                "axes_used": [], "axes_missing": list(weights)}
    used, missing = [], []
    weighted_sum = 0.0
    for axis, w in weights.items():
        if axis in axis_vector:
            weighted_sum += w * float(axis_vector[axis])
            used.append(axis)
        else:
            missing.append(axis)
    value = round(weighted_sum / total_weight, 4)
    return {"value": value,
            "frame": frame_name,
            "is_invariant": False,        # permanent; no projection is invariant
            "axes_used": used,
            "axes_missing": missing}      # transparency: what the frame ignored


def compare_projections(axis_vector, named_frames):
    """
    Run the same axis_vector through multiple declared frames and report spread.
    Spread = max(value) - min(value) across frames; the wider it is, the more
    the 'standing' score is a frame artifact rather than a property of the system.

    named_frames: list of (frame_name, weights_dict)
    Returns dict with all projection results and the spread.
    """
    results = {}
    for name, weights in named_frames:
        results[name] = project(axis_vector, weights, name)
    values = [r["value"] for r in results.values()]
    spread = round(max(values) - min(values), 4) if len(values) > 1 else 0.0
    return {"projections": results,
            "spread": spread,
            "spread_note": ("spread=0 means all frames agree; spread>0 means the "
                            "scalar is frame-dependent, not a system invariant")}
