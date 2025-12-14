import sounddevice as sd
import numpy as np
import time


class ClapControl:
    def __init__(self, core):
        self.core = core
        self.threshold = 0.6
        self.claps = 0
        self.last_time = time.time()

    def audio_callback(self, indata, frames, time_info, status):
        volume = np.linalg.norm(indata)
        if volume > self.threshold:
            now = time.time()
            if now - self.last_time > 0.3:
                self.claps += 1
                self.last_time = now

    def listen(self):
        with sd.InputStream(callback=self.audio_callback):
            while True:
                time.sleep(1)
                self.process_claps()

    def process_claps(self):
        if self.claps == 1:
            self.core.pause()
        elif self.claps == 2:
            self.core.next_song()
        elif self.claps == 3:
            self.core.prev_song()
        self.claps = 0
