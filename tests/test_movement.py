import unittest
from func_sugg import make_movement


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
            {"pitch": 60, "duration": 0.5},
            {"pitch": 67, "duration": 0.5}
        ]
        pattern_2 = [
            {"pitch": 64, "duration": 0.5},
            {"pitch": 62, "duration": 0.5}
        ]

        # when
        movement = make_movement(pattern_1, pattern_2, length)

        # then
        notes, tick_delta = movement(1)
        assert (notes is not None)
        assert (tick_delta is not None)
