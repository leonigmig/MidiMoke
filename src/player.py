import asyncio
import time
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START,
                                  SONG_STOP)
import logging

log = logging.getLogger(__name__)


class Tempo:
    def __init__(self, bpm: int):
        self.set_bpm(bpm)

    def get_beat_duration(self) -> float:
        return 60.0 / self.bpm

    def set_bpm(self, bpm: int):
        self.bpm = bpm


class Player():
    def __init__(self, tempo, movement, port):
        self.tempo = tempo
        self.tick_duration = tempo.get_beat_duration()
        self.movement = movement
        self.port = port

        # external tracking
        self.midi_ticks_counter = 0
        self.ext_last_beat_time_ms = None
        self.int_last_beat_time_ms = None

        self.open_midi_input(self.port)

    def start(self, tick=0):
        self.play = False

        self.loop = asyncio.get_event_loop()
        self.loop.run_forever()

    async def play_task(self, tick=0):
        while self.play:
            current_time = time.perf_counter()

            if self.int_last_beat_time_ms is not None:
                elapsed_time_since_last_beat = (current_time - self.int_last_beat_time_ms) * 1000
                log.debug(f"Elapsed time since last internal beat: {elapsed_time_since_last_beat:.4f} s")

            notes, delta = self.movement(tick)
            log.info(f"Tick: {tick} Delta: {delta} Notes: {notes}")

            for note in notes:
                self.port.send_event(note)

            self.int_last_beat_time_ms = current_time
            await asyncio.sleep(delta)
            tick = tick + delta
        log.info("Player stopped")

    def handle_midi_input(self, message, timestamp):
        msg, timestamp = message
        if msg[0] in (SONG_START, SONG_CONTINUE):
            log.debug("Starting player in respose to external MIDI message")
            self.play = True
            self.loop.call_soon_threadsafe(asyncio.create_task,
                                           self.play_task(0))
        elif msg[0] is SONG_STOP:
            log.debug("stop that song")
            self.play = False
        elif msg[0] is TIMING_CLOCK:
            self.midi_ticks_counter += 1
            if self.midi_ticks_counter % 24 == 0:
                self.every_external_beat(message, timestamp)

    def every_external_beat(self, message, timestamp):
        current_time = time.perf_counter()
        if self.ext_last_beat_time_ms is not None:
            last_beat_elapsed_time_ms = (
                current_time - self.ext_last_beat_time_ms) * 1000
            external_bpm = 60000 / last_beat_elapsed_time_ms
            log.debug(
                f"Beat from the T clock. Elapsed time since last beat: {last_beat_elapsed_time_ms:.4f} ms. External BPM: {external_bpm:.4f}")
            self.tempo.set_bpm(external_bpm)
        self.ext_last_beat_time_ms = current_time

    def open_midi_input(self, port):
        try:
            self.midi_in, self.port_name = open_midiinput(2)
            self.midi_in.ignore_types(timing=False)
            log.info(f"Using MIDI input port: {self.port_name}")
        except (EOFError, KeyboardInterrupt):
            return 1
        self.midi_in.set_callback(self.handle_midi_input)
