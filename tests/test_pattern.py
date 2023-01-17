import unittest
from pattern import Pattern


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
        pattern.addNoteByNumber(pitch=60, tick=1, duration=1, volume=100)
        pattern.processEventList()

        # then
        self.assertIsNotNone(pattern)
        self.assertEqual(type(pattern), Pattern)
        self.assertEqual(len(pattern.MIDIEventList), 2)
