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
        self.midiout.send_message([midi.NOTE_ON, note, 100])

    def note_off(self, note):
        self.midiout.send_message([midi.NOTE_OFF, note, 0])

    def play_note(self, note):
        self.note_on(note)
        time.sleep(0.5)
        self.note_off(note)


class Voice:

    def __init__(self, out_port):
        """Initialize the specified MIDI device."""
        self.port = out_port

    def get_note_events_for_tick(self, elapsed_time):
        self.time_since_last_tick += elapsed_time
        while self.time_since_last_tick >= self.time_per_tick:
            self.time_since_last_tick -= self.time_per_tick
            self.current_tick += 1
            self.note_events = []
            for message in self.midi_file.tracks[0]:
                if message.time == self.current_tick:
                    self.note_events.append(message)
        return self.note_events

    def play_note(self, note):
        """Play a note for a specified duration."""
        # Send a MIDI note on message
        self.port.send_message([midi.NOTE_ON, note, 100])
        print(f"Playing note {note}")
        # Wait for the duration of the note
        time.sleep(0.5)

        # Send a MIDI note off message
        self.port.send_message([midi.NOTE_OFF, note, 0])
