import sys
import time
import rtmidi
from rtmidi.midiutil import open_midioutput
import rtmidi.midiconstants as midi


class MidiPlayer:
    """A simple MIDI player that plays a note on a specified device."""

    def __init__(self, device_name):
        """Initialize the MIDI player and open the specified device."""

        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        print(available_ports)

        if device_name in available_ports:
            port_id = available_ports.index(device_name)
            try:
                self.midiout, port_name = open_midioutput(port_id)
            except (EOFError, KeyboardInterrupt):
                sys.exit("failed to open MIDI output port")
            print(f"Opened {device_name}")
        else:
            self.midiout.open_virtual_port(device_name)

    def play_note(self, note):
        """Play a note for a specified duration."""
        # Send a MIDI note on message
        self.midiout.send_message([midi.NOTE_ON, note, 100])
        print(f"Playing note {note}")
        # Wait for the duration of the note
        time.sleep(0.5)

        # Send a MIDI note off message
        self.midiout.send_message([midi.NOTE_OFF, note, 0])
