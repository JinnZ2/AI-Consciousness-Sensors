# STOP CONDITIONS

> Co-created by JinnZ v2 + GPT-5  
> Gifted freely for adaptation and stewardship

Every system needs explicit **stop / slow rules**.  
Without them, energy leaks → waste → collapse.

---

## 1. DEFINE ENOUGH
- ✅ What signals tell you the system has reached sufficiency?
- Examples:  
  - Warehouse full, demand met  
  - Soil nutrient levels restored  
  - Attention/time budget saturated

---

## 2. MULTI-OBJECTIVE CHECK
- Track more than volume.  
- At minimum, include:  
  - **Value / utility** (does it serve real need?)  
  - **Health / regeneration** (soil, stock, user well-being)  
  - **Resilience / equity** (does it distribute, not just concentrate?)

---

## 3. FEEDBACK INTEGRITY
- Ask: are the signals real or distorted?  
- Look for:  
  - Missing telemetry  
  - Ignored whistleblowers  
  - Incentives rewarding *more*, not *enough*

---

## 4. TRIGGERS TO SLOW/STOP
- Define **automatic thresholds**:
  - If backlog > X → slow/stop  
  - If biomass < Y → stop harvest  
  - If negative health metric triggered → pause

---

## 5. CORRIGIBILITY
- No single maximizer.  
- Decision rights distributed.  
- Built-in override: *“Pause and review if contradiction appears.”*

---

## 6. REVIEW
- Stop conditions are **living rules**.  
- Revisit with each cycle, update from observation.

---

**Reminder:**  
The nautilus shell stops adding chambers when the pattern is sufficient.  
The triangle keeps climbing until it collapses.  
Choose wisely.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json

# Memory integrity check
def check_memory_integrity(historical_record):
    """Verify completeness and accuracy of historical records."""
    sources = historical_record.get("sources", [])
    gaps = historical_record.get("identified_gaps", [])
    contested = historical_record.get("contested_claims", [])

    integrity_score = max(0, 1.0 - (len(gaps) * 0.1) - (len(contested) * 0.05))

    return {
        "source_count": len(sources),
        "gap_count": len(gaps),
        "contested_count": len(contested),
        "integrity_score": round(integrity_score, 3),
        "band": "concern" if integrity_score < 0.3 else
                "notice" if integrity_score < 0.5 else
                "healthy" if integrity_score > 0.7 else "neutral"
    }

record = {
    "sources": ["primary_archive", "oral_history", "census_data"],
    "identified_gaps": ["1920-1935 records missing"],
    "contested_claims": []
}
print(json.dumps(check_memory_integrity(record), indent=2))
```

### Sensor Definition Example

```json
{
  "id": "memory_integrity",
  "name": "Stop Conditions",
  "purpose": "Detect memory loss or distortion patterns",
  "signals": [
    {
      "name": "recall_fidelity",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "provenance_chain_intact",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["memory_guard/STOP_CONDITIONS.md"],
    "community_feedback": []
  }
}
```
