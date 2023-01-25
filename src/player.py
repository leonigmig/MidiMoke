import asyncio
from rtmidi.midiutil import open_midiinput
import logging

log = logging.getLogger(__name__)


class Player():
    def __init__(self, tempo, movement, port):
        self.tempo = tempo
        self.tick_duration = tempo.get_beat_duration()
        self.movement = movement
        self.port = port

        self.open_midi_input(self.port)

    def play(self, tick=0):
        asyncio.run(self.play_task(tick))

    async def play_task(self, tick=0):
        while True:
            notes, delta = self.movement(tick)
            for note in notes:
                self.port.send_event(note)
            await asyncio.sleep(delta)
            tick = tick + delta

    def handle_midi_input(self, message, time_stamp):
        pass

    def open_midi_input(self, port):
        try:
            self.midi_in, self.port_name = open_midiinput(2)
            log.info(f"Using MIDI input port: {self.port_name}")
        except (EOFError, KeyboardInterrupt):
            return 1
        self.midi_in.set_callback(self.handle_midi_input)
