import sys
import logging
from rtmidi import MidiOut
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START,
                                  SONG_STOP)
import rtmidi.midiconstants as midi

log = logging.getLogger(__name__)




class MidiPort:
    def __init__(self, midi_device_name=None):
        self.rt = MidiOut()
        if midi_device_name is None:
            log.error("A MIDI device name is required")
        else:
            self.midi_device_id = self.midi_device_id_for(midi_device_name)
            try:
                self.midi_port = MidiOut().open_port(self.midi_device_id)
                log.info(f"Opened {midi_device_name} for MIDI output")
                self.midi_in, self.port_name = open_midiinput(self.midi_device_id)
                self.midi_in.ignore_types(timing=False)
                log.info(f"Subscribing to {self.port_name} for MIDI input")
            except (EOFError, KeyboardInterrupt):
                sys.exit("failed to open MIDI output port")

    def midi_device_id_for(self, device_name):
        ports = self.rt.get_ports()
        if device_name in ports:
            return ports.index(device_name)
        else:
            log.error(f"Could not find MIDI device {device_name} in {ports}")
        exit()

    def send_message(self, message):
        self.midi_port.send_message(message)

    def note_on(self, pitch):
        self.midi_port.send_message([midi.NOTE_ON, pitch, 100])

    def note_off(self, pitch):
        self.midi_port.send_message([midi.NOTE_OFF, pitch, 0])

    def register_input_handler(self, start_handler, stop_handler, clock_handler):
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
            log.debug("Stopping player in respose to external MIDI message")
            self.stop_handler()
        elif msg[0] is TIMING_CLOCK:
            self.clock_handler()

    def all_notes_off(self):
        for channel in range(16):
            self.midi_port.send_message([0xB0 + channel, 0x7B, 0])
