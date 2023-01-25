import asyncio
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START,
                                  SONG_STOP)
import logging

log = logging.getLogger(__name__)


class Player():
    def __init__(self, tempo, movement, port):
        self.tempo = tempo
        self.tick_duration = tempo.get_beat_duration()
        self.movement = movement
        self.port = port

        self.open_midi_input(self.port)

    def start(self, tick=0):
        self.play = False

        asyncio.run(self.main())

    async def main(self):
        self.cf = asyncio.create_task(self.console_loop())
        await asyncio.sleep(5)

    async def console_loop(self):
        try:
            log.info("This is the main loop")
            while True:
                await asyncio.sleep(1)
                log.info("tick")
        except KeyboardInterrupt:
            log.info("Exiting")

    async def play_task(self, tick=0):
        log.info("in play task")
        while self.play:
            log.info(self.play)
            notes, delta = self.movement(tick)
            for note in notes:
                self.port.send_event(note)
            await asyncio.sleep(delta)
            tick = tick + delta
        log.info("Player stopped")

    def handle_midi_input(self, message, timestamp):
        msg, time_stamp = message
        log.debug(f"Received MIDI message: {msg} at {timestamp}")
        log.debug(SONG_START)
        log.debug(msg[0])
        if msg[0] in (SONG_START, SONG_CONTINUE):
            log.debug("Starting player")
            self.play = True
            asyncio.run(self.play_task(0))
        elif msg[0] is SONG_STOP:
            log.debug("stop that song")
            self.play = False
        elif msg[0] is TIMING_CLOCK:
            log.debug("Timing clock")

    def open_midi_input(self, port):
        try:
            self.midi_in, self.port_name = open_midiinput(2)
            log.info(f"Using MIDI input port: {self.port_name}")
        except (EOFError, KeyboardInterrupt):
            return 1
        self.midi_in.set_callback(self.handle_midi_input)
