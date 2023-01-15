from unittest import TestCase
from mido import MidiFile, MidiTrack, Message


class TestMidiFile(TestCase):

    def test_get_first_tick(self):
        """ Given a midi file with a track"""
        midi_file = MidiFile(type=0, ticks_per_beat=8)
        t1 = MidiTrack()
        midi_file.tracks.append(t1)
        """ when I set something on the first tick"""
        m1 = Message('note_on', note=60, velocity=127, time=0)
        t1.append(m1)

        """ then it should be on the first tick"""
        self.assertEqual(midi_file.tracks[0][0].time, 0)
