import unittest
from pattern import Pattern, NoteOn


class TestPattern(unittest.TestCase):
    def test_empty_pattern(self):
        # when
        pattern = Pattern()

        # then
        self.assertIsNotNone(pattern)
        self.assertEqual(type(pattern), Pattern)
        self.assertEqual(len(pattern.MIDIEventList), 0)

    def test_1_tick_length_pattern(self):
        # when
        pattern = Pattern()
        pattern.addNote(pitch=60, tick=1, duration=1, volume=100)
        pattern.processEventList()

        # then
        self.assertIsNotNone(pattern)
        self.assertEqual(type(pattern), Pattern)
        self.assertEqual(len(pattern.MIDIEventList), 2)

    def test_hashfunction_doesnt_work_as_expected(self):
        # when
        noteA = NoteOn(1, 60, 1, 1, 100)
        noteB = NoteOn(1, 64, 1, 1, 100)

        # then
        self.assertEqual(hash(noteA), hash(noteB))
