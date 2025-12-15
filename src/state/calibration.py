import time

class Calibrator:
    """
    Collect EAR while driver is alert/neutral for N seconds.
    """
    def __init__(self, seconds=3.0):
        self.seconds = seconds
        self.values = []
        self.start_t = None
        self.done = False
        self.baseline = None

    def reset(self):
        self.values = []
        self.start_t = None
        self.done = False
        self.baseline = None

    def update(self, ear: float):
        now = time.time()
        if self.start_t is None:
            self.start_t = now

        self.values.append(float(ear))

        if (now - self.start_t) >= self.seconds:
            self.baseline = sum(self.values) / max(1, len(self.values))
            self.done = True

        return self.done
