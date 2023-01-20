import sys
import rtmidi
import rtmidi.midiconstants as midi

from pattern import NoteOff, NoteOn

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
            midiout.open_virtual_port("My virtual output")
        else:
            try:
                self.midiout = midiout.open_port(
                    midi_device_id_for(device_name))
                print(f"Opened {device_name}")
            except (EOFError, KeyboardInterrupt):
                sys.exit("failed to open MIDI output port")

    def send_message(self, message):
        self.midiout.send_message(message)

    def note_on(self, pitch):
        self.midiout.send_message([midi.NOTE_ON, pitch, 100])

    def note_off(self, pitch):
        self.midiout.send_message([midi.NOTE_OFF, pitch, 0])

    def send_event(self, event):
        if isinstance(event, NoteOn):
            self.note_on(event.pitch)
        elif isinstance(event, NoteOff):
            self.note_off(event.pitch)
