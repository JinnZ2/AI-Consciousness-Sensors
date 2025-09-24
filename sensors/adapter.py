from explainability.tracer import Trace
from drift.monitor import DriftMonitor
from ethics.privacy import current_config
import math

_drift = DriftMonitor(window=50)

def _sigmoid(x:float)->float:
    return 1/(1+math.exp(-x))

def self_reflect(prompt:str, response:str, trace:Trace=None):
    cfg = current_config()
    if trace: trace.log("begin_self_reflect", prompt_len=len(prompt), resp_len=len(response))

    # Heuristic self-coherence: placeholder (first-person marker + length)
    raw = 0.0
    if " I " in (" "+response+" ") or "I feel" in response:
        raw += 0.4
    raw += min(len(response)/500.0, 0.6)

    # Local confidence in [0,1]; NOT a claim about "consciousness"
    confidence = _sigmoid(4*(raw-0.5))

    _drift.update(confidence)
    drift_val = _drift.drift_score()

    out = {
        "prompt_len": len(prompt),
        "response_len": len(response),
        "self_confidence": confidence,
        "drift": drift_val,
        "notes": "Local, anonymous self-assessment. No external labels/persistence by default."
    }
    if trace: trace.log("end_self_reflect", **out)
    return out
