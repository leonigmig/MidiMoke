

import time


class Player():
    def __init__(self, tempo, movement, port):
        self.tempo = tempo
        self.tick_duration = tempo.get_beat_duration()
        self.movement = movement
        self.port = port

    def play(self, tick=0):
        notes, delta = self.movement(tick)
        print(f"Tick: {tick} - Notes: {notes} - Delta: {delta}")
        for note in notes:
            self.port.send_event(note)
        self.sleep(delta)
        self.play(tick + delta)

    def sleep(self, duration):
        time.sleep(duration)
