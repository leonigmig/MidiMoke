import unittest
from func_sugg import make_movement


class TestMovementFunction(unittest.TestCase):
    def test_movement_construction(self):
        # given
        # essentially monophonic pattern per voice to start
        pattern_1 = [
            {"pitch": 60, "duration": 0.5},
            {"pitch": 67, "duration": 0.5}
        ]
        pattern_2 = [
            {"pitch": 64, "duration": 0.5},
            {"pitch": 62, "duration": 0.5}
        ]

        # when
        movement = make_movement(length=0, voice_1=pattern_1,
                                 voice_2=pattern_2)

        # then
        notes, wait = movement(1)
        assert (notes is None)
        assert (wait is None)
