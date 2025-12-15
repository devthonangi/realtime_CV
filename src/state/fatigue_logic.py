import time
from collections import deque

class FatigueLogic:
   
    def __init__(self, window_seconds=20.0):
        self.window_seconds = window_seconds
        self.eye_closed_samples = deque()  # (t, is_closed)
        self.yawn_samples = deque()        # (t, is_yawn)

        self.last_t = time.time()

        # These get set by calibration (fallback defaults if you skip calibration)
        self.ear_open_baseline = 0.30
        self.ear_close_threshold = 0.23  # will be derived from baseline

        # Alert thresholds
        self.perclos_warn = 0.20   # 20% closed in window
        self.perclos_drowsy = 0.35 # 35%
        self.perclos_critical = 0.50

        self.yawn_min_seconds = 1.0  # mouth open continuously >= 1s counts as yawn episode

        # Tracking yawn duration
        self._yawn_on = False
        self._yawn_start = None
        self.yawn_events = deque()  # timestamps of yawn events in window

    def set_calibration(self, ear_open_baseline: float):
        self.ear_open_baseline = float(ear_open_baseline)
        # dynamic threshold (common pattern: baseline * 0.75~0.8)
        self.ear_close_threshold = max(0.15, self.ear_open_baseline * 0.78)

    def _trim(self, dq, now):
        while dq and (now - dq[0][0]) > self.window_seconds:
            dq.popleft()

    def _trim_events(self, dq, now):
        while dq and (now - dq[0]) > self.window_seconds:
            dq.popleft()

    def update(self, ear: float, mar: float, mar_threshold: float):
        now = time.time()

        is_closed = ear < self.ear_close_threshold
        is_yawn_like = mar > mar_threshold

        self.eye_closed_samples.append((now, 1 if is_closed else 0))
        self.yawn_samples.append((now, 1 if is_yawn_like else 0))

        self._trim(self.eye_closed_samples, now)
        self._trim(self.yawn_samples, now)
        self._trim_events(self.yawn_events, now)

        # PERCLOS (percent eye closure) within window
        if self.eye_closed_samples:
            closed = sum(v for _, v in self.eye_closed_samples)
            perclos = closed / len(self.eye_closed_samples)
        else:
            perclos = 0.0

        # Yawn episode detection by duration
        if is_yawn_like and not self._yawn_on:
            self._yawn_on = True
            self._yawn_start = now
        elif (not is_yawn_like) and self._yawn_on:
            dur = now - (self._yawn_start or now)
            self._yawn_on = False
            self._yawn_start = None
            if dur >= self.yawn_min_seconds:
                self.yawn_events.append(now)

        # Alert level from perclos + yawn frequency
        yawns_in_window = len(self.yawn_events)

        level = 0
        if perclos >= self.perclos_warn or yawns_in_window >= 1:
            level = 1
        if perclos >= self.perclos_drowsy or yawns_in_window >= 2:
            level = 2
        if perclos >= self.perclos_critical or yawns_in_window >= 3:
            level = 3

        return {
            "perclos": perclos,
            "yawns": yawns_in_window,
            "level": level,
            "ear_thr": self.ear_close_threshold,
        }
