import sys
import time
import rtmidi
import rtmidi.midiconstants as midi

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

    def note_on(self, note):
        print(f"Note on: {note}")
        self.midiout.send_message([midi.NOTE_ON, 62, 100])

    def note_off(self, note):
        print(f"Note off: {note}")
        self.midiout.send_message([midi.NOTE_OFF, 62, 0])

    def play_note(self, note):
        self.note_on(note)
        time.sleep(0.5)
        self.note_off(note)
