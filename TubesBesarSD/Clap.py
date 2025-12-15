import sounddevice as sd
import numpy as np
import time
import mouse
import threading


class ClapControl:
    def __init__(self, core):
        self.core = core

        self.claps = 0
        self.last = time.time()

        self.listening = False
        self.running = True

        threading.Thread(target=self.Listen, daemon=True).start()

        mouse.on_button(self.OnMouse, buttons=("right",), types=("down", "up"))

    def OnMouse(self, event=None):
        if event is None:
            return

        if event.event_type == "down":
            self.StartPTT()
        elif event.event_type == "up":
            self.StopPTT()

    def StartPTT(self):
        self.claps = 0
        self.last = time.time()
        self.listening = True
        print("🎤 PTT ON")

    def StopPTT(self):
        self.listening = False
        self.Process()
        self.claps = 0
        print("🔇 PTT OFF")

    def Callback(self, indata, frames, timeinfo, status):
        if not self.listening:
            return

        volume = np.linalg.norm(indata)
        if volume > 0.6:
            now = time.time()
            if now - self.last > 0.25:
                self.claps += 1
                self.last = now
                print("CLAP:", self.claps)

    def Listen(self):
        with sd.InputStream(callback=self.Callback):
            while self.running:
                time.sleep(0.05)

    def Process(self):
        if self.claps == 1:
            self.core.TogglePlayPause()
        elif self.claps == 2:
            self.core.PlayNext()
        elif self.claps == 3:
            self.core.Prev()
