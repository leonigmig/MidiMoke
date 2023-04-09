from music21 import stream, note
from music21 import midi


def convert_music21_stream(stream):
    # Convert the Music21 stream into a MIDI stream
    midi_stream = midi.translate.streamToMidiFile(stream)
    print(type(midi_stream))
    # Calculate the number of ticks per quarter note for the desired resolution
    ticks_per_quarter_note = midi_stream.ticksPerQuarterNote
    ticks_per_24th_quarter_note = ticks_per_quarter_note // 24

    # Initialize an empty list for each tick
    midi_events = [[] for _ in range(24)]

    for track in midi_stream.tracks:
        # Keep track of the current tick position for each track
        current_tick = 0

        for event in track.events:
            if event.isDeltaTime():
                # Convert delta time to 1/24th quarter note ticks
                delta_ticks = event.time // ticks_per_24th_quarter_note
                current_tick += delta_ticks
            elif event.isNoteOn() or event.isNoteOff():
                # Append the MIDI event to the appropriate tick's list
                tick_index = current_tick % 24
                midi_events[tick_index].append(event)

    return midi_events


def get_stream():
    arpeggio = stream.Stream()
    pitches = ['C4', 'G4', 'D#4', 'B4']

    for pitch in pitches:
        arpeggio_note = note.Note(pitch)
        arpeggio_note.duration.quarterLength = 1  # Set the note duration to 1 quarter note
        arpeggio.append(arpeggio_note)

    return arpeggio
