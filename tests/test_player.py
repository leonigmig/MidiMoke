import unittest

from player import Player, Tempo
from movement import make_movement


class TestPlayer(unittest.TestCase):

    def test_stopped_when_created(self):
        # Given
        tempo = Tempo(120.0)
        movement = make_movement(None, 4)
        port = None
        player = Player(tempo, movement, port)

        # When

        # Then
        self.assertEqual(type(player), Player)


class TestTempo(unittest.TestCase):
    def test_get_beat_duration(self):
        tempo = Tempo(120)
        self.assertEqual(tempo.get_beat_duration(), 0.5)

        tempo.set_bpm(180)
        self.assertEqual(tempo.get_beat_duration(), 0.3333333333333333)
