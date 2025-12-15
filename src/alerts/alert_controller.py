import time

class AlertController:
    def __init__(self):
        self.last = 0
        self.cooldown = 3
        self.level = 0

    def update(self, score):
        if score < 3:
            self.level = 0
        elif score < 5:
            self.level = 1
        elif score < 7:
            self.level = 2
        else:
            self.level = 3

        now = time.time()
        if self.level >= 2 and now - self.last > self.cooldown:
            self.last = now
            return self.level
        return None
