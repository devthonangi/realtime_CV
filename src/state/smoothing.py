from collections import deque
import numpy as np

class Smoother:
    def __init__(self, n=8):
        self.q = deque(maxlen=n)

    def update(self, v):
        self.q.append(v)
        return float(np.mean(self.q))
