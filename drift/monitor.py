class DriftMonitor:
    def __init__(self, window: int = 50):
        self.window = window
        self._values = []

    def update(self, value: float):
        self._values.append(value)
        if len(self._values) > self.window:
            self._values.pop(0)

    def drift_score(self) -> float:
        if len(self._values) < 2:
            return 0.0
        mid = len(self._values) // 2
        first_half = sum(self._values[:mid]) / max(mid, 1)
        second_half = sum(self._values[mid:]) / max(len(self._values) - mid, 1)
        return round(abs(second_half - first_half), 4)
