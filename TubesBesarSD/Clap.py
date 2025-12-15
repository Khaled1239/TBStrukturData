import sounddevice as sd
import numpy as np
import time


class ClapControl:
    def __init__(self, core):
        self.core = core
        self.claps = 0
        self.last = time.time()

    def Callback(self, indata, frames, timeinfo, status):
        volume = np.linalg.norm(indata)
        if volume > 0.6:
            now = time.time()
            if now - self.last > 0.3:
                self.claps += 1
                self.last = now

    def Listen(self):
        with sd.InputStream(callback=self.Callback):
            while True:
                time.sleep(1)
                self.Process()

    def Process(self):
        if self.claps == 1:
            self.core.Pause()
        elif self.claps == 2:
            self.core.PlayNext()
        elif self.claps == 3:
            self.core.Prev()
        self.claps = 0
