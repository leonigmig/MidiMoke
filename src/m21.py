from music21 import stream, note
from music21 import converter, meter, key


def get_stream():
    arpeggio = stream.Stream()
    pitches = ['C4', 'G4', 'D#4', 'B4', 'C4', 'G4', 'D#4', 'B4']

    for pitch in pitches:
        arpeggio_note = note.Note(pitch)
        arpeggio_note.duration.quarterLength = 1  # Set the note duration to 1 quarter note
        arpeggio.append(arpeggio_note)

    melodic_techno_lead = '''
    6/8 e4. d8 c# d e2.
    '''

    lead_line = converter.parse("tinyNotation: " + melodic_techno_lead)

    lead_line.repeatAppend(lead_line, numberOfTimes=8)
    return lead_line

