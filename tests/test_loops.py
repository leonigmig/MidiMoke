from unittest import TestCase

from main import Loop


class TestLoop(TestCase):
    def test_get_next_event(self):
        loop = Loop(["C", "D", "C", "G"])
        self.assertEqual(loop.get_next_event(), "C")
        self.assertEqual(loop.get_next_event(), "D")
        self.assertEqual(loop.get_next_event(), "C")
        self.assertEqual(loop.get_next_event(), "G")
        self.assertEqual(loop.get_next_event(), "C")
        self.assertEqual(loop.get_next_event(), "D")
        self.assertEqual(loop.get_next_event(), "C")
        self.assertEqual(loop.get_next_event(), "G")
