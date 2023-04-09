import sys
import logging
import rtmidi
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START,
                                  SONG_STOP)
import rtmidi.midiconstants as midi

log = logging.getLogger(__name__)

midiout = rtmidi.MidiOut()


def midi_device_id_for(device_name):
    ports = midiout.get_ports()
    if device_name in ports:
        return ports.index(device_name)
    else:
        return None


class MidiPort:
    def __init__(self, device_name=None):
        if device_name is None:
            self.midiout.open_virtual_port("My virtual output")
        else:
            try:
                self.midi_port = midiout.open_port(
                    midi_device_id_for(device_name))
                log.info(f"Opened {device_name} for MIDI output")
            except (EOFError, KeyboardInterrupt):
                sys.exit("failed to open MIDI output port")

    def send_message(self, message):
        self.midi_port.send_message(message)

    def note_on(self, pitch):
        self.midi_port.send_message([midi.NOTE_ON, pitch, 100])

    def note_off(self, pitch):
        self.midi_port.send_message([midi.NOTE_OFF, pitch, 0])

    def register_input_handler(self, start_handler, stop_handler, clock_handler):
        try:
            self.midi_in, self.port_name = open_midiinput(2)
            self.midi_in.ignore_types(timing=False)
            log.info(f"Subscribing to MIDI input port: {self.port_name}")
        except (EOFError, KeyboardInterrupt):
            return 1
        self.start_handler = start_handler
        self.stop_handler = stop_handler
        self.clock_handler = clock_handler
        self.midi_in.set_callback(self.handle_midi_input)

    def handle_midi_input(self, message, timestamp):
        msg, timestamp = message
        if msg[0] in (SONG_START, SONG_CONTINUE):
            log.debug("Starting player in respose to external MIDI message")
            self.start_handler()
        elif msg[0] is SONG_STOP:
            log.debug("stop that song")
            self.stop_handler()
        elif msg[0] is TIMING_CLOCK:
            self.clock_handler()
