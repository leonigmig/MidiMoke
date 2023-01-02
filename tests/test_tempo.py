import unittest
from midisync import Tempo


class TestTempo(unittest.TestCase):
    def test_get_beat_duration(self):
        tempo = Tempo(120)
        self.assertEqual(tempo.get_beat_duration(), 0.5)

        tempo.set_bpm(180)
        self.assertEqual(tempo.get_beat_duration(), 0.3333333333333333)
