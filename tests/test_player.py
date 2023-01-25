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
