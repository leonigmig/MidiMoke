from music21 import stream, note
from music21 import midi
from music21 import converter, meter, key


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

    melodic_techno_lead = '''
    C4. C4 E-4 G4 C5 G4 E-4 C4
    G3. G3 B-3 D4 G4 D4 B-3 G3
    A3. A3 C4 E-4 A4 E-4 C4 A3
    E-3. E-3 G3 B-3 E-4 B-3 G3 E-3
    '''

    lead_line = converter.parse("tinyNotation: " + melodic_techno_lead)

    lead_line.insert(0, meter.TimeSignature('4/4'))
    lead_line.insert(0, key.KeySignature(-3))

    lead_line.repeatAppend(lead_line, numberOfTimes=2)
    return lead_line
