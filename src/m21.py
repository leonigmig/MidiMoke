from music21 import stream, note
from music21 import midi
from music21 import corpus


def convert_music21_stream(stream):
    # Convert the Music21 stream into a MIDI stream
    midi_stream = midi.translate.streamToMidiFile(stream)

    scaling_factor = 24 / midi_stream.ticksPerQuarterNote

    result = {}
    tick = 0

    for event in midi_stream.tracks[1].events:
        event.time = round(event.time * scaling_factor)
        if event.isDeltaTime():
            if event.time > 0:
                tick += event.time
        if event.isNoteOn() or event.isNoteOff():
            if tick in result:
                result[tick].append(event)
            else:
                result[tick] = [event]

    return result


def get_stream():
    arpeggio = stream.Stream()
    pitches = ['C4', 'G4', 'D#4', 'B4', 'C4', 'G4', 'D#4', 'B4']

    for pitch in pitches:
        arpeggio_note = note.Note(pitch)
        arpeggio_note.duration.quarterLength = 1  # Set the note duration to 1 quarter note
        arpeggio.append(arpeggio_note)

    fugue = corpus.parse('bwv66.6')
    return fugue
