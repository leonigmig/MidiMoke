import unittest
from pattern import Pattern


class TestPattern(unittest.TestCase):
    def test_0_tick_length_pattern(self):
        # when
        pattern = Pattern()

        # then
        self.assertIsNotNone(pattern)
        self.assertEqual(type(pattern), Pattern)

    def test_1_tick_length_pattern(self):
        # when
        pattern = Pattern()

        # then
        self.assertIsNotNone(pattern)
        self.assertEqual(type(pattern), Pattern)
