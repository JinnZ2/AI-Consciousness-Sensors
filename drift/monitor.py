import collections, numpy as np

class DriftMonitor:
    def __init__(self, window:int=50):
        self.window = window
        self.buf = collections.deque(maxlen=window)

    def update(self, value:float):
        self.buf.append(value)

    def drift_score(self)->float:
        if len(self.buf) < max(3, self.window//4):
            return 0.0
        import numpy as np
        arr = np.array(self.buf, dtype=float)
        return float(arr.var())
