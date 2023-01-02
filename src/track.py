import sys
import time
import rtmidi
from rtmidi.midiutil import open_midioutput
import rtmidi.midiconstants as midi


def midi_device_id_for(device_name):
    ports = rtmidi.MidiOut().get_ports()
    if device_name in ports:
        return ports.index(device_name)
    else:
        return None


class Voice:

    def __init__(self, device_name):
        """Initialize the specified MIDI device."""
        try:
            self.midiout, port_name = open_midioutput(
                midi_device_id_for(device_name))
            print(f"Opened {device_name}")
        except (EOFError, KeyboardInterrupt):
            sys.exit("failed to open MIDI output port")

    def play_note(self, note):
        """Play a note for a specified duration."""
        # Send a MIDI note on message
        self.midiout.send_message([midi.NOTE_ON, note, 100])
        print(f"Playing note {note}")
        # Wait for the duration of the note
        time.sleep(0.5)

        # Send a MIDI note off message
        self.midiout.send_message([midi.NOTE_OFF, note, 0])
