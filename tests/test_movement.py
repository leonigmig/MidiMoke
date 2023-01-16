import unittest
from movement import make_movement


class TestMovementFunction(unittest.TestCase):
    def test_0_tick_length_movement(self):
        # given
        length = 0
        pattern_1 = pattern_2 = []

        # when
        movement = make_movement(pattern_1, pattern_2, length)

        # then
        notes, tick_delta = movement(1)
        assert (notes is None)
        assert (tick_delta is None)

    def test_2_tick_length_movement(self):
        # given
        # essentially monophonic pattern per voice to start
        length = 2
        pattern_1 = [
            {"note": True, "pitch": 60, "tick": 1},
            {"note": False, "pitch": 60, "tick": 2},
        ]
        pattern_2 = [
            {"note": True, "pitch": 64, "tick": 1},
            {"note": False, "pitch": 64, "tick": 2},
        ]

        # when
        movement = make_movement(pattern_1, pattern_2, length)
        notes, tick_delta = movement(1)

        # then
        self.assertIsNotNone(notes)
        self.assertEqual(type(notes), list)
        self.assertEqual(notes[0], {"note": True, "pitch": 60, "tick": 1})
        self.assertEqual(notes[1], {"note": True, "pitch": 64, "tick": 1})
        self.assertIsNotNone(tick_delta)
        self.assertEqual(type(tick_delta), int)
        self.assertEqual(tick_delta, 1)
