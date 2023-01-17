import unittest
from movement import make_movement
from pattern import Pattern, NoteOn


class TestMovementFunction(unittest.TestCase):
    def test_0_tick_length_movement(self):
        # given
        movement_length = 0

        # when
        movement = make_movement([], [], movement_length)

        # then
        notes, tick_delta = movement(1)
        assert (notes is None)
        assert (tick_delta is None)

    def test_3_tick_length_movement(self):
        # given
        # essentially monophonic pattern per voice to start
        # each pattern is 2 ticks long

        length = 3

        pattern_1 = Pattern()
        # time and duration are in beats
        pattern_1.addNoteByNumber(
            pitch=60, tick=1, duration=1, volume=100)
        pattern_1.addNoteByNumber(
            pitch=60, tick=2, duration=1, volume=100)
        pattern_1.addNoteByNumber(
            pitch=64, tick=1, duration=1, volume=100)
        pattern_1.addNoteByNumber(
            pitch=64, tick=2, duration=1, volume=100)

        # when
        movement = make_movement(pattern_1, length)
        notes, tick_delta = movement(1)

        # then
        self.assertIsNotNone(notes)
        self.assertEqual(type(notes), list)
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0], NoteOn(1, 64, 1, 1, 100))
        self.assertEqual(notes[1], NoteOn(1, 60, 1, 1, 100))
        self.assertIsNotNone(tick_delta)
        self.assertEqual(type(tick_delta), int)
        self.assertEqual(tick_delta, 1)

        # and when
        notes, tick_delta = movement(2)
        self.assertEqual(len(notes), 4)
        self.assertIsNotNone(notes)
        self.assertEqual(type(notes), list)

        # and when
        notes, tick_delta = movement(3)
        self.assertEqual(len(notes), 2)
        self.assertIsNotNone(notes)
        self.assertEqual(type(notes), list)
