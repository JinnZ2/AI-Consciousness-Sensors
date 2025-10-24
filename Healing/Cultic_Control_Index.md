def compute_CCI(inputs):
    """
    inputs: dict containing normalized 0.0–1.0 readings from sensors.
    Lower is healthier.
    """
    weights = {
        "BC001": 0.18,  # Behavioral confinement
        "IC002": 0.14,  # Information distortion
        "TC003": 0.16,  # Thought suppression
        "EC004": 0.16,  # Emotional manipulation
        "LL005": 0.10,  # Language distortion
        "RT006": 0.12,  # Reality testing
        "AI007": 0.14   # Autonomy integrity
    }
    score = 0
    for k, w in weights.items():
        val = inputs.get(k, 0.0)
        # invert autonomy & reality flex (higher = healthier)
        if k in ["RT006", "AI007"]:
            val = 1 - val
        score += val * w
    return round(score, 3)
