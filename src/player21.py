import asyncio
import time

import logging

from m21 import convert_music21_stream

log = logging.getLogger(__name__)


class Player():
    def __init__(self, stream, port):
        self.play = False
        self.tick = 0
        self.loop = asyncio.get_event_loop()

        self.stream = stream
        self.converted_stream = convert_music21_stream(self.stream)
        self.midi_port = port

        # external tracking
        self.midi_ticks_counter = 0
        self.ext_last_beat_time_ms = None
        self.int_last_beat_time_ms = None
        self.last_tick_time_ms = None

        self.midi_port.register_input_handler(self.handle_midi_start_message,
                                              self.handle_midi_stop_message,
                                              self.handle_midi_timing_message)

    def start(self):
        self.loop.run_forever()

    def handle_midi_start_message(self):
        self.play = True
        self.tick = 0
        self.play_for_tick()

    def handle_midi_stop_message(self):
        self.play = False
        self.tick = 0

    def handle_midi_timing_message(self):
        if self.play:
            self.tick += 1
            self.play_for_tick()

    def play_for_tick(self):
        try:
            log.info(f"tick: {self.tick} notes: {self.converted_stream[self.tick]}")
            for event in self.converted_stream[self.tick]:
                if event.isNoteOn():
                    self.midi_port.note_on(event.pitch)
                if event.isNoteOff():
                    self.midi_port.note_off(event.pitch)
        except KeyError:
            pass

    def every_external_beat(self, message, timestamp):
        current_time = time.perf_counter()
        if self.ext_last_beat_time_ms is not None:
            last_beat_elapsed_time_ms = (
                current_time - self.ext_last_beat_time_ms) * 1000
            external_bpm = 60000 / last_beat_elapsed_time_ms
            log.debug(
                f"Beat from the DT clock. Elapsed time since last beat: {last_beat_elapsed_time_ms:.4f} ms. External BPM: {external_bpm:.4f}")
            self.tempo.set_bpm(external_bpm)
        self.ext_last_beat_time_ms = current_time

    def _log_timing(self, time_ref):
        current_time = time.perf_counter()
        if time_ref is not None:
            elapsed_time_ms = (current_time - time_ref) * 1000
            log.debug(f"elapsed time: {elapsed_time_ms:.4f} ms")
        self.last_tick_time_ms = current_time
